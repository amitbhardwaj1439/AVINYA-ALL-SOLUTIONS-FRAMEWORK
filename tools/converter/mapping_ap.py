"""AP circle: input columns -> template columns.

One builder per template sheet. Each returns a list of dicts keyed by template
column name; any key left out is written blank and shown as such in the
coverage report, so a field with no source in the AP workbooks is visibly
missing rather than quietly wrong.

Only rules that can be justified from the source data are written here. Fields
the AP inputs simply do not carry - ENM, crsGain, the ENDC anchor addressing -
are listed in UNMAPPED with the reason, which the coverage report prints.

To add a circle, copy this module and adjust the sheet-name fragments and any
column spellings that differ; `convert.py` selects the module by circle.
"""
from __future__ import annotations

import re

from .sitedata import SiteData

CIRCLE = "AP"

# Sheet-name fragments that identify each kind of source sheet. Names differ per
# workbook ('S_RN', 'S_RN - 3 sector_FD+TD+FD900_20M', 'S_RN_1-N_Sec').
RN_SHEETS = ("s_rn",)
EQUIP_SHEETS = ("site equipment",)
SITEBASIC_4G = ("sitebasic - default", "s_sitebasic")
SITEBASIC_GSM = ("gsm_delta sitebasic", "gsm delta sitebasic", "s_gsm")
PLANNING_SHEETS = ("sheet1",)
ARNE_SHEETS = ("s_arne",)
NR_CELL_SHEETS = ("5g_n78_rn",)
NR_HW_SHEETS = ("5g_air",)
NR_BASIC_SHEETS = ("5g_sitebasic",)
RIM_TAG_SHEETS = ("rim tag",)

# Template columns with no source in the AP workbooks, and why. Printed by the
# coverage report so the gaps are explicit rather than looking like a bug.
UNMAPPED = {
    "Site_Basic": {
        "ENM": "no ENM name in the AP SSIS; S_ARNE carries only an emUrl IP",
        "Bridge_tnPortId": "not present in any AP sheet",
        "fieldReplaceableUnitId": "site-level FRU not distinguishable from the per-radio FRUs",
        "NR_PORT": "not present in the 5G CCR",
        "NR_ENDC_IP": "ENDC addressing not present in the 5G CCR",
        "NR_ENDC_GW": "ENDC addressing not present in the 5G CCR",
        "Anchor_ENDC_IP": "ENDC anchor addressing not present in the AP inputs",
        "Anchor_ENDC_GW": "ENDC anchor addressing not present in the AP inputs",
        "Anchor Gnb ID": "anchor gNB not present in the AP inputs",
        "Anchor NR IP": "anchor NR address not present in the AP inputs",
    },
    "Radio_HW": {
        "Radio_Type": "no radio model anywhere in the AP inputs - the only "
                      "productName is site-level (RBS6601, the cabinet) and the "
                      "5G CCR names the AIR by FRU id (AAS-S1_N1)",
    },
    "LTE-CELL": {
        "crsGain": "no such column in any AP input sheet",
        "configuredMaxTxPower": "absent from the main RN sheet; only the "
                                "per-sector delta files state it",
    },
    "NR-CELL": {
        "Radio_Type": "5G CCR names the AIR by FRU id (AAS-S1_N1), not product",
    },
}

# Written as a fixed value rather than read from the inputs.
CONFIGURATION_IN_NODE = "LTE"
SCRIPT_REQUIRED = "YES"

# LTE-CELL's MME column is a *vendor selector*, not an MME id: views.py picks
# the Nokia script when it starts with 'NOKIA' and the Cisco one otherwise
# (LTE_Integration_Scripting_Automtion/views.py, `mme_type = ...`). The AP
# inputs name MME instances (termPointToMmeId = 'MME_000104025145'), never the
# vendor, so that column cannot supply this. CISCO is what the template ships
# and what a blank already resolves to downstream - override for Nokia sites.
MME_VENDOR = "CISCO"


