"""
Log-vs-golden-parameter-list audits.

Unlike a pre/post diff, there's no second log to align node names against —
the golden workbook's "Parent MO Class" entries are either a bare class name
(apply to every instance of that class found in the log) or a full instance
path (matched exactly). See log_parser/reference.py for the matching rules.
"""
import logging
from collections import defaultdict

import pandas as pd

from .commands import load_commands
from .config import get_input_files
from .reference import (
    clean_for_compare,
    extract_state_code,
    get_feature_index,
    get_lte_parameter_index,
    get_nr_parameter_index,
    lookup_parameter_dual,
    mo_class_root,
    normalize_mo,
)
from .extractors import (
    get_feature_state_data,
    get_gpl_audit_data,
)

log = logging.getLogger(__name__)


def _band(mo: str) -> str:
    # cell names are operator-typed and their case is not guaranteed, so match
    # the band token case-insensitively like every other MO comparison here
    mo = mo.upper()
    if "_F1_" in mo: return "L2100"
    if "_F3_" in mo: return "L1800"
    if "_F8_" in mo: return "L900"
    if "_T1_" in mo or "_T2_" in mo: return "L23"
    return ""


# One class-level golden value expands to one output row per matching instance.
# For the cell/frequency RELATION classes that means thousands of byte-identical
# "OK" rows — on a single node, 4 golden values produced 3,076 rows and buried
# every real finding. Above this many rows for one (MO class, Parameter),
# identical OK rows collapse to a single representative carrying the count.
#
# NOT OK rows are never collapsed: each one is individually actionable and
# corrections.py needs the real MO to target it. That filter only ever reads
# rows whose status is not OK, so collapsing OK rows cannot change a single
# generated `set` command.
_COLLAPSE_ABOVE = 25


def _mo_leaf_class(mo) -> str:
    """Class name of the last segment of an MO path — the thing that makes all
    1369 EUtranCellRelation instances one group."""
    return str(mo).split(",")[-1].split("=")[0].strip()


def _collapse_ok_rows(rows: list[dict]) -> list[dict]:
    """Fold runs of identical OK rows for high-cardinality MO classes into one."""
    counts: dict[tuple, int] = defaultdict(int)
    for r in rows:
        counts[(_mo_leaf_class(r["MO"]), r["Parameter"])] += 1

    out: list[dict] = []
    representative: dict[tuple, dict] = {}
    folded: dict[int, int] = defaultdict(int)

    for r in rows:
        key = (_mo_leaf_class(r["MO"]), r["Parameter"])
        if r["Parameter Setting Status"] != "OK" or counts[key] <= _COLLAPSE_ABOVE:
            out.append(r)
            continue
        # one representative per distinct reading, so a class whose instances
        # genuinely differ still shows each value it takes
        group = key + (clean_for_compare(r["Current value"]),)
        first = representative.get(group)
        if first is None:
            representative[group] = r
            out.append(r)
        else:
            folded[id(first)] += 1

    for r in out:
        n = folded.get(id(r), 0)
        if n:
            r["MO"] = f"{r['MO']}  [+{n} identical]"
    if folded:
        log.info(
            "Collapsed %d duplicate OK row(s) across %d high-cardinality "
            "parameter(s); NOT OK rows left intact",
            sum(folded.values()), len(folded),
        )
    return out


def _missing_rows(index: dict, seen: set, key_kind: str, with_band: bool) -> list[dict]:
    # reference entries never matched by any log row — reported once each,
    # not correction-actionable (Current value stays real NaN so
    # corrections.py's `.notna()` filter naturally excludes them; there's no
    # real instance to target with a `set` command for a class-level entry,
    # and for an exact-instance entry that's simply absent from the log a
    # `set` would fail anyway — it doesn't exist to set).
    rows = []
    for key, entry in index.items():
        if (key_kind, key[0], key[1]) in seen:
            continue
        row = {
            "Node_ID": "",
            "MO": entry["raw_mo"],
            "Parameter": entry["param"],
            "Pre-existing Value": entry["expected"],
            "Current value": pd.NA,
            "Parameter Setting Status": "Missing",
        }
        if with_band:
            row["Band"] = ""
        rows.append(row)
    return rows


