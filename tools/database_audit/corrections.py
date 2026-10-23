"""Correction scripts of the Database Audit, AMOS and NETCONF XML, section by section.

Every finding of a correctable section becomes one command: NOT OK -> set to the PRE value, a parameter PRE has
and POST does not -> set in 'Missing Parameter/Profile Creation', an MO (profile) PRE has and POST does not ->
created there with all its configurable PRE attributes (children the node makes itself when their parent is created -
ids 1/Default/Base - are set, not created). The audit-only sections (eNB/gNB info, cell data) are never corrected.
The XML is in the format of the KK LTE/5G Config XMLs (hello, one edit-config RPC per MO, close-session).
"""
from __future__ import annotations

import re
from collections import OrderedDict
from xml.sax.saxutils import escape

from tools.lte.amos_netconf.engine import CLOSE, HELLO, NOT_SOFT, SYSTEM_IDS, _kind

from .audit import (CELL_REL, EUTRAN_FREQ, EUTRAN_FREQ_REL, FEATURE, GERAN_FREQ_REL, GUTRAN_FREQ_REL, LTE_GPL, NR_GPL,
                    OTHER, RUNTIME, SITE_DATA, SITE_REF_TOPS, SSB_FREQ, CELL_CLASSES, AuditResult, classes_of,
                    section_of, text)
from .kget_parser import _array_items

MISSING = "Missing"
HEADERS = OrderedDict([
    (LTE_GPL, ("#####Start: LTE GPL Parameter Correction #####", "#####end: LTE GPL Parameter Correction #####")),
    (FEATURE, ("#####Start: FeatureState Correction #######", "#####end: FeatureState Correction #######")),
    (EUTRAN_FREQ, ("#####Start: Eutranfrequency Correction #####", "#####end: Eutranfrequency Correction #####")),
    (SSB_FREQ, ("#####Start: ssbFrequency Correction#######", "#####end: ssbFrequency Correction#######")),
    (EUTRAN_FREQ_REL, ("###Start: EutranfreqRelation Audit Parameter Correction ###",
                       "###end: EutranfreqRelation Audit Parameter Correction ###")),
    (GUTRAN_FREQ_REL, ("#####Start: GutranfreqRelation Parameter Correction#######",
                       "#####end: GutranfreqRelation Parameter Correction#######")),
    (GERAN_FREQ_REL, ("#####Start: GeranFreqRelation Parameter Correction#######",
                      "#####end: GeranFreqRelation Parameter Correction#######")),
    (CELL_REL, ("#####Start: CellRelation Parameter Correction#######", "#####end: CellRelation Parameter Correction#######")),
    (NR_GPL, ("#####Start:NR GPL Parameter correction#######", "#####end: NR GPL Parameter correction#######")),
    (MISSING, ("#####Start: Missing Parameter/Profile Creation#######", "#####end: Missing Parameter/Profile Creation#######")),
])
RPC_PREFIX = {LTE_GPL: "LTEGPL", FEATURE: "Feature", EUTRAN_FREQ: "EutranFreq", SSB_FREQ: "SsbFreq",
              EUTRAN_FREQ_REL: "EutranFreqRel", GUTRAN_FREQ_REL: "GutranFreqRel", GERAN_FREQ_REL: "GeranFreqRel",
              CELL_REL: "CellRel", NR_GPL: "NRGPL", MISSING: "Create"}
_ENUM = re.compile(r"^(-?\d+)\s*\((\w+)\)$")
# node limits (BG1499: "Cardinality 129 is above [0-128]", "Maximum number of MOs of type GeranFrequency in reservedBy
# attribute on ...GeranFreqGroup=1 already reached. Maximum possible number is 32"): creates beyond them are left out
MAX_CHILDREN = {"EUtranCellRelation": 128}             # per parent MO
MAX_RESERVED = {"GeranFrequency": ("geranFreqGroupRef", 32)}   # per referenced MO
# MOM 'Precondition:' texts: a LOCKED condition (the MO itself, its cells, a parent) puts the MOs to lock into the
# Lock section at the start of the scripts and the Unlock section at the end (only MOs UNLOCKED in POST); a switch
# attribute of the same MO is switched for the change and back
_OWN_LOCK = re.compile(r"^(?:value can only be changed if (?:the )?administrativeState is LOCKED|(?:attribute )?"
                       r"administrativeState must (?:equal|be set to) LOCKED(?: before modifying this attribute)?)\.?$", re.I)
