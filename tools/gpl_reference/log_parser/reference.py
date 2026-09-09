"""
Loads the hand-maintained golden-parameter workbooks — three of them, one per
audit section, so a quarterly refresh of one set of values replaces a single
file (see config.LTE_REFERENCE_FILE / NR_REFERENCE_FILE / FEATURE_REFERENCE_FILE):

  LTE_GPL_UPDATED.xlsx  LTE_GPL_<CIRCLE> sheets
                        — Parent MO Class | Sub MO Class | Parameter | SubParameter | FINAL GPL (UPDATED)
  NR_GPL_UPDATED.xlsx   NR_GPL_<CIRCLE> sheets
                        — Parent MO Class | Parameter | FINAL GPL (UPDATED) | Description / Notes (Optional)
  FEATURES.xlsx         a single FEATURESTATE sheet
                        — Parent MO Class | Parameter | FINAL GPL (UPDATED)

Both parameter workbooks are split per circle because the expected value for a
parameter differs between circles; the run's circle (config.set_circle) picks
the sheet in each, and there is no pan-India fallback — see lte_sheet_for_circle
/ nr_sheet_for_circle, which raise rather than substitute another circle's
values. Features are pan-India and live in one sheet.

For the parameter sheets: "Parent MO Class" is either
  - a bare class name with no "=" (e.g. "EUtranCellFDD", "ENodeBFunction")
    meaning the expected value applies to EVERY instance of that class found
    in the log, or
  - a full instance path containing "=" (e.g. "QciProfilePredefined=qci1",
    "ENodeBFunction=1,DrxProfile=1") meaning it's matched exactly against
    one specific MO in the log.
Matching is case-insensitive and whitespace-tolerant, since the sheet has
inconsistent casing ("EUtranCellFDD" vs "eutrancellfdd") and stray spaces
("RlfProfile =1").

For the FEATURESTATE sheet the two columns are the OTHER way round from the
*_PARAMETER sheets: "Parent MO Class" holds the CXC ID (matched against the
log's featureState MO, which IS the CXC ID) and "Parameter" is a
human-readable feature label, not used for matching.

LTE and NR features live together in this one sheet and are audited as one
list; it is maintained by pasting the LTE list and then the NR list, so it
also carries a repeated header row between the two blocks (skipped on load)
and can name the same CXC twice. A node has a single featureState per CXC, so
a CXC listed twice with two different expected values cannot be honoured both
ways: the first row wins and the clash is logged (see _load_feature_sheet).
"""
import datetime
import functools
import logging
import re
from pathlib import Path

import pandas as pd

from .config import (
    FEATURE_SHEET,
    LTE_CIRCLE_SHEET_PREFIX,
    NR_CIRCLE_SHEET_PREFIX,
    get_circle,
    get_feature_reference_file,
    get_lte_reference_file,
    get_nr_reference_file,
)
from .extractors import _ARRAY_PREFIX_RE, _clean_value

log = logging.getLogger(__name__)

_WS_EQ_RE = re.compile(r"\s*=\s*")
_WS_COMMA_RE = re.compile(r"\s*,\s*")
_PAREN_NUM_RE = re.compile(r"\((\d+)\)")
_LEADING_NUM_RE = re.compile(r"^(\d+)\b")
_CXC_RE = re.compile(r"CXC\d+", re.IGNORECASE)

# The sheet annotates list-valued attributes with their element count —
# 'csiRsActivePortConfig[2]', 'pcp0[44]', 'ueGroupList[1]'. The node prints the
# attribute name alone, so the bracket is documentation, not part of the name,
# and has to come off before matching (44 rows carry one).
_ELEM_COUNT_RE = re.compile(r"\[\d+\]\s*$")

# "caller didn't tell us the log value" — distinct from a NaN value, which is
# itself meaningful to lookup_parameter_dual.
_UNSET = object()

# Added to a match found only via a struct member's bare name, so any sheet
# naming the parameter outright outranks it. See lookup_parameter.
_LEAF_ANCHOR_PENALTY = 100

# A feature state has no numeric code to read off when the sheet spells it as a
# word. 13 FEATURESTATE rows hold a real Excel boolean rather than 1/0, and the
# node prints the matching state as "ACTIVATED (1)" / "DEACTIVATED (0)".
_STATE_WORDS = {"true": "1", "activated": "1", "false": "0", "deactivated": "0"}

# module-level cache: {workbook_path: pd.ExcelFile}
_workbook_cache: dict[str, pd.ExcelFile] = {}
# module-level cache: {(workbook_path, sheet_name): parsed index}
_index_cache: dict[tuple, object] = {}
# side table: {id(exact_index): suffix_index} — see _load_parameter_sheet
_SUFFIX_INDEXES: dict[int, dict] = {}
# side table: {id(exact_index): (exact_leaf, class_leaf, suffix_leaf)} — the
# struct-member-by-bare-name fallback, see _load_parameter_sheet._register_leaf
_LEAF_INDEXES: dict[int, tuple[dict, dict, dict]] = {}


