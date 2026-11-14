"""RJ_Vi: Vi Rajasthan's L900 (T-5) RF data list + its ATOM IP plan.

Two workbooks:

    'L900_Sites-RF_Data required list_*.xlsx'
        'RF Data'   one row per SITE. Row 0 is a band banner (L900 / L1800 /
                    L2100 / L2500 / GSM) over the first column of each band
                    block; the real header is row 1 (ssis._header_row skips
                    the banner). Site-level columns (SAP ID, EnodeB Name/ID,
                    TAC, OSS, 'PCI Cell1..4', 'rootSequenceIndexcell1..4')
                    are followed by one 12-column block per band:
                        eNodeB Cell Name 1..4, EUTRA Cell ID 1..4,
                        dlChannelBandwidth, ulChannelBandwidth,
                        earfcndl, earfcnul
                    The block headers repeat word for word across the FDD
                    bands, so blocks are found by position: each starts at an
                    'eNodeB Cell Name 1' column. The TDD (L2500) block says
                    'TDD' in its cell-name header.
        'Sheet1'    new-site list with Lat/Long per SAP ID - used only for
                    coordinates when the site is on it.
        'MME', 'SGW', 'MIMO Configuration', 'RET User Lable'
                    circle-wide reference tabs, not site data.

    'T-5 L900 IP plan.xlsx'
        'Sheet1'    the same ATOM report MP_Vi reads (one row per site,
                    CODE_IP_SERVICE_PLANNING_<tech>_<plane>_*), so the
                    transport is read with MP_Vi's helpers.

The two join on the NSS id: the RF sheet calls it 'SAP ID', the IP plan
'NSS ID' ('INRJ002565'). Node names cannot be the key - many existing nodes
keep a legacy name ('LO1SG1SGMBH') that carries no NSS id.

Values are the ones the RJ_Vi scripts in the LTE tool were built from (nodes
LO01INRJ207062 and LMWUKES02): OAM/S1-C/S1-U in IPv6 with the IPv4 side of
S1-C/S1-U in the *_V4 columns, Abis in IPv4, Baseband 6631, TN_IDL_B (the
port the RJ_Vi 01 script configures), SectorCarrier power 40000 mW on L900 and
80000 mW on L1800/L2100/TDD, 2T2R FDD and 4T4R TDD.

Radio_HW is not in either source: it is built from the RJ_Vi standard per
technology (RADIO_HW below), see build_radio_hw.
"""
from __future__ import annotations

import ipaddress
import re

from .sitedata import SiteData
from . import vi_defaults
from .mapping_mp_vi import _get, _int, _plane, _plane_in, _rows

CIRCLE = "RJ_Vi"

STRIP_NODE_PREFIX = False
NUMERIC_SITE_IDS = False
#: 'LO01INRJ002565' -> 'INRJ002565', so the node name also finds the site.
VI_NODE_PREFIX = True
#: 'SAP ID' on the RF workbook, 'NSS ID' on the IP plan.
KEY_COLUMNS = ("sap id", "nss id")

RF_SHEETS = ("rf data",)
COORD_SHEETS = ("sheet1",)
IP_SHEETS = ("sheet1",)

CONFIGURATION_IN_NODE = "LTE"
SCRIPT_REQUIRED = "YES"

#: Not in the shared template, read by the LTE tool's RJ_Vi GSM part (02 Cell_Def): the site's BSC (the tool looks
#: its broker up by BSC name when Site_Basic Broker_IP is empty) and per L900 cell the GSM sector name the BSC knows
#: the sector by (RF Data 'BTS Cell Name n', e.g. GGMCW21). The broker itself is the template's added Broker_IP column
#: (convert.TEMPLATE_ADDITIONS, after ABIS_GW), named BSC_Broker_IP for RJ_Vi (user 2026-11-14), filled from the IP
#: plan's BSCIP when that holds an address, else left for the user.
EXTRA_COLUMNS = {
    "Site_Basic": ("BSC",),
    "LTE-CELL": ("GSM_Sector_Name",),
}
TEMPLATE_RENAMES = {"Site_Basic": {"Broker_IP": "BSC_Broker_IP"}}

