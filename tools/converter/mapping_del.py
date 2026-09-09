"""DEL circle: input columns -> template columns.

DEL supplies Ericsson SSIS exports like AP, but laid out the other way round.
AP's sheets are **wide**: one row per site, with the cell/radio block repeated
across the columns. DEL's are **tall**: one row per cell and one row per radio,
with the node named in column 0 of every row. So none of AP's block machinery is
needed here - a row *is* a record - and the rules read columns by occurrence
instead, which matters because these sheets do repeat a name within one row
(`fieldReplaceableUnitId` is the radio first and the baseband second).

The other structural difference is that **a DEL site carries two 4G nodes**:
'LD47793' holds the L900, L1800 and TDD layers, 'LU47793' the L2100 one, and
they are separate managed elements with their own eNBId, cells and radios. Every
sheet therefore has to be grouped by its own row's node name rather than given a
site-level one, because the generator joins Site_Basic, Radio_HW and LTE-CELL on
`eNodeBName`.

The 2G node is spelled 'X47793' and lives in its own SSIS, which supplies the
ABIS transport.
"""
from __future__ import annotations

import re

from .mapping_ap import band_label, ri_port, strip_dot, unit_id
from .sitedata import SheetHit, SiteData

CIRCLE = "DEL"

# 'LD47793', 'LU47793' and 'X47793' are three nodes of site 47793; the id is the
# bare number. The AP rule ('L' + site id) never fires on these and would be
# wrong if it did, so it stays on only to leave AP-shaped names alone.
STRIP_NODE_PREFIX = True
NUMERIC_SITE_IDS = True

# Sheets are found by the columns they carry, not by name: the numbers in
# 'S_FDD_22RN' / 'S_TDD_44RN' / 'S_SiteBasic_IPv6' spell the configuration and
# the IP version of one particular delivery, and a substring that matched them
# would miss the next SSIS. The anchor column is the sheet's subject and does
# not move.
FDD_CELL_ANCHOR = "eUtranCellFDDId"
TDD_CELL_ANCHOR = "eUtranCellTDDId"
RADIO_ANCHOR = "riLinkId"
NODE_ANCHOR = "eNBId"           # S_SiteBasic_IPv4 / _IPv6
GSM_ANCHOR = "gsmSectorId"      # S_2G_RN

# Written as a fixed value rather than read from the inputs, as in AP.
CONFIGURATION_IN_NODE = "LTE"
SCRIPT_REQUIRED = "YES"

# LTE-CELL's MME column is a vendor selector, not an MME id - see
# mapping_ap.MME_VENDOR. Nothing in the DEL inputs names a vendor either.
MME_VENDOR = "CISCO"

UNMAPPED = {
    "Site_Basic": {
        "ENM": "no ENM name in the DEL SSIS",
        # LTE_Integration_Scripting_Automtion picks DEL's SiteBasic and
        # SiteEquipment scripts by the BBU model in this column ('6630',
        # '6651', '5216', ...), so a blank here means no commissioning script
        # is written for the node.
        "BB_Type": "the DEL SSIS never names the baseband model: Node Type is "
                   "'Baseband', #Template is the folder path 'DL\\4G_SiteBasic_IPv6' "
                   "and S_Base_HW carries no columns at all. Only the file name "
                   "hints at the hardware - fill this in before generating scripts",
        "tnPortId": "no transport-port reference in the DEL SSIS: nothing names a "
                    "TN_ interface, and there is no upIpAddressRef column as in AP",
        "Bridge_tnPortId": "not present in any DEL sheet",
        "NR_PORT": "no 5G data in the DEL inputs",
        "NR_vlan": "no 5G data in the DEL inputs",
        "NR_IP": "no 5G data in the DEL inputs",
        "NR_GW": "no 5G data in the DEL inputs",
        "NR_ENDC_IP": "no 5G data in the DEL inputs",
        "NR_ENDC_GW": "no 5G data in the DEL inputs",
        "Anchor_ENDC_IP": "no 5G data in the DEL inputs",
        "Anchor_ENDC_GW": "no 5G data in the DEL inputs",
        "Anchor Gnb ID": "no 5G data in the DEL inputs",
        "Anchor NR IP": "no 5G data in the DEL inputs",
    },
    "Radio_HW": {
        # Same consequence as BB_Type: the RRU_* script templates are chosen by
        # the model number in this column.
        "Radio_Type": "the DEL SSIS names radios by position ('RRU-31'), never by "
                      "model; only the SSIS file name mentions one - fill this in "
                      "before generating scripts",
        "Baseband_Type": "no baseband model anywhere in the DEL inputs; the "
                         "equipment sheets give the baseband only its FRU number ('4')",
    },
    "LTE-CELL": {
        "crsGain": "no such column in any DEL input sheet",
    },
    "NR-CELL": {
        "*": "no 5G data in the DEL inputs - the DEL CCR workbooks are 2G RF data "
             "entry forms (BCCH/BSIC/CGI), and a 5G CCR would be needed",
    },
}