# -- small parsers -----------------------------------------------------------

def bb_type(value: str | None) -> str | None:
    """'BB6630_ L900+L1800+TDD-L2300\\Site...' -> 'BB6630'.

    No trailing \\b: the name is followed by '_' in the #Template string, which
    is a word character, so a boundary there never matches.
    """
    if not value:
        return None
    m = re.search(r"BB\d{4}", value)
    return m.group(0) if m else None


def tn_port(ref: str | None) -> str | None:
    """'Transport=1,Router=LTEUP,InterfaceIPv4=TN_C_UP' -> 'TN_C'.

    The interface is named <port>_<purpose>; the template wants the port.
    """
    if not ref:
        return None
    m = re.search(r"InterfaceIPv4=(TN_[A-Z]+)", ref)
    return m.group(1) if m else None


def unit_id(fru: str | None) -> str | None:
    """'RRU-4' -> '4', 'AAS-S1_N1' -> 'S1_N1'."""
    if not fru:
        return None
    m = re.fullmatch(r"[A-Za-z]+-(.+)", fru.strip())
    return m.group(1) if m else fru.strip()


def ri_port(ref: str | None) -> str | None:
    """'Equipment=1,FieldReplaceableUnit=DU-1,RiPort=D' -> 'D'."""
    if not ref:
        return None
    m = re.search(r"RiPort=([A-Za-z0-9_]+)", ref)
    return m.group(1) if m else None


def sector_carrier_id(ref: str | None) -> str | None:
    """'ENodeBFunction=1,SectorCarrier=1' -> '1'."""
    if not ref:
        return None
    m = re.search(r"SectorCarrier=([A-Za-z0-9_]+)", ref)
    return m.group(1) if m else None


def sector_equipment_id(ref: str | None) -> str | None:
    """'NodeSupport=1,SectorEquipmentFunction=S1_N1' -> 'S1_N1'."""
    if not ref:
        return None
    m = re.search(r"SectorEquipmentFunction=([A-Za-z0-9_]+)", ref)
    return m.group(1) if m else None


def fru_from_ref(ref: str | None) -> str | None:
    """'Equipment=1,FieldReplaceableUnit=RRU-19,RiPort=DATA_1' -> 'RRU-19'."""
    if not ref:
        return None
    m = re.search(r"FieldReplaceableUnit=([A-Za-z0-9_-]+)", ref)
    return m.group(1) if m else None


def antenna_group(ref: str | None) -> str | None:
    """'Equipment=1,AntennaUnitGroup=19,RfBranch=1;...' -> '19'."""
    if not ref:
        return None
    m = re.search(r"AntennaUnitGroup=(\d+)", ref)
    return m.group(1) if m else None


def sector_carrier_number(ref: str | None) -> str | None:
    """'ENodeBFunction=1,SectorCarrier=19' -> '19'."""
    if not ref:
        return None
    m = re.search(r"SectorCarrier=(\d+)", ref)
    return m.group(1) if m else None


def strip_dot(value: str | None) -> str | None:
    """'17.398127' -> '17398127'.

    Coordinates go into the template without a decimal point; the 5G CCR
    already stores them that way ('17334600'), the 4G planning sheet does not.
    """
    if value is None:
        return None
    s = str(value).strip()
    return s.replace(".", "") if s else None


# EARFCN -> the band label used in the #Template strings
# ('BB6630_ L900+L1800+TDD-L2300...'), which is the vocabulary the template's
# Tech column uses. Ranges are the 3GPP downlink EARFCN allocations.
_BANDS = (
    (0, 599, "L2100"),         # band 1
    (1200, 1949, "L1800"),     # band 3
    (3450, 3799, "L900"),      # band 8
    (38650, 39649, "L2300"),   # band 40, TDD
)


def band_label(earfcn: str | None) -> str | None:
    if not earfcn:
        return None
    try:
        n = int(str(earfcn).strip())
    except ValueError:
        return None
    for lo, hi, label in _BANDS:
        if lo <= n <= hi:
            return label
    return None