def clear_reference_cache() -> None:
    _workbook_cache.clear()
    _index_cache.clear()
    _SUFFIX_INDEXES.clear()
    _LEAF_INDEXES.clear()


def _get_workbook(book: "Path | str") -> pd.ExcelFile:
    path = str(book)
    xl = _workbook_cache.get(path)
    if xl is None:
        try:
            xl = pd.ExcelFile(path)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Reference workbook not found: {path}\n"
                "Place the golden-parameter .xlsx at this path, or point the "
                "matching config.*_REFERENCE_FILE at it."
            )
        _workbook_cache[path] = xl
    return xl


def _cell_text(v):
    """Render one raw Excel cell as the text the sheet actually holds.

    NEVER goes through pandas' column type inference, which silently rewrites
    these sheets in BOTH directions: the "FINAL GPL (UPDATED)" column mixes
    real Excel booleans with plain integers, so ``dtype=str`` unified each
    column to one type before stringifying — LTE_PARAMETER's 31 TRUE/FALSE
    cells came out as '1'/'0', and NR_PARAMETER's 1/0 cells came out as
    'True'/'False'. Every one of those compared wrong against a log that
    prints 'true' for a boolean attribute and '1' for a numeric one.

    Rendering rules, all chosen to match how the node prints the attribute:
      bool          -> 'true'/'false'   (log prints lowercase words)
      int / whole float -> '1', '35'    (never '1.0', never 'True')
      time          -> '20:30'          (log prints HH:MM, not '20:30:00')
      blank         -> pd.NA            (callers already guard with pd.isna)
    """
    if hasattr(v, "item") and not isinstance(v, (str, bytes)):
        v = v.item()                   # unwrap numpy scalars to Python types
    if v is None or v == "":
        return pd.NA
    if isinstance(v, bool):            # must precede int — bool IS an int
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        if pd.isna(v):
            return pd.NA
        return str(int(v)) if v.is_integer() else repr(v)
    if isinstance(v, datetime.datetime):
        return v.strftime("%Y-%m-%d %H:%M") if (v.hour or v.minute) else v.strftime("%Y-%m-%d")
    if isinstance(v, datetime.time):
        return v.strftime("%H:%M:%S") if v.second else v.strftime("%H:%M")
    s = str(v).strip()
    return s if s else pd.NA


def _parse_sheet(sheet_name: str, book) -> pd.DataFrame:
    """Read a sheet with every column routed through _cell_text.

    A `converters` entry makes pandas hand the converter the raw cell and skip
    type inference for that column, so this is what keeps the bool/int mangling
    described in _cell_text from ever happening.
    """
    xl = _get_workbook(book)
    columns = xl.parse(sheet_name, nrows=0).columns
    return xl.parse(sheet_name, converters={c: _cell_text for c in columns})


def normalize_mo(mo) -> str:
    """Collapse whitespace around '=' and ',' so 'RlfProfile =1' and
    'RlfProfile=1' compare equal."""
    s = str(mo).strip()
    s = _WS_EQ_RE.sub("=", s)
    s = _WS_COMMA_RE.sub(",", s)
    return s


def mo_class_root(mo) -> str:
    """The class name before the first '=', lowercased. For an MO with no
    '=' at all (shouldn't normally happen for a real log MO), returns the
    whole (normalized, lowercased) string."""
    norm = normalize_mo(mo)
    return norm.split("=", 1)[0].strip().lower()


def clean_for_compare(val) -> str | None:
    """Strip a parenthetical annotation (e.g. '0 (NO_OVERRIDE)' -> '0'),
    then lowercase + strip for a case/whitespace-insensitive comparison.
    Returns None for NaN/blank."""
    if pd.isna(val):
        return None
    cleaned = _clean_value(val)
    if cleaned is None or (isinstance(cleaned, float) and pd.isna(cleaned)):
        return None
    # Collapse runs of whitespace to one space. List values are space-separated
    # and the sheet is maintained by pasting, so several cells carry NBSPs
    # (\xa0) between elements — LTE_PARAMETER's pcp0 read NOT OK on that alone
    # while the identical NR_PARAMETER row read OK.
    s = re.sub(r"\s+", " ", str(cleaned)).strip()
    return s.lower() if s else None


# Text inside a parenthetical annotation. hgetc prints an enum as
# "<code> (<LABEL>)"; the golden sheet writes whichever half its author had to
# hand, sometimes with the other half in the parens ("LARGE_SIZE(1)"). Both
# halves are the same reading of the same value, so both are kept — see
# _readings, which is why values_match sees past the half that differs.
_PAREN_RE = re.compile(r"\(([^)]*)\)")