# -- reading a tall sheet ----------------------------------------------------

class Record:
    """One row of a sheet, read by column name and occurrence.

    `Block` cannot serve here: it keys its window by column name, so where a
    name repeats within the row it keeps only the last one - and on the DEL
    equipment sheets `fieldReplaceableUnitId` is the radio ('RRU-31') at its
    first occurrence and the baseband ('4') at its second.
    """

    def __init__(self, hit: SheetHit, row: list):
        self.hit = hit
        self.row = row

    def get(self, column_name: str, occurrence: int = 0) -> str | None:
        cols = self.hit.sheet.occurrences(column_name)
        if occurrence >= len(cols):
            return None
        index = cols[occurrence].index
        return self.row[index] if index < len(self.row) else None

    def by_mo(self, mo_pattern: str) -> str | None:
        """The value of the first column whose MO path matches.

        The transport columns are all called 'address' or 'vlanId' and are told
        apart only by the MO they write to - Router(1) vs Router(2), the
        interface address vs the route's next hop.
        """
        rx = re.compile(mo_pattern, re.IGNORECASE)
        for col in self.hit.sheet.columns:
            if col.mo and rx.search(col.mo) and col.index < len(self.row):
                if self.row[col.index] is not None:
                    return self.row[col.index]
        return None

    @property
    def node(self) -> str | None:
        """The node this row belongs to - column 0 on every DEL sheet."""
        return self.get("Name")


def records(data: SiteData, anchor: str) -> list[Record]:
    """Every row of every sheet carrying `anchor`, as records."""
    out = []
    for hit in data.sheets_with(anchor):
        for row in hit.rows:
            record = Record(hit, row)
            if record.get(anchor) is not None:
                out.append(record)
    return out


def _router(record: Record, router: int) -> dict:
    """The IP / gateway / VLAN of one router, selected on MO path.

    Router(1)/(2)/(3) are positional in the SSIS and map to OAM / LTE_S1 /
    LTE_UP, as in AP. Both IP versions are accepted: DEL delivers OAM over IPv6
    (`Router(1) InterfaceIPv6(1) AddressIPv6(1)`) while S1 and UP stay IPv4, and
    the same workbook ships an all-IPv4 sheet for the sites that use it.
    """
    return {
        "ip": record.by_mo(rf"Router\({router}\).*InterfaceIPv[46]\(1\)"
                           rf".*AddressIPv[46]\(1\).*address"),
        "gw": record.by_mo(rf"Router\({router}\).*RouteTableIPv[46]Static\(1\)"
                           rf".*NextHop\(1\).*address"),
        "vlan": record.by_mo(rf"VlanPort\({router}\).*vlanId"),
    }


# -- Site_Basic --------------------------------------------------------------

def _baseband_units(data: SiteData) -> dict[str, str]:
    """node -> the FRU number of its baseband.

    The equipment sheets state two FRUs per radio row: the radio at the first
    `fieldReplaceableUnitId` and, at the second, the baseband it hangs off - the
    same unit the RiLink's `riPortRef1` points at ('FieldReplaceableUnit=4').
    """
    out: dict[str, str] = {}
    for record in records(data, RADIO_ANCHOR):
        node, unit = record.node, record.get("fieldReplaceableUnitId", 1)
        if node and unit:
            out.setdefault(node, unit)
    return out


def _abis(data: SiteData) -> dict | None:
    """The GSM node's transport, from the 2G SSIS.

    Recognised as the transport sheet that has no eNBId: the 2G delta sheet
    carries the same 'address' and 'vlanId' columns under the same Router(1) /
    VlanPort(1) MO paths as the 4G SiteBasic sheets, and nothing but the
    absence of the eNB tells them apart.
    """
    for hit in data.sheets_with("vlanId"):
        if hit.sheet.has(NODE_ANCHOR):
            continue
        for row in hit.rows:
            return _router(Record(hit, row), 1)
    return None


