import asyncio
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

from .log_parser.corrections import generate_correction_scripts
from .log_parser.audits import (
    feature_state_reference_audit,
    gpl_reference_audit,
)
from .log_parser.commands import clear_commands_cache
from .log_parser.output import write_excel
from .log_parser.reader import clear_parse_cache
from .log_parser.reference import clear_reference_cache

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)


def _site_name_from_files(files: list[Path]) -> str:
    """Extract site/node name from log file names.

    e.g. "KK-NLCTPR12-1_GPL_AUDIT.txt" -> "KK-NLCTPR12-1"
    """
    names: list[str] = []
    for f in files:
        name = _node_name(f.stem)
        if name and name not in names:
            names.append(name)
    return "_".join(names) if names else "AUDIT"


# Node names look like 'KK-NLCTPR12-1', 'AS-NLBORPT3-1', 'AP-NLHY5979-1':
# a short circle code, a site token, then an instance number.
_NODE_RE = re.compile(r"[A-Za-z]{2,4}-[A-Za-z0-9]+-\d+")


def _node_name(stem: str) -> str:
    """The node name inside a log file's name.

    Matching the node pattern beats stripping known suffixes: the suffix list
    only ever covered the spellings we had seen, so '..._GPLAUDIT.txt' kept its
    suffix and a file called 'pre something.txt' collapsed to 'pre'. The
    pattern finds the node wherever it sits in the name, and the old
    suffix-stripping remains as the fallback for names without one.
    """
    found = _NODE_RE.search(stem)
    if found:
        return found.group(0)

    upper = stem.upper()
    cut = len(stem)
    for sfx in ("_GPL_AUDIT_POST", "_GPL_AUDIT_PRE", "_GPL_AUDIT", "_GPLAUDIT",
                "_POST", "_PRE", " POST", " PRE"):
        idx = upper.find(sfx)
        if idx != -1:
            cut = idx
            break
    name = stem[:cut] if cut < len(stem) else stem.split("_")[0]
    return name.strip(" _-")


def _parameter_status_summary(sections: list[tuple[str, pd.DataFrame, str]]) -> pd.DataFrame:
    """Roll up per-audit parameter counts (total / OK / NOT OK / Missing) for
    the Summary sheet. `sections` is a list of (label, audit_df, status_column).
    """
    rows = []
    for label, df, status_col in sections:
        if df.empty or status_col not in df.columns:
            rows.append({"Audit Section": label, "Total Parameters": 0, "OK": 0, "NOT OK": 0, "Missing": 0})
            continue
        status = df[status_col].astype(str).str.upper()
        rows.append({
            "Audit Section": label,
            "Total Parameters": len(df),
            "OK": int((status == "OK").sum()),
            "NOT OK": int((status == "NOT OK").sum()),
            "Missing": int(status.str.contains("MISS").sum()),
        })
    return pd.DataFrame(rows)


async def main() -> Path:
    from .log_parser.config import (
        get_circle,
        get_input_files,
        get_output_file,
        set_output_file,
        set_session_dir,
    )
    from .log_parser.reference import lte_sheet_for_circle, nr_sheet_for_circle

    clear_parse_cache()
    clear_reference_cache()
    clear_commands_cache()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    log_files = get_input_files()
    site = _site_name_from_files(log_files)

    # Resolved (and validated) up front: an unknown circle must stop the run
    # before any parsing, not produce a report audited against the wrong sheet.
    circle = get_circle()
    lte_sheet = lte_sheet_for_circle(circle)
    nr_sheet = nr_sheet_for_circle(circle)
    log.info("Circle: %s — LTE sheet '%s', NR sheet '%s'", circle, lte_sheet, nr_sheet)

    # session folder: {output_parent}/{site}_{circle}_GPL_Audit_{ts}/
    # Every run gets its own folder — excel + correction scripts all land inside.
    # The circle is in the name because the verdict is only meaningful against
    # the golden sheets of that circle.
    # "Reference" is in the name so this cannot be mistaken for the PRE/POST
    # GPL audit, which otherwise produces an identically shaped filename.
    stem = "_".join(p for p in (site, circle, "GPL_Reference_Audit", ts) if p)
    base_dir = get_output_file().parent
    session_dir = base_dir / stem
    session_dir.mkdir(parents=True, exist_ok=True)

    excel_path = session_dir / f"{stem}.xlsx"
    set_output_file(excel_path)
    set_session_dir(session_dir)

    start = datetime.now()
    try:
        (lte_gpl, nr_gpl), feat = await asyncio.gather(
            gpl_reference_audit(),
            feature_state_reference_audit(),
        )
    except FileNotFoundError as e:
        log.error("Input file not found: %s", e)
        sys.exit(1)
    except Exception as e:
        log.exception("Unexpected error during parsing: %s", e)
        sys.exit(1)

    summary_counts = _parameter_status_summary(
        [
            # name the circle in the roll-up so a downloaded report says on its
            # face which golden sheets the numbers were measured against
            (f"LTE_GPL_AUDIT ({circle})", lte_gpl, "Parameter Setting Status"),
            (f"NR_GPL_AUDIT ({circle})", nr_gpl, "Parameter Setting Status"),
            ("Featurestate", feat, "Feature setting Status"),
        ]
    )

    write_excel(
        {
            "summary_counts": summary_counts,
            "lte_gpl": lte_gpl,
            "nr_gpl_audit": nr_gpl,
            "feature_state": feat,
        }
    )

    zip_path = await generate_correction_scripts(excel_path, session_dir, ts)
    log.info("All output → %s", session_dir)
    log.info("Zip       → %s", zip_path)
    log.info("Done in %s", datetime.now() - start)
    return zip_path


if __name__ == "__main__":
    asyncio.run(main())
    
##########################end################    