# A full MO reference: comma-separated "Class=value" segments and nothing else.
# Deliberately rejects a condition like '5qi==6', whose "value" holds another
# '=' — that is a settable string, not a path, and must not be leaf-matched.
_MO_PATH_RE = re.compile(r"^[^\s,=]+=[^,=]+(?:,[^\s,=]+=[^,=]+)*$")
# The other side of a leaf match: a bare label, not prose and not a path.
_BARE_LABEL_RE = re.compile(r"^[^\s,=]+$")


def _norm(s) -> str | None:
    """Whitespace-collapsed, lowercased — or None if nothing is left."""
    out = re.sub(r"\s+", " ", str(s)).strip().lower()
    return out or None


@functools.lru_cache(maxsize=8192)
def _readings(text: str) -> frozenset[str]:
    """Every spelling one value can legitimately take.

    A value carries up to two readings of the same setting, and the two sides
    of a comparison do not have to have picked the same one:

        node  '1 (RRC_OR_DL_PRB)'   sheet 'RRC_OR_DL_PRB'
        node  '1 (LARGE_SIZE)'      sheet 'LARGE_SIZE(1)'

    Both are the code and the label of one enum, so both are returned and
    values_match asks only that the two sides agree on ONE of them. The code
    alone already matched (clean_for_compare drops the annotation) — it is the
    rows whose sheet cell spells the LABEL that were reading NOT OK against a
    compliant node.

    A comma-separated list gets its space-separated spelling too, since the
    sheet is hand-typed ('false, false, false') and the node prints the same
    list bare ('false false false'). Never applied to an MO path, where the
    commas separate path segments rather than list elements.
    """
    out: set[str] = set()

    def add(part) -> None:
        n = _norm(part)
        if not n:
            return
        out.add(n)
        if "," in n and "=" not in n:
            listed = _norm(n.replace(",", " "))
            if listed:
                out.add(listed)

    # the count prefix ('i[2] = ') is hgetc's, not part of the value
    body = _ARRAY_PREFIX_RE.sub("", text)
    add(_PAREN_RE.sub(" ", body))            # outside the parens
    for m in _PAREN_RE.finditer(body):       # and inside them
        add(m.group(1))
    return frozenset(out)


def _mo_reference_match(expected_readings, current_readings) -> bool:
    """True when the two sides name the same MO, at different path depths.

    An MO-valued attribute is printed by the node as the full path
    ('ManagedElement=LVALL06,ENodeBFunction=1,QciTable=default,'
    'QciProfilePredefined=qci1') while the sheet names only what identifies it
    ('QCI1', or 'QciProfilePredefined=qci1').

    Two full paths must still match segment-for-segment from the leaf up —
    only a BARE label is matched against a path's leaf value, so two different
    profiles that happen to end in the same word ('...FreqRelProfile=HO' vs
    '...OtherProfile=HO') stay NOT OK.
    """
    for a in expected_readings:
        for b in current_readings:
            pa, pb = normalize_mo(a), normalize_mo(b)
            a_path, b_path = _MO_PATH_RE.match(pa), _MO_PATH_RE.match(pb)
            if a_path and b_path:
                if pa.endswith("," + pb) or pb.endswith("," + pa):
                    return True
            elif a_path and _BARE_LABEL_RE.match(pb):
                if pa.rsplit("=", 1)[1] == pb:
                    return True
            elif b_path and _BARE_LABEL_RE.match(pa):
                if pb.rsplit("=", 1)[1] == pa:
                    return True
    return False


def values_match(expected, current) -> bool:
    """Is the node's value the golden value, however either side spells it?

    The plain comparison first — the two agree outright for the vast majority
    of rows — then the equivalences above, each of which is a difference in
    NOTATION only. Anything that is a real difference in the setting (a
    different code, a different label, a list in a different order) falls
    through all of them and stays NOT OK.
    """
    exp = clean_for_compare(expected)
    cur = clean_for_compare(current)
    if exp is None or cur is None:
        return False
    if exp == cur:
        return True

    exp_readings = _readings(str(expected))
    cur_readings = _readings(str(current))
    if exp_readings & cur_readings:
        return True
    return _mo_reference_match(exp_readings, cur_readings)


def extract_state_code(val) -> str | None:
    """Reduce a feature-state value to its bare numeric code.

    Both orderings occur, on the log side and in the golden sheet:
        'ACTIVATED (1)'  -> '1'   (label first, code parenthesised)
        '1 (ACTIVATED)'  -> '1'   (code first, label parenthesised)
        '1'              -> '1'
    Falls back to the lowercased string when there is no number at all."""
    if pd.isna(val):
        return None
    s = str(val).strip()
    if not s:
        return None
    m = _PAREN_NUM_RE.search(s)
    if m:
        return m.group(1)
    m = _LEADING_NUM_RE.match(s)
    if m:
        return m.group(1)
    return _STATE_WORDS.get(s.lower(), s.lower())