#: Site_Basic constants of the RJ_Vi build (on top of vi_defaults.SITE_BASIC).
SITE_BASIC = {
    **vi_defaults.SITE_BASIC,
    "BB_Type": "Baseband 6631",
    "tnPortId": "TN_IDL_B",
}

#: Per-layer SectorCarrier values from the RJ reference nodes.
LAYER = {
    "L900": {"configuredMaxTxPower": "40000", "noOfTxAntennas": "2", "noOfRxAntennas": "2"},
    "L1800": {"configuredMaxTxPower": "80000", "noOfTxAntennas": "2", "noOfRxAntennas": "2"},
    "L2100": {"configuredMaxTxPower": "80000", "noOfTxAntennas": "2", "noOfRxAntennas": "2"},
    "TDD": {"configuredMaxTxPower": "80000", "noOfTxAntennas": "4", "noOfRxAntennas": "4"},
}

#: Radio per technology on a Vi RJ Baseband 6631 site, from the kgets of
#: LO01INRJ207062 (6631: L900 on Radio 2271 B0C, L1800+L2100 on one UBR Radio
#: 4490 B1B3 - the RF list's 'UBR case (L18+L21)') and LMWUKES02 (TDD band 41
#: on Radio 4412 B41, 4T4R). One radio per sector and group. The SEF, RRU and
#: RiLink take the cell id of the sector's cell (the plan numbers cells by
#: layer: 1x L900, 2x L1800, 3x L2100, 5x L2500), so F11 sits on S11 / RRU-11
#: / RiLink=11 as on LO01INRJ207062, and a UBR radio on its L1800 cell's id
#: (its L2100 cell's when the sector has no L1800). Baseband RiPorts: L900
#: J/K/L as on LO01INRJ207062 (M for a 4th sector), UBR A-D, TDD E-H, so the
#: groups never share a port on the 6631. The radio side is always DATA_1.
RADIO_HW = {
    "L900": {"Radio_Type": "Radio 2271 B0C", "RiPort_BB": "JKLM"},
    "UBR": {"Radio_Type": "Radio 4490 44B1 44B3 C", "RiPort_BB": "ABCD"},
    "TDD": {"Radio_Type": "Radio 4412 B41", "RiPort_BB": "EFGH"},
}
RIPORT_RADIO = "DATA_1"
#: Unit number when a cell has no id: layer digit + sector.
_GROUP_DIGIT = {"L900": 1, "UBR": 2, "TDD": 5}
_NO_5G = "No 5G layer is planned in these sources."

UNMAPPED = {
    "Site_Basic": {
        "Anchor_ENDC_IP": _NO_5G, "Anchor_ENDC_GW": _NO_5G,
        "Anchor Gnb ID": _NO_5G, "Anchor NR IP": _NO_5G,
        "NR_PORT": _NO_5G, "NR_vlan": _NO_5G, "NR_IP": _NO_5G, "NR_GW": _NO_5G,
        "NR_ENDC_IP": _NO_5G, "NR_ENDC_GW": _NO_5G,
    },
    "LTE-CELL": {
        "Latitude": "The RF Data sheet has no coordinates and the site is not "
                    "on Sheet1 (the only tab with Lat/Long).",
        "Longitude": "The RF Data sheet has no coordinates and the site is not "
                     "on Sheet1 (the only tab with Lat/Long).",
    },
    "NR-CELL": {"*": _NO_5G},
}

#: Warnings about values the plan states but that cannot be right, collected
#: per conversion and printed by the builders (the API has no field for them).
_TDD_BANDS = (36000, 46589)          # EARFCN range of the TDD bands 33-43


# --------------------------------------------------------------------------
# RF Data: site-level columns + per-band blocks
# --------------------------------------------------------------------------

def _norm(name) -> str:
    return " ".join(str(name).split()).lower()