_SWITCH = re.compile(r"^(?:value )?can only be changed if (?:attribute )?(\w+) is (true|false)\.?$", re.I)
_LOCK = re.compile(r"\block", re.I)
_CELL = re.compile(r"^(?:ENodeBFunction=[^,]+,EUtranCell[FT]DD|GNBDUFunction=[^,]+,NRCellDU)=[^,]+$")
LOCK_HEADERS = (("#####Start: Cell Lock #######", "#####end: Cell Lock #######"),
                ("#####Start: Cell Unlock #######", "#####end: Cell Unlock #######"))


# ---------------------------------------------------------------------------------------------------- plan
class Plan:
    """what to write, shared by the AMOS and the XML writer"""

    def __init__(self):
        self.sets = OrderedDict((s, OrderedDict()) for s in HEADERS)   # section -> {ldn: [attr]}
        self.creates = []          # [(ldn, soft)] in creation order
        self.notes = OrderedDict((s, []) for s in HEADERS)             # section -> [comment]
        self.guards = {}           # ldn -> (switch attr, value it must have for the change, value afterwards)
        self.locks = OrderedDict()  # MOs locked at the start and unlocked at the end -> reason
        self.stay_locked = set()    # locked MOs PRE has LOCKED: not unlocked at the end
        self.missing_why = {}       # MO missing in POST and not created by the script -> reason


def _mom_info(res, ldn, attr):
    mom = res.post.mom
    return mom.attr(mom.class_key(ldn), attr)


def _creatable(res, ldn) -> str:
    """'' or the reason an MO missing in POST is not created by the script"""
    cls = classes_of(ldn)
    sec = section_of(ldn)
    if CELL_CLASSES.match(ldn) or re.match(r"^(?:ENodeBFunction=[^,]+,SectorCarrier|GNBDUFunction=[^,]+,NRSectorCarrier)=[^,]+$", ldn):
        return "cell / sector carrier of the site - not created by the audit"
    if sec == OTHER:
        return "site specific (transport / equipment / system functions) - not scripted"
    if cls[-1] in RUNTIME:
        return "made by the node from live traffic - not scripted"
    if sec == FEATURE:
        return "FeatureState is created by the node software - not scripted"
    if "Predefined" in cls[-1]:
        return "predefined by the node - not scripted"
    if cls[-1].startswith("EP_"):
        return "endpoint made by the node (\"is system created\") - not scripted"
    if cls[-1] == "PmFlexCounterFilter":
        same = _same_flex_filter(res, ldn)
        if same:
            return (f"POST {same.rsplit(',', 1)[-1]} has the same filter values (the node allows each filter combination "
                    "once: \"... is not unique\") - not scripted")
    # a class without any writable attribute is made by the node unless a child of it is scripted
    # (RpUserPlaneTermination / S1UTermination with only live links below, PmUlInterferenceReport: "is system created")
    key = res.post.mom.class_key(ldn)
    if key and not any(not set((f or "").split(",")) & {"readOnly", "key"} for t, f, d in res.post.mom.attrs[key].values())             and not any(k.startswith(ldn + ",") and k.count(",") == ldn.count(",") + 1 and k not in res.post.mos
                        and not _creatable(res, k) for k in res.pre_mos):
        return "made by the node (no writable attribute) - not scripted"
    return ""


# NR resource blocks per channel bandwidth (MHz) at 30 kHz subcarrier spacing (band n78)
NR_RBS_30KHZ = {10: 24, 15: 38, 20: 51, 25: 65, 30: 78, 40: 106, 50: 133, 60: 162, 70: 189, 80: 217, 90: 245, 100: 273}


def _local(ref: str) -> str:
    return re.sub(r"^ManagedElement=[^,]+,", "", str(ref).strip())