def _log_summary(label: str, result: pd.DataFrame) -> None:
    log.info(
        "%s Reference — %d rows | OK: %d | NOT OK: %d | Missing: %d",
        label, len(result),
        (result["Parameter Setting Status"] == "OK").sum() if not result.empty else 0,
        (result["Parameter Setting Status"] == "NOT OK").sum() if not result.empty else 0,
        (result["Parameter Setting Status"] == "Missing").sum() if not result.empty else 0,
    )


async def gpl_reference_audit() -> tuple[pd.DataFrame, pd.DataFrame]:
    """LTE + NR golden-parameter-list audit in one pass.

    Every hgetc command relevant to this audit is pulled together (see
    extractors.get_gpl_audit_data — commands-file section placement no
    longer matters), then each (MO, Parameter) row is matched against BOTH
    LTE_PARAMETER and NR_PARAMETER (reference.lookup_parameter_dual) and
    routed to whichever sheet(s) it actually belongs to — not to whichever
    section the command used to live in. The MO path's own root class picks
    the preferred sheet on a name collision, but it does NOT gate which
    sheets get consulted: the golden list keeps its EN-DC rows in
    NR_PARAMETER even though those MOs hang off LTE roots, so a miss in the
    preferred sheet falls through to the other one.
    """
    commands = load_commands()
    log_files = get_input_files()
    log.info("GPL Reference Audit — %d log file(s)", len(log_files))

    lte_exact, lte_class = get_lte_parameter_index()
    nr_exact, nr_class = get_nr_parameter_index()
    if not lte_exact and not lte_class and not nr_exact and not nr_class:
        log.warning("GPL Reference Audit: reference workbook has no matching rows — skipped.")
        return pd.DataFrame(), pd.DataFrame()

    log_df = await get_gpl_audit_data(commands, log_files)
    

    if log_df.empty:
        log.warning("GPL Reference Audit: uploaded log produced no data — skipped.")
        return pd.DataFrame(), pd.DataFrame()

    log_df = log_df.rename(columns={"Perameter": "Parameter", "value": "Value"})

    lte_rows: list[dict] = []
    nr_rows: list[dict] = []
    lte_seen: set[tuple[str, str, str]] = set()
    nr_seen: set[tuple[str, str, str]] = set()
    # One reference entry, on one MO instance, is one output row. A struct
    # member reaches the audit twice — once under its bare log name and once
    # struct-qualified (see extractors._qualify_struct_members) — and both
    # resolve to the same golden row, so without this the report showed
    # csiRsControl8Ports and csiRsConfig8P.csiRsControl8Ports side by side.
    emitted: dict[tuple, tuple[list, int]] = {}

    for _, r in log_df.iterrows():
        mo = str(r["MO"])
        param = str(r["Parameter"])
        node_id = r.get("Node_ID", "")
        raw_value = r.get("Value")

        matches = lookup_parameter_dual(
            mo, param, (lte_exact, lte_class), (nr_exact, nr_class), raw_value
        )
        if not matches:
            continue  # parameter not covered by either reference sheet — not audited

        expected_clean_cache: dict[str, object] = {}
        current_clean = clean_for_compare(raw_value)

        for sheet, entry, seen_key in matches:
            if sheet == "LTE":
                lte_seen.add(seen_key)
            else:
                nr_seen.add(seen_key)

            expected_clean = expected_clean_cache.setdefault(
                sheet, clean_for_compare(entry["expected"])
            )
            if current_clean is None:
                status = "NOT OK"
            else:
                status = "OK" if expected_clean == current_clean else "NOT OK"

            row = {
                "Node_ID": node_id,
                "MO": mo,
                "Parameter": param,
                "Pre-existing Value": entry["expected"],
                "Current value": raw_value,
                "Parameter Setting Status": status,
            }
            target = lte_rows if sheet == "LTE" else nr_rows
            if sheet == "LTE":
                row["Band"] = _band(mo)

            emit_key = (sheet, node_id, mo, seen_key)
            prev = emitted.get(emit_key)
            if prev is not None:
                # already reported — keep whichever spelling the sheet itself
                # uses, so the report echoes the golden list
                prev_rows, prev_i = prev
                sheet_name = str(entry["param"]).strip().lower()
                if (param.lower() == sheet_name
                        and str(prev_rows[prev_i]["Parameter"]).lower() != sheet_name):
                    prev_rows[prev_i] = row
                continue

            emitted[emit_key] = (target, len(target))
            target.append(row)

    # collapse before appending Missing rows — those are already one per entry
    lte_rows = _collapse_ok_rows(lte_rows)
    nr_rows = _collapse_ok_rows(nr_rows)

    lte_rows.extend(_missing_rows(lte_exact, lte_seen, "exact", with_band=True))
    lte_rows.extend(_missing_rows(lte_class, lte_seen, "class", with_band=True))
    nr_rows.extend(_missing_rows(nr_exact, nr_seen, "exact", with_band=False))
    nr_rows.extend(_missing_rows(nr_class, nr_seen, "class", with_band=False))

    lte_result = pd.DataFrame(lte_rows)
    nr_result = pd.DataFrame(nr_rows)
    _log_summary("LTE GPL", lte_result)
    _log_summary("NR GPL", nr_result)
    return lte_result, nr_result


