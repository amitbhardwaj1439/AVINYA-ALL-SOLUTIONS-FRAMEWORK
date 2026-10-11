"""Values the Vi circles fix by convention rather than read from a plan.

DEL_Vi, MAG_Vi and MP_Vi commission the same hardware profile, so a handful of
Site_Basic and LTE-CELL fields are constants of the build rather than data. The
plans genuinely do not carry them - which is why these columns used to come out
blank and be listed in UNMAPPED - and every Vi site is built the same way, so
they are declared once here instead of three times over.

Anything a plan *does* carry still wins; see `cell_overrides`, which is applied
on top of the values read from the sheet only for the fields it names.
"""
from __future__ import annotations

#: Site_Basic fields that are the same on every Vi site.
SITE_BASIC: dict[str, str] = {
    "BB_Type": "6631",
    "fieldReplaceableUnitId": "BB-1",
    "tnPortId": "TN_E",
    "Bridge_tnPortId": "NA",
}

#: LTE-CELL fields that are the same on every Vi cell.
CELL: dict[str, str] = {
    "crsGain": "0",
    "MME": "ERICSSON",
    "configuredMaxTxPower": "40000",
}

#: Added for FDD cells only - a TDD cell's antenna count is not this fixed.
FDD_CELL: dict[str, str] = {
    "noOfTxAntennas": "2",
    "noOfRxAntennas": "2",
}

def cell_overrides(cell_name, cell_type=None, carriers=None) -> dict[str, str]:
    """The fixed LTE-CELL values for one cell, ready to merge over the sheet's.

    `cell_type` decides only whether the FDD antenna counts apply; it is read
    from the sheet ('FDD', or MAG's 'FDD_900') and treated as FDD unless it
    says TDD, because every Vi cell seen so far is FDD.

    `carriers` maps a cell-name suffix to the values that follow from it -
    bandwidth, uplink EARFCN and sector carrier id. Those are per circle, not
    shared: the same F1x/F2x/F3x suffixes mean different frequencies and
    different sector-carrier allocations in each one, so only a circle that has
    stated its own table passes one. Without it a cell still gets the
    circle-wide values above and keeps whatever the plan gave it for the rest.
    """
    out = dict(CELL)
    if "TDD" not in str(cell_type or "").upper():
        out.update(FDD_CELL)

    if carriers:
        suffix = str(cell_name or "").strip().upper()[-3:]
        out.update(carriers.get(suffix, {}))
    return out


def without_decimal(value):
    """'21.20424' -> '2120424'.

    Site_Basic and LTE-CELL carry coordinates as whole digits; the generator
    does the same strip on its way to the scripts
    (views.py::generate_integration_script), so doing it here just means the
    workbook already reads the way the scripts will.
    """
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return text.replace(".", "") if "." in text else text