def _band(earfcn) -> str | None:
    """Layer name from the downlink EARFCN (bands 8 / 3 / 1, TDD 33-43)."""
    try:
        n = int(float(earfcn))
    except (TypeError, ValueError):
        return None
    if 3450 <= n <= 3799:
        return "L900"
    if 1200 <= n <= 1949:
        return "L1800"
    if 0 <= n <= 599:
        return "L2100"
    if _TDD_BANDS[0] <= n <= _TDD_BANDS[1]:
        return "TDD"
    return None


def _blocks(sheet) -> list[dict]:
    """The band blocks of the RF Data sheet as {field: column index}.

    A block starts at each 'eNodeB Cell Name 1' column and runs to the next
    one (or to 'BSC', where the GSM columns start). Inside it the cell names
    and ids are numbered 1..4, the four channel columns are not.
    """
    cols = sorted(sheet.columns, key=lambda c: c.index)
    starts = [c.index for c in cols if _norm(c.name).startswith("enodeb cell name 1")]
    end_at = next((c.index for c in cols if _norm(c.name) == "bsc"), None)
    blocks = []
    for k, start in enumerate(starts):
        stop = starts[k + 1] if k + 1 < len(starts) else (end_at or 10 ** 6)
        block = {"tdd": False}
        for c in cols:
            if not start <= c.index < stop:
                continue
            n = _norm(c.name)
            m = re.match(r"enodeb cell name (\d)", n)
            if m:
                block[f"name{m.group(1)}"] = c.index
                block["tdd"] |= " tdd " in f" {n} "
                continue
            m = re.match(r"eutra cell id (\d)", n)
            if m:
                block[f"id{m.group(1)}"] = c.index
                continue
            if n in ("dlchannelbandwidth", "ulchannelbandwidth", "earfcndl", "earfcnul"):
                block[n] = c.index
        blocks.append(block)
    return blocks


def _site_index(sheet) -> dict:
    """Site-level column name -> index (first occurrence, before the blocks)."""
    out = {}
    for c in sorted(sheet.columns, key=lambda c: c.index):
        out.setdefault(_norm(c.name), c.index)
    return out


def _cell(r, i):
    if i is None or i >= len(r):
        return None
    v = r[i]
    return None if v is None or str(v).strip() == "" else str(v).strip()


def _rf_sites(data: SiteData) -> list[tuple[dict, list[dict]]]:
    """This site's RF Data rows as (site fields, [cell dicts])."""
    out = []
    for hit in data.sheets_matching(*RF_SHEETS):
        sheet = hit.sheet
        idx = _site_index(sheet)
        blocks = _blocks(sheet)
        for r in hit.rows:
            site = {name: _cell(r, i) for name, i in idx.items()}
            cells = []
            for b in blocks:
                for n in range(1, 5):
                    name = _cell(r, b.get(f"name{n}"))
                    if not name:
                        continue
                    cells.append({
                        "sector": n,
                        "name": name,
                        "tdd": b["tdd"],
                        "cellId": _int(_cell(r, b.get(f"id{n}"))),
                        "dl_bw": _int(_cell(r, b.get("dlchannelbandwidth"))),
                        "ul_bw": _int(_cell(r, b.get("ulchannelbandwidth"))),
                        "earfcndl": _int(_cell(r, b.get("earfcndl"))),
                        "earfcnul": _int(_cell(r, b.get("earfcnul"))),
                    })
            out.append((site, cells))
    return out


def _coordinates(data: SiteData) -> tuple:
    """(lat, long) from the new-site list, when the site is on it."""
    for row, _label in _rows(data, COORD_SHEETS):
        if "lat" in row and "long" in row:
            return (vi_defaults.without_decimal(_get(row, "lat")),
                    vi_defaults.without_decimal(_get(row, "long")))
    return (None, None)


def _broker_ip(ip_row: dict):
    """The BSC broker address from the IP plan's BSCIP - only when it is an IP address (the column is mostly empty and
    sometimes holds a BSC name)."""
    value = _get(ip_row, "bscip")
    try:
        return str(ipaddress.ip_address(value.split("/")[0].strip())) if value else None
    except ValueError:
        return None


