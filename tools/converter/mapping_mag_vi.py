"""MAG_Vi: Vodafone Idea's RF database + IP plan -> integration template.

Seeded from mapping_del_vi.py. Everything below still describes DEL_Vi's
sources - sheet names, IP-family choices and the cell-naming rule are
repeated verbatim and have NOT been checked against MAG's workbooks.

The sources look nothing like the other circles'. AP/DEL ship Ericsson SSIS
exports - wide sheets whose columns repeat once per cell, with the MO path on
row 1 and the header on row 3. VI ships two ordinary tables instead:

    Ericsson RF DataBase *.xlsb   header on row 0, one row per CELL
        '4G DB'  one row per EUtranCell   (~1300 rows, ~395 sites)
        '2G DB'  one row per GSM cell
        '5G DB'  one row per NR cell
        others   'DB Ask List', 'CGI', 'NBR', '5G MM Wave' - not used here

    IP Plan *.xlsx                header on row 0, one row per SITE
        every transport address, as CODE_IP_SERVICE_PLANNING_<tech>_<plane>_*

So there is no block-walking to do: a cell is a row, and `data.hits` already
holds only this site's rows. The builders iterate rows directly rather than
using `SiteData.blocks()`, which exists for the repeated-column layouts.

The split across two files matters: the RF database carries no transport and
the IP plan carries no radio data, so a site needs a row in BOTH to produce a
complete Site_Basic. See UNMAPPED and the module docstring note below.

IP families: the plan holds IPv4 and IPv6 for each plane. VI's Delhi nodes are
IPv6 for OAM/S1C/S1U and IPv4 for Abis, and the LTE generator detects the family
from the address text, so IPv6 is preferred where present and IPv4 used
otherwise. Addresses are emitted with their prefix length ('…/126'), which is
the form Site_Basic carries and 01_SiteBasic expects.
"""
from __future__ import annotations

from .sitedata import SiteData

CIRCLE = "MAG_Vi"

# Site ids are already canonical here ('DEL22561'), not node names, so no
# prefix stripping: 'LO01INDL414669' is the node and never the key.
STRIP_NODE_PREFIX = False
NUMERIC_SITE_IDS = False

# Sheet name fragments, matched case-insensitively.
FOURG_SHEETS = ("4g db",)
TWOG_SHEETS = ("2g db",)
FIVEG_SHEETS = ("5g db",)
IP_SHEETS = ("sheet1",)          # the IP plan's only tab

CONFIGURATION_IN_NODE = "LTE"
SCRIPT_REQUIRED = "YES"

#: Columns nothing in these two sources can fill, with the reason. Surfaced by
#: the API as `empty_columns` so the gap is visible before the output is used
#: to generate scripts.
_NO_EQUIPMENT = ("The RF database describes cells, not equipment: it carries no "
                 "radio type, RiLink, baseband port or FRU id.")

UNMAPPED = {
    "Site_Basic": {
        "BB_Type": "Not in the RF database or the IP plan.",
        "fieldReplaceableUnitId": _NO_EQUIPMENT,
        "tnPortId": "Transport port naming is not in the IP plan.",
        "Bridge_tnPortId": "Transport port naming is not in the IP plan.",
        "Anchor_ENDC_IP": "ENDC anchoring is not planned in these sources.",
        "Anchor_ENDC_GW": "ENDC anchoring is not planned in these sources.",
        "Anchor Gnb ID": "ENDC anchoring is not planned in these sources.",
        "Anchor NR IP": "ENDC anchoring is not planned in these sources.",
        "NR_PORT": "Transport port naming is not in the IP plan.",
    },
    "Radio_HW": {"*": _NO_EQUIPMENT},
    "LTE-CELL": {
        "earfcnul": "The 4G DB carries earfcndl only; the uplink is not planned.",
        "noOfTxAntennas": "Antenna counts are not in the 4G DB "
                          "('Transmission Mode' names the MIMO mode, not the count).",
        "noOfRxAntennas": "Antenna counts are not in the 4G DB.",
        "crsGain": "Not in the 4G DB.",
        "MME": "The IP plan's MME_ID/MME_IP columns are blank in this export.",
    },
    "NR-CELL": {
        "Radio_Type": "Not in the 5G DB.",
        "sectorEquipmentFunctionId": _NO_EQUIPMENT,
        "nRSectorCarrierId": _NO_EQUIPMENT,
        "ssbFrequency": "Frequencies are not in the 5G DB.",
        "arfcnDL": "Frequencies are not in the 5G DB.",
        "arfcnUL": "Frequencies are not in the 5G DB.",
        "bSChannelBwDL/UL": "Bandwidth is not in the 5G DB.",
        "configuredMaxTxPower": "Not in the 5G DB.",
        "SetID": "Not in the 5G DB.",
    },
}


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _rows(data: SiteData, fragments: tuple[str, ...]) -> list[tuple[dict, str]]:
    """This site's rows on the matching sheets, as {column name: value}.

    Returns (row, sheet label) so a builder can record where a value came from.
    Column names are lower-cased because the same field is spelled 'Site ID',
    'Site_id' and 'site name' across the three RF sheets.
    """
    out = []
    for hit in data.sheets_matching(*fragments):
        index = {c.name.strip().lower(): c.index for c in hit.sheet.columns}
        for r in hit.rows:
            out.append((
                {name: (r[i] if i < len(r) else None) for name, i in index.items()},
                hit.label,
            ))
    return out


