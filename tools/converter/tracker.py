"""RF Data template(s) -> Integration tracker rows (a new workbook in the tracker's format, only these sites' rows).

    path, rows = build_tracker([rf.xlsx, ...], out.xlsx, TRACKER_TEMPLATE)

Input: the RF_Data_Scripting_Template_4G_5G workbook(s) the integration scripts are made from (Site_Basic, Radio_HW,
LTE-CELL, NR-CELL). The nodes of one site (2 BBUs: KK-NLMYE757-1 + KK-LMYE757-2) may be in one file or several.
Rows per node: one LTE row (Activity "Relocation") and, with NR cells, one 5G row ("5G Relocation").

Column rules (as the KK tracker rows filled 2026-10-24/25):
    PCI / RSI       physicalLayerCellIdGroup*3 + physicalLayerSubCellId / rachRootSequence of the band's cells, sector
                    order A,B,C,L,M,N, each value once; band from earfcndl (Eutrancell_Type in the RF data is not reliable)
                    L2100 -> FDD 2100, L1800 -> FDD 1800, L900 -> L900, L2300 carrier T1 -> TDD 20, T2 -> TDD 10/20
    CIRCLE          cell name prefix (KK_E_F1_.., AS_E_F3_..); Site ID from the node name KK-NLMYE757-1, else from the
                    cell names (AS nodes LKMKT4 / LKMKTT4, cells AS_E_F3_OM_KMRKT4A_A -> site KMRKT4, 2 BBUs)
    Band            whole site; Allocated / Deployed / Old Site Tech: whole site, 5G row: bands of that node
    RRU Type        Radio_HW Radio_Type 'RRU2219B3' -> '2219 B3', counted ('2219 B3 *3') in Radio_UnitId order, AIR
                    units only in the 5G row; TRX Count / BSC NAME 'NA' unless the node has L900 (GSM: left for the integrator)
    BBU TYPE        Site_Basic BB_Type digits, Mplane IP = OAM_IP without the prefix, OSS = ENM 'KK3' -> 'KK ENM3'
Node state (cell status, GPS clock, licence, alarms, VSWR, ...) is not in the RF data: those cells are left empty and
yellow for the integrator, as are the old-site columns.
"""
from __future__ import annotations

import copy
import datetime
import re
from collections import Counter, OrderedDict
from pathlib import Path

import openpyxl
import pandas as pd
from openpyxl.styles import PatternFill

from .template import REFERENCE_DIR

TRACKER_TEMPLATE = REFERENCE_DIR / "Integration_Tracker_Template.xlsx"
YELLOW = PatternFill("solid", fgColor="FFFF00")
SECTORS = "ABCLMN"
BAND_ORDER = ["L850", "L900", "L1800", "L2100", "L2300", "L2500", "L2600", "700", "3500"]
TDD_BANDS = {"L2300", "L2500", "L2600"}
# tracker PCI / RSI column (header without 'PCI'/'RSI') per LTE band; L2300 split by carrier below
PCI_COLUMN = {"L2100": "FDD 2100", "L1800": "FDD 1800", "L900": "L900"}
TDD20_EARFCN = 39275            # KK T1, when the cell name has no T1 / T2
MANUAL = ["PRE-ALARM", "GPS/IP CLK", "POST-VSWR", "POST Alarms", "CELL STATUS", "CTR STATUS", "Integration Remark",
          "Site Status", "External Alarm Confirmation", "LICENCE Status", "GPL", "Pre/Post Check", "Customer Approval",
          "Old Site ID", "Old Site OSS"]


def lte_band(earfcn) -> str:
    """3GPP DL EARFCN ranges -> tracker band name"""
    e = int(float(earfcn))
    for lo, hi, name in ((0, 599, "L2100"), (1200, 1949, "L1800"), (2400, 2649, "L850"), (3450, 3799, "L900"),
                         (37750, 38249, "L2600"), (38650, 39649, "L2300"), (39650, 41589, "L2500")):
        if lo <= e <= hi:
            return name
    return f"EARFCN {e}"


def nr_band(arfcn) -> str:
    try:
        a = int(float(arfcn))
    except (TypeError, ValueError):
        return "3500"
    if 620000 <= a <= 653333:
        return "3500"
    if 151600 <= a <= 160600:
        return "700"
    return f"NR {a}"