def _ip_row(data: SiteData) -> dict:
    for row, _label in _rows(data, IP_SHEETS):
        if any(k.startswith("code_ip_service_planning_") for k in row):
            return row
    return {}


# --------------------------------------------------------------------------
# builders
# --------------------------------------------------------------------------

def build_site_basic(data: SiteData) -> list[dict]:
    ip = _ip_row(data)
    oam_vlan, oam_ip, oam_gw = _plane(ip, "4g", "oam")
    s1c_vlan, s1c_ip, s1c_gw = _plane(ip, "4g", "s1c")
    s1u_vlan, s1u_ip, s1u_gw = _plane(ip, "4g", "s1u")
    abis_vlan, abis_ip, abis_gw = _plane(ip, "2g", "bts")
    s1c_ip_v4, s1c_gw_v4 = _plane_in(ip, "4g", "s1c", "ipv4")
    s1u_ip_v4, s1u_gw_v4 = _plane_in(ip, "4g", "s1u", "ipv4")
    transport = {
        "OAM_vlan": oam_vlan, "OAM_IP": oam_ip, "OAM_GW": oam_gw,
        "LTE_S1_vlan": s1c_vlan, "LTE_S1_IP": s1c_ip, "LTE_S1_GW": s1c_gw,
        "LTE_S1_IP_V4": s1c_ip_v4, "LTE_S1_GW_V4": s1c_gw_v4,
        "LTE_UP_vlan": s1u_vlan, "LTE_UP_IP": s1u_ip, "LTE_UP_GW": s1u_gw,
        "LTE_UP_IP_V4": s1u_ip_v4, "LTE_UP_GW_V4": s1u_gw_v4,
        "ABIS_vlan": abis_vlan, "ABIS_IP": abis_ip, "ABIS_GW": abis_gw,
    }

    rows = []
    for site, _cells in _rf_sites(data):
        node = site.get("enodeb name")
        rows.append({
            "Site ID": data.key,
            "eNodeBName": node,
            "Fingerprint": node,
            "ENM": site.get("oss"),
            # The RJ_Vi scripts set the node userLabel to the node name.
            "Phy SiteID/Userlabel": node,
            "Configuration_in_Node": CONFIGURATION_IN_NODE,
            **SITE_BASIC,
            "eNBId": _int(site.get("enodeb id")),
            **transport,
            "BSC_Broker_IP": _broker_ip(ip),
            "BSC": site.get("bsc") or _get(ip, "bsc"),
        })
        break                      # one node per site in this list

    # A site the IP plan has but the RF list does not: transport half only.
    if not rows and ip:
        rows.append({
            "Site ID": data.key,
            "Configuration_in_Node": CONFIGURATION_IN_NODE,
            **SITE_BASIC,
            **transport,
        })
    return rows


def _group(cell) -> str | None:
    """Radio group of a cell: L900, UBR (L1800 / L2100) or TDD."""
    if cell["tdd"]:
        return "TDD"
    layer = _band(cell["earfcndl"])
    if layer == "L900":
        return "L900"
    if layer in ("L1800", "L2100"):
        return "UBR"
    # No usable EARFCN: the cell id's layer digit (1 L900, 2/3 L1800/L2100).
    cid = str(cell["cellId"] or "")
    return {"1": "L900", "2": "UBR", "3": "UBR"}.get(cid[:1]) if len(cid) == 2 else None


def _radios(cells) -> dict:
    """(group, sector) -> radio unit number for this site's cells."""
    units = {}
    # L1800 before L2100, so a UBR radio takes its L1800 cell's id.
    for c in sorted(cells, key=lambda c: (_band(c["earfcndl"]) == "L2100", str(c["cellId"]))):
        g = _group(c)
        if g is None or (g, c["sector"]) in units:
            continue
        cid = c["cellId"]
        units[(g, c["sector"])] = cid if cid and cid.isdigit() else str(_GROUP_DIGIT[g] * 10 + c["sector"])
    return units