# -- Site_Basic --------------------------------------------------------------

def _router_block(data: SiteData, router: int, sheets: tuple[str, ...]) -> dict:
    """The IP / gateway / VLAN of one router, selected on MO path.

    Router(1)/(2)/(3) are positional in the SSIS and map to OAM / LTE_S1 /
    LTE_UP respectively.
    """
    ip = data.value_by_mo(
        rf"Router\({router}\).*InterfaceIPv4\(1\).*AddressIPv4\(1\).*address",
        sheet_fragments=sheets, record_as=f"Router{router}.address")
    gw = data.value_by_mo(
        rf"Router\({router}\).*RouteTableIPv4Static\(1\).*NextHop\(1\).*address",
        sheet_fragments=sheets, record_as=f"Router{router}.nexthop")
    vlan = data.value_by_mo(
        rf"VlanPort\({router}\).*vlanId",
        sheet_fragments=sheets, record_as=f"VlanPort{router}.vlanId")
    return {"ip": ip, "gw": gw, "vlan": vlan}


def build_site_basic(data: SiteData) -> list[dict]:
    """One row per node: the LTE node, then the 5G node when the site has one."""
    rows = []

    name = data.value("Name", sheet_fragments=RN_SHEETS + SITEBASIC_4G + ARNE_SHEETS,
                      record_as="eNodeBName")
    oam = _router_block(data, 1, SITEBASIC_4G)
    s1 = _router_block(data, 2, SITEBASIC_4G)
    up = _router_block(data, 3, SITEBASIC_4G)
    abis = _router_block(data, 1, SITEBASIC_GSM)

    lte = {
        "Site ID": data.key,
        "eNodeBName": name,
        "Fingerprint": data.value("fingerprint", sheet_fragments=SITEBASIC_4G),
        "Phy SiteID/Userlabel": data.value("User Lable", sheet_fragments=PLANNING_SHEETS)
                                or data.value("USER LABLE", sheet_fragments=PLANNING_SHEETS),
        "Configuration_in_Node": CONFIGURATION_IN_NODE,
        "BB_Type": bb_type(data.value("#Template", sheet_fragments=SITEBASIC_4G)),
        "eNBId": data.value("eNBId", sheet_fragments=RN_SHEETS),
        "tnPortId": tn_port(data.value("upIpAddressRef", sheet_fragments=RN_SHEETS)),
        "OAM_vlan": oam["vlan"], "OAM_IP": oam["ip"], "OAM_GW": oam["gw"],
        "LTE_S1_vlan": s1["vlan"], "LTE_S1_IP": s1["ip"], "LTE_S1_GW": s1["gw"],
        "LTE_UP_vlan": up["vlan"], "LTE_UP_IP": up["ip"], "LTE_UP_GW": up["gw"],
        "ABIS_vlan": abis["vlan"], "ABIS_IP": abis["ip"], "ABIS_GW": abis["gw"],
    }
    rows.append(lte)

    # The 5G node is a separate row, as in the template (LNWG07 then
    # RJ-NLNWG007-1), and only exists when the site is in the CCR.
    nr_name = data.value("Name", sheet_fragments=NR_BASIC_SHEETS, record_as="gNodeBName")
    if nr_name:
        rows.append({
            "Site ID": data.key,
            "eNodeBName": nr_name,
            "Fingerprint": data.value("fingerprint", sheet_fragments=NR_BASIC_SHEETS),
            "Phy SiteID/Userlabel": data.value("userLabel", sheet_fragments=NR_BASIC_SHEETS),
            "NR_vlan": data.value("vlanId", sheet_fragments=NR_BASIC_SHEETS),
            "NR_IP": data.value("address-5g", sheet_fragments=NR_BASIC_SHEETS),
            "NR_GW": data.value("address-Gateway", sheet_fragments=NR_BASIC_SHEETS),
        })
    return rows


# -- Radio_HW ----------------------------------------------------------------