def _get(row: dict, *names: str):
    """First non-empty value under any of `names` (case-insensitive)."""
    for n in names:
        v = row.get(n.strip().lower())
        if v is not None and str(v).strip() != "":
            return str(v).strip()
    return None


def _int(value):
    """'21.0' -> '21'. Excel hands every number back as a float."""
    if value is None:
        return None
    s = str(value).strip()
    try:
        f = float(s)
    except ValueError:
        return s
    return str(int(f)) if f.is_integer() else s


def prefix_length(subnet):
    """A subnet as the '/n' the template carries.

    The plan writes IPv6 subnets as a length already ('126') and IPv4 subnets
    as a dotted mask ('255.255.255.252'). A mask is the count of its set bits,
    so 255.255.255.240 -> 28, .248 -> 29, .252 -> 30 - the whole rule, no table
    needed. Anything unrecognised returns None so the address is emitted bare
    rather than with a wrong prefix.
    """
    if subnet is None:
        return None
    text = str(subnet).strip()
    if not text:
        return None
    if "." in text:
        octets = text.split(".")
        if len(octets) != 4:
            return None
        try:
            values = [int(o) for o in octets]
        except ValueError:
            return None
        if any(v < 0 or v > 255 for v in values):
            return None
        bits = "".join(f"{v:08b}" for v in values)
        # A valid mask is set bits then clear bits; a non-contiguous one is a
        # data error and guessing a length from it would be worse than nothing.
        if "01" in bits:
            return None
        return str(bits.count("1"))
    length = _int(text)
    if length is None or not length.isdigit():
        return None
    return length if 0 <= int(length) <= 128 else None


def _with_prefix(address, subnet):
    """'2400:…:34da' + '126' -> '2400:…:34da/126'.

    Site_Basic carries the prefix on the address and 01_SiteBasic renders it
    straight into the Address MO, so the two are joined here.
    """
    if address is None:
        return None
    address = str(address).strip()
    if not address:
        return None
    length = prefix_length(subnet)
    return f"{address}/{length}" if length else address


#: Which IP family each Site_Basic transport field is planned in.
#:
#: Not uniform, and not inferable: VI plans the OAM *addresses* in IPv6 while
#: still numbering that VLAN in the IPv4 column, and plans S1-C and S1-U
#: wholly in IPv4 even though the plan carries IPv6 columns for them too.
#: Picking "whichever family has a value" would silently take the IPv6 S1-C
#: address, so the family is declared per field instead.
#:
#:   plane -> (vlan family, address/gateway/subnet family)
PLANE_FAMILIES = {
    ("2g", "bts"): ("ipv4", "ipv4"),      # Abis
    ("4g", "oam"): ("ipv4", "ipv6"),      # VLAN from the IPv4 column, address IPv6
    ("4g", "s1c"): ("ipv4", "ipv4"),
    ("4g", "s1u"): ("ipv4", "ipv4"),
    ("5g", "oam"): ("ipv6", "ipv6"),
    ("5g", "s1c"): ("ipv6", "ipv6"),
    ("5g", "s1u"): ("ipv6", "ipv6"),
}