def _load_parameter_sheet(sheet_name: str, book) -> tuple[dict, dict]:
    """Returns (exact_index, class_index).
    exact_index: {(normalized_mo_lower, parameter_lower): entry}
    class_index: {(class_name_lower, parameter_lower): entry}
    entry = {"raw_mo": str, "param": str, "expected": raw value}

    A third, private index (suffix_index) is attached to exact_index so
    lookup_parameter() can match MO paths that name a different number of
    ancestors on either side — see that function.
    """
    cache_key = (str(book), sheet_name, "param")
    if cache_key in _index_cache:
        return _index_cache[cache_key]

    xl = _get_workbook(book)
    if sheet_name not in xl.sheet_names:
        log.warning("Reference workbook %s has no '%s' sheet.", book, sheet_name)
        result = ({}, {})
        _index_cache[cache_key] = result
        return result

    df = _parse_sheet(sheet_name, book)

    exact_index: dict[tuple[str, str], dict] = {}
    class_index: dict[tuple[str, str], dict] = {}
    suffix_index: dict[tuple[str, str], list] = {}
    # parallel set of indexes keyed by a struct member's LEAF name — see
    # _register_leaf below. Consulted only after the full-name lookup misses.
    exact_leaf: dict[tuple[str, str], dict] = {}
    class_leaf: dict[tuple[str, str], dict] = {}
    suffix_leaf: dict[tuple[str, str], list] = {}
    leaf_ambiguous: set[tuple[str, str]] = set()
    # (own key, plain-class twin's key, entry) for rows whose MO class named a
    # struct — resolved once the whole sheet is read, see below.
    struct_class_rows: list[tuple[tuple[str, str], tuple[str, str], dict]] = []

    def _register_leaf(target, key, entry):
        """Index a dotted 'struct.member' row under its bare member name too.

        The sheet names struct attributes as 'esNotAllowedTimePeriod.endTime',
        but hgetc's header for a ``^struct$@member$`` query prints only the
        member ('MO;endTime;startTime'), so the sheet's name never matched the
        log column and the row was reported Missing while sitting right there
        in the log. (Other structs DO print dotted — 'rsrpCandidateA5.hysteresis'
        — which is why the full name is still tried first.)

        Bare member names are not unique: one MO can carry several structs with
        a member of the same name (rsrpCritical/rsrpCandidateA5/rsrpSearchZone
        all have .hysteresis). A bare log column cannot say which struct it came
        from, so the moment a leaf is claimed twice it is marked ambiguous and
        dropped — better a Missing row than a value compared against the wrong
        struct's expected value.
        """
        prev = target.get(key)
        if prev is not None and prev is not entry:
            leaf_ambiguous.add(key)
        target[key] = entry

    for _, row in df.iterrows():
        mo_raw = row.get("Parent MO Class")
        param_raw = row.get("Parameter")
        expected_raw = row.get("FINAL GPL (UPDATED)")
        if pd.isna(mo_raw) or pd.isna(param_raw) or pd.isna(expected_raw):
            continue

        mo_raw = str(mo_raw).strip()
        param_raw = str(param_raw).strip()

        sub_param = row.get("SubParameter")
        if pd.notna(sub_param) and str(sub_param).strip():
            param_raw = f"{param_raw}.{str(sub_param).strip()}"

        # A class-level row sometimes carries the struct in the MO-class column
        # ('EUtranCellTDD.ductIntPerfTuning') instead of naming the parameter
        # 'struct.member'. No MO class hgetc prints has a dot in it, so those
        # rows matched nothing and came out Missing while the value sat in the
        # log — fold the struct into the parameter name, the form the rest of
        # this module already knows how to match.
        cls_raw, struct = mo_raw, None
        if "=" not in mo_raw and "." in mo_raw:
            cls_raw, struct = mo_raw.split(".", 1)
            s_lower, p_lower = struct.lower(), param_raw.lower()
            if (p_lower != s_lower
                    and not p_lower.startswith(s_lower + ".")
                    and not p_lower.endswith("." + s_lower)):
                param_raw = f"{struct}.{param_raw}"

        entry = {"raw_mo": mo_raw, "param": param_raw, "expected": expected_raw}
        # indexed without the '[n]' element count; entry["param"] keeps the
        # sheet's own text so the report still shows what the sheet says
        param_lower = _ELEM_COUNT_RE.sub("", param_raw).strip().lower()
        leaf_lower = param_lower.rsplit(".", 1)[-1] if "." in param_lower else None

        if "=" in mo_raw:
            norm = normalize_mo(mo_raw).lower()
            entry["norm_mo"] = norm
            key = (norm, param_lower)
            entry["key"] = ("exact", norm, param_lower)
            exact_index[key] = entry
            # Also index every segment-aligned suffix of the sheet's MO, so a
            # log MO that prints FEWER ancestors than the sheet names still
            # finds it (sheet 'GNBCUCPFunction=1,CUCP5qiTable=1,CUCP5qi=5qi1'
            # vs log 'CUCP5qiTable=1,CUCP5qi=5qi1'). Candidates are verified
            # for suffix-compatibility at lookup time, so this only widens the
            # search, it does not loosen what counts as a match.
            segs = norm.split(",")
            for i in range(len(segs)):
                suffix_index.setdefault((",".join(segs[i:]), param_lower), []).append(entry)
            if leaf_lower:
                _register_leaf(exact_leaf, (norm, leaf_lower), entry)
                for i in range(len(segs)):
                    suffix_leaf.setdefault((",".join(segs[i:]), leaf_lower), []).append(entry)
        else:
            key = (cls_raw.lower(), param_lower)
            entry["key"] = ("class", cls_raw.lower(), param_lower)
            class_index[key] = entry
            if leaf_lower:
                _register_leaf(class_leaf, (cls_raw.lower(), leaf_lower), entry)
            if struct is not None and leaf_lower:
                struct_class_rows.append((key, (cls_raw.lower(), leaf_lower), entry))

    # The sheets list many of these parameters TWICE — once plainly under the
    # MO class and once again with the struct spelled into that column. Where
    # the two rows say the same thing the second is pure restatement, and
    # keeping both reported the same value twice (once matched bare, once
    # struct-qualified). Keep the plain row. A restatement that DISAGREES is
    # kept, so a sheet contradicting itself still shows up in the report
    # rather than being silently resolved here.
    for key, plain_key, entry in struct_class_rows:
        twin = class_index.get(plain_key)
        if twin is None or twin is entry:
            continue
        if str(twin["expected"]).strip() != str(entry["expected"]).strip():
            continue
        class_index.pop(key, None)
        for leaf_key in [k for k, v in class_leaf.items() if v is entry]:
            del class_leaf[leaf_key]

    # A leaf must never outrank, or be confused with, a real parameter of that
    # name, and must never be guessed when two structs claim it.
    for target in (exact_leaf, class_leaf):
        for key in [k for k in target if k in leaf_ambiguous or k in exact_index or k in class_index]:
            del target[key]
    for key in [k for k in suffix_leaf if k in leaf_ambiguous or k in suffix_index]:
        del suffix_leaf[key]
    for key, cands in list(suffix_leaf.items()):
        if len({id(c) for c in cands}) > 1:
            del suffix_leaf[key]  # same ambiguity, seen through a suffix

    log.info(
        "Reference '%s': %d exact-instance entries, %d class-level entries, "
        "%d struct member(s) also indexed by bare name (%d ambiguous, left unmatched)",
        sheet_name, len(exact_index), len(class_index),
        len(exact_leaf) + len(class_leaf), len(leaf_ambiguous),
    )
    _SUFFIX_INDEXES[id(exact_index)] = suffix_index
    _LEAF_INDEXES[id(exact_index)] = (exact_leaf, class_leaf, suffix_leaf)
    result = (exact_index, class_index)
    _index_cache[cache_key] = result
    return result