def _bwp_too_wide(res, ldn, attr, pv) -> str:
    """'' or why an NRCellDU bWPRef / bWPSetRef of PRE cannot go on the POST cell: BWPs wider than the POST cell
    ("BWP ... is wider than the ... NRCellDU ... DL cell width", HSN143-1 40 MHz with the 100 MHz BWPs of PRE)"""
    if attr not in ("bWPRef", "bWPSetRef") or not re.match(r"^GNBDUFunction=[^,]+,NRCellDU=[^,]+$", ldn):
        return ""
    mos = lambda k: res.post.mos.get(k) or res.pre_mos.get(k) or {}
    carriers = [_local(r) for r in _refs(res.post.mos.get(ldn, {}).get("nRSectorCarrierRef", ""))]
    widths = [int(m.group(1)) for c in carriers for m in [re.match(r"^\s*(\d+)", text(mos(c).get("bSChannelBwDL", "")))] if m]
    if not widths:
        return ""
    cell_rbs = NR_RBS_30KHZ.get(min(widths), 0)
    bwps = [_local(r) for r in _refs(pv)]
    for s in [b for b in bwps if ",BWPSet=" in b]:             # a BWPSet: its BWPs
        bwps += [_local(r) for a in ("allBWPRegularRef", "startBWPDlRef", "startBWPUlRef") for r in _refs(mos(s).get(a, ""))]
    rbs = [int(m.group(1)) for b in bwps if ",BWP=" in b for m in [re.match(r"^\s*(\d+)", text(mos(b).get("numberOfRBs", "")))] if m]
    if cell_rbs and rbs and max(rbs) > cell_rbs:
        return f"the BWPs ({max(rbs)} RBs) are wider than the POST cell ({min(widths)} MHz = {cell_rbs} RBs)"
    return ""


def _flex_filter_key(mo) -> tuple:
    """the enabled filters of a PmFlexCounterFilter with their ranges (what the node keeps unique)"""
    out = []
    for a, v in mo.items():
        m = re.match(r"^(\w+)FilterEnabled$", a)
        if m and text(v).strip().lower() == "true":
            out.append((m.group(1), text(mo.get(m.group(1) + "FilterMin", "")), text(mo.get(m.group(1) + "FilterMax", ""))))
    return tuple(sorted(out))


def _same_flex_filter(res, ldn) -> str:
    """POST PmFlexCounterFilter of the same function with the filter values of the missing PRE one (HSN143-1: PRE ENDC =
    POST ENDC2To99 made by the 5G GPL: 'combination ... is not unique')"""
    key = _flex_filter_key(res.pre_mos[ldn])
    parent = ldn.rsplit(",", 1)[0]
    return next((k for k, v in res.post.mos.items() if k.rsplit(",", 1)[0] == parent
                 and classes_of(k)[-1] == "PmFlexCounterFilter" and key and _flex_filter_key(v) == key), "")


def _order_creates(res, ldns):
    """parents first, then MOs other new MOs refer to, else in kget order"""
    todo = set(ldns)
    pos = {k: n for n, k in enumerate(ldns)}

    def refs(v):
        if isinstance(v, dict):
            for x in v.values():
                yield from refs(x)
        elif isinstance(v, list):
            for x in v:
                yield from refs(x)
        elif isinstance(v, str) and "=" in v and "," in v:
            yield v

    deps = {}
    for k in ldns:
        d = {p for p in todo if p != k and (k.startswith(p + ","))}
        # written attributes only: the read-only back reference (EUtranFrequency reservedBy -> its relations) made a
        # loop, and the relation was created before its EUtranFrequency
        for v in create_attrs(res, k).values():
            for r in refs(v):
                if r in todo and r != k and not r.startswith(k + ","):
                    d.add(r)
        deps[k] = d
    out, done = [], set()
    while todo:
        ready = sorted((k for k in todo if deps[k] <= done), key=lambda k: (k.count(","), pos[k]))
        if not ready:                                  # reference loop: fall back to depth order
            ready = sorted(todo, key=lambda k: (k.count(","), pos[k]))[:1]
        k = ready[0]
        out.append(k)
        done.add(k)
        todo.discard(k)
    return out


def _refs(v):
    """moRef-like strings in a value"""
    if isinstance(v, dict):
        for x in v.values():
            yield from _refs(x)
    elif isinstance(v, list):
        for x in v:
            yield from _refs(x)
    elif isinstance(v, str) and "=" in v:
        yield v.strip()


def _locked(v) -> bool:
    return "LOCKED" in str(v).upper() and "UNLOCKED" not in str(v).upper()


