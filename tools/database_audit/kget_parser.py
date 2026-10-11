"""kget_mom log -> MOs + MOM.

Built on the kget/MOM reading of the KK XML work (LTE_Integration_Scripting_Automtion/amos_netconf: the
'MO <ldn>' block rule and the 'mom all all' ATTR/ENUM rules of its model builder, engine.Mom for lookups),
extended to keep every attribute of every MO, structs, sequences and sequences of structs included.

    data = parse_kget(path)
    data.node          'KK-NLAAZAD1-1'
    data.mos           {'ENodeBFunction=1,EUtranCellFDD=...': {attr: value}}   (LDN below ManagedElement)
    data.mom           engine.Mom of the log's own 'mom all all' (falls back to the bundled 25.Q2 MOM)

value = str | list[str] | dict(member -> str | list[str]) | list[dict]
enum values are kept as printed ('3 (OFF)'), references without the 'ManagedElement=<node>,' prefix.
"""
from __future__ import annotations

import re
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path

from tools.lte.amos_netconf.engine import Mom, _load

_PROMPT = re.compile(r"^(\S+?)>\s+(\S.*)$")
_MO = re.compile(r"^MO\s+\S*?ManagedElement=([^,\s]+)(?:,(\S+))?\s*$")
_ATTR_LINE = re.compile(r"^([A-Za-z]\w*)(?:\[(\d+)\])?(?:\s+(.*?))?\s*$")
_STRUCT_HEAD = re.compile(r"^Struct\s+(\w+)\s+has\s+\d+\s+members:")
_ARR_STRUCT = re.compile(r"^\s*>>>\s*Struct\[(\d+)\]\s+has\s+\d+\s+members:")
_MEMBER = re.compile(r"^\s*>>>\s*\d+\.(\w+)\s*=\s?(.*?)\s*$")
_ARR_ITEM = re.compile(r"^\s*>>>\s*(\w+)\s*=\s?(.*?)\s*$")
# MOM ('mom all all'): same rules as the KK XML model builder
_MOM_ATTR = re.compile(r"^(\w+)\.(\w+)\s{2,}(\w+)\s{2,}(\S+)\s*(\S*)\s*$")
_MOM_ENUM = re.compile(r"^(\w+\.\w+)\s{2,}(-?\d+:\w+(?:,\s*-?\d+:\w+)*)\s*$")
_ME_PREFIX = re.compile(r"(?:SubNetwork=[^,]*,)*(?:MeContext=[^,]*,)?ManagedElement=[^,\s]+,?")


@dataclass
class KgetData:
    path: Path
    node: str = ""
    mos: "OrderedDict[str, OrderedDict]" = field(default_factory=OrderedDict)
    mom: Mom | None = None
    mom_from_log: bool = False
    release: str = ""
    # 'Precondition:' line of the MOM description, ("Ns.Class", attr) -> text (only from the log's own 'mom all all')
    preconditions: dict = field(default_factory=dict)


def _strip_me(value: str) -> str:
    """'ManagedElement=KK-NLAAZAD1-1,ENodeBFunction=1,...' -> 'ENodeBFunction=1,...' (node-independent)"""
    return _ME_PREFIX.sub("", value) if "ManagedElement=" in value else value


def _parse_mom(lines: list[str]) -> tuple[Mom | None, dict]:
    attrs, enums, preconditions = {}, {}, {}
    i = 0
    while i < len(lines):
        line = lines[i]
        m = _MOM_ENUM.match(line)
        if m:
            enums[m.group(1)] = {int(k): v for k, v in (p.strip().split(":") for p in m.group(2).split(","))}
            i += 1
            continue
        m = _MOM_ATTR.match(line)
        if m and not re.match(r"^-?\d+:", m.group(4)):
            ns, cls, attr, typ, flags = m.groups()
            default = None
            j = i + 1
            while j < len(lines) and not lines[j].startswith("*****") and not _MOM_ATTR.match(lines[j]):
                d = re.match(r"^Default=(.*)$", lines[j].strip())
                if d:
                    default = d.group(1).strip()
                p = re.match(r"^Precondition:\s*(.+)$", lines[j].strip())
                if p:
                    preconditions[(f"{ns}.{cls}", attr)] = p.group(1).strip()
                j += 1
            attrs.setdefault(f"{ns}.{cls}", {})[attr] = [typ, flags, default]
            i = j
            continue
        i += 1
    if not attrs:
        return None, {}
    return Mom({"attrs": attrs, "enums": {k: {str(n): v for n, v in e.items()} for k, e in enums.items()}}), preconditions