def sector_names(data: SiteData) -> tuple[dict[str, str], str]:
    """sector number -> SectorEquipmentFunction name, plus the node's prefix.

    Two spellings coexist in one node's inputs: the main SSIS references
    'SectorEquipmentFunction=Sector7' while the per-sector delta files declare
    'S4' / 'S22'. Neither can be assumed, so the names actually stated are
    collected and the prefix seen most often is used for the sectors that no
    sheet names - the main sheet only references three of its nine.
    """
    names: dict[str, str] = {}
    prefixes: list[str] = []

    def note(value: str | None):
        if not value:
            return
        m = re.fullmatch(r"([A-Za-z_]*?)(\d+)", value.strip())
        if not m:
            return
        prefix, number = m.group(1), m.group(2)
        names.setdefault(number, value.strip())
        prefixes.append(prefix)

    for hit in data.hits:
        for col in hit.sheet.columns:
            low = col.name.strip().lower()
            for r in hit.rows:
                if col.index >= len(r) or not r[col.index]:
                    continue
                if low == "sectorequipmentfunctionid":
                    note(r[col.index])
                elif low in ("sectorfunctionref", "sectorequipmentfunctionref"):
                    note(sector_equipment_id(r[col.index]))

    prefix = max(set(prefixes), key=prefixes.count) if prefixes else "S"
    return names, prefix


def sector_name(number: str | None, names: dict[str, str], prefix: str) -> str | None:
    if not number:
        return None
    return names.get(number) or f"{prefix}{number}"


def radio_units(data: SiteData) -> set[str]:
    """Sector numbers that actually have a radio at this site.

    A carrier with no radio of its own is a second carrier riding another
    carrier's RRU, which is what `resolve_sectors` uses to place it.
    """
    units = set()
    for blk in data.blocks("riPortRef2", sheet_fragments=EQUIP_SHEETS):
        fru = blk.get("fieldReplaceableUnitId") or fru_from_ref(blk.get("riPortRef2"))
        unit = unit_id(fru)
        if unit:
            units.add(unit)
    return units


def cell_sector_suffix(cell: str | None) -> str | None:
    """'AP_E_T1_OM_HY9532A_A' -> 'A' — the physical sector the cell serves."""
    if not cell:
        return None
    tail = cell.strip().rsplit("_", 1)[-1]
    return tail.upper() or None


def resolve_sectors(cells: list[dict], units: set[str],
                    names: dict[str, str], prefix: str) -> None:
    """Fill each cell's sectorEquipmentFunctionId in place.

    Carriers of one sector share its radio: T1 and T2 are two TDD carriers on
    the same antenna, so AP_E_T1_OM_..A_A and AP_E_T2_OM_..A_A both belong to
    Sector7 even though their sector-carrier numbers are 7 and 13. Only the
    carrier that owns a radio names the sector; a carrier with no RRU of its own
    borrows the sector from the carrier on the same band and the same physical
    sector that does have one.

    A value the source states outright always wins - the per-sector delta files
    declare their own sectorFunctionRef.
    """
    owners: dict[tuple[str | None, str | None], str] = {}
    for c in cells:
        if c["carrier"] in units:
            owners.setdefault((c["band"], c["suffix"]), c["carrier"])

    for c in cells:
        if c["explicit"]:
            c["sector"] = c["explicit"]
            continue
        carrier = c["carrier"]
        if carrier not in units:
            carrier = owners.get((c["band"], c["suffix"]), carrier)
        c["sector"] = sector_name(carrier, names, prefix)


def sector_bands(data: SiteData) -> dict[str, str]:
    """sector number -> band label, read from the cells carried on that sector.

    The AP equipment sheets never state a radio's band; the cells do, through
    their EARFCN, and each cell names the sector carrier it sits on.
    """
    out: dict[str, str] = {}
    for anchor in ("eUtranCellFDDId", "eUtranCellTDDId"):
        for blk in data.blocks(anchor, sheet_fragments=RN_SHEETS):
            get = blk.get
            number = (sector_carrier_number(get("sectorCarrierRef"))
                      or get("sectorCarrierId"))
            band = band_label(get("earfcndl") or get("earfcn"))
            if number and band:
                out.setdefault(number, band)
    return out