def abis_node(data: SiteData, nodes: list[str]) -> str | None:
    """Which 4G node the GSM ABIS transport belongs to.

    A DEL site runs two 4G nodes, and the 2G SSIS names neither: its ABIS row is
    keyed on the GSM node ('X47793'). But its TRXs say which sectors they sit
    on - `sectorEquipmentFunctionRef = ...SectorEquipmentFunction=S31` - and
    those sector equipment functions are declared by exactly one of the 4G
    nodes' equipment sheets. So GSM shares that node's radios, and the ABIS
    addressing belongs on its row.
    """
    wanted = set()
    for record in records(data, GSM_ANCHOR):
        for col in record.hit.sheet.occurrences("sectorEquipmentFunctionRef"):
            if col.index >= len(record.row):
                continue
            m = re.search(r"SectorEquipmentFunction=([A-Za-z0-9_]+)",
                          str(record.row[col.index] or ""))
            if m:
                wanted.add(m.group(1))
    if not wanted:
        return None

    for record in records(data, RADIO_ANCHOR):
        if record.get("sectorEquipmentFunctionId") in wanted and record.node in nodes:
            return record.node
    return None


def build_site_basic(data: SiteData) -> list[dict]:
    """One row per node - a DEL site has two 4G nodes, not one."""
    basebands = _baseband_units(data)

    rows, nodes = [], []
    for record in records(data, NODE_ANCHOR):
        node = record.node
        if node in nodes:               # the IPv4 and IPv6 sheets overlap
            continue
        nodes.append(node)
        oam, s1, up = _router(record, 1), _router(record, 2), _router(record, 3)
        rows.append({
            "Site ID": data.key,
            "eNodeBName": node,
            "Fingerprint": record.get("fingerprint"),
            "Phy SiteID/Userlabel": record.get("userLabel"),
            "Configuration_in_Node": CONFIGURATION_IN_NODE,
            "eNBId": record.get("eNBId"),
            "fieldReplaceableUnitId": basebands.get(node),
            "OAM_vlan": oam["vlan"], "OAM_IP": oam["ip"], "OAM_GW": oam["gw"],
            "LTE_S1_vlan": s1["vlan"], "LTE_S1_IP": s1["ip"], "LTE_S1_GW": s1["gw"],
            "LTE_UP_vlan": up["vlan"], "LTE_UP_IP": up["ip"], "LTE_UP_GW": up["gw"],
        })

    # ABIS comes from the 2G SSIS and belongs to one node, not to both.
    abis = _abis(data)
    if abis and rows:
        owner = abis_node(data, nodes) or nodes[0]
        for row in rows:
            if row["eNodeBName"] == owner:
                row.update({"ABIS_vlan": abis["vlan"], "ABIS_IP": abis["ip"],
                            "ABIS_GW": abis["gw"]})
    return rows


# -- Radio_HW ----------------------------------------------------------------

def sector_bands(data: SiteData) -> dict[tuple[str | None, str | None], str]:
    """(node, sectorEquipmentFunctionId) -> band label.

    The equipment sheets never state a radio's band; the cells carried on it do,
    through their EARFCN, and every cell names its sector equipment function
    outright in `sectorFunctionRef`. Keyed by node as well as by sector because
    the two nodes number their sectors independently.
    """
    out: dict[tuple[str | None, str | None], str] = {}
    for anchor, earfcn_columns in ((FDD_CELL_ANCHOR, ("earfcndl",)),
                                   (TDD_CELL_ANCHOR, ("earfcn",))):
        for record in records(data, anchor):
            sector = sector_equipment_id(record.get("sectorFunctionRef"))
            band = band_label(next((record.get(c) for c in earfcn_columns
                                    if record.get(c)), None))
            if sector and band:
                out.setdefault((record.node, sector), band)
    return out


def sector_equipment_id(ref: str | None) -> str | None:
    """'NodeSupport=1,SectorEquipmentFunction=S31' -> 'S31'."""
    if not ref:
        return None
    m = re.search(r"SectorEquipmentFunction=([A-Za-z0-9_]+)", ref)
    return m.group(1) if m else None


