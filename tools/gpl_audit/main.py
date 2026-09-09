import asyncio
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

from .log_parser.corrections import generate_correction_scripts
from .log_parser.audits import (
    lte_cell_data_audit,
    lte_cell_relation_audit,
    lte_enbinfo_audit,
    lte_eutran_freq_audit,
    lte_eutran_freq_relation_audit,
    lte_feature_state_audit,
    lte_gpl_audit,
    lte_summary_audit,
    nr_baseline_audit,
    nr_cell_data_audit,
    nr_gnbinfo_audit,
    nr_gutran_freq_relation_audit,
)

from .log_parser.extractors import (
    get_nr_baseline_data,
    get_nr_cell_data,
    get_lte_gpl_data,
    get_lte_enbinfo_data,
    get_nr_gnbinfo_data,
    get_lte_feature_state_data,
    get_lte_eutran_freq_data,
    get_lte_eutran_freq_relation_data,
    get_nr_gutran_freq_relation_data,
    get_lte_cell_relation_data,
    get_lte_cell_data,
)
from .log_parser.output import write_excel
from .log_parser.reader import clear_parse_cache

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)


def _site_name_from_files(files: list[Path]) -> str:
    """Extract site/node name from post file names.

    e.g. "KK-NLCTPR12-1_GPL_AUDIT_POST.txt" -> "KK-NLCTPR12-1"
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


def _node_ids_from_logs(files: list[Path]) -> list[str]:
    """Node names read from the logs themselves, via the AMOS prompt.

    The filename is not a reliable source - operators name captures things
    like "pre.txt" / "post.txt" - but every command in the log is preceded by
    a "<NODE>> " prompt, which is where reader.py gets Node_ID from too. Using
    the same source means the name in the report and the Node_ID the
    correction scripts are filtered by can never disagree.
    """
    from .log_parser.reader import _PROMPT_RE

    found: list[str] = []
    for f in files:
        try:
            lines = Path(f).read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line in lines:
            m = _PROMPT_RE.match(line)
            if m:
                node = m.group(1)
                if node not in found:
                    found.append(node)
                break                       # one prompt is enough per file
    return found


def _circle_from_node(node: str) -> str:
    """The circle code a node name starts with: 'AP-NLHY5979-1' -> 'AP'.

    Node names lead with the circle in both spellings the logs use, hyphenated
    and underscored ('HR_BB1_KRLI58'), so the audit does not need to be told
    which circle it is looking at.
    """
    head = re.split(r"[-_]", str(node).strip(), maxsplit=1)[0]
    return head.upper() if head.isalpha() else ""


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


async def main_parse_only() -> Path:
    """
    Parse-only pipeline: extract raw data from a single set of log files
    (single or multiple files, no pre/post pairing) straight into Excel.
    """
    from .log_parser.config import (
        get_pre_files,
        get_output_file,
        set_output_file,
        set_session_dir,
    )
    from .log_parser.commands import load_commands

    global COMMANDS
    COMMANDS = load_commands()  # load once at the start
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_paths = get_pre_files()
    site = _site_name_from_files(file_paths)   # reuse your existing helper

    stem = "_".join(p for p in (site, "GPL_DATA", ts) if p)
    base_dir = get_output_file().parent
    session_dir = base_dir / stem
    session_dir.mkdir(parents=True, exist_ok=True)

    excel_path = session_dir / f"{stem}.xlsx"
    set_output_file(excel_path)
    set_session_dir(session_dir)

    start = datetime.now()
    try:
        (
            nr_gpl,
            nr_cell,
            lte_gpl,
            lte_enbinfo,
            nr_gnbinfo,
            lte_feat,
            lte_freq,
            lte_freq_rel,
            nr_gutran_freq_rel,
            lte_cell_rel,
            lte_cell,
        ) = await asyncio.gather(
            get_nr_baseline_data(COMMANDS, file_paths),
            get_nr_cell_data(COMMANDS, file_paths),
            get_lte_gpl_data(COMMANDS, file_paths),
            get_lte_enbinfo_data(COMMANDS, file_paths),
            get_nr_gnbinfo_data(COMMANDS, file_paths),
            get_lte_feature_state_data(COMMANDS, file_paths),
            get_lte_eutran_freq_data(COMMANDS, file_paths),
            get_lte_eutran_freq_relation_data(COMMANDS, file_paths),
            get_nr_gutran_freq_relation_data(COMMANDS, file_paths),
            get_lte_cell_relation_data(COMMANDS, file_paths),
            get_lte_cell_data(COMMANDS, file_paths),
        )
    except FileNotFoundError as e:
        log.error("Input file not found: %s", e)
        sys.exit(f"Input file not found: {e}")
    except Exception as e:
        # exit WITH the reason so the API can report what actually failed —
        # a bare sys.exit(1) reached the view as a bare SystemExit and turned
        # every failure into the same "Parsing failed" message
        log.exception("Unexpected error during parsing: %s", e)
        sys.exit(f"{type(e).__name__}: {e}")

    # No status/comparison columns — just the raw extracted sheets.
    write_excel(
        {
            "nr_gpl_audit": nr_gpl,
            "nr_cell_data": nr_cell,
            "lte_gpl": lte_gpl,
            "lte_enbinfo": lte_enbinfo,
            "nr_gnbinfo": nr_gnbinfo,
            "lte_feature_state": lte_feat,
            "lte_eutran_freq": lte_freq,
            "lte_eutran_freq_relation": lte_freq_rel,
            "nr_gutran_freq_relation": nr_gutran_freq_rel,
            "lte_cell_relation": lte_cell_rel,
            "lte_cell_data": lte_cell,
        }
    )

    log.info("Parsed output → %s", excel_path)
    log.info("Done in %s", datetime.now() - start)
    return excel_path

async def main() -> Path:
    from .log_parser.config import (
        get_circle,
        get_post_files,
        get_pre_files,
        get_output_file,
        set_output_file,
        set_session_dir,
    )

    clear_parse_cache()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Named after the PRE node: the audit reports what the POST logs changed
    # Everything is keyed off the POST node: it is the site being corrected,
    # so it names the report and it is the only node the scripts apply to.
    # Read from the log's AMOS prompt rather than the filename, which is often
    # just "post.txt" - a filename-derived name produced "pre_AP_GPL_Audit_..."
    # and, worse, matched no Node_ID so the correction scripts came out empty.
    post_nodes = _node_ids_from_logs(get_post_files())
    site = "_".join(post_nodes) if post_nodes else _site_name_from_files(get_post_files())

    # The circle is the node name's own prefix, so the operator is not asked
    # for something the logs already state. get_circle() still wins if set.
    circle = get_circle() or (_circle_from_node(post_nodes[0]) if post_nodes else "")
    stem = "_".join(p for p in (site, circle, "GPL_Audit", ts) if p)

    # session folder: {output_parent}/{stem}/
    # Every run gets its own folder — excel + correction scripts all land inside.
    base_dir = get_output_file().parent
    session_dir = base_dir / stem
    session_dir.mkdir(parents=True, exist_ok=True)

    # Excel lands inside session folder with the standard name
    excel_path = session_dir / f"{stem}.xlsx"
    set_output_file(excel_path)
    set_session_dir(session_dir)

    start = datetime.now()
    try:
        (
            lte_summary,
            lte_enbinfo,
            nr_gnbinfo,
            nr_gpl,
            (_, nr_cell_post),
            lte_gpl,
            (_, lte_cell_post),
            lte_feat,
            lte_freq,
            lte_freq_rel,
            lte_cell_rel,
            nr_gutran_freq_rel,
        ) = await asyncio.gather(
            lte_summary_audit(),
            lte_enbinfo_audit(),
            nr_gnbinfo_audit(),
            nr_baseline_audit(),
            nr_cell_data_audit(),
            lte_gpl_audit(),
            lte_cell_data_audit(),
            lte_feature_state_audit(),
            lte_eutran_freq_audit(),
            lte_eutran_freq_relation_audit(),
            lte_cell_relation_audit(),
            nr_gutran_freq_relation_audit()
        )
    except FileNotFoundError as e:
        log.error("Input file not found: %s", e)
        sys.exit(f"Input file not found: {e}")
    except Exception as e:
        # exit WITH the reason so the API can report what actually failed —
        # a bare sys.exit(1) reached the view as a bare SystemExit and turned
        # every failure into the same "Parsing failed" message
        log.exception("Unexpected error during parsing: %s", e)
        sys.exit(f"{type(e).__name__}: {e}")

    summary_counts = _parameter_status_summary(
        [
            ("LTE_GPL_AUDIT", lte_gpl, "Parameter Setting Status"),
            ("NR_GPL_AUDIT", nr_gpl, "status"),
            ("EUTRANFREQRELATION", lte_freq_rel, "Status"),
            ("FEATURESTATE", lte_feat, "Feature setting Status"),
            ("CellRelation", lte_cell_rel, "Status"),
        ]
    )

    write_excel(
        {
            "lte_summary": lte_summary,
            "lte_summary_counts": summary_counts,
            "lte_enbinfo": lte_enbinfo,
            "nr_gnbinfo": nr_gnbinfo,
            "nr_gpl_audit": nr_gpl,
            "cell_post": nr_cell_post,
            "lte_gpl": lte_gpl,
            "LTE_CELL_DATA": lte_cell_post,
            "lte_feature_state": lte_feat,
            "lte_eutran_freq": lte_freq,
            "lte_eutran_freq_relation": lte_freq_rel,
            "nr_gutran_freq_relation": nr_gutran_freq_rel,
            "lte_cell_relation": lte_cell_rel,
        }
    )

    zip_path = await generate_correction_scripts(excel_path, session_dir, ts,
                                                 only_nodes=post_nodes)
    log.info("All output → %s", session_dir)
    log.info("Zip       → %s", zip_path)
    log.info("Done in %s", datetime.now() - start)
    return zip_path


if __name__ == "__main__":
    asyncio.run(main())