def _plane(ip_row: dict, tech: str, plane: str) -> tuple:
    """(vlan, address/prefix, gateway) for one transport plane.

    Families come from PLANE_FAMILIES. The other family is used only as a
    fallback when the planned one is blank, so a plan that fills just one side
    still converts rather than emitting nothing.
    """
    stem = f"code_ip_service_planning_{tech}_{plane}"
    vlan_family, addr_family = PLANE_FAMILIES.get((tech, plane), ("ipv4", "ipv4"))
    other = "ipv4" if addr_family == "ipv6" else "ipv6"

    vlan = _get(ip_row, f"{stem}_vlan_{vlan_family}",
                f"{stem}_vlan_{'ipv6' if vlan_family == 'ipv4' else 'ipv4'}")

    address = _get(ip_row, f"{stem}_ip_{addr_family}")
    subnet = _get(ip_row, f"{stem}_subnet_{addr_family}")
    gateway = _get(ip_row, f"{stem}_gw_{addr_family}")
    if not address:
        address = _get(ip_row, f"{stem}_ip_{other}")
        subnet = _get(ip_row, f"{stem}_subnet_{other}")
        gateway = _get(ip_row, f"{stem}_gw_{other}")

    return (_int(vlan), _with_prefix(address, subnet), gateway)


def _cell_type(row: dict) -> str:
    """FDD or TDD, from the band or the cell name.

    VI's Delhi 4G cells are named <node>F<sector><carrier> for FDD and
    <node>T<...> for TDD, matching the _F/_T convention the script generator
    keys on.
    """
    band = (_get(row, "band") or "").upper()
    if "TDD" in band:
        return "TDD"
    if "FDD" in band:
        return "FDD"
    name = (_get(row, "4g cell name") or "").upper()
    return "TDD" if "T" in name[-4:] and "F" not in name[-4:] else "FDD"


# --------------------------------------------------------------------------
# builders
# --------------------------------------------------------------------------

def build_site_basic(data: SiteData) -> list[dict]:
    """One row per node: the 4G node, plus the 5G node when the site has one.

    Transport comes from the IP plan and everything else from the RF database,
    so a site listed in only one of them still produces a row - with the other
    half of the columns empty, which `empty_columns` then reports.
    """
    four_g = _rows(data, FOURG_SHEETS)
    five_g = _rows(data, FIVEG_SHEETS)
    ip_rows = _rows(data, IP_SHEETS)
    ip = ip_rows[0][0] if ip_rows else {}

    oam_vlan, oam_ip, oam_gw = _plane(ip, "4g", "oam")
    s1c_vlan, s1c_ip, s1c_gw = _plane(ip, "4g", "s1c")
    s1u_vlan, s1u_ip, s1u_gw = _plane(ip, "4g", "s1u")
    abis_vlan, abis_ip, abis_gw = _plane(ip, "2g", "bts")
    nr_oam_vlan, nr_oam_ip, nr_oam_gw = _plane(ip, "5g", "oam")

    rows = []
    if four_g:
        row = four_g[0][0]
        node = _get(row, "4g site name")
        rows.append({
            "Site ID": data.key,
            "eNodeBName": node,
            "Fingerprint": node,
            "ENM": _get(row, "enm"),
            "Phy SiteID/Userlabel": _get(row, "site id"),
            "Configuration_in_Node": CONFIGURATION_IN_NODE,
            "eNBId": _int(_get(row, "enodeb id")),
            "OAM_vlan": oam_vlan, "OAM_IP": oam_ip, "OAM_GW": oam_gw,
            "LTE_S1_vlan": s1c_vlan, "LTE_S1_IP": s1c_ip, "LTE_S1_GW": s1c_gw,
            "LTE_UP_vlan": s1u_vlan, "LTE_UP_IP": s1u_ip, "LTE_UP_GW": s1u_gw,
            "ABIS_vlan": abis_vlan, "ABIS_IP": abis_ip, "ABIS_GW": abis_gw,
        })

    if five_g:
        row = five_g[0][0]
        node = _get(row, "gnodb name")
        rows.append({
            "Site ID": data.key,
            "eNodeBName": node,
            "Fingerprint": node,
            "ENM": _get(row, "enm"),
            "Phy SiteID/Userlabel": _get(row, "site_id", "site id"),
            "Configuration_in_Node": "LTENR",
            "eNBId": _int(_get(row, "gnodeb id")),
            "NR_vlan": nr_oam_vlan, "NR_IP": nr_oam_ip, "NR_GW": nr_oam_gw,
        })

    # A site the IP plan knows but the RF database does not still gets a row,
    # carrying the transport half. Emitting nothing would hide the fact that
    # the two sources cover different sites -- see the module docstring.
    if not rows and ip:
        rows.append({
            "Site ID": data.key,
            "Phy SiteID/Userlabel": _get(ip, "site_id"),
            "Configuration_in_Node": CONFIGURATION_IN_NODE,
            "OAM_vlan": oam_vlan, "OAM_IP": oam_ip, "OAM_GW": oam_gw,
            "LTE_S1_vlan": s1c_vlan, "LTE_S1_IP": s1c_ip, "LTE_S1_GW": s1c_gw,
            "LTE_UP_vlan": s1u_vlan, "LTE_UP_IP": s1u_ip, "LTE_UP_GW": s1u_gw,
            "ABIS_vlan": abis_vlan, "ABIS_IP": abis_ip, "ABIS_GW": abis_gw,
            "NR_vlan": nr_oam_vlan, "NR_IP": nr_oam_ip, "NR_GW": nr_oam_gw,
        })
    return rows