def build_radio_hw(data: SiteData) -> list[dict]:
    """One row per radio, from the equipment sheets (4G) and the CCR (5G)."""
    rows = []
    name = data.value("Name", sheet_fragments=RN_SHEETS + SITEBASIC_4G)
    baseband = bb_type(data.value("#Template", sheet_fragments=SITEBASIC_4G))
    names, prefix = sector_names(data)
    bands = sector_bands(data)

    # Anchored on riPortRef2 rather than on riLinkId: the main LTE equipment
    # sheet names its radios only through the RiLink port refs and carries no
    # riLinkId / fieldReplaceableUnitId columns at all, while the per-sector
    # delta files carry both. Anchoring on the ref covers both, and the explicit
    # columns are preferred wherever they exist.
    seen = set()
    for blk in data.blocks("riPortRef2", sheet_fragments=EQUIP_SHEETS):
        get = blk.get
        port_ref = get("riPortRef2")
        fru = get("fieldReplaceableUnitId") or fru_from_ref(port_ref)
        unit = unit_id(fru)
        # The radio's own number identifies its sector: the RiLink and
        # SectorEquipmentFunction column groups are separate blocks on this
        # sheet, but RRU-19 hangs off AntennaUnitGroup=19 and carries
        # SectorCarrier=19, so the unit number is the join key.
        group = antenna_group(get("rfBranchRef")) or unit

        if (fru, get("riPortRef1")) in seen:
            continue
        seen.add((fru, get("riPortRef1")))
        rows.append({
            "eNodeBName": name,
            "Configuration_in_Node": CONFIGURATION_IN_NODE,
            # The antenna-unit-group number identifies the sector (RRU-19 sits
            # on AntennaUnitGroup=19, carrying SectorCarrier=19), and the name
            # is spelled the way this node's own sheets spell it.
            "sectorEquipmentFunctionId": get("sectorEquipmentFunctionId")
                                         or sector_name(group, names, prefix),
            "Tech": bands.get(group),
            "Baseband_Type": baseband,
            "Radio_UnitId": unit,
            # riLinkId is absent from the main equipment sheet; it equals the
            # radio's unit number in every row that does carry it.
            "riLinkId": get("riLinkId") or unit,
            "RiPort_BB": ri_port(get("riPortRef1")),
            "RiPort_Radio": ri_port(port_ref),
        })

    nr_name = data.value("Name", sheet_fragments=NR_BASIC_SHEETS)
    for blk in data.blocks("riLinkId", sheet_fragments=NR_HW_SHEETS):
        get = blk.get
        # The AIR sheet names two FRUs per row - the radio (AAS-S1_N1) and the
        # baseband it hangs off (BB-1) - and both land in the same block, so
        # they are told apart by column order, radio first.
        frus = [c for c in blk.hit.sheet.occurrences("fieldReplaceableUnitId")]
        row = blk.hit.rows[blk.row]
        vals = [row[c.index] for c in frus if c.index < len(row)]
        radio_fru = vals[0] if vals else None
        bb_fru = vals[1] if len(vals) > 1 else None
        nr_band = data.value("bandListManual", sheet_fragments=NR_CELL_SHEETS)
        rows.append({
            "eNodeBName": nr_name,
            "Configuration_in_Node": "NR",
            "sectorEquipmentFunctionId": get("sectorEquipmentFunctionId"),
            "Tech": f"N{nr_band}" if nr_band else None,
            # The CCR names the baseband by FRU id ('BB-1'), which is a position
            # and not a type, so it is only accepted when it actually spells a
            # BBU model. Nothing in the 5G CCR does, so this stays blank rather
            # than passing 'BB-1' off as a baseband type.
            "Baseband_Type": bb_type(bb_fru),
            "Radio_UnitId": unit_id(radio_fru),
            "riLinkId": get("riLinkId"),
            "RiPort_BB": get("riPortId") or ri_port(get("riPortRef1")),
            "RiPort_Radio": ri_port(get("riPortRef2")),
        })
    return rows