def _suffixes(norm_mo: str) -> list[str]:
    """Segment-aligned suffixes of a normalised MO path, longest first:
    'a=1,b=2,c=3' -> ['a=1,b=2,c=3', 'b=2,c=3', 'c=3']"""
    segs = norm_mo.split(",")
    return [",".join(segs[i:]) for i in range(len(segs))]


def _same_mo(a: str, b: str) -> bool:
    """Two MO paths denote the same instance when one is a segment-aligned
    suffix of the other — hgetc prints a different number of ancestors
    depending on how the command was scoped."""
    return a == b or a.endswith("," + b) or b.endswith("," + a)


def _match_mo(norm: str, param_lower: str, exact_index: dict, class_index: dict,
              suffix_index: dict):
    """One MO-matching pass for an already-normalised (MO, parameter).

    Returns (entry, seen_key, anchor). `anchor` is how far ABOVE the log MO's
    leaf segment the match was anchored — 0 means the sheet row is about the
    leaf itself, 1 its parent, and so on. It exists so two sheets' matches for
    the same log row can be compared on substance rather than one sheet simply
    winning by default.

    Only ancestor distance is measured, deliberately. The class scan walks UP
    the MO path, so on 'EUtranCellFDD=…,GUtranFreqRelation=629952' a golden row
    for the parent class EUtranCellFDD will happily answer for a leaf parameter
    of GUtranFreqRelation — that is the mismatch worth catching (anchor 1 vs
    the other sheet's 0).

    Exact and suffix matches both score 0: they always cover the leaf. They are
    NOT ranked above a leaf class match, because a sheet MO that names no
    ancestor ('Rrc=1') is an instance id, not evidence of which tree the row
    belongs to — it suffix-matches GNBDUFunction=1,Rrc=1 and ENodeBFunction=1,
    Rrc=1 alike. Ranking it above the leaf class would let NR_PARAMETER's Rrc=1
    steal the LTE node's Rrc row. Ties are for classify_mo_tree to break.
    """
    entry = exact_index.get((norm, param_lower))
    if entry is not None:
        return entry, ("exact", norm, param_lower), 0

    best = None
    for suf in _suffixes(norm):
        for cand in suffix_index.get((suf, param_lower), ()):
            if not _same_mo(norm, cand["norm_mo"]):
                continue
            # prefer the sheet row that pins down the most ancestors
            if best is None or len(cand["norm_mo"]) > len(best["norm_mo"]):
                best = cand
        if best is not None:
            return best, ("exact", best["norm_mo"], param_lower), 0

    for depth, cls in enumerate(
        s.split("=", 1)[0].strip() for s in reversed(norm.split(","))
    ):
        entry = class_index.get((cls, param_lower))
        if entry is not None:
            return entry, ("class", cls, param_lower), depth

    return None, None, None