def _feature_lookup_keys(mo: str):
    """Index keys to try for a featurestate MO, best first.

    hgetc prints the MO as a full path, e.g. "Lm=1,FeatureState=CXC4010319",
    so the CXC ID is the LEAF INSTANCE VALUE — not the class root (that's
    "Lm"). Some dumps instead print the leaf as "CXC4011946=1", where the CXC
    is the leaf CLASS. Try the full path, then both halves of the leaf, then
    the class root for backwards compatibility.
    """
    norm = normalize_mo(mo)
    keys = [norm.lower()]
    leaf = norm.split(",")[-1].strip()
    if "=" in leaf:
        cls, _, val = leaf.partition("=")
        keys.append(val.strip().lower())
        keys.append(cls.strip().lower())
    elif leaf:
        keys.append(leaf.lower())
    keys.append(mo_class_root(mo))
    seen = set()
    return [k for k in keys if k and not (k in seen or seen.add(k))]


async def _feature_reference_audit(
    ref_getter, log_getter, commands, log_files, label: str
) -> pd.DataFrame:
    feature_index = ref_getter()
    if not feature_index:
        log.warning("%s Reference Audit: reference workbook has no feature rows — skipped.", label)
        return pd.DataFrame()

    log_df = await log_getter(commands, log_files)
    if log_df.empty:
        log.warning("%s Reference Audit: uploaded log produced no feature-state data — skipped.", label)
        return pd.DataFrame()

    rows: list[dict] = []
    seen: set[str] = set()

    for _, r in log_df.iterrows():
        cxc = str(r["MO"]).strip()
        entry = matched_key = None
        for key in _feature_lookup_keys(cxc):
            entry = feature_index.get(key)
            if entry is not None:
                matched_key = key
                break
        if entry is None:
            continue
        seen.add(matched_key)

        current_code = extract_state_code(r.get("featureState"))
        expected_code = extract_state_code(entry["expected"])
        status = "Missing" if current_code is None else ("OK" if current_code == expected_code else "NOT OK")

        rows.append({
            "Node_ID": r.get("Node_ID", ""),
            # the bare CXC from the sheet, not the log's full MO path
            # ("Lm=1,FeatureState=CXC4010618"), so this column stays homogeneous
            # with the unmatched rows below and corrections.py can target it.
            "CXC ID": entry["raw_cxc"],
            "description": entry["description"],
            "Pre Existing FeatureState": entry["expected"],
            "Current FeatureState": r.get("featureState"),
            "Feature setting Status": status,
        })

    for cxc_lower, entry in feature_index.items():
        if cxc_lower in seen:
            continue
        rows.append({
            "Node_ID": "",
            "CXC ID": entry["raw_cxc"],
            "description": entry["description"],
            "Pre Existing FeatureState": entry["expected"],
            "Current FeatureState": pd.NA,
            "Feature setting Status": "Missing",
        })

    result = pd.DataFrame(rows)
    log.info(
        "%s Reference — %d rows | OK: %d | NOT OK: %d | Missing: %d",
        label, len(result),
        (result["Feature setting Status"] == "OK").sum(),
        (result["Feature setting Status"] == "NOT OK").sum(),
        (result["Feature setting Status"] == "Missing").sum(),
    )
    return result


async def feature_state_reference_audit() -> pd.DataFrame:
    """One audit over every feature in the reference sheet — LTE and NR
    together, since a node exposes them all under the same Lm=1,FeatureState."""
    commands = load_commands()
    log_files = get_input_files()
    log.info("FeatureState Reference Audit — %d log file(s)", len(log_files))
    return await _feature_reference_audit(
        get_feature_index, get_feature_state_data, commands, log_files, "FeatureState"
    )