def build_radio_hw(data: SiteData) -> list[dict]:
    """One radio per sector and technology group, from the RJ_Vi standard (RADIO_HW)."""
    rows = []
    for site, cells in _rf_sites(data):
        node = site.get("enodeb name")
        for (g, sector), unit in sorted(_radios(cells).items(), key=lambda kv: int(kv[1])):
            std = RADIO_HW[g]
            if sector > len(std["RiPort_BB"]):
                print(f"RJ_Vi: {node} {g} sector {sector} has no baseband RiPort in the standard - row skipped")
                continue
            rows.append({
                "eNodeBName": node,
                "Configuration_in_Node": CONFIGURATION_IN_NODE,
                "sectorEquipmentFunctionId": f"S{unit}",
                "Tech": {"L900": "L900", "UBR": "L1800+L2100", "TDD": "L2500"}[g],
                "Baseband_Type": SITE_BASIC["BB_Type"],
                "Radio_Type": std["Radio_Type"],
                "Radio_UnitId": unit,
                "riLinkId": unit,
                "RiPort_BB": std["RiPort_BB"][sector - 1],
                "RiPort_Radio": RIPORT_RADIO,
            })
        break                      # one node per site in this list
    return rows


def build_lte_cell(data: SiteData) -> list[dict]:
    lat, lon = _coordinates(data)
    rows = []
    for site, cells in _rf_sites(data):
        node = site.get("enodeb name")
        units = _radios(cells)
        for c in cells:
            unit = units.get((_group(c), c["sector"]))
            band = _band(c["earfcndl"])
            earfcndl, earfcnul = c["earfcndl"], c["earfcnul"]
            if c["tdd"]:
                layer = "TDD"
                earfcnul = None            # a TDD cell has one EARFCN
                if band != "TDD":
                    print(f"RJ_Vi: {c['name']} is a TDD cell but the plan gives "
                          f"EARFCN {earfcndl} (not a TDD band) - earfcndl left blank")
                    earfcndl = None
            else:
                layer = band if band in ("L900", "L1800", "L2100") else None
            pci = _int(site.get(f"pci cell{c['sector']}"))
            group = sub = None
            if pci and pci.isdigit():
                group, sub = str(int(pci) // 3), str(int(pci) % 3)
            rows.append({
                "eNodeBName": node,
                "eUtranCellFDDId": c["name"],
                "Eutrancell_Type": "TDD" if c["tdd"] else "FDD",
                "Configuration_in_Node": CONFIGURATION_IN_NODE,
                "Script_Required": SCRIPT_REQUIRED,
                # The sector's radio (Radio_HW): S11 for F11, S21 for F21 + F31.
                "sectorEquipmentFunctionId": f"S{unit}" if unit else None,
                # Vi RJ numbers its SectorCarriers after the cell (LO01INRJ207062).
                "sectorCarrierId": c["cellId"],
                "enbId": _int(site.get("enodeb id")),
                "earfcndl": earfcndl,
                "earfcnul": earfcnul,
                "dlChannelBandwidth": c["dl_bw"],
                "ulChannelBandwidth": c["ul_bw"],
                "Latitude": lat,
                "Longitude": lon,
                "cellId": c["cellId"],
                "physicalLayerCellIdGroup": group,
                "physicalLayerSubCellId": sub,
                "tac": _int(site.get("tac")),
                "rachRootSequence": _int(site.get(f"rootsequenceindexcell{c['sector']}")),
                "crsGain": vi_defaults.CELL["crsGain"],
                "MME": vi_defaults.CELL["MME"],
                **LAYER.get(layer, {}),
                # GSM shares the L900 radio: sector n of the BTS
                "GSM_Sector_Name": site.get(f"bts cell name {c['sector']}") if layer == "L900" else None,
            })
    return rows


def build_nr_cell(data: SiteData) -> list[dict]:
    return []


BUILDERS = {
    "Site_Basic": build_site_basic,
    "Radio_HW": build_radio_hw,
    "LTE-CELL": build_lte_cell,
    "NR-CELL": build_nr_cell,
}