def lookup_parameter(mo: str, param: str, exact_index: dict, class_index: dict):
    """Find the reference row for a log (MO, parameter), or (None, None, None).

    Returns (entry, seen_key, anchor) where seen_key identifies which index
    entry was consumed, so the caller can report never-matched reference rows,
    and anchor is _match_mo's ancestor distance (lower is better).

    Two passes over the same MO-matching rules (_match_mo): the log's parameter
    name as printed, then — only if that missed — the same name read as the
    bare member of a 'struct.member' sheet row, since hgetc prints some struct
    members without their struct prefix. The leaf pass is deliberately second
    and deliberately incomplete (ambiguous members are not indexed at all), so
    it can only ever add a match the exact name failed to find.
    """
    param_lower = _ELEM_COUNT_RE.sub("", str(param).strip()).strip().lower()
    norm = normalize_mo(mo).lower()

    entry, key, anchor = _match_mo(
        norm, param_lower, exact_index, class_index,
        _SUFFIX_INDEXES.get(id(exact_index)) or {},
    )
    if entry is not None:
        return entry, key, anchor

    exact_leaf, class_leaf, suffix_leaf = _LEAF_INDEXES.get(id(exact_index)) or ({}, {}, {})
    entry, _, anchor = _match_mo(norm, param_lower, exact_leaf, class_leaf, suffix_leaf)
    if entry is not None:
        # report against the sheet's own key ('struct.member'), never the bare
        # leaf we matched on, so _missing_rows() clears the right reference row.
        # Ranked below every full-name match: a sheet that names the parameter
        # outright always beats one that only matches its bare struct member.
        return entry, entry["key"], _LEAF_ANCHOR_PENALTY + anchor

    return None, None, None


def classify_mo_tree(mo: str) -> str | None:
    """LTE vs NR from the log's own MO path root, independent of which
    commands-file section produced the command that captured it. Returns
    None when the root itself doesn't disambiguate — this happens for a
    handful of golden-list rows (e.g. ENodeBFunction.x2retryTimerMaxAuto)
    that are listed under both LTE_PARAMETER and NR_PARAMETER for what is,
    physically, the same ENodeBFunction instance either way; no MO-path
    classifier can resolve that, it's a golden-list data question."""
    root = mo_class_root(mo)
    if "gnb" in root or root.startswith(("nrcell", "nrsectorcarrier", "nrfreq")):
        return "NR"
    if "enodeb" in root or root.startswith("eutran"):
        return "LTE"
    return None