def site_id(node: str) -> str:
    """'KK-NLMYE757-1' / 'KK-LMYE757-2' -> 'MYE757'; '' when the node name has no circle-site-number form (AS 'LKMKT4')"""
    m = re.match(r"^[A-Za-z_]+-(?:NL|L)?([A-Za-z0-9]+)-\d+$", node)
    return m.group(1) if m else ""


def cell_site(cell: str) -> str:
    """'AS_E_F3_OM_KMRKT4A_A' -> 'KMRKT4', 'KK_5_EE_T1_OM_5_xxxxBG1248_A' -> 'BG1248'"""
    parts = cell.split("_")
    if len(parts) < 3:
        return ""
    sector, site = parts[-1], parts[-2]
    if len(sector) == 1 and site.upper().endswith(sector.upper()) and len(site) > 1 and not site.lower().startswith("x"):
        site = site[:-1]
    return site.lstrip("x")


def cell_circle(cell: str) -> str:
    """'AS_E_F3_OM_KMRKT4A_A' -> 'AS' (cell names start with the circle)"""
    head = cell.split("_", 1)[0]
    return head.upper() if head.isalpha() else ""


def _carrier(cell: str) -> str:
    """'KK_E_T1_OM_..' -> 'T1'"""
    m = re.search(r"_(T\d)_", cell)
    return m.group(1) if m else ""


def _s(v) -> str:
    return "" if v is None or (isinstance(v, float) and pd.isna(v)) else str(v).strip()


def _int(v):
    s = _s(v)
    return int(float(s)) if re.fullmatch(r"-?\d+(\.0+)?", s) else s


def _sector(cell: str) -> int:
    last = cell.rsplit("_", 1)[-1][-1:].upper()
    return SECTORS.index(last) if last in SECTORS else len(SECTORS)


def _values(cells, key) -> str:
    """'156,157,158,165,172': per sector order, each value once"""
    out = []
    for c in sorted(cells, key=lambda c: _sector(c["name"])):
        v = c[key]
        if v != "" and v not in out:
            out.append(v)
    return ",".join(str(v) for v in out)


def radio_text(radio_type: str) -> str:
    """'RRU2219B3' -> '2219 B3', 'RRU6626B1B3' -> '6626 B1B3', 'AIR3268B78AA' -> 'AIR 3268 B78AA'"""
    t = _s(radio_type)
    m = re.match(r"^(RRU|AIR|Radio)?\s*(\d{4})\s*(.*)$", t, re.I)
    if not m:
        return t
    return " ".join(x for x in ("AIR" if (m.group(1) or "").upper() == "AIR" else "", m.group(2), m.group(3).strip()) if x)


def _unit_order(unit_id: str):
    """Radio_UnitId order: '1' < '2' < '10' < 'AAS-S1_N1' (numbers first, numerically)"""
    return (0, int(unit_id), "") if unit_id.isdigit() else (1, 0, unit_id)


def _count_text(names) -> str:
    return "/".join(f"{n} *{c}" for n, c in Counter(n for n in names if n).items())


def _bands(bands) -> str:
    return ",".join(sorted(set(bands), key=lambda b: (BAND_ORDER.index(b) if b in BAND_ORDER else 99, b)))