def _lock_targets(res, ldn, pre) -> list:
    """MOs that must be LOCKED for a change of ldn, from the precondition text"""
    mos = res.post.mos
    if _OWN_LOCK.match(pre):
        return [ldn]
    low = pre.lower()
    if "all eutrancell" in low:
        kinds = "FT" if "fdd/tdd" in low else ("T" if "eutrancelltdd" in low else "F")
        return [k for k in mos if re.match(rf"^ENodeBFunction=[^,]+,EUtranCell[{kinds}]DD=[^,]+$", k)]
    m = re.search(r"parent (?:main )?(\w+)", pre)
    if m:                                         # 'parent NRSectorCarrier', 'parent FieldReplaceableUnit'
        parts = ldn.split(",")
        for n in range(len(parts) - 1, 0, -1):
            if parts[n - 1].split("=")[0].lower() == m.group(1).lower():
                return [",".join(parts[:n])]
    # the cells using the MO (SectorCarrier/NRSectorCarrier reservedBy, NRCellDU bWPRef -> BWP ...), else all cells of
    # its function
    chain = [",".join(ldn.split(",")[:n]) for n in range(len(ldn.split(",")), 0, -1)]
    cells = [r for r in _refs(mos.get(ldn, {}).get("reservedBy", "")) if _CELL.match(r)]
    cells += [k for k in mos if _CELL.match(k) and k not in cells and k not in chain
              and any(r == ldn for v in mos[k].values() for r in _refs(v))]
    cells += [k for k in chain if _CELL.match(k)]
    if cells:
        return cells
    top = ldn.split(",")[0]
    return [k for k in mos if _CELL.match(k) and k.split(",")[0] == top]


def _precondition(res, plan, ldn, attr) -> str:
    """MOM precondition of the POST node: MOs to lock go into plan.locks, a switch into plan.guards"""
    mom = res.post.mom
    pre = res.post.preconditions.get((mom.class_key(ldn), attr), "")
    if not pre:
        return ""
    post = res.post.mos.get(ldn, {})
    m = _SWITCH.match(pre)
    if m and m.group(1) in post:
        need = m.group(2).lower()
        if text(post[m.group(1)]).lower() != need:
            sw = m.group(1)
            after = text(res.pre_mos[ldn].get(sw, post[sw])).lower()
            plan.guards[ldn] = (sw, need, after)
        return ""
    if _LOCK.search(pre) and "thdstatus" not in pre.lower():      # not the TheftDeterrence lock token
        for k in _lock_targets(res, ldn, pre):
            st = res.post.mos.get(k, {}).get("administrativeState")
            if st is not None and not _locked(st):
                plan.locks.setdefault(k, f"{ldn} {attr}: {pre}")
    return ""


def _lock_order(plan, unlock=False) -> list:
    """lock the cells first, then sector carriers / others; unlock the other way round"""
    keys = sorted(plan.locks, key=lambda k: 0 if _CELL.match(k) else 1)
    return [k for k in reversed(keys) if k not in plan.stay_locked] if unlock else keys