def lookup_parameter_dual(
    mo: str, param: str, lte_indices: tuple, nr_indices: tuple, value=_UNSET
):
    """Try both reference sheets for one log row.

    The MO's own root tree decides which sheet is *preferred*, not which
    sheet is *consulted*. Preferring matters on a genuine name collision:
    the golden list defines a handful of same-named class/params under both
    sheets with DIFFERENT expected values (UeMeasControl.sMeasure,
    AnrFunction.removeNrelTime, Rrc.t300/t301/t311, ...), and the MO's own
    root is the right tiebreak — an ENodeBFunction instance is audited
    against LTE_PARAMETER's value, a GNBDUFunction instance against
    NR_PARAMETER's.

    But the sheets are NOT partitioned by MO tree, so a miss in the
    preferred sheet must fall through to the other one. NR_PARAMETER carries
    a large block of EN-DC rows whose MOs are physically LTE-rooted
    (ReportConfigB1GUtra, ReportConfigB1NR, ReportConfigA5EndcHo,
    UeMeasControl.endc*, ENodeBFunction.endc*, EUtranCellFDD/TDD.looping*),
    and LTE_PARAMETER likewise has class rows (EUtranFreqRelation.anrMeasOn)
    that only ever appear under an NRCellCU path. Consulting one sheet alone
    dropped every one of those log rows on the floor and then reported the
    reference entry as "Missing" — the parameter was in the log and in the
    extractor output, just never compared.

    The fallback is gated on the log row having a real value, which is what
    keeps the wide-table union artifact out. hgetc commands with a
    multi-attribute regex (e.g. ``^Paging= ...|n$|nS$``) run against every MO
    instance the pattern matches, and reader.py's parsing unions the
    requested attribute names as columns across ALL matched instances — so a
    GNBDUFunction (NR) instance picks up a NaN placeholder column for an
    attribute that is only real on a sibling LTE instance. Those rows carry
    no value, so they never reach the other sheet and never get misrouted.

    Returns a list of (sheet, entry, seen_key) tuples — usually 0 or 1,
    occasionally 2 when the root itself doesn't disambiguate
    (classify_mo_tree returns None) and the golden list lists the same
    class/param under both sheets for what is physically the same instance
    either way.
    """
    tree = classify_mo_tree(mo)

    if tree is not None:
        preferred, fallback = (
            (lte_indices, nr_indices) if tree == "LTE" else (nr_indices, lte_indices)
        )
        other = "NR" if tree == "LTE" else "LTE"

        entry, key, anchor = lookup_parameter(mo, param, *preferred)
        if value is not _UNSET and pd.isna(value):
            # union artifact — no real reading, so never reach across sheets
            return [(tree, entry, key)] if entry is not None else []

        alt, alt_key, alt_anchor = lookup_parameter(mo, param, *fallback)
        # The tree only breaks a TIE. A sheet that matched the MO's leaf class
        # outranks one that only matched an ancestor, whichever tree the root
        # belongs to — otherwise GUtranFreqRelation.qRxLevMin gets audited
        # against the parent EUtranCellFDD's golden value and the correct
        # GUtranFreqRelation row is reported Missing.
        if alt is not None and (entry is None or alt_anchor < anchor):
            return [(other, alt, alt_key)]
        return [(tree, entry, key)] if entry is not None else []

    lte_entry, lte_key, lte_anchor = lookup_parameter(mo, param, *lte_indices)
    nr_entry, nr_key, nr_anchor = lookup_parameter(mo, param, *nr_indices)

    # root doesn't disambiguate: a strictly more specific match still wins;
    # only a genuine tie reports against both sheets
    if lte_entry is not None and nr_entry is not None and lte_anchor != nr_anchor:
        return ([("LTE", lte_entry, lte_key)] if lte_anchor < nr_anchor
                else [("NR", nr_entry, nr_key)])

    if lte_entry is None and nr_entry is None:
        return []
    if nr_entry is None:
        return [("LTE", lte_entry, lte_key)]
    if lte_entry is None:
        return [("NR", nr_entry, nr_key)]
    return [("LTE", lte_entry, lte_key), ("NR", nr_entry, nr_key)]


def _load_feature_sheet(sheet_name: str, book) -> dict:
    """Returns {cxc_id_lower: {"raw_cxc": str, "description": str, "expected": raw value}}
    over EVERY row of `sheet_name` — LTE and NR features are one list.

    "Parent MO Class" is the CXC ID here and "Parameter" the human label —
    the reverse of the *_PARAMETER sheets. Rows whose first column is not a
    CXC ID are skipped: the sheet carries a repeated header row where the LTE
    block ends and the NR block begins.

    A CXC can appear twice. Where both rows agree that's harmless; where they
    disagree only one can be audited (the node has a single featureState per
    CXC), so the FIRST row wins and every clash is logged loudly — delete the
    stale duplicate row to change the outcome."""
    cache_key = (str(book), sheet_name, "feature")
    if cache_key in _index_cache:
        return _index_cache[cache_key]

    xl = _get_workbook(book)
    if sheet_name not in xl.sheet_names:
        log.warning("Reference workbook %s has no '%s' sheet.", book, sheet_name)
        _index_cache[cache_key] = {}
        return {}

    df = _parse_sheet(sheet_name, book)

    idx: dict[str, dict] = {}
    clashes: list[tuple[str, str, str]] = []
    skipped = 0
    for _, row in df.iterrows():
        cxc_raw = row.get("Parent MO Class")
        expected_raw = row.get("FINAL GPL (UPDATED)")
        if pd.isna(cxc_raw) or pd.isna(expected_raw):
            continue
        cxc_raw = str(cxc_raw).strip()
        if not _CXC_RE.fullmatch(cxc_raw):
            skipped += 1
            continue
        key = cxc_raw.lower()

        desc_raw = row.get("Parameter")
        description = str(desc_raw).strip() if pd.notna(desc_raw) else ""

        prev = idx.get(key)
        if prev is not None:
            # compare the way the audit itself will (extract_state_code), not as
            # raw text — a CXC listed once as TRUE and once as 1 means the same
            # ACTIVATED state and is not a clash worth reporting.
            if extract_state_code(prev["expected"]) != extract_state_code(expected_raw):
                clashes.append((cxc_raw, str(prev["expected"]).strip(), str(expected_raw).strip()))
            # 13 rows leave the label blank; if a later duplicate names the
            # feature, use it. Cosmetic only — the expected value still comes
            # from the first row.
            elif not prev["description"] and description:
                prev["description"] = description
            continue  # first row wins

        idx[key] = {"raw_cxc": cxc_raw, "description": description, "expected": expected_raw}

    if skipped:
        log.info("Reference '%s': skipped %d non-CXC row(s) (header separators).", sheet_name, skipped)

    if clashes:
        log.warning(
            "Reference '%s': %d CXC ID(s) listed twice with DIFFERENT expected states — "
            "keeping the first and ignoring the second. Remove the stale duplicate row "
            "from the sheet to change this:", sheet_name, len(clashes),
        )
        for cxc, kept, ignored in clashes:
            log.warning("    %s: using %r, ignoring %r", cxc, kept, ignored)

    log.info("Reference '%s': %d feature entries", sheet_name, len(idx))
    _index_cache[cache_key] = idx
    return idx


