"""MP_Vi: one workbook holding MP's 2G/4G RF data and its IP plan.

Unlike DEL_Vi and MAG_Vi, which ship the RF database and the IP plan as two
files, MP delivers a single '2G & 4G RF Data and IP Plan.xlsx' whose tabs are:

    '4G RF Data'    header on row 0, one row per CELL (one node per site)
    'ATOM Report'   header on row 0, one row per SITE - every transport
                    address, as CODE_IP_SERVICE_PLANNING_<tech>_<plane>_*
    'G900_DT', '2G-4G Interworking', 'HANDOVER RELATION', 'Summary'
                    2G planning and scratch tabs, not read here

Both sheets are already one row per cell / per site, so there is no
block-walking: `data.hits` holds this site's rows and the builders iterate them
directly.

The site key is 'NSS ID' ('INMP606361'). It has to be, because the workbook
names sites three ways - the RF sheet by node ('LO01INMP606361', which is
'LO01' + the NSS id), the ATOM report by VIL id ('FY27MPC10568') and G900_DT by
a bare 2G number - and NSS is the only one written on both sheets the converter
reads. KEY_COLUMNS below declares it; see `Naming.key_columns`.

IP families: the plan carries IPv4 and IPv6 for each plane. MP's nodes are IPv6
for OAM, S1-C and S1-U, and IPv4 for Abis, always - so unlike DEL_Vi, where the
choice varies per plane, PLANE_FAMILIES here is uniform. Addresses are emitted
with their prefix length ('.../126'), which is the form Site_Basic carries and
01_SiteBasic expects.

There is no 5G tab, so NR-CELL comes out empty and Site_Basic carries no NR
transport. Nothing here describes equipment, so Radio_HW is empty too.
"""
from __future__ import annotations

from .sitedata import SiteData
from . import vi_defaults

CIRCLE = "MP_Vi"

# The key is the NSS id, taken from the column named below, so no prefix
# stripping is wanted: it would only mangle an id that is already canonical.
STRIP_NODE_PREFIX = False
NUMERIC_SITE_IDS = False

#: The column naming the site, tried in this order. '4G RF Data' spells it
#: 'NSS ID' and 'ATOM Report' 'NSS_ID'; naming it here is what joins the two.
#: Sheets carrying neither name no sites, which keeps G900_DT's bare 2G numbers
#: ('3473', '4470') out of the site list.
KEY_COLUMNS = ("nss_id", "nss id")

# Sheet name fragments, matched case-insensitively.
FOURG_SHEETS = ("4g rf data",)
TWOG_SHEETS = ()                 # the 2G tabs carry no field this template wants
FIVEG_SHEETS = ()                # no 5G tab in this workbook
IP_SHEETS = ("atom report",)

CONFIGURATION_IN_NODE = "LTE"
SCRIPT_REQUIRED = "YES"

#: Columns nothing in these two sources can fill, with the reason. Surfaced by
#: the API as `empty_columns` so the gap is visible before the output is used
#: to generate scripts.
_NO_EQUIPMENT = ("The RF data describes cells, not equipment: it carries no "
                 "radio type, RiLink, baseband port or FRU id.")

_NO_5G = "This workbook has no 5G tab; the site's NR layer is not planned here."