def build_plan(res: AuditResult) -> Plan:
    plan = Plan()
    seen = set()
    for it in res.items:
        if it.info or it.status == "OK" or it.section not in HEADERS:
            continue
        key = (it.ldn, it.attr)
        if key in seen:
            continue
        seen.add(key)
        whole_missing = it.attr not in res.post.mos.get(it.ldn, {})
        target = MISSING if whole_missing else it.section
        info = _mom_info(res, it.ldn, it.attr)
        label = f"{it.ldn} {it.attr}"
        pv = res.pre_mos[it.ldn][it.attr]
        if info is None:
            plan.notes[target].append(f"{label}: not in the POST node MOM - not scripted")
        elif "restricted" in info[2]:
            plan.notes[target].append(f"{label}: restricted (only settable when the MO is created) - "
                                      f"PRE '{text(pv)}' - not scripted")
        elif _bwp_too_wide(res, it.ldn, it.attr, pv):
            plan.notes[target].append(f"{label}: {_bwp_too_wide(res, it.ldn, it.attr, pv)} - not scripted")
        elif res.cross_site and it.attr.lower() in SITE_DATA:
            plan.notes[target].append(f"{label}: site data of a different site - not scripted")
        elif res.cross_site and any(r.startswith(SITE_REF_TOPS) for v in (pv, res.post.mos.get(it.ldn, {}).get(it.attr))
                                    for r in _refs(v)):
            plan.notes[target].append(f"{label}: reference to the site's own equipment/transport (PRE '{text(pv)}') - "
                                      "site wiring of a different site - not scripted")
        else:
            why = _precondition(res, plan, it.ldn, it.attr)
            if why:
                plan.notes[target].append(f"{label}: {why} - PRE '{text(pv)}' - not scripted")
            else:
                plan.sets[target].setdefault(it.ldn, []).append(it.attr)
    for ldn in list(plan.guards):              # switch only where a guarded attribute is really changed
        sw = plan.guards[ldn][0]
        if not any(ldn in s and any(a != sw for a in s[ldn]) for s in plan.sets.values()):
            del plan.guards[ldn]

    creatable, skipped, not_made = [], OrderedDict(), set()
    for ldn in res.missing_mos:
        why = _creatable(res, ldn)
        parent = ldn.rsplit(",", 1)[0] if "," in ldn else ""
        if not why and parent and parent not in res.post.mos and parent not in res.missing_mos:
            why = "parent MO is in neither log - not scripted"
        parts = ldn.split(",")
        if not why and any(",".join(parts[:n]) in not_made for n in range(1, len(parts))):
            why = "its parent MO is not created - not scripted"
        if why:
            not_made.add(ldn)
            plan.missing_why[ldn] = why
            skipped.setdefault((classes_of(ldn)[-1], why), []).append(ldn)
        else:
            creatable.append(ldn)
    # one line per class (a kget pair of two sites differs in thousands of inventory / system MOs);
    # every MO is listed in the report's MISSING_MO_PROFILE sheet
    for (cls, why), ldns in skipped.items():
        plan.notes[MISSING].append(ldns[0] + f": {why}" if len(ldns) == 1 else
                                   f"{len(ldns)} x {cls}: {why} (see MISSING_MO_PROFILE sheet)")
    children, reserved, left_out = {}, {}, set(not_made)
    for k, v in res.post.mos.items():
        cls = classes_of(k)[-1]
        if cls in MAX_CHILDREN:
            p = k.rsplit(",", 1)[0]
            children[(p, cls)] = children.get((p, cls), 0) + 1
        if cls in MAX_RESERVED:
            r = (cls, text(v.get(MAX_RESERVED[cls][0], "")))
            reserved[r] = reserved.get(r, 0) + 1
    for ldn in _order_creates(res, creatable):
        parent = ldn.rsplit(",", 1)[0] if "," in ldn else ""
        cls = classes_of(ldn)[-1]
        if parent in left_out or any(r in left_out for v in create_attrs(res, ldn).values() for r in _refs(v)):
            left_out.add(ldn)
            plan.missing_why[ldn] = "its parent / a referenced MO is not created - not scripted"
            plan.notes[MISSING].append(f"{ldn}: {plan.missing_why[ldn]}")
            continue
        if cls in MAX_CHILDREN:
            n = children.get((parent, cls), 0) + 1
            if n > MAX_CHILDREN[cls]:
                left_out.add(ldn)
                plan.missing_why[ldn] = f"the parent has {n - 1} {cls} already (node maximum {MAX_CHILDREN[cls]}) - not scripted"
                plan.notes[MISSING].append(f"{ldn}: {plan.missing_why[ldn]}")
                continue
            children[(parent, cls)] = n
        if cls in MAX_RESERVED:
            attr, top = MAX_RESERVED[cls]
            r = (cls, text(res.pre_mos[ldn].get(attr, "")))
            n = reserved.get(r, 0) + 1
            if n > top:
                left_out.add(ldn)
                plan.missing_why[ldn] = f"{r[1]} is used by {n - 1} {cls} already (node maximum {top}) - not scripted"
                plan.notes[MISSING].append(f"{ldn}: {plan.missing_why[ldn]}")
                continue
            reserved[r] = n
        # an id 1/Default/Base child is taken as node-made (own merge RPC after its parent) - not the NOT_SOFT classes:
        # BWPSet needs its BWPSetUeCfg=1 in its own create (HSN143-1: "must have exactly one BWPSetUeCfg instance ...")
        soft = parent in creatable and ldn.rsplit("=", 1)[-1] in SYSTEM_IDS and cls not in NOT_SOFT
        plan.creates.append((ldn, soft))

    # changes that point to an MO created by the script go behind the creates (NRCellCU mcpcPSCellProfileRef ->
    # McpcPSCellProfile=Default_copy was set in the NR GPL section before the profile existed); changes of left out
    # MOs are dropped with them
    new = {ldn for ldn, _ in plan.creates}
    for sec in [s for s in HEADERS if s != MISSING]:
        for ldn, attrs in list(plan.sets[sec].items()):
            for a in list(attrs):
                if any(r in new or r in left_out for r in _refs(res.pre_mos[ldn][a])):
                    attrs.remove(a)
                    if any(r in left_out for r in _refs(res.pre_mos[ldn][a])):
                        plan.notes[sec].append(f"{ldn} {a}: refers to an MO that is not created - not scripted")
                    else:
                        plan.sets[MISSING].setdefault(ldn, []).append(a)
            if not attrs:
                del plan.sets[sec][ldn]
    # an MO of the Lock section keeps the lock where PRE has it LOCKED (its administrativeState correction is the
    # lock itself); its unlock is left out
    for ldn in plan.locks:
        for sec in HEADERS:
            attrs = plan.sets[sec].get(ldn, [])
            if "administrativeState" in attrs:
                attrs.remove("administrativeState")
                if not attrs:
                    del plan.sets[sec][ldn]
                if _locked(res.pre_mos[ldn]["administrativeState"]):
                    plan.stay_locked.add(ldn)
    return plan


