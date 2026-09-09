"""HR circle: input columns -> template columns.

HR's inputs are a different kind of document from AP's. AP supplies Ericsson
SSIS exports - per-node, with MO paths, transport addressing and an equipment
inventory. HR supplies circle-wide **master RF data**: one row per cell, listing
what RF planning decided (cell name, eNB, sector, PCI, RSI, TAC, coordinates)
and nothing else.

So only LTE-CELL can be filled properly. The consequences are stated in
UNMAPPED and repeated here because they matter before the output is used:

  * **Radio_HW comes out empty.** Nothing in these files describes a radio,
    a baseband, a RiLink or a sector equipment function.
  * **NR-CELL comes out empty.** There is no 5G data.
  * **Site_Basic has the identity fields only** - no OAM/S1/UP/ABIS addressing,
    no VLANs, no fingerprint, no BB type, because none of it is in the inputs.

Filling those needs HR's SSIS / CCR workbooks in reference/HR/ as well; the AP
mapping shows what they look like. The two bands arrive as separate files
(L2100 and L850) and are merged here into one cell list.
"""
from __future__ import annotations

import re

from .sitedata import SiteData

CIRCLE = "HR"

# HR keys on bare site ids, several of which begin with L ('LOOK48'), so the
# leading letter must not be treated as AP's 4G node prefix.
STRIP_NODE_PREFIX = False

# Sheet-name fragments per source. 'RF Data Sheet' is the full L2100 master but
# is normally skipped by the reader for width (see ssis.MAX_SHEET_WIDTH); the
# Ericsson subsets carry the same columns and are read instead.
L2100_SHEETS = ("rf data sheet", "script data", "ericcson shared data")
L850_SHEETS = ("l850",)

UNMAPPED = {
    "Site_Basic": {
        "Fingerprint": "HR master RF data carries no node fingerprint",
        "ENM": "not in the HR inputs",
        "BB_Type": "no baseband type in the HR inputs",
        "Configuration_in_Node": "not stated; AP takes it from the SSIS template name",
        "fieldReplaceableUnitId": "no equipment inventory in the HR inputs",
        "tnPortId": "no transport data in the HR inputs",
        "Bridge_tnPortId": "no transport data in the HR inputs",
        "OAM_vlan": "no transport data in the HR inputs",
        "OAM_IP": "no transport data in the HR inputs",
        "OAM_GW": "no transport data in the HR inputs",
        "LTE_S1_vlan": "no transport data in the HR inputs",
        "LTE_S1_IP": "no transport data in the HR inputs",
        "LTE_S1_GW": "no transport data in the HR inputs",
        "LTE_UP_vlan": "no transport data in the HR inputs",
        "LTE_UP_IP": "no transport data in the HR inputs",
        "LTE_UP_GW": "no transport data in the HR inputs",
        "ABIS_vlan": "no transport data in the HR inputs",
        "ABIS_IP": "no transport data in the HR inputs",
        "ABIS_GW": "no transport data in the HR inputs",
        "NR_PORT": "no 5G data in the HR inputs",
        "NR_vlan": "no 5G data in the HR inputs",
        "NR_IP": "no 5G data in the HR inputs",
        "NR_GW": "no 5G data in the HR inputs",
        "NR_ENDC_IP": "no 5G data in the HR inputs",
        "NR_ENDC_GW": "no 5G data in the HR inputs",
        "Anchor_ENDC_IP": "no 5G data in the HR inputs",
        "Anchor_ENDC_GW": "no 5G data in the HR inputs",
        "Anchor Gnb ID": "no 5G data in the HR inputs",
        "Anchor NR IP": "no 5G data in the HR inputs",
    },
    "Radio_HW": {
        "*": "the HR inputs are RF planning data and describe no equipment; "
             "an SSIS export is needed to fill this sheet",
    },
    "LTE-CELL": {
        "sectorEquipmentFunctionId": "no equipment inventory in the HR inputs",
        "earfcnul": "master RF data states no uplink EARFCN",
        "dlChannelBandwidth": "bandwidth not stated in the HR master RF data",
        "ulChannelBandwidth": "bandwidth not stated in the HR master RF data",
        "configuredMaxTxPower": "not stated in the HR master RF data",
        "crsGain": "not stated in the HR master RF data",
        "noOfTxAntennas": "not stated in the HR master RF data",
        "noOfRxAntennas": "not stated in the HR master RF data",
        "MME": "vendor not stated in the HR inputs; see mapping_ap.MME_VENDOR",
    },
    "NR-CELL": {
        "*": "no 5G data in the HR inputs",
    },
}

CONFIGURATION_IN_NODE = "LTE"
SCRIPT_REQUIRED = "YES"

# Downlink EARFCN per band, from the L850 workbook's own Sheet2 lookup
# (L850 2438, L1800 1434, L2100 415, TDD1 39150, TDD2 39348).
EARFCN = {"L850": "2438", "L1800": "1434", "L2100": "415"}


def strip_dot(value: str | None) -> str | None:
    """'30.374685' -> '30374685', matching the template's coordinate style."""
    if value is None:
        return None
    s = str(value).strip()
    return s.replace(".", "") if s else None