def read_rf(paths) -> "OrderedDict[str, dict]":
    """RF Data workbooks -> {site id: {"nodes": OrderedDict(node -> {basic, radios, lte, nr})}}"""
    nodes = OrderedDict()
    for path in paths:
        xl = pd.ExcelFile(path)
        missing = [s for s in ("Site_Basic", "LTE-CELL") if s not in xl.sheet_names]
        if missing:
            raise ValueError(f"{Path(path).name}: not an RF Data template (sheet {', '.join(missing)} missing).")
        basic = xl.parse("Site_Basic", dtype=object)
        radios = xl.parse("Radio_HW", dtype=object) if "Radio_HW" in xl.sheet_names else pd.DataFrame()
        lte = xl.parse("LTE-CELL", dtype=object)
        nr = xl.parse("NR-CELL", dtype=object) if "NR-CELL" in xl.sheet_names else pd.DataFrame()

        def node_entry(node):
            return nodes.setdefault(node, {"basic": {}, "radios": [], "lte": [], "nr": []})

        for _, r in basic.iterrows():
            if _s(r.get("eNodeBName")):
                node_entry(_s(r["eNodeBName"]))["basic"] = {k: _s(v) for k, v in r.items()}
        for _, r in radios.iterrows():
            if _s(r.get("eNodeBName")):
                node_entry(_s(r["eNodeBName"]))["radios"].append((_s(r.get("Radio_UnitId")), _s(r.get("Radio_Type"))))
        for _, r in lte.iterrows():
            if not _s(r.get("eNodeBName")) or not _s(r.get("earfcndl")):
                continue
            pci = (_int(r.get("physicalLayerCellIdGroup")), _int(r.get("physicalLayerSubCellId")))
            node_entry(_s(r["eNodeBName"]))["lte"].append({
                "name": _s(r.get("eUtranCellFDDId")), "earfcn": _int(r["earfcndl"]), "band": lte_band(r["earfcndl"]),
                "pci": pci[0] * 3 + pci[1] if all(isinstance(x, int) for x in pci) else "",
                "rsi": _int(r.get("rachRootSequence")), "tac": _int(r.get("tac")), "tx": _int(r.get("noOfTxAntennas"))})
        for _, r in nr.iterrows():
            if not _s(r.get("gNodeBName")) or not _s(r.get("gUtranCell")):
                continue
            node_entry(_s(r["gNodeBName"]))["nr"].append({
                "name": _s(r["gUtranCell"]), "band": nr_band(r.get("ssbFrequency")), "pci": _int(r.get("nRPCI")),
                "rsi": _int(r.get("rachRootSequence")), "tac": _int(r.get("nRTAC"))})
    if not any(n["lte"] or n["nr"] for n in nodes.values()):
        raise ValueError("No LTE-CELL / NR-CELL rows found in the uploaded RF Data template(s).")
    sites = OrderedDict()
    for node, n in nodes.items():
        names = [c["name"] for c in n["lte"] + n["nr"]]
        n["circle"] = Counter(filter(None, map(cell_circle, names))).most_common(1)[0][0] if any(map(cell_circle, names))             else (node.split("-", 1)[0] if "-" in node else "")
        sid = site_id(node) or (Counter(filter(None, map(cell_site, names))).most_common(1)[0][0]
                                if any(map(cell_site, names)) else node)
        sites.setdefault(sid, {"nodes": OrderedDict()})["nodes"][node] = n
    return sites