def set_value(res, ldn, attr):
    """PRE value to write on an existing MO; a struct is written whole with the PRE members, empty ones included (the
    node needs every member: csiRsConfig4P without i11Restriction = "Multiplicity violation"; taking POST's member
    instead gave csiRsControl4Ports OFF + i11Restriction FF = "incorrect configuration", HSN143-1); only members PRE
    does not have at all (other release) come from POST"""
    v = res.pre_mos[ldn][attr]
    cur = res.post.mos.get(ldn, {}).get(attr)
    if isinstance(v, dict) and isinstance(cur, dict):
        v = OrderedDict(v)
        v.update((m, x) for m, x in cur.items() if m not in v)
    return v


def create_attrs(res, ldn):
    """configurable PRE attributes of a missing MO that the POST MOM knows"""
    out = OrderedDict()
    for a, v in res.pre_mos[ldn].items():
        info = _mom_info(res, ldn, a)
        if not info or "readOnly" in info[2] or "key" in info[2]:
            continue
        cls = classes_of(ldn)[-1]
        if a.lower() == (cls[0].lower() + cls[1:] + "Id").lower():
            continue
        if text(v) == "" and "mandatory" not in info[2]:
            continue
        out[a] = v
    return out


# ---------------------------------------------------------------------------------------------------- AMOS
def _amos_scalar(v: str) -> str:
    m = _ENUM.match(str(v).strip())
    return m.group(1) if m else str(v).strip()


def _amos_member(x) -> str:
    x = str(x).strip()
    if _ENUM.match(x):
        return _amos_scalar(x)
    return " ".join(_amos_scalar(t) for t in _array_items(x))     # sequence member: 'false false false', '1 2 (A B)'


def amos_value(v) -> str:
    if isinstance(v, dict):
        return ",".join(f"{m}={_amos_member(x)}" for m, x in v.items())
    if isinstance(v, list):
        if v and isinstance(v[0], dict):
            return ";".join(amos_value(x) for x in v)
        return " ".join(_amos_scalar(x) for x in v)
    return _amos_scalar(v)


def _amos_mo(ldn: str) -> str:
    return re.sub(r"([+()\[\]*?^|])", r"\\\1", ldn) + "$"


def write_amos(res: AuditResult, plan: Plan, ts: str) -> str:
    out = [f"##### Database Audit correction script (AMOS) | POST node {res.node} | reference PRE node {res.pre.node} "
           f"| {ts} #####", "", "lt all", ""]
    (lock_start, lock_end), (unlock_start, unlock_end) = LOCK_HEADERS
    out.append(lock_start)
    for ldn in _lock_order(plan):
        out += [f"# needed for {plan.locks[ldn]}", f"bl {_amos_mo(ldn)}"]
    out += [lock_end, ""]
    for sec, (start, end) in HEADERS.items():
        out.append(start)               # the 'not scripted' notes stay out of the scripts (user); the report lists them
        if sec == MISSING:
            # same groups and order as the XML; a new MO with new children in one transaction (confb+ ... confb-):
            # a CUCP5qiTable needs at least one CUCP5qi when it is created
            soft_of = dict(plan.creates)
            for group in _create_groups(res, plan):
                bulk = len([m for m in group if not soft_of[m]]) > 1
                if bulk:
                    out.append("confb+")
                for ldn in group:
                    attrs = create_attrs(res, ldn)
                    if soft_of[ldn]:
                        out += [f"set {_amos_mo(ldn)} {a} {amos_value(v)}".rstrip() for a, v in attrs.items()]
                        continue
                    out.append(f"crn {ldn}")
                    out += [f"{a} {amos_value(v)}".rstrip() for a, v in attrs.items()]
                    out.append("end")
                if bulk:
                    out.append("confb-")
        for ldn, attrs in plan.sets[sec].items():
            g = plan.guards.get(ldn)
            if g:
                out.append(f"set {_amos_mo(ldn)} {g[0]} {g[1]}")
            for a in attrs:
                if not (g and a == g[0]):
                    out.append(f"set {_amos_mo(ldn)} {a} {amos_value(set_value(res, ldn, a))}".rstrip())
            if g and g[2] != g[1]:
                out.append(f"set {_amos_mo(ldn)} {g[0]} {g[2]}")
        out += [end, ""]
    out.append(unlock_start)
    out += [f"deb {_amos_mo(ldn)}" for ldn in _lock_order(plan, unlock=True)]
    out += [unlock_end, ""]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------------------------------- XML