def pci_split(pci: str | None) -> tuple[str | None, str | None]:
    """PCI -> (physicalLayerCellIdGroup, physicalLayerSubCellId).

    PCI = 3 * group + sub, so the pair is recoverable where the sheet gives only
    the PCI. The L850 sheet states PCG/PSG outright and those are preferred.
    """
    if pci is None:
        return None, None
    try:
        n = int(float(str(pci).strip()))
    except ValueError:
        return None, None
    return str(n // 3), str(n % 3)


def _first(data: SiteData, names: tuple[str, ...],
           sheets: tuple[str, ...]) -> str | None:
    for n in names:
        v = data.value(n, sheet_fragments=sheets)
        if v is not None:
            return v
    return None


def build_site_basic(data: SiteData) -> list[dict]:
    """A single identity row - all the HR inputs support."""
    enb = _first(data, ("L2100 eNB ID (old)", "Enode B", "L2100 eNB ID (ZTE)"),
                 L2100_SHEETS) or data.value("L850 eNB", sheet_fragments=L850_SHEETS)
    return [{
        "Site ID": data.key,
        "eNodeBName": data.key,
        "Phy SiteID/Userlabel": _first(data, ("Physical Site Id", "Pyhsical Site ID"),
                                       L2100_SHEETS),
        "eNBId": enb,
    }]


def build_radio_hw(data: SiteData) -> list[dict]:
    """Empty: the HR inputs describe no equipment."""
    return []


def _cells(data: SiteData, sheets: tuple[str, ...], spec: dict) -> list[dict]:
    """Cells from one band, merged across that band's sheets.

    A site is usually listed on more than one sheet of the same workbook, and
    they do not carry the same columns - 'Ericcson Shared Data' names the eNB
    but has no coordinates, 'Script Data' has both. So a cell seen again fills
    in the fields still missing rather than being discarded, and each field is
    looked up under every spelling the sheets use for it.
    """
    # Every value the sheets offer for this cell, keyed by column name.
    raw: dict[str, dict[str, str]] = {}
    names: dict[str, str] = {}
    order: list[str] = []

    for blk in data.blocks(spec["cell"], sheet_fragments=sheets):
        cell = blk.get(spec["cell"])
        if not cell:
            continue
        key = cell.upper()
        if key not in raw:
            order.append(key)
            raw[key], names[key] = {}, cell
        seen = raw[key]
        for column in spec["columns"]:
            if column not in seen:
                v = blk.get(column)
                if v is not None:
                    seen[column] = v

    def pick(seen: dict, candidates: tuple[str, ...]):
        """The value under the first column name that has one.

        Priority is by *column*, not by which sheet happened to be read first:
        the sheets disagree, and the disagreement is systematic. 'Enode B' is
        the Ericsson eNB where 'L2100 eNB ID (ZTE)' is ZTE's, and 'Updated TAC'
        supersedes 'L2100 TAC' - for ADPR96 that is 620, agreeing with the L850
        workbook, where the un-updated column says 690.
        """
        for c in candidates:
            if seen.get(c) is not None:
                return seen[c]
        return None

    rows = []
    for key in order:
        seen = raw[key]
        group = pick(seen, spec.get("group", ()))
        sub = pick(seen, spec.get("sub", ()))
        if group is None:
            group, sub = pci_split(pick(seen, spec["pci"]))

        sector = pick(seen, spec["sector"])
        rows.append({
            "eNodeBName": data.key,
            "eUtranCellFDDId": names[key],
            "Eutrancell_Type": "FDD",
            "Configuration_in_Node": CONFIGURATION_IN_NODE,
            "Script_Required": SCRIPT_REQUIRED,
            "earfcndl": EARFCN.get(spec["band"]),
            "sectorCarrierId": sector,
            "cellId": sector,
            "enbId": pick(seen, spec["enb"]),
            "tac": pick(seen, spec["tac"]),
            "rachRootSequence": pick(seen, spec["rsi"]),
            "physicalLayerCellIdGroup": group,
            "physicalLayerSubCellId": sub,
            "Latitude": strip_dot(pick(seen, spec["lat"])),
            "Longitude": strip_dot(pick(seen, spec["long"])),
        })
    return rows


def _with_columns(spec: dict) -> dict:
    """Every column name a spec references, for the gather pass."""
    cols = set()
    for key, value in spec.items():
        if isinstance(value, tuple):
            cols |= set(value)
    spec["columns"] = tuple(cols)
    return spec


def build_lte_cell(data: SiteData) -> list[dict]:
    """One row per cell, merging the L2100 and L850 masters."""
    return (
        _cells(data, L2100_SHEETS, _with_columns({
            "band": "L2100",
            "cell": "L2100 Cell Name New Nomenclature",
            "sector": ("L2100 Sector ID",),
            # Spelled differently on each sheet: 'Enode B' on Script Data,
            # '(ZTE)'/'(Eric)' on Ericcson Shared Data, '(old)' on the master.
            "enb": ("Enode B", "L2100 eNB ID (old)", "L2100 eNB ID (ZTE)"),
            "pci": ("L2100 PCI",),
            "rsi": ("L2100 RSI",),
            "tac": ("Updated TAC", "L2100 TAC"),
            # 'Script Lat/Long' are already point-free; plain Lat/Long are not.
            "lat": ("Script Lat", "Lat"),
            "long": ("Script Long", "Long"),
        }))
        + _cells(data, L850_SHEETS, _with_columns({
            "band": "L850",
            "cell": "E/// Cell Nomenclature",
            "sector": ("L850 FDD Sector ID",),
            "enb": ("L850 eNB",),
            "pci": ("L850 PCI",),
            "group": ("PCG",),
            "sub": ("PSG",),
            "rsi": ("L850 RSI",),
            "tac": ("L850 TAC",),
            "lat": ("Lat",),
            "long": ("Long",),
        }))
    )


def build_nr_cell(data: SiteData) -> list[dict]:
    """Empty: no 5G data in the HR inputs."""
    return []


BUILDERS = {
    "Site_Basic": build_site_basic,
    "Radio_HW": build_radio_hw,
    "LTE-CELL": build_lte_cell,
    "NR-CELL": build_nr_cell,
}