def _circles_in(book, prefix: str) -> list[str]:
    return sorted(
        s[len(prefix):].strip().upper()
        for s in _get_workbook(book).sheet_names
        if s.upper().startswith(prefix.upper()) and s[len(prefix):].strip()
    )


def list_available_circles() -> list[str]:
    """Circles that can actually be audited — i.e. that BOTH parameter
    workbooks carry a sheet for.

    Read off the sheet names rather than hardcoded, so a new circle is
    supported the moment an LTE_GPL_<CIRCLE> and an NR_GPL_<CIRCLE> sheet
    exist. Intersected rather than unioned because a circle present in only
    one workbook would audit that half against its own values and the other
    half against nothing.
    """
    lte = set(_circles_in(get_lte_reference_file(), LTE_CIRCLE_SHEET_PREFIX))
    nr = set(_circles_in(get_nr_reference_file(), NR_CIRCLE_SHEET_PREFIX))
    only_lte, only_nr = sorted(lte - nr), sorted(nr - lte)
    if only_lte or only_nr:
        log.warning(
            "Circle sheets present in only one workbook (not selectable): "
            "LTE-only=%s NR-only=%s", only_lte or "-", only_nr or "-",
        )
    return sorted(lte & nr)


def _sheet_for_circle(circle: str | None, book, prefix: str, kind: str) -> str:
    """Sheet in `book` holding `kind` golden values for `circle`.

    Raises for a missing circle rather than falling back to some other sheet:
    every sheet here is circle-specific, so any substitute would silently
    report another circle's expected values as this circle's verdict.
    """
    if not circle:
        raise ValueError(
            f"No circle selected — {kind} golden values are per-circle. "
            f"Pass a circle (available: {', '.join(list_available_circles()) or '(none)'})."
        )

    wanted = str(circle).strip().upper()
    for sheet in _get_workbook(book).sheet_names:
        if (sheet.upper().startswith(prefix.upper())
                and sheet[len(prefix):].strip().upper() == wanted):
            return sheet

    raise ValueError(
        f"No {kind} reference sheet for circle {wanted!r} in "
        f"{Path(book).name}. Available: "
        f"{', '.join(_circles_in(book, prefix)) or '(none)'}. "
        f"Add a '{prefix}{wanted}' sheet to that workbook to support it."
    )


def lte_sheet_for_circle(circle: str | None) -> str:
    return _sheet_for_circle(circle, get_lte_reference_file(), LTE_CIRCLE_SHEET_PREFIX, "LTE")


def nr_sheet_for_circle(circle: str | None) -> str:
    return _sheet_for_circle(circle, get_nr_reference_file(), NR_CIRCLE_SHEET_PREFIX, "NR")


def get_lte_parameter_index() -> tuple[dict, dict]:
    """LTE golden values for the circle selected on this run (config.set_circle)."""
    book = get_lte_reference_file()
    return _load_parameter_sheet(lte_sheet_for_circle(get_circle()), book)


def get_nr_parameter_index() -> tuple[dict, dict]:
    """NR golden values for the circle selected on this run (config.set_circle)."""
    book = get_nr_reference_file()
    return _load_parameter_sheet(nr_sheet_for_circle(get_circle()), book)


def get_feature_index() -> dict:
    """All features — LTE and NR together — from the single FEATURESTATE sheet.
    Pan-India: features are not split per circle."""
    return _load_feature_sheet(FEATURE_SHEET, get_feature_reference_file())