def build_radio_hw(data: SiteData) -> list[dict]:
    """Empty: neither source describes equipment. See UNMAPPED['Radio_HW']."""
    return []


def build_lte_cell(data: SiteData) -> list[dict]:
    """One row per '4G DB' row - the sheet is already one row per cell."""
    rows = []
    for row, _label in _rows(data, FOURG_SHEETS):
        cell = _get(row, "4g cell name")
        if not cell:
            continue
        bandwidth = _int(_get(row, "bandwidth"))
        rows.append({
            "eNodeBName": _get(row, "4g site name"),
            "eUtranCellFDDId": cell,
            "Eutrancell_Type": _cell_type(row),
            "Configuration_in_Node": CONFIGURATION_IN_NODE,
            "Script_Required": SCRIPT_REQUIRED,
            "sectorEquipmentFunctionId": _get(row, "sector equipment function id"),
            "sectorCarrierId": _int(_get(row, "sector carried id")),
            "enbId": _int(_get(row, "enodeb id")),
            "earfcndl": _int(_get(row, "earfcndl")),
            "dlChannelBandwidth": bandwidth,
            "ulChannelBandwidth": bandwidth,
            "Latitude": _get(row, "lat"),
            "Longitude": _get(row, "long"),
            "cellId": _int(_get(row, "cell id")),
            "physicalLayerCellIdGroup": _int(_get(row, "physicallayercellidgroup")),
            "physicalLayerSubCellId": _int(_get(row, "physicallayersubcellid")),
            "tac": _int(_get(row, "tac")),
            "rachRootSequence": _int(_get(row, "rach rootsequence")),
            "configuredMaxTxPower": _int(_get(row, "sector power")),
        })
    return rows


def build_nr_cell(data: SiteData) -> list[dict]:
    """One row per '5G DB' row."""
    rows = []
    for row, _label in _rows(data, FIVEG_SHEETS):
        cell = _get(row, "cell name")
        if not cell:
            continue
        rows.append({
            "gNodeBName": _get(row, "gnodb name"),
            "gUtranCell": cell,
            "gNBId": _int(_get(row, "gnodeb id")),
            "cellLocalId": _int(_get(row, "cell id")),
            "nRPCI": _int(_get(row, "pci")),
            "nRTAC": _int(_get(row, "tracking area code")),
            "rachRootSequence": _int(_get(row, "rsi")),
            "Latitude": _get(row, "lat"),
            "Longitude": _get(row, "long"),
        })
    return rows


BUILDERS = {
    "Site_Basic": build_site_basic,
    "Radio_HW": build_radio_hw,
    "LTE-CELL": build_lte_cell,
    "NR-CELL": build_nr_cell,
}