def build_radio_hw(data: SiteData) -> list[dict]:
    """One row per radio, from the FDD and TDD equipment sheets."""
    bands = sector_bands(data)
    rows, seen = [], set()

    for record in records(data, RADIO_ANCHOR):
        node = record.node
        sector = record.get("sectorEquipmentFunctionId")
        # One row per RiLink of a node. The FDD and TDD sheets never describe
        # the same radio, but a re-delivered SSIS can repeat one.
        key = (node, record.get(RADIO_ANCHOR))
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            "eNodeBName": node,
            "Configuration_in_Node": CONFIGURATION_IN_NODE,
            "sectorEquipmentFunctionId": sector,
            "Tech": bands.get((node, sector)),
            # The radio is the first fieldReplaceableUnitId ('RRU-31'); the
            # second is the baseband it hangs off ('4').
            "Radio_UnitId": unit_id(record.get("fieldReplaceableUnitId", 0)),
            "riLinkId": record.get(RADIO_ANCHOR),
            # riPortId is the baseband end of the link, stated under
            # FieldReplaceableUnit(2)/RiPort(1), and repeated in riPortRef1.
            "RiPort_BB": record.get("riPortId") or ri_port(record.get("riPortRef1")),
            "RiPort_Radio": ri_port(record.get("riPortRef2")),
        })
    return rows


# -- LTE-CELL ----------------------------------------------------------------

def _enb_ids(data: SiteData) -> dict[str, str]:
    """node -> eNBId, from the SiteBasic sheet.

    The DEL cell sheets do not carry eNBId at all, and the site's two nodes have
    different ones (947793 and 647793), so it is looked up per node.
    """
    out: dict[str, str] = {}
    for record in records(data, NODE_ANCHOR):
        if record.node:
            out.setdefault(record.node, record.get("eNBId"))
    return out


def build_lte_cell(data: SiteData) -> list[dict]:
    """One row per LTE cell, FDD and TDD."""
    enbs = _enb_ids(data)
    rows = []

    for anchor, kind in ((FDD_CELL_ANCHOR, "FDD"), (TDD_CELL_ANCHOR, "TDD")):
        for record in records(data, anchor):
            # The TDD sheet carries a single 'earfcn' and 'channelBandwidth'
            # where FDD splits them into dl/ul.
            earfcn_dl = record.get("earfcndl") or record.get("earfcn")
            bandwidth = record.get("channelBandwidth")
            rows.append({
                "eNodeBName": record.node,
                "eUtranCellFDDId": record.get(anchor),
                "Eutrancell_Type": kind,
                "Configuration_in_Node": CONFIGURATION_IN_NODE,
                "Script_Required": SCRIPT_REQUIRED,
                "MME": MME_VENDOR,
                "sectorEquipmentFunctionId": sector_equipment_id(
                    record.get("sectorFunctionRef")),
                "sectorCarrierId": record.get("sectorCarrierId"),
                "enbId": enbs.get(record.node),
                "earfcndl": earfcn_dl,
                "earfcnul": record.get("earfcnul"),
                "dlChannelBandwidth": record.get("dlChannelBandwidth") or bandwidth,
                "ulChannelBandwidth": record.get("ulChannelBandwidth") or bandwidth,
                # Already written without the decimal point in these sheets
                # ('28418236' = 28.418236); strip_dot leaves them alone.
                "Latitude": strip_dot(record.get("latitude")),
                "Longitude": strip_dot(record.get("longitude")),
                "cellId": record.get("cellId"),
                "physicalLayerCellIdGroup": record.get("physicalLayerCellIdGroup"),
                "physicalLayerSubCellId": record.get("physicalLayerSubCellId"),
                "tac": record.get("tac"),
                "rachRootSequence": record.get("rachRootSequence"),
                "configuredMaxTxPower": record.get("configuredMaxTxPower"),
                "noOfTxAntennas": record.get("noOfTxAntennas"),
                "noOfRxAntennas": record.get("noOfRxAntennas"),
            })
    return rows


# -- NR-CELL -----------------------------------------------------------------

def build_nr_cell(data: SiteData) -> list[dict]:
    """Empty: the DEL inputs carry no 5G data."""
    return []


BUILDERS = {
    "Site_Basic": build_site_basic,
    "Radio_HW": build_radio_hw,
    "LTE-CELL": build_lte_cell,
    "NR-CELL": build_nr_cell,
}