def _xml_scalar(res, kind, ref, v: str) -> str:
    v = str(v).strip()
    m = _ENUM.match(v)
    if m:
        return m.group(2)
    if kind == "enumRef" and re.fullmatch(r"-?\d+", v):
        return res.post.mom.enums.get(ref, {}).get(int(v), v)
    if kind == "moRef" and v and not v.startswith("ManagedElement="):
        return f"ManagedElement={res.node},{v}"
    if kind == "boolean":
        return v.lower()
    return v


def _xml_attr(res, ldn, attr, v) -> str:
    info = _mom_info(res, ldn, attr)
    seq, kind, ref = _kind(info[1]) if info else (isinstance(v, list), "string", "")
    if v in ("", None) or (isinstance(v, list) and not v):
        return f'<{attr} xc:operation="delete"></{attr}>'
    if isinstance(v, dict) or (isinstance(v, list) and v and isinstance(v[0], dict)):
        members = res.post.mom.attrs.get(ref, {})

        def struct(d):
            inner = []
            for m, x in d.items():
                mt = members.get(m)
                mseq, mkind, mref = _kind(mt[0]) if mt else (False, "string", "")
                vals = _array_items(str(x)) if mseq else [x]
                if not mseq and text(x) == "" and mkind in ("string", "derivedRef"):
                    inner.append(f"<{m}></{m}>")        # empty member (csiRsConfig4P i11Restriction) - not left out
                    continue
                inner += [f"<{m}>{escape(_xml_scalar(res, mkind, mref, y))}</{m}>" for y in vals if str(y) != ""]
            return f"<{attr}>{''.join(inner)}</{attr}>"
        return "".join(struct(d) for d in (v if isinstance(v, list) else [v]))
    vals = v if isinstance(v, list) else [v]
    return "".join(f"<{attr}>{escape(_xml_scalar(res, kind, ref, x))}</{attr}>" for x in vals)


def _xml_mo(res, ldn, attrs, create=False) -> list[str]:
    rdns = ldn.split(",")
    out, tags = [], []
    for n, rdn in enumerate(rdns):
        cls, _, idv = rdn.partition("=")
        idtag = cls[0].lower() + cls[1:] + "Id"
        op = ' xc:operation="create"' if create and n == len(rdns) - 1 else ""
        out.append(f"<{cls}{op}><{idtag}>{escape(idv)}</{idtag}>")
        tags.append(cls)
    out += [_xml_attr(res, ldn, a, v) for a, v in attrs.items()]
    out.append("".join(f"</{c}>" for c in reversed(tags)))
    return out


def _create_groups(res, plan) -> list:
    """creates -> RPCs: a new MO with all its new children in one RPC (a CUCP5qiTable needs at least one CUCP5qi in
    its create transaction: "Cardinality 0 is below [1-29]"); an MO with a system id (1/Default/Base) starts a group
    of its own; groups in reference order (parents and referenced MOs first)"""
    soft = dict(plan.creates)
    root = {}
    for ldn, _ in plan.creates:                       # parents come first in plan.creates
        parent = ldn.rsplit(",", 1)[0] if "," in ldn else ""
        root[ldn] = root[parent] if parent in root and not soft[ldn] else ldn
    groups = OrderedDict()
    for ldn, _ in plan.creates:
        groups.setdefault(root[ldn], []).append(ldn)
    deps = {}
    for r, members in groups.items():
        d = set()
        for m in members:
            parent = m.rsplit(",", 1)[0] if "," in m else ""
            refs = {x for v in create_attrs(res, m).values() for x in _refs(v)} | {parent}
            d |= {root[x] for x in refs if x in root}
        deps[r] = d - {r}
    out, done, todo = [], set(), list(groups)
    while todo:
        k = next((r for r in todo if deps[r] <= done), todo[0])     # reference loop: keep the plan order
        out.append(groups[k])
        done.add(k)
        todo.remove(k)
    return out


