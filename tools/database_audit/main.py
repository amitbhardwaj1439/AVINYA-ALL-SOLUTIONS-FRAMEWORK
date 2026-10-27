"""Database Audit pipeline: PRE + POST kget_mom logs -> Excel report + AMOS / XML correction scripts (zipped).

    zip_path = run_database_audit([pre.log], [post.log], output_dir)
    zip_path = run_database_audit([pre.log], [post.log], output_dir, xml=False)   # report + AMOS only (GPL Audit V2)

A site of several BBUs: one kget per node on each side (2 PRE + 2 POST, or 2 PRE + 1 POST when the POST site has
one BBU) - the nodes are paired by audit.pair_bbus; one report for the site, scripts per POST node.
"""
from __future__ import annotations

import logging
import os
import re
import zipfile
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

from .audit import pair_bbus, run_audit, site_token
from .corrections import build_plan, count_commands, write_amos, write_xml
from .kget_parser import KgetData, parse_kget
from .report import build_sheets, merge_sheets, write_report

log = logging.getLogger(__name__)


def load_nodes(paths: list[Path], side: str) -> list[KgetData]:
    """kget logs -> one KgetData per node (a kget split over several files of the same node: MOs merged)"""
    if not paths:
        raise ValueError(f"No {side} kget_mom log uploaded.")
    nodes = OrderedDict()
    for path in paths:
        extra = parse_kget(path)
        data = nodes.get(extra.node)
        if data is None:
            nodes[extra.node] = extra
            continue
        for k, v in extra.mos.items():
            data.mos.setdefault(k, v).update(v)
        if not data.mom_from_log and extra.mom_from_log:
            data.mom, data.mom_from_log, data.preconditions = extra.mom, True, extra.preconditions
    return list(nodes.values())


def _circle(node: str) -> str:
    head = re.split(r"[-_]", str(node).strip(), maxsplit=1)[0]
    return head.upper() if head.isalpha() else ""


def run_database_audit(pre_paths: list[Path], post_paths: list[Path], output_dir: Path, xml: bool = True) -> Path:
    start = datetime.now()
    ts = start.strftime("%Y%m%d_%H%M%S")
    pres, posts = load_nodes(pre_paths, "Pre_logs"), load_nodes(post_paths, "Post_logs")
    pairs = pair_bbus(pres, posts)

    first = posts[0].node
    site = first if len(posts) == 1 else (site_token(first) or first)
    stem = "_".join(p for p in (site, _circle(first), "Database_Audit", ts) if p)
    session = Path(output_dir) / stem
    session.mkdir(parents=True, exist_ok=True)

    per_node = []
    for post, group in pairs:
        log.info("Database Audit: PRE %s vs POST %s (%d MOs)",
                 ", ".join(f"{p.node} ({len(p.mos)} MOs)" for p in group), post.node, len(post.mos))
        res = run_audit(group, post)
        plan = build_plan(res)
        per_node.append((post.node, build_sheets(res, plan)))
        (session / f"{post.node}_Database_Correction_Script_AMOS_{ts}.txt").write_text(write_amos(res, plan, ts), encoding="utf-8")
        if xml:
            (session / f"{post.node}_Database_Correction_Script_XML_{ts}.xml").write_text(write_xml(res, plan, ts), encoding="utf-8")
        log.info("Database Audit %s: %d items, %d missing MOs, commands %s", post.node, len(res.items),
                 len(res.missing_mos), dict(count_commands(plan)))
    write_report(merge_sheets(per_node), session / f"{stem}.xlsx")

    zip_path = session.parent / f"{stem}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _dirs, files in os.walk(session):
            for f in files:
                p = Path(root) / f
                zf.write(p, p.relative_to(session.parent))
    log.info("Database Audit -> %s (%s)", zip_path, datetime.now() - start)
    return zip_path
