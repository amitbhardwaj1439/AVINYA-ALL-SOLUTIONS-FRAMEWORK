"""kget_mom logs -> the full site data in Excel (parse only, no comparison).

    path, sheets = write_site_data([bbu1.log, bbu2.log], out_dir / "Site_Data.xlsx")

Summary sheet (per node: release, MOs, cells; per MO class: MOs and its sheet) + one sheet per MO class: a row per MO
(Node_ID, MO = LDN below ManagedElement), a column per attribute. Several nodes (BBUs) go into the same sheets.
"""
from __future__ import annotations

import re
from collections import OrderedDict
from pathlib import Path

import pandas as pd
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

from .audit import CELL_CLASSES, classes_of, text
from .report import write_report

_EXCEL_CELL_MAX = 32000


def _cell(v) -> str:
    s = ILLEGAL_CHARACTERS_RE.sub("", text(v))
    return s if len(s) <= _EXCEL_CELL_MAX else s[:_EXCEL_CELL_MAX] + " ...(truncated)"


def _sheet_name(cls: str, taken: set) -> str:
    name = re.sub(r"[\[\]:*?/\\]", "_", cls)[:31]
    n = 2
    while name.lower() in taken:
        tail = f"~{n}"
        name, n = name[:31 - len(tail)] + tail, n + 1
    taken.add(name.lower())
    return name


def write_site_data(nodes: list, path: Path) -> tuple[Path, list[dict]]:
    """nodes: KgetData per node (main.load_nodes) -> (xlsx path, [{sheet, rows, columns}])"""
    by_cls = OrderedDict()
    for data in nodes:
        for ldn, attrs in data.mos.items():
            by_cls.setdefault(classes_of(ldn)[-1], []).append((data.node, ldn, attrs))

    node_rows = []
    for data in nodes:
        cells = [k for k in data.mos if CELL_CLASSES.match(k)]
        node_rows.append({"Node_ID": data.node, "Release": data.release or "NA", "MOs": len(data.mos),
                          "MO classes": len({classes_of(k)[-1] for k in data.mos}),
                          "LTE cells": sum(",EUtranCell" in k for k in cells),
                          "NR cells (NRCellDU)": sum(",NRCellDU=" in k for k in cells),
                          "MOM": "from the log ('mom all all')" if data.mom_from_log else "bundled 25.Q2",
                          "File": data.path.name})

    taken, index, class_sheets = {"summary"}, [], OrderedDict()
    for cls in sorted(by_cls, key=str.lower):
        rows = []
        for node, ldn, attrs in by_cls[cls]:
            row = OrderedDict(Node_ID=node, MO=ldn or "ManagedElement")
            for a, v in attrs.items():
                row[a] = _cell(v)
            rows.append(row)
        sheet = _sheet_name(cls, taken)
        class_sheets[sheet] = [("", pd.DataFrame(rows).fillna(""))]
        index.append({"MO Class": cls, "Sheet": sheet, "MOs": len(rows),
                      **{n.node: sum(1 for x in by_cls[cls] if x[0] == n.node) for n in nodes if len(nodes) > 1}})

    sheets = OrderedDict(Summary=[("Nodes", pd.DataFrame(node_rows)), ("MO Classes", pd.DataFrame(index))])
    sheets.update(class_sheets)
    write_report(sheets, path)
    return path, [{"sheet": s, "rows": int(sum(len(df) for _, df in t)),
                   "columns": [str(c) for c in t[0][1].columns] if len(t) == 1 else []} for s, t in sheets.items()]