# -- LTE-CELL ----------------------------------------------------------------

def _first_index_map(columns) -> dict[str, int]:
    """name -> index of its FIRST occurrence.

    Sheet1 repeats several headers ('LAT' sits at both c23 and c54, the second
    block being empty), so keeping the last index - as a plain dict
    comprehension does - reads the blank copy.
    """
    out: dict[str, int] = {}
    for c in columns:
        out.setdefault(c.name.strip().lower(), c.index)
    return out


def _planning_by_cell(data: SiteData) -> tuple[dict[str, dict], dict]:
    """Sheet1's RF planning rows keyed by cell name, plus a site-level fallback.

    LAT/LONG and the physical-layer ids live here rather than on the RN sheets,
    which leave those columns empty in the AP files. Sheet1 lists only the base
    carrier's cells (the F3 block), so the second return value carries the
    site-level values used for the carriers it does not name - correct for the
    coordinates, which are a property of the site, not of the carrier.
    """
    out: dict[str, dict] = {}
    site_level: dict = {}
    for hit in data.sheets_matching(*PLANNING_SHEETS):
        cols = _first_index_map(hit.sheet.columns)
        cell_col = next((cols[k] for k in cols
                         if k.startswith("sector carrier id")), None)
        if cell_col is None:
            continue
        for r in hit.rows:
            if cell_col >= len(r) or not r[cell_col]:
                continue
            get = lambda k: (r[cols[k]] if k in cols and cols[k] < len(r) else None)  # noqa: E731
            entry = {
                "Latitude": get("lat"),
                "Longitude": get("long"),
                "physicalLayerCellIdGroup": get("sss (physical layer cell id group)"),
                "physicalLayerSubCellId": get("pss(physical layer subcell id)"),
                "tac": get("tac"),
            }
            out[r[cell_col].strip().upper()] = entry
            for k in ("Latitude", "Longitude"):
                if entry[k] and k not in site_level:
                    site_level[k] = entry[k]
    return out, site_level


def build_lte_cell(data: SiteData) -> list[dict]:
    """One row per LTE cell, FDD and TDD."""
    rows = []
    name = data.value("Name", sheet_fragments=RN_SHEETS + SITEBASIC_4G)
    planning, site_coords = _planning_by_cell(data)
    names, prefix = sector_names(data)
    units = radio_units(data)
    pending = []

    for anchor, kind in (("eUtranCellFDDId", "FDD"), ("eUtranCellTDDId", "TDD")):
        for blk in data.blocks(anchor, sheet_fragments=RN_SHEETS):
            get = blk.get
            cell = get(anchor)
            plan = planning.get((cell or "").strip().upper(), {})

            # TDD sheets carry a single 'earfcn' and 'channelBandwidth' where
            # FDD splits them into dl/ul.
            earfcn_dl = get("earfcndl") or get("earfcn")
            earfcn_ul = get("earfcnul")
            bw_dl = get("dlChannelBandwidth") or get("channelBandwidth")
            bw_ul = get("ulChannelBandwidth") or get("channelBandwidth")

            # The sector the cell sits on, named as Radio_HW names it so the two
            # sheets agree - the generator joins them on this value.
            carrier = (sector_carrier_number(get("sectorCarrierRef"))
                       or get("sectorCarrierId"))

            # Sectors are resolved once every cell is known, because a second
            # carrier takes its sector from a sibling cell that may not have
            # been read yet.
            pending.append({
                "carrier": carrier,
                "band": band_label(earfcn_dl),
                "suffix": cell_sector_suffix(cell),
                "explicit": sector_equipment_id(get("sectorFunctionRef")),
            })

            rows.append({
                "eNodeBName": name,
                "eUtranCellFDDId": cell,
                "Eutrancell_Type": kind,
                "Configuration_in_Node": CONFIGURATION_IN_NODE,
                "Script_Required": SCRIPT_REQUIRED,
                "MME": MME_VENDOR,
                "sectorCarrierId": sector_carrier_id(get("sectorCarrierRef"))
                                   or get("sectorCarrierId"),
                "enbId": get("eNBId"),
                "earfcndl": earfcn_dl,
                "earfcnul": earfcn_ul,
                "dlChannelBandwidth": bw_dl,
                "ulChannelBandwidth": bw_ul,
                "Latitude": strip_dot(get("latitude") or plan.get("Latitude")
                                      or site_coords.get("Latitude")),
                "Longitude": strip_dot(get("longitude") or plan.get("Longitude")
                                       or site_coords.get("Longitude")),
                "cellId": get("cellId"),
                "physicalLayerCellIdGroup": get("physicalLayerCellIdGroup")
                                            or plan.get("physicalLayerCellIdGroup"),
                "physicalLayerSubCellId": get("physicalLayerSubCellId")
                                          or plan.get("physicalLayerSubCellId"),
                "tac": get("tac") or plan.get("tac"),
                "rachRootSequence": get("rachRootSequence"),
                "configuredMaxTxPower": get("configuredMaxTxPower"),
                "noOfTxAntennas": get("noOfTxAntennas"),
                "noOfRxAntennas": get("noOfRxAntennas"),
            })

    resolve_sectors(pending, units, names, prefix)
    for row, info in zip(rows, pending):
        row["sectorEquipmentFunctionId"] = info["sector"]
    return rows


