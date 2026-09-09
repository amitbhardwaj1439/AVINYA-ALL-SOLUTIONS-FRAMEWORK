"""
Generate AMOS correction scripts from the reference-audit Excel and zip them.

This tool's workbook only ever contains the 5 sheets listed in config.SHEETS
(GPL parameters + feature state — see the note there). There are no
frequency/relation sections, so only the GPL/FeatureState correction script is
produced; there is no relation correction script.
"""
import asyncio
import logging
import os
import zipfile
from datetime import datetime
from pathlib import Path

import pandas as pd

from .reference import extract_state_code

log = logging.getLogger(__name__)


# ── helpers ───────────────────────────────────────────────────────────────────

def _write_script(lines: list[str], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(str(ln) for ln in lines))
    log.info("Written: %s", path)


def _feature_state_value(val):
    """AMOS needs the bare numeric state. The golden sheet writes it either way
    round ('0', 'Deactivated (0)', '0 (DEACTIVATED)') — reduce it to '0'/'1'
    using the same rule the audit compares with."""
    code = extract_state_code(str(val).split("|")[0])
    return val if code is None else code


def _zip_output(output_dir: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _dirs, files in os.walk(output_dir):
            for file in files:
                abs_path = Path(root) / file
                if abs_path == zip_path:
                    continue
                zf.write(abs_path, abs_path.relative_to(output_dir))
    log.info("Zipped → %s", zip_path)


# ── per-node script writer (runs in thread pool) ───────────────────────────────

def _gpl_set_commands(df: pd.DataFrame) -> list[str]:
    """`set` commands for one GPL audit sheet. LTE_GPL_AUDIT and NR_GPL_AUDIT
    are produced by the same audit routine, so they share these columns."""
    lines = []
    for _, row in df.iterrows():
        if pd.notna(row.get("Pre-existing Value")) and pd.notna(row.get("MO")):
            value = str(row["Pre-existing Value"]).split()[0]
            lines.append(f"set {row['MO']}$ {row['Parameter']} {value}")
    return lines


def _write_node_scripts(
    node: str,
    node_dir: Path,
    ts: str,
    gpl_df: pd.DataFrame,
    nr_gpl_df: pd.DataFrame,
    feat_df: pd.DataFrame,
) -> None:

    # ── GPL Parameter Correction ──────────────────────────────────────────────
    gpl_lines = [
        f"##################### LTE GPL Parameter Correction Commands {node} ####################",
    ]
    gpl_lines += _gpl_set_commands(gpl_df)

    gpl_lines.append(
        f"\n##################### NR GPL Parameter Correction Commands {node} ####################"
    )
    gpl_lines += _gpl_set_commands(nr_gpl_df)

    gpl_lines.append(
        f"\n##################### Feature Correction Commands {node} ####################"
    )
    for _, row in feat_df.iterrows():
        if pd.notna(row.get("Pre Existing FeatureState")) and pd.notna(row.get("CXC ID")):
            gpl_lines.append(f"set {row['CXC ID']}$ featureState {_feature_state_value(row['Pre Existing FeatureState'])}")

    _write_script(gpl_lines, node_dir / f"{node}_GPL_Correction_Script_{ts}.txt")


# ── public entry point ─────────────────────────────────────────────────────────

async def generate_correction_scripts(
    excel_path: Path, output_dir: Path, ts: str | None = None
) -> Path:
    """
    Read the reference-audit Excel, generate per-node AMOS correction scripts
    directly into output_dir (no per-node sub-folders), then zip the whole
    directory.

    output_dir is expected to already be named after the site/node (e.g.
    output/KK-NLCTPR12-1/).  The Excel file should already be written there
    before this is called.  The zip is placed at
    output_dir.parent/{output_dir.name}.zip.

    Returns the path to the zip file.
    """
    if ts is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)

    xl = pd.ExcelFile(excel_path)
    sheet_names = xl.sheet_names

    def _parse(sheet: str) -> pd.DataFrame:
        return xl.parse(sheet) if sheet in sheet_names else pd.DataFrame()

    gpl_df, nr_gpl_df, feat_df = await asyncio.gather(
        asyncio.to_thread(_parse, "LTE_GPL_AUDIT"),
        asyncio.to_thread(_parse, "NR_GPL_AUDIT"),
        asyncio.to_thread(_parse, "Featurestate"),
    )

    # ── filter rows ───────────────────────────────────────────────────────────
    feat_notok = feat_df[feat_df.get("Feature setting Status", pd.Series(dtype=str)) == "NOT OK"].copy() if not feat_df.empty else pd.DataFrame()

    def _notok(df: pd.DataFrame) -> pd.DataFrame:
        """Rows worth a `set`: status isn't OK AND the MO actually exists in the
        log. 'Missing' rows have a NaN Current value — there is no instance to
        target, so a `set` would just fail."""
        if df.empty or "Parameter Setting Status" not in df.columns:
            return pd.DataFrame()
        mask = (df["Parameter Setting Status"] != "OK") & df["Current value"].notna()
        return df[mask].copy()

    gpl_notok = _notok(gpl_df)
    nr_gpl_notok = _notok(nr_gpl_df)

    # ── discover node names from any available sheet ──────────────────────────
    nodes: list[str] = []
    for df in (gpl_notok, nr_gpl_notok, feat_df):
        if not df.empty and "Node_ID" in df.columns:
            candidates = df["Node_ID"].dropna().unique().tolist()
            candidates = [
                n for n in candidates
                if n not in ("", "cell not found in post", "Cell is not Found in Post",
                             "cell not found in log", "Cell is not Found in Log")
            ]
            if candidates:
                nodes = candidates
                break

    if not nodes:
        log.warning("No nodes found in audit data — correction scripts skipped.")
        return output_dir / f"GPL_AUDIT_{ts}.zip"

    log.info("Generating correction scripts for nodes: %s", nodes)

    # ── per-node tasks ─────────────────────────────────────────────────────────
    tasks = []
    for node in nodes:
        # Scripts go directly into output_dir (flat — no sub-folder per node).
        # output_dir is already named after the site, e.g. output/KK-NLCTPR12-1/

        def _node_slice(df: pd.DataFrame, node_val: str) -> pd.DataFrame:
            if df.empty or "Node_ID" not in df.columns:
                return df.copy() if not df.empty else pd.DataFrame()
            return df[df["Node_ID"] == node_val].copy()

        tasks.append(asyncio.to_thread(
            _write_node_scripts,
            node, output_dir, ts,
            _node_slice(gpl_notok, node),
            _node_slice(nr_gpl_notok, node),
            _node_slice(feat_notok, node) if not feat_notok.empty else pd.DataFrame(),
        ))

    await asyncio.gather(*tasks)

    # ── zip the entire session folder ─────────────────────────────────────────
    zip_path = output_dir.parent / f"{output_dir.name}.zip"
    await asyncio.to_thread(_zip_output, output_dir, zip_path)

    return zip_path