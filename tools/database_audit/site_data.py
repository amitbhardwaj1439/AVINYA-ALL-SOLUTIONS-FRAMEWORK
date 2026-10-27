"""kget_mom logs -> the full site data in Excel (parse only, no comparison).

    path, sheets = write_site_data([bbu1, bbu2], out_dir / "Site_Data.xlsx")      # KgetData per node (main.load_nodes)

Same sheets, sections and columns as the Database Audit / GPL Audit V2 report, with the node's own value in place of
the PRE / POST pair and the status: the parameters are sorted by the audit itself (each node against itself), so a
parameter is on the same sheet here as in an audit. Several nodes (BBUs) go into the same tables (Node_ID column).
"""
from __future__ import annotations

import re
from collections import OrderedDict
from pathlib import Path

import pandas as pd

from .audit import CELL_CLASSES, FEATURE, LTE_GPL, NR_GPL, OTHER, classes_of, run_audit, section_of, text
from .report import (INFO_SHEETS, NOT_ON_MO, SECTION_LABEL, WIDE_SHEETS, _band, _cell_of, _param, _show, merge_sheets,
                     write_report)


def _state(attrs, a) -> str:
    v = text((attrs or {}).get(a, ""))
    m = re.match(r"^-?\d+\s*\((\w+)\)$", v)
    return m.group(1) if m else (v or "nan")


def _node_sheets(data) -> "OrderedDict[str, list[tuple[str, pd.DataFrame]]]":
    res = run_audit(data, data)
    node = data.node
    lte_cells = {k: v for k, v in data.mos.items() if re.match(r"^ENodeBFunction=1,EUtranCell[FT]DD=[^,]+$", k)}
    cell_ids = {k: text(v.get("cellId", "")) for k, v in lte_cells.items()}
    sheets = OrderedDict()

    # ---------------------------------------------------------------- Summary
    enb = text((data.mos.get("ENodeBFunction=1") or {}).get("eNBId", "")) or "NA"
    cells = [{"Node_ID": node, "CellName": k.split("=")[-1], "Type": classes_of(k)[-1], "eNBID": enb, "cellId": cell_ids[k],
              "earfcndl / arfcnDL": text(v.get("earfcndl") or v.get("earfcn") or "")} for k, v in lte_cells.items()]
    for k, v in data.mos.items():
        if CELL_CLASSES.match(k) and ",NRCellDU=" in k:
            cells.append({"Node_ID": node, "CellName": k.split("=")[-1], "Type": "NRCellDU", "eNBID": "NA",
                          "cellId": text(v.get("cellLocalId", "")), "earfcndl / arfcnDL": text(v.get("ssbFrequency", ""))})
    counts = []
    for sec, label in SECTION_LABEL.items():
        counts.append({"Section": label, "Parameters": sum(1 for i in res.items if i.section == sec and not i.info)})
    for sheet in INFO_SHEETS:
        counts.append({"Section": sheet, "Parameters": sum(1 for i in res.items if i.info == sheet)})
    info = [("Node", node), ("Release", data.release or "NA"), ("MOs", len(data.mos)),
            ("MOM", "from the log ('mom all all')" if data.mom_from_log else "bundled 25.Q2"), ("File", data.path.name)]
    sheets["Summary"] = [("", pd.DataFrame(cells, columns=["Node_ID", "CellName", "Type", "eNBID", "cellId",
                                                            "earfcndl / arfcnDL"])),
                         ("Parameter Summary", pd.DataFrame(counts)),
                         ("Node Information", pd.DataFrame(info, columns=["Item", "Value"]))]

    # ---------------------------------------------------------------- wide sheets: one row per MO, one table per class
    def wide(items, with_cell):
        by_cls = OrderedDict()
        for it in items:
            c = classes_of(it.ldn)
            by_cls.setdefault((c[-1], c[0]), OrderedDict()).setdefault(it.ldn, []).append(it)
        names = {}
        for cls, top in by_cls:
            names.setdefault(cls, []).append(top)
        tables = []
        for (cls, top), mos in by_cls.items():
            rows = []
            for ldn, its in mos.items():
                row = OrderedDict(Node_ID=node, MO=ldn)
                if with_cell:
                    row["cellId"] = cell_ids.get(_cell_of(ldn), "") or NOT_ON_MO
                for i in its:
                    row[_param(i)] = _show(i.pre)
                rows.append(row)
            tables.append((f"{cls} ({top})" if len(names[cls]) > 1 else cls, pd.DataFrame(rows).fillna(NOT_ON_MO)))
        return tables

    for sheet in INFO_SHEETS:
        tables = wide([i for i in res.items if i.info == sheet], with_cell=False)
        if tables:
            sheets[sheet] = tables

    rows = [{"Node_ID": node, "MO": it.ldn, "cellId": cell_ids.get(_cell_of(it.ldn), "") or 0, "Parameter": _param(it),
             "Value": _show(it.pre), "Band": _band(it.ldn)}
            for it in res.items if it.section == LTE_GPL and not it.info]
    if rows:
        sheets["LTE_GPL_AUDIT"] = [("", pd.DataFrame(rows))]

    rows = [{"Node_ID": node, "MO": it.ldn, "Perameter": _param(it), "Value": _show(it.pre)}
            for it in res.items if it.section == NR_GPL and not it.info]
    if rows:
        sheets["NR_GPL_AUDIT"] = [("", pd.DataFrame(rows))]

    rows = [{"Node_ID": node, "CXC ID": k.split("=")[-1], "description": _show(text(v.get("description", ""))),
             "FeatureState": _state(v, "featureState"), "LicenseState": _state(v, "licenseState"),
             "ServiceState": _state(v, "serviceState")}
            for k, v in data.mos.items() if section_of(k) == FEATURE]
    if rows:
        sheets["FEATURESTATE"] = [("", pd.DataFrame(rows))]

    for sheet, secs in WIDE_SHEETS.items():
        tables = wide([i for i in res.items if i.section in secs and not i.info], with_cell=sheet != "FREQ_AUDIT")
        if tables:
            sheets[sheet] = tables

    rows = [{"Node_ID": node, "MO": it.ldn, "Parameter": _param(it), "Value": _show(it.pre)}
            for it in res.items if it.section == OTHER and not it.info]
    if rows:
        sheets["OTHER_MO_AUDIT"] = [("", pd.DataFrame(rows))]
    return sheets


def write_site_data(nodes: list, path: Path) -> tuple[Path, list[dict]]:
    """nodes: KgetData per node (main.load_nodes) -> (xlsx path, [{sheet, rows, columns}])"""
    sheets = merge_sheets([(data.node, _node_sheets(data)) for data in nodes])
    write_report(sheets, path)
    return path, [{"sheet": s, "rows": int(sum(len(df) for _, df in t)),
                   "columns": [str(c) for c in t[0][1].columns] if len(t) == 1 else []} for s, t in sheets.items()]