def _array_items(value: str) -> list[str]:
    """'1 2 0 (EEA1 EEA2 EEA0)' (sequence of enums) -> ['1 (EEA1)', '2 (EEA2)', '0 (EEA0)'], like a single enum
    '3 (OFF)'; anything else -> split on blanks"""
    m = re.match(r"^(.*?)\s*\((.*)\)$", value.strip())
    if m:
        nums, names = m.group(1).split(), m.group(2).split()
        if nums and len(nums) == len(names) and all(re.fullmatch(r"-?\d+", n) for n in nums):
            return [f"{n} ({x})" for n, x in zip(nums, names)]
    return value.split()


def parse_kget(path: Path | str) -> KgetData:
    path = Path(path)
    text = path.read_bytes().decode("utf-8", "replace").replace("\r\n", "\n")
    lines = text.split("\n")
    data = KgetData(path=path)

    mom_start = None
    for n, line in enumerate(lines):
        p = _PROMPT.match(line)
        if p and p.group(2).strip().lower().startswith("mom "):
            mom_start = n
            break
        if not data.release and "MSRBS_NODE_MODEL_" in line:
            data.release = re.search(r"MSRBS_NODE_MODEL_\S+", line).group(0)

    cur = None                 # attrs of the current MO
    pending = None             # ("struct", name, dict) | ("array", name, list) | ("sarray", name, list)
    for line in lines[:mom_start]:
        m = _MO.match(line)
        if m:
            data.node = data.node or m.group(1)
            ldn = m.group(2) or ""
            cur = data.mos.setdefault(ldn, OrderedDict())
            pending = None
            continue
        if cur is None:
            continue
        if line.startswith("=") or line.startswith("Proxy Id") or not line.strip():
            continue
        if _PROMPT.match(line) and not line.startswith(" "):
            cur, pending = None, None             # next command: the kget is over
            continue
        if line.lstrip().startswith(">>>"):
            if pending is None:
                continue
            kind, name, holder = pending
            s = _ARR_STRUCT.match(line)
            if s and kind in ("array", "sarray"):
                if kind == "array":                # first element tells: array of structs
                    pending = ("sarray", name, holder)
                    cur[name] = holder
                holder.append(OrderedDict())
                continue
            mm = _MEMBER.match(line)
            if mm and kind == "struct":
                holder[mm.group(1)] = _strip_me(mm.group(2))
                continue
            if mm and kind == "sarray" and holder:
                holder[-1][mm.group(1)] = _strip_me(mm.group(2))
                continue
            it = _ARR_ITEM.match(line)
            if it and kind == "array":
                holder.append(_strip_me(it.group(2)))
            continue
        s = _STRUCT_HEAD.match(line)
        if s:
            holder = OrderedDict()
            cur[s.group(1)] = holder
            pending = ("struct", s.group(1), holder)
            continue
        a = _ATTR_LINE.match(line)
        if not a:
            continue
        name, count, value = a.group(1), a.group(2), (a.group(3) or "")
        if count is not None:
            items = _array_items(value) if value.strip() else []
            holder = [_strip_me(x) for x in items]
            cur[name] = holder
            pending = ("array", name, holder)
        else:
            cur[name] = _strip_me(value)
            pending = None

    if mom_start is not None:
        data.mom, data.preconditions = _parse_mom(lines[mom_start:])
        data.mom_from_log = data.mom is not None
    if data.mom is None:
        data.mom = Mom(_load("mom_25Q2.json.gz"))
    if not data.node:
        for line in lines:
            p = _PROMPT.match(line)
            if p:
                data.node = p.group(1)
                break
    if not data.mos:
        raise ValueError(f"{path.name}: no 'MO ...' blocks found - upload the output of 'kget' (kget_mom log).")
    return data