def tracker_rows(sites, integration_date=None, prepared_by="", integrated_by="") -> list[dict]:
    """{site: nodes} -> tracker rows {header: value}; None = left for the integrator (yellow)"""
    date = integration_date or datetime.date.today()
    rows = []
    for sid, site in sites.items():
        nodes = site["nodes"]
        all_cells = [c for n in nodes.values() for c in n["lte"] + n["nr"]]
        site_bands = _bands(c["band"] for c in all_cells)
        has_nr = any(n["nr"] for n in nodes.values())
        for node, n in nodes.items():
            b = n["basic"]
            node_bands = _bands(c["band"] for c in n["lte"] + n["nr"])
            radios = [t for _, t in sorted(n["radios"], key=lambda ur: _unit_order(ur[0]))]
            enm = b.get("ENM", "")
            base = {
                "OEM": "ERICSSON", "Integration Date": date, "CIRCLE": n["circle"], "Site ID": sid, "MO NAME": node,
                "LNBTS ID": "NA", "New NRBTS ID": "NA", "5G Configuration": "NSA+SA" if has_nr else "NA",
                "OSS Details": (f"{n['circle']} ENM{re.sub(r'[^0-9]', '', enm)}" if re.search(r"\d", enm) else enm) or None,
                "Cell ID": "NA", "BCF": "NA", "RET": "NA", "Activity Mode (SA/NSA)": "SA", "Activity Type (SIWA)": "Relocation",
                "Band (SIWA)": site_bands, "BB CARD": "NA", "Media Status": "OK",
                "BBU TYPE": _int(re.sub(r"\D", "", b.get("BB_Type", ""))) if re.search(r"\d", b.get("BB_Type", "")) else (b.get("BB_Type") or None),
                "Mplane IP": (b.get("OAM_IP", "").split("/")[0] or None), "SCF PREPARED BY": prepared_by or None,
                "SITE INTEGRATE BY(Integrator Name)": integrated_by or None, "SOFT AT STATUS": "NA", "ESN NO": "NA",
                "Responsibility for alarm clearance": "Circle", "Old Site LNBTS": "NA", "Old NRBTS ID": "NA",
                "Old Site MPlane IP": 1, "NO OF BBU": len(nodes), "TRX Count": "NA", "BSC NAME": "NA",
                "Old Site Tech": site_bands, "Allocated Tech": site_bands, "Deployed Tech": site_bands}
            for col in ("TDD 20", "TDD 10/20", "FDD 2100", "FDD 1800", "L900"):
                base[f"PCI {col}"] = base[f"RSI {col}"] = "NA"
            base["5G PCI"] = base["5G RSI"] = "NA"
            lte, nr = n["lte"], n["nr"]
            if lte:
                bands = {c["band"] for c in lte}
                row = dict(base, **{
                    "Activity Name": "Relocation",
                    "Technology (SIWA)": "+".join(t for t, hit in (("FDD", bands - TDD_BANDS), ("TDD", bands & TDD_BANDS)) if hit),
                    "CELL COUNT": len(lte),
                    "2T2R/4T4R": "/".join(f"{t}T{t}R" for t in sorted({c["tx"] for c in lte if isinstance(c["tx"], int)})) or "2T2R",
                    "RRU Type": _count_text(radio_text(r) for r in radios if not r.upper().startswith("AIR")) or None,
                    "TAC": lte[0]["tac"]})
                groups = {}
                for c in lte:
                    tdd20 = _carrier(c["name"]) == "T1" if _carrier(c["name"]) else c["earfcn"] == TDD20_EARFCN
                    col = PCI_COLUMN.get(c["band"]) or (("TDD 20" if tdd20 else "TDD 10/20") if c["band"] == "L2300" else None)
                    if col:
                        groups.setdefault(col, []).append(c)
                for col, cs in groups.items():
                    row[f"PCI {col}"], row[f"RSI {col}"] = _values(cs, "pci"), _values(cs, "rsi")
                if "L900" in bands:
                    row["TRX Count"] = row["BSC NAME"] = None   # GSM on the L900 radios: not in the RF data
                rows.append(row)
            if nr:
                rows.append(dict(base, **{
                    "Activity Name": "5G Relocation", "Technology (SIWA)": "5G", "CELL COUNT": len(nr), "2T2R/4T4R": "2T2R",
                    "RRU Type": _count_text(radio_text(r) for r in radios if r.upper().startswith("AIR")) or None,
                    "TAC": nr[0]["tac"], "5G PCI": _values(nr, "pci"), "5G RSI": _values(nr, "rsi"),
                    "Old Site Tech": node_bands, "Allocated Tech": node_bands, "Deployed Tech": node_bands}))
    return rows


def _key(header) -> str:
    """'PCI- TDD 20' / 'PCI TDD 10/20 ' -> 'PCI TDD 20' / 'PCI TDD 10/20' (headers carry stray '-' and blanks)"""
    return re.sub(r"\s+", " ", re.sub(r"^(PCI|RSI)-\s*", r"\1 ", str(header))).strip()


def write_tracker(rows, out_path: Path, template_path: Path = TRACKER_TEMPLATE) -> Path:
    """rows -> the tracker template: header row 1, row 2 = data-row style; key formula in column A"""
    wb = openpyxl.load_workbook(template_path)
    ws = wb.worksheets[0]
    cols = {_key(c.value): c.column for c in ws[1] if c.value}
    unknown = sorted({k for row in rows for k in row} - set(cols))
    if unknown:
        raise ValueError(f"Tracker template has no column for {unknown}.")
    style = [copy.copy(ws.cell(2, c)._style) for c in range(1, ws.max_column + 1)]
    for i, row in enumerate(rows):
        r = 2 + i
        for c, st in enumerate(style, 1):
            ws.cell(r, c)._style = copy.copy(st)
        ws.cell(r, 1).value = f"=_xlfn.CONCAT(C{r},E{r},F{r},I{r},D{r},L{r},H{r},B{r})"
        for k, v in row.items():
            cell = ws.cell(r, cols[k])
            cell.value = v
            if v is None:
                cell.fill = YELLOW
        for k in MANUAL:
            if _key(k) in cols and k not in row:
                ws.cell(r, cols[_key(k)]).value = None
                ws.cell(r, cols[_key(k)]).fill = YELLOW
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    return out_path


def build_tracker(rf_paths, out_path: Path, template_path: Path = TRACKER_TEMPLATE, integration_date=None,
                  prepared_by: str = "", integrated_by: str = "") -> tuple[Path, list[dict]]:
    rows = tracker_rows(read_rf(rf_paths), integration_date, prepared_by, integrated_by)
    return write_tracker(rows, out_path, template_path), rows