# -- NR-CELL -----------------------------------------------------------------

def _set_ids(data: SiteData) -> dict[str, str]:
    """'RIM TAG' Set ID Range, keyed by cell short name."""
    out = {}
    for hit in data.sheets_matching(*RIM_TAG_SHEETS):
        cols = _first_index_map(hit.sheet.columns)
        short, setid = cols.get("short name"), cols.get("set id range")
        if short is None or setid is None:
            continue
        for r in hit.rows:
            if short < len(r) and setid < len(r) and r[short]:
                out[r[short].strip().upper()] = r[setid]
    return out


def build_nr_cell(data: SiteData) -> list[dict]:
    """One row per NR cell, from the 5G CCR."""
    rows = []
    name = data.value("Name", sheet_fragments=NR_CELL_SHEETS, record_as="gNodeBName")
    set_ids = _set_ids(data)

    for blk in data.blocks("nRCellDUId", sheet_fragments=NR_CELL_SHEETS):
        get = blk.get
        cell = get("nRCellDUId")
        rows.append({
            "gNodeBName": blk.hit.rows[blk.row][blk.hit.sheet.key_index] or name,
            "gUtranCell": cell,
            "gNBId": get("gNBId"),
            "sectorEquipmentFunctionId": sector_equipment_id(
                get("sectorEquipmentFunctionRef")),
            "nRSectorCarrierId": get("nRSectorCarrierId"),
            "cellLocalId": get("cellLocalId"),
            "nRPCI": get("nRPCI"),
            "nRTAC": get("nRTAC"),
            "rachRootSequence": get("rachRootSequence"),
            "ssbFrequency": get("ssbFrequency"),
            "arfcnDL": get("arfcnDL"),
            "arfcnUL": get("arfcnUL"),
            "bSChannelBwDL/UL": get("bSChannelBwDL") or get("bSChannelBwUL"),
            "configuredMaxTxPower": get("configuredMaxTxPower"),
            "Latitude": strip_dot(get("latitude")),
            "Longitude": strip_dot(get("longitude")),
            "SetID": set_ids.get((cell or "").strip().upper()),
        })
    return rows


BUILDERS = {
    "Site_Basic": build_site_basic,
    "Radio_HW": build_radio_hw,
    "LTE-CELL": build_lte_cell,
    "NR-CELL": build_nr_cell,
}
