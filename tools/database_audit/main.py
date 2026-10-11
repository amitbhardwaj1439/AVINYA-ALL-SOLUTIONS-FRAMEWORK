"""Database Audit pipeline: PRE + POST kget_mom logs -> Excel report + AMOS / XML correction scripts (zipped).

    zip_path = run_database_audit([pre.log], [post.log], output_dir)
"""
from __future__ import annotations

import logging
import os
import re
import zipfile
from datetime import datetime
from pathlib import Path

from .audit import run_audit
from .corrections import build_plan, count_commands, write_amos, write_xml
from .kget_parser import KgetData, parse_kget
from .report import build_sheets, write_report

log = logging.getLogger(__name__)


def _load(paths: list[Path], side: str) -> KgetData:
    if not paths:
        raise ValueError(f"No {side} kget_mom log uploaded.")
    parts = [parse_kget(p) for p in paths]
    data = parts[0]
    for extra in parts[1:]:             # a kget split over several files: same node, MOs merged
        if extra.node and data.node and extra.node != data.node:
            raise ValueError(f"{side} logs are of different nodes ({data.node}, {extra.node}) - upload one node per side.")
        for k, v in extra.mos.items():
            data.mos.setdefault(k, v).update(v)
        if not data.mom_from_log and extra.mom_from_log:
            data.mom, data.mom_from_log = extra.mom, True
    return data


def _circle(node: str) -> str:
    head = re.split(r"[-_]", str(node).strip(), maxsplit=1)[0]
    return head.upper() if head.isalpha() else ""


def run_database_audit(pre_paths: list[Path], post_paths: list[Path], output_dir: Path) -> Path:
    start = datetime.now()
    ts = start.strftime("%Y%m%d_%H%M%S")
    pre, post = _load(pre_paths, "Pre_logs"), _load(post_paths, "Post_logs")
    log.info("Database Audit: PRE %s (%d MOs) vs POST %s (%d MOs)", pre.node, len(pre.mos), post.node, len(post.mos))

    res = run_audit(pre, post)
    plan = build_plan(res)
    stem = "_".join(p for p in (post.node, _circle(post.node), "Database_Audit", ts) if p)
    session = Path(output_dir) / stem
    session.mkdir(parents=True, exist_ok=True)

    write_report(build_sheets(res, plan), session / f"{stem}.xlsx")
    (session / f"{post.node}_Database_Correction_Script_AMOS_{ts}.txt").write_text(write_amos(res, plan, ts), encoding="utf-8")
    (session / f"{post.node}_Database_Correction_Script_XML_{ts}.xml").write_text(write_xml(res, plan, ts), encoding="utf-8")

    zip_path = session.parent / f"{stem}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _dirs, files in os.walk(session):
            for f in files:
                p = Path(root) / f
                zf.write(p, p.relative_to(session.parent))
    log.info("Database Audit: %d items, %d missing MOs, commands %s -> %s (%s)", len(res.items), len(res.missing_mos),
             dict(count_commands(plan)), zip_path, datetime.now() - start)
    return zip_path