def _xml_tree(res, items) -> list[str]:
    """several MOs (ldn, attrs) in one nested edit-config body"""
    tree = OrderedDict()
    for ldn, attrs in items:
        node = tree
        for rdn in ldn.split(","):
            node = node.setdefault(rdn, OrderedDict({"": None}))
        node[""] = (ldn, attrs)

    def render(node):
        out = []
        for rdn, child in node.items():
            if rdn == "":
                continue
            cls, _, idv = rdn.partition("=")
            idtag = cls[0].lower() + cls[1:] + "Id"
            out.append(f"<{cls}><{idtag}>{escape(idv)}</{idtag}>")
            if child[""]:
                ldn, attrs = child[""]
                out += [_xml_attr(res, ldn, a, v) for a, v in attrs.items()]
            out += render(child)
            out.append(f"</{cls}>")
        return out
    return render(tree)


def _rpc(node, mid, body) -> str:
    return (f'<rpc message-id="{mid}" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
            '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n<target>\n<running/>\n</target>\n'
            '<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">\n<ManagedElement>\n'
            f"<managedElementId>{escape(node)}</managedElementId>\n" + "\n".join(body) +
            "\n</ManagedElement>\n</config>\n</edit-config>\n</rpc>\n")


def _comment(s: str) -> str:
    return "<!-- " + s.replace("--", "- -") + " -->\n"


def write_xml(res: AuditResult, plan: Plan, ts: str) -> str:
    """hello, then per section: one RPC per MO (one per FeatureState / created MO); section headers and notes are
    XML comments in front of / behind the RPCs (comments are allowed around the root element of a NETCONF message)"""
    messages, pending = [], [_comment(f"Database Audit correction script (NETCONF) | POST node {res.node} | "
                                      f"reference PRE node {res.pre.node} | {ts}")]

    def add(mid, body):
        nonlocal pending
        messages.append(["".join(pending), _rpc(res.node, mid, body), ""])
        pending = []

    def lock_section(headers, keys, state, prefix):
        nonlocal pending
        pending.append(_comment(headers[0]))
        for n, ldn in enumerate(keys, 1):
            if state == "LOCKED":
                pending.append(_comment(f"needed for {plan.locks[ldn]}"))
            add(f"{prefix}_{n:04d}_{classes_of(ldn)[-1]}", _xml_mo(res, ldn, {"administrativeState": state}))
        if keys:
            messages[-1][2] += _comment(headers[1])
        else:
            pending.append(_comment(headers[1]))

    lock_section(LOCK_HEADERS[0], _lock_order(plan), "LOCKED", "Lock")
    for sec, (start, end) in HEADERS.items():
        pending.append(_comment(start))
        n = 0
        if sec == MISSING:
            # merge, not create: a missing MO the node has made meanwhile (BG1499 UlServiceDefinitionUeCfg=VoNR
            # "already exist") is then set instead of failing
            for group in _create_groups(res, plan):
                n += 1
                add(f"{RPC_PREFIX[sec]}_{n:04d}_{classes_of(group[0])[-1]}",
                    _xml_tree(res, [(ldn, create_attrs(res, ldn)) for ldn in group]))
        for ldn, attrs in plan.sets[sec].items():
            name = ldn.rsplit(",", 1)[-1].replace("=", "_") if sec == FEATURE else classes_of(ldn)[-1]
            g = plan.guards.get(ldn)
            vals = OrderedDict((a, set_value(res, ldn, a)) for a in attrs if not (g and a == g[0]))
            # a switch guarding the change (DESManagementFunction desSwitch): own RPCs before and after it
            for part in ([{g[0]: g[1]}] if g else []) + [vals] + ([{g[0]: g[2]}] if g and g[2] != g[1] else []):
                if part:
                    n += 1
                    add(f"{RPC_PREFIX[sec]}_{n:04d}_{name}", _xml_mo(res, ldn, part))
        if n:
            messages[-1][2] += _comment(end)
        else:
            pending.append(_comment(end))
    lock_section(LOCK_HEADERS[1], _lock_order(plan, unlock=True), "UNLOCKED", "Unlock")
    out = [HELLO]
    out += [pre + rpc + post + "]]>]]>\n" for pre, rpc, post in messages]
    out.append("".join(pending) + CLOSE)
    return "".join(out)


def count_commands(plan: Plan) -> dict:
    out = OrderedDict()
    for sec in HEADERS:
        n = sum(len(v) for v in plan.sets[sec].values())
        out[sec] = n + (len(plan.creates) if sec == MISSING else 0)
    return out