UNMAPPED = {
    "Site_Basic": {
        "BB_Type": "Not in the RF data or the ATOM report.",
        "ENM": "The ATOM report names the vendor, not the managing ENM.",
        "fieldReplaceableUnitId": _NO_EQUIPMENT,
        "tnPortId": "Transport port naming is not in the ATOM report.",
        "Bridge_tnPortId": "Transport port naming is not in the ATOM report.",
        "Anchor_ENDC_IP": "ENDC anchoring is not planned in these sources.",
        "Anchor_ENDC_GW": "ENDC anchoring is not planned in these sources.",
        "Anchor Gnb ID": "ENDC anchoring is not planned in these sources.",
        "Anchor NR IP": "ENDC anchoring is not planned in these sources.",
        "NR_PORT": "Transport port naming is not in the ATOM report.",
        "NR_vlan": _NO_5G, "NR_IP": _NO_5G, "NR_GW": _NO_5G,
    },
    "Radio_HW": {"*": _NO_EQUIPMENT},
    "LTE-CELL": {
        "noOfTxAntennas": "Antenna counts are not in the 4G RF Data sheet.",
        "noOfRxAntennas": "Antenna counts are not in the 4G RF Data sheet.",
        "Latitude": "Coordinates are on the 2G tab (G900_DT), not the 4G sheet.",
        "Longitude": "Coordinates are on the 2G tab (G900_DT), not the 4G sheet.",
        "sectorEquipmentFunctionId": _NO_EQUIPMENT,
        "sectorCarrierId": _NO_EQUIPMENT,
        "MME": "The ATOM report carries no MME id or address.",
    },
    "NR-CELL": {"*": _NO_5G},
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

    The ATOM report writes both families as a length with the slash already on
    it ('/126', '/30'); DEL_Vi's plan writes the length bare ('126') and IPv4
    subnets as a dotted mask ('255.255.255.252'). All three are accepted: the
    slash is stripped, and a mask is the count of its set bits, so
    255.255.255.240 -> 28, .248 -> 29, .252 -> 30 - the whole rule, no table
    needed. Anything unrecognised returns None so the address is emitted bare
    rather than with a wrong prefix.
    """
    if subnet is None:
        return None
    text = str(subnet).strip().lstrip("/").strip()
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
#: MP is uniform where DEL_Vi is not: OAM, S1-C and S1-U are planned in IPv6,
#: Abis always in IPv4. Declared rather than inferred, because the ATOM report
#: fills the IPv4 columns for those three planes as well and "whichever family
#: has a value" would silently take the IPv4 address.
#:
#: The VLAN is numbered in the IPv4 column for S1-C and S1-U - the report has no
#: _VLAN_IPV6 for them at all - so `_plane` falls back to the other family for
#: the VLAN only. 4G OAM carries both and they agree.
#:
#:   plane -> (vlan family, address/gateway/subnet family)
PLANE_FAMILIES = {
    ("2g", "bts"): ("ipv4", "ipv4"),      # Abis: IPv4 always
    ("4g", "oam"): ("ipv6", "ipv6"),
    ("4g", "s1c"): ("ipv6", "ipv6"),
    ("4g", "s1u"): ("ipv6", "ipv6"),
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


def _plane_in(ip_row: dict, tech: str, plane: str, family: str) -> tuple:
    """(address/prefix, gateway) for one plane in one named IP family.

    `_plane` answers "the planned family, whatever that is"; this answers "this
    family, specifically", with no fallback to the other one -- a blank here
    means the plan genuinely has no address of that family, and a substituted
    IPv6 address would be worse than an empty cell.

    MP needs both: S1-C and S1-U are planned in IPv6 and carried in LTE_S1_IP /
    LTE_UP_IP, while the dual-stack script also configures the IPv4 side of the
    same two planes from the *_V4 columns.
    """
    stem = f"code_ip_service_planning_{tech}_{plane}"
    address = _get(ip_row, f"{stem}_ip_{family}")
    subnet = _get(ip_row, f"{stem}_subnet_{family}")
    gateway = _get(ip_row, f"{stem}_gw_{family}")
    return (_with_prefix(address, subnet), gateway)


def _cell_type(row: dict) -> str:
    """FDD or TDD, from the band or the cell name.

    VI 4G cells are named <node>F<sector><carrier> for FDD and <node>T<...>
    for TDD, matching the _F/_T convention the script generator keys on. This
    sheet has no band column, so the name is all there is to go on.
    """
    band = (_get(row, "band") or "").upper()
    if "TDD" in band:
        return "TDD"
    if "FDD" in band:
        return "FDD"
    name = (_get(row, "4g cell id", "4g cell name") or "").upper()
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

    # The dual-stack script configures IPv4 alongside the IPv6 above, on the
    # same two planes, so both families are emitted for S1-C and S1-U.
    s1c_ip_v4, s1c_gw_v4 = _plane_in(ip, "4g", "s1c", "ipv4")
    s1u_ip_v4, s1u_gw_v4 = _plane_in(ip, "4g", "s1u", "ipv4")
    nr_oam_vlan, nr_oam_ip, nr_oam_gw = _plane(ip, "5g", "oam")

    rows = []
    if four_g:
        row = four_g[0][0]
        node = _get(row, "4g site name")
        rows.append({
            "Site ID": data.key,
            "eNodeBName": node,
            "Fingerprint": node,
            # The VIL site id lives on the ATOM report ('FY27MPC10568'); the RF
            # sheet carries only the NSS id, which is the fallback.
            "Phy SiteID/Userlabel": _get(ip, "site_id") or _get(row, "nss id"),
            "Configuration_in_Node": CONFIGURATION_IN_NODE,
            **vi_defaults.SITE_BASIC,
            "eNBId": _int(_get(row, "enodeb id")),
            "OAM_vlan": oam_vlan, "OAM_IP": oam_ip, "OAM_GW": oam_gw,
            "LTE_S1_vlan": s1c_vlan, "LTE_S1_IP": s1c_ip, "LTE_S1_GW": s1c_gw,
            "LTE_S1_IP_V4": s1c_ip_v4, "LTE_S1_GW_V4": s1c_gw_v4,
            "LTE_UP_vlan": s1u_vlan, "LTE_UP_IP": s1u_ip, "LTE_UP_GW": s1u_gw,
            "LTE_UP_IP_V4": s1u_ip_v4, "LTE_UP_GW_V4": s1u_gw_v4,
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
            **vi_defaults.SITE_BASIC,
            "OAM_vlan": oam_vlan, "OAM_IP": oam_ip, "OAM_GW": oam_gw,
            "LTE_S1_vlan": s1c_vlan, "LTE_S1_IP": s1c_ip, "LTE_S1_GW": s1c_gw,
            "LTE_S1_IP_V4": s1c_ip_v4, "LTE_S1_GW_V4": s1c_gw_v4,
            "LTE_UP_vlan": s1u_vlan, "LTE_UP_IP": s1u_ip, "LTE_UP_GW": s1u_gw,
            "LTE_UP_IP_V4": s1u_ip_v4, "LTE_UP_GW_V4": s1u_gw_v4,
            "ABIS_vlan": abis_vlan, "ABIS_IP": abis_ip, "ABIS_GW": abis_gw,
            "NR_vlan": nr_oam_vlan, "NR_IP": nr_oam_ip, "NR_GW": nr_oam_gw,
        })
    return rows


def build_radio_hw(data: SiteData) -> list[dict]:
    """Empty: neither source describes equipment. See UNMAPPED['Radio_HW']."""
    return []


def build_lte_cell(data: SiteData) -> list[dict]:
    """One row per '4G RF Data' row - the sheet is already one row per cell."""
    rows = []
    for row, _label in _rows(data, FOURG_SHEETS):
        cell = _get(row, "4g cell id", "4g cell name")
        if not cell:
            continue
        # Written as '20 Mhz', the spelling DEL_Vi's database uses too
        # ('20 MHZ'), so it is passed through rather than reduced to a number.
        bandwidth = _int(_get(row, "bandwidth"))
        # 'Bucket' names the carrier where the plan has it (MAG); this sheet
        # does not, so the cell-name rule stands in.
        cell_type = _get(row, "bucket") or _cell_type(row)
        rows.append({
            "eNodeBName": _get(row, "4g site name"),
            "eUtranCellFDDId": cell,
            "Eutrancell_Type": cell_type,
            "Configuration_in_Node": CONFIGURATION_IN_NODE,
            "Script_Required": SCRIPT_REQUIRED,
            "enbId": _int(_get(row, "enodeb id")),
            "earfcndl": _int(_get(row, "earfcndl")),
            "earfcnul": _int(_get(row, "earfcnul")),
            "dlChannelBandwidth": bandwidth,
            "ulChannelBandwidth": bandwidth,
            "cellId": _int(_get(row, "cellid", "cell id")),
            "physicalLayerCellIdGroup": _int(_get(row, "physicallayercellidgroup")),
            "physicalLayerSubCellId": _int(_get(row, "physicallayersubcellid")),
            "tac": _int(_get(row, "tac")),
            "rachRootSequence": _int(_get(row, "rach rootsequence")),
            "configuredMaxTxPower": _int(_get(row, "sector power")),
            "crsGain": _int(_get(row, "crs gain")),
            # Fixed for the circle, so applied last: these win over the sheet.
            **vi_defaults.cell_overrides(cell, cell_type),
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
