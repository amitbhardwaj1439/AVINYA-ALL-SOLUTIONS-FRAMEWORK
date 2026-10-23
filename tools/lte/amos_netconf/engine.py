"""Convert moshell/AMOS integration scripts into one NETCONF edit-config XML.

The scripts are replayed (moshell semantics: MO patterns, crn/cr/set/lset/setm/bl/deb/del, ma groups, for/func/if,
$variables, get) on a model of the node, then the end state is written as NETCONF:
create for MOs made by the scripts, merge for attributes changed on MOs that already exist, delete for existing MOs
the scripts remove. Commands that cannot be expressed in NETCONF (scw, /cm/sysconwrite, cvms, shell, values only
known on the live node, ...) are returned as leftovers.

Model = commissioning XML + earlier NETCONF XML (e.g. 04 LTE_Config) + system-created MOs of a reference node
(data/system_mos_KK.json.gz) + MOM of the node release (data/mom_25Q2.json.gz).
"""
import gzip
import json
import os
import re
import xml.parsers.expat
from collections import OrderedDict
from xml.sax.saxutils import escape

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
TOP_NS = {"enodebfunction": "Lrat", "gnbdufunction": "GNBDU", "gnbcucpfunction": "GNBCUCP", "gnbcuupfunction": "GNBCUUP"}
SKIP_SYSTEM = re.compile(r"^SystemFunctions=1,(Pm=1,PmGroup|PmEventM=1,EventProducer|PmEventSigM=1,EventProducer|HealthCheckM|SwInventory|HwInventory|SysM=1,Schema|LogM)")
UNKNOWN = object()
GNB_NS = {"GNBDU", "GNBCUCP", "GNBCUUP"}
SYSTEM_IDS = {"1", "Default", "Base"}          # ids the node uses for the MOs it creates itself
# classes of the reference kget that are not made by the node at integration: neighbour frequencies/relations of the
# reference site (EUtranFrequency=39175 ...) and S1-U paths the node only learns from live traffic
NOT_SYSTEM = {"EUtranFrequency", "EUtranFreqRelation", "TermPointToSGW", "GtpPath"}
# attributes the node validates together: written in one RPC (final values) at the last write of any of them
# (NRCellDU: dlMaxMuMimoLayers > 0 is only accepted with a matching csiRsConfig<n>P - AMOS sets 32P first)
GROUPED_ATTRS = {"DscpPcpMap": re.compile(r"^pcp\d$"), "NRCellDU": re.compile(r"^(dlMaxMuMimoLayers|csiRsConfig\d+P)$")}
# MOs whose changes go in an RPC of their own: a FeatureState missing in the node's software, SecurityHandling needs a
# security-admin role ("User is not Authorized") - either fails alone instead of taking other changes with it
SOLO_CLASSES = re.compile(r",(featurestate|securityhandling)=|^,gnbcucpfunction=[^,]+,eutranetwork=[^,]+,eutranfrequency=")
# MOs the live node may have made itself before the script creates them: the gNodeB adds the EUtranFrequency of a
# neighbour eNodeB on X2/ANR ("EUtranFrequency=39126 already exist" on BGR583, the create also took the
# EUtranFreqRelations of the same RPC down). Written as merge in an RPC of their own (SOLO_CLASSES).
NODE_MADE = re.compile(r"^,gnbcucpfunction=[^,]+,eutranetwork=[^,]+,eutranfrequency=")
# id-1 classes the node does not make itself (soft() would take them for system MOs): BWPSet needs at least one
# BWPSetUeCfg in its create transaction ("child MOC: BWPSetUeCfg, Cardinality 0 is below [1-8]")
NOT_SOFT = {"BWPSetUeCfg"}
# MOM per circle: KK runs 25.Q2; AS / NE must work on 25.Q2 and 26.Q2 (user 2026-10-13) -> only what both releases have
MOM_FILES = {"KK": ("mom_25Q2.json.gz", "preconditions_25Q2.json.gz")}
MOM_DEFAULT = ("mom_25Q2_26Q2.json.gz", "preconditions_25Q2_26Q2.json.gz")
BRANCH_ORDER = ["Transport", "NodeSupport", "GNBCUUPFunction", "GNBDUFunction", "GNBCUCPFunction", "ENodeBFunction", "SystemFunctions"]
HELLO = """<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
<capabilities>
<capability>urn:ietf:params:netconf:base:1.0</capability>
<capability>urn:com:ericsson:ebase:0.1.0</capability>
<capability>urn:com:ericsson:ebase:1.1.0</capability>
</capabilities>
</hello>
]]>]]>
"""
CLOSE = """<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
"""

_cache = {}


def _load(name):
    if name not in _cache:
        with gzip.open(os.path.join(DATA, name), "rt", encoding="utf-8") as f:
            _cache[name] = json.load(f)
    return _cache[name]


class Mom:
    def __init__(self, data):
        self.attrs = data["attrs"]                      # "Ns.Class" -> {attr: [type, flags, default]}
        self.enums = {k: {int(n): v for n, v in e.items()} for k, e in data["enums"].items()}
        self.by_class = {}
        for key in self.attrs:
            ns, cls = key.split(".", 1)
            self.by_class.setdefault(cls.lower(), {})[ns] = key
        self.lower = {key: {a.lower(): a for a in v} for key, v in self.attrs.items()}
        self.classes_with_attr = {}
        for key, v in self.attrs.items():
            for a in v:
                self.classes_with_attr.setdefault(a.lower(), set()).add(key)

    def class_key(self, ldn):
        parts = ldn.split(",") if ldn else []
        cls = parts[-1].split("=")[0] if parts else "ManagedElement"
        cands = self.by_class.get(cls.lower(), {})
        if not cands:
            return None
        ns = TOP_NS.get(parts[0].split("=")[0].lower()) if parts else None
        if ns in cands:
            return cands[ns]
        other = [k for n, k in cands.items() if n not in TOP_NS.values()]
        if ns:
            # never the class of another radio function (GNBDUFunction,...,DataRadioBearer is not Lrat.DataRadioBearer)
            return other[0] if other else None
        return (other or list(cands.values()))[0]

    def attr(self, key, name):
        """-> (canonical name, type, flags set, default) or None"""
        if not key:
            return None
        a = self.lower.get(key, {}).get(name.lower())
        if a is None:
            return None
        t, fl, d = self.attrs[key][a]
        return a, t, set(fl.split(",")) if fl else set(), d

    def prompts(self, key):
        """attributes moshell 'cr' asks for, in MOM order"""
        out = []
        for a, (t, fl, d) in self.attrs.get(key, {}).items():
            f = set(fl.split(",")) if fl else set()
            if ("mandatory" in f or "restricted" in f) and "key" not in f and "readOnly" not in f:
                out.append(a)
        return out


def _kind(t):
    seq = t.startswith("sequence")
    if seq:
        t = t.split(":", 1)[1] if ":" in t else t
    m = re.match(r"^(\w+)(?:[:-](.*))?$", t)
    return seq, (m.group(1) if m else t), (m.group(2) if m else "")


class Ref:
    __slots__ = ("raw", "ctx")

    def __init__(self, raw, ctx):
        self.raw, self.ctx = raw, ctx

    def __repr__(self):
        return self.raw


class Cleared(list):
    """sequence emptied by a set without value (only_changes steps): holds the entries to delete on the node"""


class Model:
    def __init__(self, mom, system):
        self.mom, self.system = mom, system
        self.mos = OrderedDict()           # key(lower ldn) -> MO dict
        self.by_cls = {}                   # class key -> set(mo keys)
        self.version = 0
        self._mcache = {}
        self.add("", "base")

    def add(self, ldn, origin, created=False):
        k = ldn.lower()
        if k in self.mos:
            return self.mos[k]
        key = self.mom.class_key(ldn)
        mo = {"ldn": ldn, "key": key, "attrs": OrderedDict(), "origin": origin, "created": created, "set": []}
        self.mos[k] = mo
        self.by_cls.setdefault(key, set()).add(k)
        self.version += 1
        cls = ldn.split(",")[-1].split("=")[0] if ldn else "ManagedElement"
        for rel, vals in self.system.get(cls, []):
            child = f"{ldn},{rel}" if ldn else rel
            if SKIP_SYSTEM.match(child):
                continue
            parent = child.rsplit(",", 1)[0] if "," in child else ""
            if parent.lower() not in self.mos:
                # add intermediate system MOs in order
                chain = rel.split(",")
                for n in range(1, len(chain)):
                    p = ",".join(([ldn] if ldn else []) + chain[:n])
                    if p.lower() not in self.mos:
                        self._raw_add(p, "system")
            c = self._raw_add(child, "system")
            for a, v in vals.items():
                info = self.mom.attr(c["key"], a)
                if info:
                    c["attrs"].setdefault(info[0], v)
        return mo

    def _raw_add(self, ldn, origin):
        k = ldn.lower()
        if k not in self.mos:
            key = self.mom.class_key(ldn)
            self.mos[k] = {"ldn": ldn, "key": key, "attrs": OrderedDict(), "origin": origin, "created": False, "set": []}
            self.by_cls.setdefault(key, set()).add(k)
            self.version += 1
        return self.mos[k]

    def delete(self, k):
        sub = [x for x in self.mos if x == k or x.startswith(k + ",")]
        for x in sub:
            mo = self.mos.pop(x)
            self.by_cls.get(mo["key"], set()).discard(x)
        self.version += 1
        return sub

    def match(self, pat, subtree=False, attr=None):
        """moshell MO filter: without 'l' prefix the regex is matched against the MO's RDN, or - if the pattern has a
        comma - against the LDN with the match ending inside the MO's own RDN; l-commands (subtree=True) match the
        full LDN, so children are included."""
        if pat == "0":
            return [""]
        ck = (pat, subtree, attr, self.version)
        if ck in self._mcache:
            return self._mcache[ck]
        p = pat.strip()
        if "," in p and not subtree:
            p = f"(?:{p})[^,]*$"
        try:
            rx = re.compile(p, re.I)
        except re.error:
            rx = re.compile(re.escape(pat.strip()), re.I)
        full = subtree or "," in pat
        if attr:
            keys = set()
            for ck2 in self.mom.classes_with_attr.get(attr.lower(), ()):
                keys |= self.by_cls.get(ck2, set())
            cand = [k for k in self.mos if k and k in keys]
        else:
            cand = [k for k in self.mos if k]
        hit = [k for k in cand if rx.search(self.mos[k]["ldn"] if full else self.mos[k]["ldn"].rsplit(",", 1)[-1])]
        self._mcache[ck] = hit
        return hit

    def resolve(self, raw, ctx=""):
        r = re.sub(r"(?i)^(?:.*?,)?ManagedElement=[^,]*,?", "", raw.strip())
        if not r:
            return ""
        k = r.lower()
        if k in self.mos:
            return self.mos[k]["ldn"]
        cands = [m["ldn"] for x, m in self.mos.items() if x.endswith("," + k)]
        if len(cands) > 1 and ctx:
            top = ctx.split(",")[0].lower()
            same = [c for c in cands if c.lower().startswith(top)]
            cands = same or cands
        return cands[0] if cands else None


# ---------------------------------------------------------------------------------------------------- values
def _enum_map(mom, ref):
    return mom.enums.get(ref) or {}


def convert(mom, model, key, attr_info, raw, ctx):
    """moshell text value -> canonical python value (str | list | dict | Ref). None = empty (unset)."""
    name, t, flags, default = attr_info
    raw = re.sub(r"^\w\[\d+\]\s*=\s*", "", raw.strip())      # moshell array display form: i[2] = 2 1
    if raw == "":
        return None
    seq, kind, ref = _kind(t)
    if seq:
        if kind == "structRef":
            elems = [e for e in raw.split(";") if e.strip()]
        elif kind == "moRef":
            elems = raw.split()
        else:
            elems = [e for e in re.split(r"[\s,]+", raw) if e]
        return [_scalar(mom, model, kind, ref, e, ctx) for e in elems]
    return _scalar(mom, model, kind, ref, raw, ctx)


def _scalar(mom, model, kind, ref, raw, ctx):
    raw = raw.strip().strip('"')
    if kind == "enumRef":
        em = _enum_map(mom, ref)
        if re.fullmatch(r"-?\d+", raw) and int(raw) in em:
            return em[int(raw)]
        up = raw.upper()
        for v in em.values():
            if v.upper() == up:
                return v
        return raw
    if kind == "boolean":
        return {"1": "true", "0": "false", "true": "true", "false": "false"}.get(raw.lower(), raw)
    if kind == "moRef":
        return Ref(raw, ctx)
    if kind == "structRef":
        skey = ref
        members = mom.attrs.get(skey, {})
        low = {m.lower(): m for m in members}
        out, cur = OrderedDict(), None
        for tok in raw.split(","):
            k = tok.split("=", 1)[0].strip().lower()
            if "=" in tok and k in low:
                cur = low[k]
                out[cur] = tok.split("=", 1)[1]
            elif cur:
                out[cur] += "," + tok
        res = OrderedDict()
        for m, v in out.items():
            mt, mf, md = members[m]
            mseq, mk, mr = _kind(mt)
            if mseq:
                res[m] = [_scalar(mom, model, mk, mr, x, ctx) for x in (v.split() if mk == "moRef" else re.split(r"[\s,]+", v.strip())) if x]
            else:
                res[m] = _scalar(mom, model, mk, mr, v, ctx)
        return res
    return raw


def display(mom, attr_info, v):
    """canonical -> moshell-like text (enum as number) for get / ma / if"""
    if v is None:
        return ""
    if isinstance(v, list):
        return " ".join(display(mom, attr_info, x) for x in v)
    if isinstance(v, dict):
        return ",".join(f"{k}={display(mom, None, x)}" for k, x in v.items())
    if isinstance(v, Ref):
        return v.raw
    if attr_info:
        seq, kind, ref = _kind(attr_info[1])
        if kind == "enumRef":
            for n, name in _enum_map(mom, ref).items():
                if name == v:
                    return str(n)
    return str(v)


# ---------------------------------------------------------------------------------------------------- XML input
class _N:
    __slots__ = ("tag", "attrs", "children", "text")

    def __init__(self, tag, attrs):
        self.tag, self.attrs, self.children, self.text = tag, attrs, [], ""


def load_netconf(model, text, origin, as_script=False, events=None, step=""):
    """apply NETCONF edit-config RPCs to the model (initial state or a script step).
    -> attributes of a script step that the node MOM does not accept [(ldn, attr, reason)]"""
    dropped = []
    for chunk in text.replace("\r\n", "\n").split("]]>]]>"):
        if "<rpc" not in chunk or "edit-config" not in chunk:
            continue
        chunk = chunk[chunk.index("<rpc"):]
        st, top = [], []
        p = xml.parsers.expat.ParserCreate()

        def se(t, a, st=st, top=top):
            n = _N(t, a)
            (st[-1].children if st else top).append(n)
            st.append(n)

        p.StartElementHandler = se
        p.EndElementHandler = lambda t, st=st: st.pop()
        p.CharacterDataHandler = lambda d, st=st: st and setattr(st[-1], "text", st[-1].text + d)
        p.Parse(chunk, True)

        def idc(n):
            want = n.tag[0].lower() + n.tag[1:] + "Id"
            return next((c for c in n.children if c.tag == want and not c.children), None)

        def walk(n, path, creating):
            op = n.attrs.get("xc:operation")
            creating = creating or op == "create"
            i = idc(n)
            if i is None:
                for c in n.children:
                    walk(c, path, creating)
                return
            if n.tag != "ManagedElement":
                path = path + [f"{n.tag}={i.text.strip()}"]
            ldn = ",".join(path)
            if op == "delete":
                model.delete(ldn.lower())
                return
            existed = ldn.lower() in model.mos
            mo = model.add(ldn, origin, created=as_script and creating and not existed)
            if as_script and creating and not existed:
                mo["created"] = True
            new_here = as_script and mo["created"] and not existed
            vals = OrderedDict()
            for c in n.children:
                if c is i or idc(c) is not None:
                    continue
                vals.setdefault(c.tag, []).append(_xml_value(c, ldn))
            for a, lst in vals.items():
                info = model.mom.attr(mo["key"], a)
                if as_script and (info is None or "readOnly" in info[2]):
                    dropped.append((ldn, a, "not in the node MOM" if info is None else "read-only"))
                    continue
                name = info[0] if info else a
                seq = bool(info) and _kind(info[1])[0]
                mo["attrs"][name] = lst if (seq or len(lst) > 1) else lst[0]
                if as_script and name not in mo["set"]:
                    mo["set"].append(name)
                if events is not None and not new_here:
                    events.append(("set", ldn.lower(), step, name))
            if new_here:
                mo["create_attrs"] = OrderedDict((a, mo["attrs"][a]) for a in mo["set"] if a in mo["attrs"])
                if events is not None:
                    events.append(("cr", ldn.lower(), step, None))
            for c in n.children:
                if idc(c) is not None:
                    walk(c, path, creating)

        for r in top:
            walk(r, [], False)
    return dropped


def _xml_value(n, ctx):
    if n.children:
        out = OrderedDict()
        for m in n.children:
            v = m.text.strip()
            v = Ref(v, ctx) if v.startswith("ManagedElement=") else v
            if m.tag in out:
                out[m.tag] = (out[m.tag] if isinstance(out[m.tag], list) else [out[m.tag]]) + [v]
            else:
                out[m.tag] = v
        return out
    v = n.text.strip()
    return Ref(v, ctx) if v.startswith("ManagedElement=") else v


# ---------------------------------------------------------------------------------------------------- replay
KEYW = re.compile(r"^(l?set[im]?|l?cr|crn|for|done|func|endfunc|if|fi|else|elseif|l?pr|ma|mr|wait|lt|del|rdel|l?bl|l?deb|st|lst|l?get|acc|unset|rbs|cvms|cvcu|scw|l|y|return|end|\$\S+|/cm/\S+|ld|print|!.*)\b|^(confbd?|gs)[+-]$", re.I)


class Replay:
    def __init__(self, model):
        self.m, self.mom = model, model.mom
        self.vars, self.groups, self.funcs = {}, {}, {}
        self.nr = 0
        self.leftover, self.notes = [], []
        self.deleted_existing = OrderedDict()
        self.events = []          # (kind "cr"|"mod"|"del", key, step) in script execution order
        self.step = ""
        self.only_changes = set()  # steps whose sets are written only if they change the value (07 VoNR on top of 04-06)
        self.created_in = {}       # key -> step of its crn/cr

    # ------------------------------------------------ helpers
    def subst(self, s):
        s = re.sub(r"\$(\w+)\[\$(\w+)\]", lambda m: str(self.vars.get(f"${m.group(1)}[{self.vars.get('$' + m.group(2), '')}]", m.group(0))), s)

        def rep(m):
            v = self.vars.get(m.group(0))
            return m.group(0) if v is None or v is UNKNOWN else str(v)
        return re.sub(r"\$\w+(?!\w)", rep, s)

    def unknown_in(self, s):
        return any(self.vars.get(v) is UNKNOWN for v in re.findall(r"\$\w+(?!\w)", s))

    def left(self, script, ln, s, why):
        self.leftover.append((script, ln, s.strip(), why))

    def set_attr(self, k, attr, raw, script, ln, s, creating=False):
        mo = self.m.mos.get(k)
        if mo is None:
            return False
        info = self.mom.attr(mo["key"], attr)
        if info is None:
            return False
        name, t, flags, d = info
        if "readOnly" in flags:
            self.notes.append((script, ln, s, f"{name} is read-only - ignored"))
            return True
        if "restricted" in flags and not creating:
            self.left(script, ln, s, f"{name} is restricted (only settable when the MO is created) - AMOS set fails too")
            return True
        if "EricssonOnly" in flags:
            self.left(script, ln, s, f"{name} is EricssonOnly - not settable over NETCONF")
            return True
        v = convert(self.mom, self.m, mo["key"], info, raw, mo["ldn"])
        if isinstance(v, dict):
            v = self.whole_struct(mo, info, v)
        elif isinstance(v, list) and v and all(isinstance(x, dict) for x in v):
            v = self.whole_struct_list(mo, info, v)
        bad = self.bad_ref(v)
        if bad:
            self.notes.append((script, ln, s, f"reference target {bad} does not exist at this point - fails in AMOS too"))
            return "badref"
        if not creating and self.step in self.only_changes:
            if "key" in flags:
                self.notes.append((script, ln, s, f"{name} is the MO key - AMOS set fails too, ignored"))
                return True
            old = mo["attrs"].get(name)
            if name not in mo["attrs"] and mo["origin"] == "script" and d is not None:
                old = convert(self.mom, self.m, mo["key"], info, d, mo["ldn"])     # MO made by the scripts: MOM default
            if v is None:
                if self.created_in.get(k) == self.step:     # created in this step: leave it out of the create
                    for dct in (mo["attrs"], mo.get("create_attrs") or {}):
                        dct.pop(name, None)
                    if name in mo["set"]:
                        mo["set"].remove(name)
                elif isinstance(old, list) and not isinstance(old, Cleared) and old:
                    mo["attrs"][name] = Cleared(old)
                    if name not in mo["set"]:
                        mo["set"].append(name)
                    self.events.append(("set", k, self.step, name))
                return True
            if self.canon(old) == self.canon(v):
                return True
        if v is None:
            if name in mo["attrs"] and name in mo["set"]:
                mo["attrs"].pop(name)
                mo["set"].remove(name)
            return True
        if name in mo["attrs"]:
            mo.setdefault("prev", {})[name] = mo["attrs"][name]       # for _node_rules: a rejected set keeps the value before
        mo["attrs"][name] = v
        if name not in mo["set"]:
            mo["set"].append(name)
        if not creating:
            self.events.append(("set", k, self.step, name))
        return True

    def canon(self, v):
        """comparable form of a value (moRefs by the MO they point to)"""
        if isinstance(v, Cleared):
            return ()
        if isinstance(v, dict):
            return tuple((m, self.canon(x)) for m, x in v.items())
        if isinstance(v, list):
            return tuple(self.canon(x) for x in v)
        if isinstance(v, Ref):
            r = self.m.resolve(v.raw, v.ctx)
            return ("ref", (r or v.raw).lower())
        return v

    def whole_struct(self, mo, info, v, cur=None):
        """moshell 'set X struct a=1' keeps the other members; NETCONF needs the whole struct (else 'Multiplicity
        violation'): missing members come from the current value, else the MOM default, else empty (as the node
        shows them, e.g. NRCellDU csiRsConfig16P i11Restriction / i12Restriction - HSN143-1 NR02 failed without)"""
        members = self.mom.attrs.get(_kind(info[1])[2], {})
        if cur is None:
            cur = mo["attrs"].get(info[0])
        cur = cur if isinstance(cur, dict) else {}
        out = OrderedDict()
        for m, (mt, mf, md) in members.items():
            mseq, mk, mr = _kind(mt)
            if m in v:
                out[m] = v[m]
            elif m in cur:
                out[m] = cur[m]
            elif md is not None and not mseq:
                out[m] = _scalar(self.mom, self.m, mk, mr, md, mo["ldn"])
            elif not mseq and mk in ("string", "derivedRef"):
                out[m] = ""
        out.update((m, x) for m, x in v.items() if m not in out)
        return out

    def whole_struct_list(self, mo, info, v):
        """sequence of structs: 'set X structs a=1' on a list the MO has (04 LTE cells: qciA1A2ThrOffsetsEndc for
        qci1/6/9 with their qciProfileRef) changes that member in every entry (one struct given) or entry by entry;
        an entry without its moRef member is rejected by the node (HSN143-1 NR02 'Multiplicity violation qciProfileRef')"""
        cur = mo["attrs"].get(info[0])
        cur = [c for c in cur if isinstance(c, dict)] if isinstance(cur, list) else []
        if not cur:
            return [self.whole_struct(mo, info, x, {}) for x in v]
        if len(v) == 1:
            return [self.whole_struct(mo, info, v[0], c) for c in cur]
        return [self.whole_struct(mo, info, x, cur[i] if i < len(cur) else {}) for i, x in enumerate(v)]

    def soft(self, ldn):
        """MO the node may already have created itself (system id 1/Default/Base, nothing mandatory or restricted,
        e.g. GNBCUCPFunction=1,IntraFreqMC=1 / Mcfb=1, Mcpc=1,McpcPSCellProfile=Default, CpriLinkSupervision=1):
        written as merge instead of create, which works whether or not the node has it"""
        key = self.mom.class_key(ldn)
        cls, _, idv = ldn.rsplit(",", 1)[-1].partition("=")
        if not key or idv not in SYSTEM_IDS or cls in NOT_SOFT:
            return False
        return not any(("mandatory" in fl or "restricted" in fl) and "key" not in fl for t, fl, d in self.mom.attrs[key].values())

    def bad_ref(self, v):
        """first moRef in a value whose target MO does not exist in the model now"""
        vals = v if isinstance(v, list) else [v]
        for x in vals:
            if isinstance(x, dict):
                r = self.bad_ref(list(x.values()))
                if r:
                    return r
            elif isinstance(x, Ref) and x.raw.strip() and self.m.resolve(x.raw, x.ctx) is None:
                return x.raw
        return None

    def created_done(self, k):
        mo = self.m.mos[k]
        mo["create_attrs"] = OrderedDict((a, mo["attrs"][a]) for a in mo["set"] if a in mo["attrs"])
        self.events.append(("cr", k, self.step, None))
        self.created_in[k] = self.step

    def undo_create(self, k):
        self.m.delete(k)
        self.events = [e for e in self.events if not (e[1] == k or e[1].startswith(k + ","))]

    def value_of(self, k, attr):
        mo = self.m.mos[k]
        info = self.mom.attr(mo["key"], attr)
        if info is None:
            return None
        if info[0] in mo["attrs"]:
            return display(self.mom, info, mo["attrs"][info[0]])
        if info[0].lower().startswith("used"):
            base = self.mom.attr(mo["key"], info[0][4:])
            if base and base[0] in mo["attrs"]:
                return re.sub(r"/\d+$", "", display(self.mom, base, mo["attrs"][base[0]]))
        return info[3] if info[3] is not None else ""

    def cond(self, c):
        c = c.strip()
        if "||" in c:
            parts = [self.cond(x) for x in c.split("||")]
            return UNKNOWN if UNKNOWN in parts and True not in parts else any(p is True for p in parts)
        if "&&" in c:
            parts = [self.cond(x) for x in c.split("&&")]
            return UNKNOWN if UNKNOWN in parts and False not in parts else all(p is True for p in parts)
        if self.unknown_in(c):
            return UNKNOWN
        c = self.subst(c)
        m = re.match(r"^(\S+)\s*(!=|=|>=|<=|>|<|!~|~)\s*(.*?)\s*$", c)
        if not m:
            return UNKNOWN
        a, op, b = m.groups()
        if a == "$nr_of_mos":
            a = str(self.nr)
        if a.startswith("$") or b.startswith("$"):
            return UNKNOWN
        if op in ("~", "!~"):
            r = bool(re.search(b, a))
            return r if op == "~" else not r
        try:
            x, y = float(a), float(b)
        except ValueError:
            x, y = a, b
            if op not in ("=", "!="):
                return UNKNOWN
        return {"=": x == y, "!=": x != y, ">": x > y, "<": x < y, ">=": x >= y, "<=": x <= y}[op]

    def parent_exists(self, ldn):
        return "," not in ldn or ldn.rsplit(",", 1)[0].lower() in self.m.mos

    def full_ldn(self, ldn):
        """moshell accepts short LDNs (Router=LTE_NR,DnsClient=1) and any class-name case"""
        parts = ldn.split(",")
        parent = ",".join(parts[:-1])
        if parent and parent.lower() not in self.m.mos:
            r = self.m.resolve(parent)
            if r:
                parent = r
        elif parent:
            parent = self.m.mos[parent.lower()]["ldn"]
        c, _, i = parts[-1].partition("=")
        key = self.mom.class_key(f"{parent},{c}=x" if parent else f"{c}=x")
        if key:
            c = key.split(".", 1)[1]
        return f"{parent},{c}={i}" if parent else f"{c}={i}"

    # ------------------------------------------------ main loop
    def run(self, lines, script):
        i = 0
        while i < len(lines):
            ln, raw = lines[i]
            i += 1
            s = raw.strip()
            if not s or s.startswith("#"):
                continue
            s = re.sub(r"\s+#.*$", "", s)
            low = s.lower()
            w = low.split()[0]
            if w == "func":
                body = []
                while i < len(lines) and not lines[i][1].strip().lower().startswith("endfunc"):
                    body.append(lines[i])
                    i += 1
                i += 1
                self.funcs[s.split()[1].lower()] = body
                continue
            if w == "for":
                depth, body = 1, []
                while i < len(lines):
                    t = lines[i][1].strip().lower()
                    if re.match(r"^for\b", t):
                        depth += 1
                    if re.match(r"^done\b", t):
                        depth -= 1
                        if depth == 0:
                            break
                    body.append(lines[i])
                    i += 1
                i += 1
                m = re.match(r"^for\s+(\$\w+)\s*=\s*(\S+)\s+to\s+(\S+)", s, re.I)
                if m:
                    for v in range(int(self.subst(m.group(2))), int(self.subst(m.group(3))) + 1):
                        self.vars[m.group(1)] = v
                        self.run(body, script)
                    continue
                m = re.match(r"^for\s+(\$\w+)\s+in\s+(\S+)", s, re.I)
                if m:
                    for k in list(self.groups.get(self.subst(m.group(2)).lower(), [])):
                        if k in self.m.mos:
                            self.vars[m.group(1)] = self.m.mos[k]["ldn"]
                            self.run(body, script)
                    continue
                self.left(script, ln, s, "for-loop form not understood")
                continue
            if w == "if":
                branches, cur, depth = [], [s[2:].strip(), []], 1
                block = [(ln, raw)]
                while i < len(lines):
                    t = lines[i][1].strip()
                    tl = t.lower()
                    block.append(lines[i])
                    if re.match(r"^if\b", tl):
                        depth += 1
                    elif re.match(r"^fi\b", tl):
                        depth -= 1
                        if depth == 0:
                            break
                    if depth == 1 and re.match(r"^elseif\b", tl):
                        branches.append(cur)
                        cur = [t[6:].strip(), []]
                    elif depth == 1 and re.match(r"^else\b", tl):
                        branches.append(cur)
                        cur = [None, []]
                    else:
                        cur[1].append(lines[i])
                    i += 1
                i += 1
                branches.append(cur)
                for c, body in branches:
                    r = True if c is None else self.cond(c)
                    if r is UNKNOWN:
                        for bl, bt in block:
                            if bt.strip() and not bt.strip().startswith("#"):
                                self.left(script, bl, bt, "condition depends on a value only known on the live node")
                        break
                    if r:
                        self.run(body, script)
                        break
                continue
            if w in self.funcs and len(s.split()) == 1:
                self.run(self.funcs[w], script)
                continue
            m = re.match(r"^(\$[\w\[\]]+)\s*=\s*(.+)$", s)
            if m:
                v = m.group(2).strip()
                if "`" in v or re.search(r"\$(currentUP|nodename|moshell|date)\b", v) or self.unknown_in(v):
                    self.vars[m.group(1)] = UNKNOWN
                    continue
                v = self.subst(v)
                mm = re.match(r"^rdn\((.+)\)$", v)
                if mm:
                    v = mm.group(1).split(",")[-1]
                mm = re.match(r"^(.*?)\s+-s\s+(\S+)\s+-r\s*(\S*)$", v)       # moshell string substitution
                if mm:
                    v = mm.group(1).replace(mm.group(2), mm.group(3))
                self.vars[m.group(1)] = v
                continue
            if w in ("scw", "acc", "cvms", "cvcu") or w.startswith("/cm/") or w.startswith("!"):
                self.left(script, ln, s, {"scw": "hidden parameter (scw)", "cvms": "CV backup", "acc": "MO action", "cvcu": "CV/UP check"}.get(w, "system command"))
                continue
            mg = re.match(r"^l?get\s+(.+?)\s*>\s*(\$\w+)\s*$", s, re.I)
            if mg and not self.unknown_in(mg.group(1)):
                s = "get " + self.subst(mg.group(1)) + " > " + mg.group(2)
            elif self.unknown_in(s):
                self.left(script, ln, s, "uses a value only known on the live node")
                continue
            else:
                s = self.subst(s)
            low = s.lower()
            if w == "crn":
                ldn = self.full_ldn(s.split()[1])
                attrs = []
                unknown = []
                while i < len(lines) and lines[i][1].strip().lower() != "end":
                    t = re.sub(r"\s+#.*$", "", lines[i][1].strip())
                    if t and not t.startswith("#"):
                        if self.unknown_in(t):          # e.g. ipv6Address $reqip from a 'get' that found nothing
                            unknown.append((lines[i][0], t))
                        else:
                            p = self.subst(t).split(None, 1)
                            attrs.append((lines[i][0], p[0], p[1].strip() if len(p) > 1 else ""))
                    i += 1
                i += 1
                if not self.parent_exists(ldn):
                    self.notes.append((script, ln, f"crn {ldn}", "parent MO does not exist - crn fails in AMOS too, skipped"))
                    continue
                if self.mom.class_key(ldn) is None:
                    self.left(script, ln, f"crn {ldn}", "MO class not in the node MOM - crn fails in AMOS too, skipped")
                    continue
                key = self.mom.class_key(ldn)
                needed = [t for _, t in unknown if (self.mom.attr(key, t.split()[0]) or (0, 0, set()))[2] & {"mandatory", "restricted"}]
                for aln, t in unknown:
                    self.left(script, aln, f"crn {ldn}: {t}", "uses a value only known on the live node" +
                              (" - MO not created" if needed else " - attribute left out"))
                if needed:
                    continue
                if ldn.lower() in self.m.mos:
                    if self.soft(ldn):          # the node made it itself: crn fails in AMOS, its values become sets here
                        for aln, a, v in attrs:
                            if v:
                                self.set_attr(ldn.lower(), a, v, script, aln, f"crn {ldn}: {a} {v}")
                        continue
                    self.notes.append((script, ln, f"crn {ldn}", "MO already exists - crn fails in AMOS, its attributes are not applied"))
                    continue
                self.m.add(ldn, "script", created=True)["soft"] = self.soft(ldn)
                failed = False
                for aln, a, v in attrs:
                    r = self.set_attr(ldn.lower(), a, v, script, aln, f"crn {ldn}: {a} {v}", creating=True) if v else True
                    if r == "badref":
                        failed = True
                        break
                    if not r:
                        self.notes.append((script, aln, f"crn {ldn}: {a} {v}", "attribute not in MOM - ignored"))
                if failed:                      # moshell crn fails as a whole -> MO not created
                    self.undo_create(ldn.lower())
                else:
                    self.created_done(ldn.lower())
                continue
            if w == "cr":
                ldn = self.full_ldn(s.split()[1])
                args = []
                while i < len(lines):
                    t = re.sub(r"\s+#.*$", "", lines[i][1].strip())
                    if not t or t.startswith("#") or (KEYW.match(t) and not re.match(r"^\$\w+$", t)) or t.lower().split()[0] in self.funcs:
                        break
                    args.append(self.subst(t))
                    i += 1
                if not self.parent_exists(ldn):
                    self.notes.append((script, ln, s, "parent MO does not exist - cr fails in AMOS too, skipped"))
                    continue
                if self.mom.class_key(ldn) is None:
                    self.left(script, ln, s, "MO class not in the node MOM - cr fails in AMOS too, skipped")
                    continue
                if ldn.lower() in self.m.mos:
                    self.notes.append((script, ln, s, "MO already exists - cr fails (harmless)"))
                    continue
                mo = self.m.add(ldn, "script", created=True)
                mo["soft"] = self.soft(ldn)
                if any(self.set_attr(ldn.lower(), a, v, script, ln, s, creating=True) == "badref" for a, v in zip(self.mom.prompts(mo["key"]), args)):
                    self.undo_create(ldn.lower())
                else:
                    self.created_done(ldn.lower())
                continue
            m = re.match(r"^(l?set[i]?)\s+(\S+)\s+(\S+)\s*(.*)$", s, re.I)
            if m and m.group(1).lower() in ("set", "lset", "seti"):
                kind, pat, attr, val = m.group(1).lower(), m.group(2), m.group(3), m.group(4).strip()
                keys = self.m.match(pat, subtree=kind == "lset", attr=attr)
                hit = False
                for k in keys:
                    hit = self.set_attr(k, attr, val, script, ln, s) or hit
                if not hit:
                    self.notes.append((script, ln, s, "no MO on the node has this MO pattern + attribute - no-op"))
                continue
            m = re.match(r"^setm\s+(\S+)\s+(.+)$", s, re.I)
            if m:
                toks = m.group(2).split()
                for a, v in zip(toks[::2], toks[1::2]):
                    for k in self.m.match(m.group(1), attr=a):
                        self.set_attr(k, a, v, script, ln, s)
                continue
            m = re.match(r"^(l?)(bl|deb)\s+(\S+)", s, re.I)
            if m:
                for k in self.m.match(m.group(3), subtree=bool(m.group(1)), attr=None if m.group(1) else "administrativeState"):
                    mo = self.m.mos[k]
                    if self.mom.attr(mo["key"], "administrativeState"):
                        self.set_attr(k, "administrativeState", "0" if m.group(2).lower() == "bl" else "1", script, ln, s)
                continue
            m = re.match(r"^([rl]?del)\s+(\S+)", s, re.I)
            if m:
                for k in self.m.match(m.group(2)):
                    mo = self.m.mos.get(k)
                    if mo is None:
                        continue
                    if mo["origin"] != "script" and k not in self.deleted_existing:
                        self.deleted_existing[k] = (mo["ldn"], script, ln, s)
                        self.events.append(("del", k, self.step, None))
                    self.m.delete(k)
                continue
            m = re.match(r"^(l?pr|st|lst)\s+(\S+)", s, re.I)
            if m:
                self.nr = len(self.m.match(m.group(2)))
                continue
            m = re.match(r"^l?get\s+(\S+)\s+(\S+)(?:\s+(\S+))?\s*(?:>\s*(\$\w+))?\s*$", s, re.I)
            if m:
                keys = self.m.match(m.group(1))
                arx = re.compile(m.group(2), re.I)
                val = None
                for k in keys:
                    mo = self.m.mos[k]
                    for a in self.mom.attrs.get(mo["key"], {}):
                        if arx.search(a):
                            val = self.value_of(k, a)
                            break
                    if val is not None:
                        break
                self.nr = len(keys)
                if m.group(4):
                    self.vars[m.group(4)] = val if val is not None else UNKNOWN
                continue
            m = re.match(r"^ma\s+(\S+)\s+(\S+)(?:\s+(\S+)\s+(.+))?$", s, re.I)
            if m:
                keys = self.m.match(m.group(2))
                if m.group(3):
                    arx, vrx = re.compile(m.group(3), re.I), re.compile(m.group(4).strip(), re.I)
                    keys = [k for k in keys if any(arx.search(a) and vrx.search(self.value_of(k, a) or "")
                                                   for a in self.mom.attrs.get(self.m.mos[k]["key"], {}))]
                g = self.groups.setdefault(m.group(1).lower(), [])
                g += [k for k in keys if k not in g]
                self.nr = len(keys)
                continue
            if w == "mr":
                self.groups.pop(s.split()[1].lower(), None)
                continue
            if w == "unset":
                if "all" in low:
                    self.vars = {k: v for k, v in self.vars.items() if k.startswith("$Par")}
                continue
            if w in ("scw", "acc", "cvms", "cvcu") or w.startswith("/cm/") or w.startswith("!"):
                self.left(script, ln, s, {"scw": "hidden parameter (scw)", "cvms": "CV backup", "acc": "MO action", "cvcu": "CV/UP check"}.get(w, "system command"))
                continue
            if re.match(r"^(confbd?[+-]|gs[+-])$", low) or re.match(r"^(lt|l|y|return|get|lget|hget|ld|print|end|rbs|wait|st|lst)\b", low) or low.startswith("//"):
                continue
            self.left(script, ln, s, "command not interpreted")


# ---------------------------------------------------------------------------------------------------- XML output
def _render(model, node, mo, name, v):
    if isinstance(v, Cleared):          # emptied sequence: delete the attribute (the node refuses deletes of single entries)
        return f'<{name} xc:operation="delete"/>'
    if isinstance(v, list):
        return "".join(_render(model, node, mo, name, x) for x in v)
    if isinstance(v, dict):
        inner = "".join(_render(model, node, mo, m, x) for m, x in v.items())
        return f"<{name}>{inner}</{name}>"
    if isinstance(v, Ref):
        r = model.resolve(v.raw, v.ctx)
        text = f"ManagedElement={node},{r}" if r is not None else v.raw
        return f"<{name}>{escape(text)}</{name}>"
    return f"<{name}>{escape(str(v))}</{name}>"


def _step_id(step):
    """RPC id prefix: NR steps '01'..'06RIM' -> NR01.., named steps ('LTE01') as they are"""
    return f"NR{step}" if step[:1].isdigit() else step


def emit(model, node, events, deleted_existing, pull_back=None):
    """RPCs in script execution order (like running 01..06 in AMOS):
    - an MO is created where its crn/cr (or XML create) is, with the values given at creation
    - every later change is placed where the script changes that attribute for the last time (final value)
    A new RPC starts when the script step or the top branch changes, or when an item depends on an MO created in the
    current RPC through an MO the node creates itself (that one exists only after the RPC is committed).
    Node behaviour that AMOS hides by running one command at a time:
    - an MO created UNLOCKED is created LOCKED and unlocked by a later change (a cell rejects e.g. bSChannelBwDL/UL
      of its sector carrier in the transaction that unlocks it)
    - attributes validated together (DscpPcpMap pcp0..7 must not overlap) are written together
    - the node creates the children of a new MO (UeCfg=Base ...) in its own transaction just after the create; changes
      to such children go to the end of the script step instead of the next RPC, which would collide with it
      (creates stay in place: later items may reference them)
    - one RPC per FeatureState: a feature missing in the node's software fails alone"""
    mos = model.mos
    events = list(events)
    unlock = OrderedDict()
    for n, (kind, k, step, a) in enumerate(events):
        if kind == "cr" and k in mos and (mos[k].get("create_attrs") or {}).get("administrativeState") == "UNLOCKED":
            mos[k]["create_attrs"] = OrderedDict(mos[k]["create_attrs"], administrativeState="LOCKED")
            if not any(e[0] == "set" and e[1] == k and e[3] == "administrativeState" for e in events[n + 1:]):
                unlock.setdefault(step, []).append(k)
    for step, keys in unlock.items():
        end = max(n for n, e in enumerate(events) if e[2] == step) + 1
        events[end:end] = [("set", k, step, "administrativeState") for k in keys]
        for k in keys:
            if "administrativeState" not in mos[k]["set"]:
                mos[k]["set"].append("administrativeState")

    def group_rx(k, a):
        rx = GROUPED_ATTRS.get(mos[k]["ldn"].rsplit(",", 1)[-1].split("=")[0]) if k in mos and a else None
        return rx if rx and rx.match(a) else None

    last_cr, last_set = {}, {}
    for n, (kind, k, step, a) in enumerate(events):
        if kind == "cr":
            last_cr[k] = n
        elif kind == "set":
            last_set[(k, group_rx(k, a) or a)] = n
    def targets(v):
        for x in (v if isinstance(v, list) else [v]):
            if isinstance(x, dict):
                yield from targets(list(x.values()))
            elif isinstance(x, Ref):
                t = model.resolve(x.raw, x.ctx)
                if t is not None:
                    yield t.lower()
    # pull_back {later step: earlier step}: an attribute the later step changes last that the earlier step writes too is
    # written where the earlier step writes it, with the final value (KK 06: VoNR values in the RIM part, not twice)
    for later, earlier in (pull_back or {}).items():
        for key, n in list(last_set.items()):
            if events[n][2] != later:
                continue
            k = key[0]
            back = [i for i, e in enumerate(events[:n]) if e[0] == "set" and e[1] == k and e[2] == earlier
                    and (group_rx(k, e[3]) or e[3]) == key[1]]
            vals = [mos[k]["attrs"].get(a) for a in mos[k]["attrs"] if (group_rx(k, a) or a) == key[1]] if k in mos else []
            if back and not any(last_cr.get(t, -1) > back[-1] for v in vals for t in targets(v)):
                last_set[key] = back[-1]
    referenced = {t for mo in mos.values() for d in (mo["attrs"], mo.get("create_attrs") or {}) for v in d.values() for t in targets(v)}

    def build(needed):
        out = []      # (kind, key, step, attr)
        for n, (kind, k, step, a) in enumerate(events):
            if kind == "del":
                out.append(("del", k, step, None))
            elif kind == "cr" and last_cr.get(k) == n and k in mos and mos[k]["created"]:
                if not (mos[k].get("soft") and not mos[k].get("create_attrs")) or k in needed:     # else nothing to write
                    out.append(("cr", k, step, None))
            elif kind == "set" and k in mos and n > last_cr.get(k, -1):
                rx = group_rx(k, a)
                if rx and last_set.get((k, rx)) == n:
                    out += [("set", k, step, b) for b in mos[k]["set"] if rx.match(b) and b in mos[k]["attrs"]]
                elif not rx and last_set.get((k, a)) == n and a in mos[k]["set"] and a in mos[k]["attrs"]:
                    out.append(("set", k, step, a))
        return out

    def written_refs(it):
        kind, k, _, a = it
        if kind == "cr":
            vals = list((mos[k].get("create_attrs") or {}).values())
        elif kind == "set":
            vals = [mos[k]["attrs"].get(a)]
        else:
            vals = []
        return {t for v in vals for t in targets(v)}

    # a soft create without attributes has nothing to write (the MO appears with the edits of itself/its children,
    # or the node has it already) - unless an RPC refers to it before it appears that way: then it is written (merge)
    # where AMOS creates it (McfbCellProfile=1 / DynPowerOpt=1 were referenced before they existed on a fresh node)
    items = build(set())
    needed = set()
    for k in {k for k, mo in mos.items() if mo.get("created") and mo.get("soft") and not mo.get("create_attrs")} & referenced:
        first_ref = next((i for i, it in enumerate(items) if k in written_refs(it)), None)
        first_app = next((i for i, it in enumerate(items) if it[1] == k or it[1].startswith(k + ",")), None)
        if first_ref is not None and (first_app is None or first_ref < first_app):
            needed.add(k)
    if needed:
        items = build(needed)

    def chain(k):
        parts = k.split(",") if k else []
        return [",".join(parts[:n]) for n in range(1, len(parts) + 1)]

    def settling(k, step):
        """k is (below) an MO the node creates itself under an MO created earlier in this step"""
        ch = chain(k)
        new = [i for i, y in enumerate(ch) if y in last_cr and mos.get(y, {}).get("created") and events[last_cr[y]][2] == step]
        return any(x in mos and (mos[x]["origin"] == "system" or mos[x].get("soft")) for x in ch[new[0] + 1:]) if new else False

    ordered, later, cur = [], [], None
    for it in items:
        if it[2] != cur:
            ordered, later, cur = ordered + later, [], it[2]
        # soft create = merge, an edit too - unless other MOs refer to it
        edit = it[0] == "set" or (it[0] == "cr" and mos[it[1]].get("soft") and it[1] not in referenced)
        (later if edit and settling(it[1], it[2]) else ordered).append(it)
    items = ordered + later

    groups = []     # dict(step, top, created=set, attrs={key: [attr...]}, keys=[...]) or dict(del=[keys], step)
    for kind, k, step, a in items:
        if kind == "del":
            groups.append({"del": [k], "step": step})
            continue
        top = k.split(",")[0] if k else ""
        solo = bool(SOLO_CLASSES.search("," + k))
        # an unlock (AMOS deb) is its own transaction in AMOS: keep it apart from the changes before and after it,
        # so a cell is never changed in the transaction that unlocks it
        unl = kind == "set" and a == "administrativeState" and k in mos and mos[k]["attrs"].get("administrativeState") == "UNLOCKED"
        g = groups[-1] if groups and "del" not in groups[-1] else None
        # a solo MO keeps its consecutive changes together, but shares the RPC with nothing else
        brk = (g is None or g["step"] != step or g["top"] != top or (solo or g.get("solo")) and g["keys"] != [k]
               or bool(g.get("unl")) != unl)
        if not brk:
            ch = chain(k)
            inside = [n for n, x in enumerate(ch[:-1]) if x in g["created"]]
            if inside:
                below = ch[inside[0] + 1:]
                if kind == "cr":
                    brk = any(x not in g["created"] for x in below[:-1])
                else:
                    brk = any(x not in g["created"] for x in below)
        if brk:
            g = {"step": step, "top": top, "created": set(), "attrs": OrderedDict(), "keys": [], "solo": solo, "unl": unl}
            groups.append(g)
        if k not in g["attrs"]:
            g["attrs"][k] = []
            g["keys"].append(k)
        if kind == "cr":
            g["created"].add(k)
        elif a not in g["attrs"][k]:
            g["attrs"][k].append(a)

    def values(g, k):
        mo = mos[k]
        out = OrderedDict()
        if k in g["created"]:
            out.update(mo.get("create_attrs", {}))
        for a in g["attrs"][k]:
            out[a] = mo["attrs"][a]
        return out

    # self-check: references must point to MOs existing before the scripts or created in an earlier/same RPC
    rpc_of = {}
    for n, g in enumerate(groups):
        for k in g.get("created", ()):
            rpc_of[k] = n
    order_problems = []

    def refs(v):
        for x in (v if isinstance(v, list) else [v]):
            if isinstance(x, dict):
                yield from refs(list(x.values()))
            elif isinstance(x, Ref):
                yield x
    for n, g in enumerate(groups):
        if "del" in g:
            continue
        for k in g["keys"]:
            for a, v in values(g, k).items():
                for r in refs(v):
                    t = model.resolve(r.raw, r.ctx)
                    if t is not None and rpc_of.get(t.lower(), -1) > n:
                        order_problems.append((mos[k]["ldn"], a, t))

    def element(g, k, need, order):
        mo = mos[k]
        cls, _, idv = mo["ldn"].split(",")[-1].partition("=")
        idtag = cls[0].lower() + cls[1:] + "Id"
        op = ' xc:operation="create"' if k in g["created"] and not mo.get("soft") and not NODE_MADE.search("," + k) else ""     # explicit on every created MO (1 per crn/cr)
        out = [f"<{cls}{op}>", f"<{idtag}>{escape(idv)}</{idtag}>"]
        if k in g["attrs"]:
            out += [_render(model, node, mo, a, v) for a, v in values(g, k).items()]
        kids = sorted((c for c in need if c != k and (c.rsplit(",", 1)[0] if "," in c else "") == k), key=lambda c: order[c])
        for c in kids:
            out.extend(element(g, c, need, order))
        out.append(f"</{cls}>")
        return out

    def rpc(mid, body, root=None):
        return (f'<rpc message-id="{mid}" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
                '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n<target>\n<running/>\n</target>\n'
                '<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">\n<ManagedElement>\n'
                f"<managedElementId>{escape(node)}</managedElementId>\n" + "\n".join((root or []) + body) +
                "\n</ManagedElement>\n</config>\n</edit-config>\n</rpc>\n]]>]]>\n")

    rpcs, count = [], {}
    for g in groups:
        step = g["step"]
        count[step] = count.get(step, 0) + 1
        if "del" in g:
            body = []
            for k in g["del"]:
                parts, tags = deleted_existing[k][0].split(","), []
                for n, p in enumerate(parts):
                    c, _, i = p.partition("=")
                    idtag = c[0].lower() + c[1:] + "Id"
                    op = ' xc:operation="delete"' if n == len(parts) - 1 else ""
                    body.append(f"<{c}{op}><{idtag}>{escape(i)}</{idtag}>")
                    tags.append(c)
                body.append("".join(f"</{c}>" for c in reversed(tags)))
            rpcs.append(rpc(f"{_step_id(step)}_{count[step]:03d}_delete", body))
            continue
        order = {}
        for n, k in enumerate(g["keys"]):
            for x in chain(k):
                order.setdefault(x, n)
        need = {x for k in g["keys"] for x in chain(k)}
        root = [_render(model, node, mos[""], a, v) for a, v in values(g, "").items()] if "" in g["attrs"] else []
        body = []
        for t in sorted({k.split(",")[0] for k in g["keys"] if k}, key=lambda t: order[t]):
            body.extend(element(g, t, need, order))
        name = mos[g["top"]]["ldn"].split("=")[0] if g["top"] else "ManagedElement"
        if g["solo"]:
            name = mos[g["keys"][0]]["ldn"].rsplit(",", 1)[-1].replace("=", "_")
        rpcs.append(rpc(f"{_step_id(step)}_{count[step]:03d}_{name}", body, root))
    return HELLO + "".join(rpcs) + CLOSE, order_problems


# ---------------------------------------------------------------------------------------------------- API
def _system_templates(mom, templates):
    """The reference node was integrated with the same scripts, so its kget also has MOs made by the scripts, the SA
    XMLs or ANR (BWPSet=100, CUCP5qi=5qi1, NRFrequency=629952-30 ...): taking them as system MOs makes the XML set
    MOs that a fresh node does not have. Below the gNodeB functions only the ids the node uses itself are kept."""
    out = {}
    for anchor, lst in templates.items():
        ns = set(mom.by_class.get(anchor.lower(), {}))
        gnb = bool(ns) and ns <= GNB_NS
        out[anchor] = [(r, v) for r, v in lst
                       if (not gnb or all(p.partition("=")[2] in SYSTEM_IDS for p in r.split(",")))
                       and not any(p.partition("=")[0] in NOT_SYSTEM for p in r.split(","))]
    return out


def _node_rules(model, rp):
    """value combinations the node rejects whatever the order (the AMOS set fails as well)"""
    def target(v):
        return (model.resolve(v.raw, v.ctx) or "").lower() if isinstance(v, Ref) else None

    for k, mo in list(model.mos.items()):
        if not (mo["ldn"].rsplit(",", 1)[-1].startswith("NRCellCU=") and mo["attrs"].get("transmitSib4") == "true"
                and "transmitSib4" in mo["set"]):
            continue
        own = target(mo["attrs"].get("nRFrequencyRef"))
        inter = []
        for c, rel in model.mos.items():
            if c.startswith(k + ",nrfreqrelation=") and target(rel["attrs"].get("nRFrequencyRef")) != own:
                default = (model.mom.attr(rel["key"], "cellReselectionPriority") or (None,) * 4)[3]
                inter.append(str(rel["attrs"].get("cellReselectionPriority", default)))
        if not any(p != "-1" for p in inter):
            mo["set"].remove("transmitSib4")
            (mo.get("create_attrs") or {}).pop("transmitSib4", None)
            rp.left("XML", 0, f"{mo['ldn']} transmitSib4 true", "the node rejects it without an inter-frequency NRFreqRelation "
                    "(cellReselectionPriority not -1) under this NRCellCU - AMOS set fails too, left out")

    # NRCellDU srsHoppingBandwidth HALF is rejected with tddSpecialSlotPattern 02, advancedDlSuMimoEnabled false or
    # aperiodicSrsEnabled true (final values; the KK SA script sets HALF, the GPL aperiodicSrsEnabled true): the cell
    # keeps the value it had before
    for k, mo in model.mos.items():
        if not (mo["ldn"].rsplit(",", 1)[-1].startswith("NRCellDU=") and mo["attrs"].get("srsHoppingBandwidth") == "HALF"
                and "srsHoppingBandwidth" in mo["set"]):
            continue
        val = lambda a: str(mo["attrs"].get(a, (model.mom.attr(mo["key"], a) or (None,) * 4)[3]))
        why = [w for w, bad in (("tddSpecialSlotPattern 02", val("tddSpecialSlotPattern") == "TDD_SPECIAL_SLOT_PATTERN_02"),
                                ("advancedDlSuMimoEnabled false", val("advancedDlSuMimoEnabled") == "false"),
                                ("aperiodicSrsEnabled true", val("aperiodicSrsEnabled") == "true")) if bad]
        if not why:
            continue
        prev = mo.get("prev", {}).get("srsHoppingBandwidth")
        if prev is None or prev == "HALF":
            mo["attrs"].pop("srsHoppingBandwidth")
            mo["set"].remove("srsHoppingBandwidth")
        else:
            mo["attrs"]["srsHoppingBandwidth"] = prev
        if (mo.get("create_attrs") or {}).get("srsHoppingBandwidth") == "HALF":
            mo["create_attrs"].pop("srsHoppingBandwidth")
        rp.left("XML", 0, f"{mo['ldn']} srsHoppingBandwidth HALF", f"the node rejects HALF with {', '.join(why)} - "
                "AMOS set fails too, left out")

    # 'set . egressQosMarking' also hits the loopback interfaces (Node_Internal_F1 NR_CUCP/NR_DU): the node rejects it
    # there and the whole RPC with the real interfaces/ports would fail
    for k, mo in model.mos.items():
        if "loopback" in mo["attrs"] and "egressQosMarking" in mo["set"]:
            mo["set"].remove("egressQosMarking")
            (mo.get("create_attrs") or {}).pop("egressQosMarking", None)
            rp.left("XML", 0, f"{mo['ldn']} egressQosMarking", "not allowed on an IP loopback interface - AMOS set fails too, left out")

    # PmFlexCounterFilter: the filter values must be unique per node (the GPL creates ENDC 0-99 = Endc0To99 of
    # 04 LTE_Config and sets endcFilterMin 2 on every ENDC* filter = ENDC2To99). Changes that would duplicate the
    # values of another filter are left out, the filters of 04 LTE_Config stay as they are.
    def combo(mo):
        out = []
        for a, (t, fl, d) in model.mom.attrs.get(mo["key"], {}).items():
            if re.search(r"Filter(Enabled|Min|Max)$", a):
                v = mo["attrs"].get(a)
                if v is None and d is not None:
                    v = convert(model.mom, model, mo["key"], model.mom.attr(mo["key"], a), d, mo["ldn"])
                out.append((a, str(v)))
        return tuple(out)

    filters = [(k, mo) for k, mo in model.mos.items() if mo["ldn"].rsplit(",", 1)[-1].startswith("PmFlexCounterFilter=")]
    changed = lambda mo: any(re.search(r"Filter(Enabled|Min|Max)$", a) for a in mo["set"])
    rank = lambda item: 2 if item[1]["created"] else (1 if changed(item[1]) else 0)
    seen = {}
    for k, mo in sorted(filters, key=rank):
        c = combo(mo)
        if c not in seen:
            seen[c] = mo["ldn"]
            continue
        if mo["created"]:
            rp.undo_create(k)
            rp.left("XML", 0, f"{mo['ldn']} create", f"same filter values as {seen[c]} - the node rejects duplicates "
                    "(AMOS crn fails too), left out")
        else:
            for a in [a for a in mo["set"] if re.search(r"Filter(Enabled|Min|Max)$", a)]:
                mo["set"].remove(a)
                rp.left("XML", 0, f"{mo['ldn']} {a}", f"would give the same filter values as {seen[c]} - the node "
                        "rejects duplicates (AMOS set fails too), left out")


def amos_to_netconf(node, initial_xml, steps, system="KK"):
    """initial_xml: NETCONF texts describing the node before the scripts (commissioning, 04 LTE_Config ...)
    steps: (name, "amos"|"xml", text) in execution order.
    -> (xml_text, leftovers[(script, line, command, reason)], notes[(script, line, command, note)])"""
    return amos_to_netconf_model(node, initial_xml, steps, system)[:3]


# ---------------------------------------------------------------------------------------------------- lock sections
_OWN_LOCK = re.compile(r"^(?:value can only be changed if (?:the )?administrativeState is LOCKED|(?:attribute )?"
                       r"administrativeState must (?:equal|be set to) LOCKED(?: before modifying this attribute)?)\.?$", re.I)
_CELL = re.compile(r"^(?:enodebfunction=[^,]+,eutrancell[ft]dd|gnbdufunction=[^,]+,nrcelldu)=[^,]+$")


def _lock_targets(model, k, pre):
    """model keys of the MOs that must be LOCKED to change MO k (MOM 'Precondition:' text)"""
    mos = model.mos
    if _OWN_LOCK.match(pre):
        return [k]
    if "matching cellLocalId" in pre:              # NRCellCU -> the NRCellDU of the same cell
        cid = str(mos[k]["attrs"].get("cellLocalId", ""))
        same = [c for c in mos if c.startswith("gnbdufunction=") and ",nrcelldu=" in c and _CELL.match(c)
                and cid and str(mos[c]["attrs"].get("cellLocalId", "")) == cid]
        return same or [c for c in mos if _CELL.match(c) and c.rsplit("=", 1)[1] == k.rsplit("=", 1)[1]]
    m = re.search(r"parent (?:main )?(\w+)", pre)
    if m:
        parts = k.split(",")
        for n in range(len(parts) - 1, 0, -1):
            if parts[n - 1].split("=")[0] == m.group(1).lower():
                return [",".join(parts[:n])]
    chain = [",".join(k.split(",")[:n]) for n in range(len(k.split(",")), 0, -1)]
    def points_here(v):
        for x in (v if isinstance(v, list) else [v]):
            if isinstance(x, dict):
                if points_here(list(x.values())):
                    return True
            elif isinstance(x, Ref) and (model.resolve(x.raw, x.ctx) or "").lower() in chain:
                return True
        return False
    cells = [c for c in chain if _CELL.match(c)] or [c for c in mos if _CELL.match(c)
                                                     and any(points_here(v) for v in mos[c]["attrs"].values())]
    return cells or [c for c in mos if _CELL.match(c) and c.split(",")[0] == k.split(",")[0]]


def lock_sections(model, node, text, prefix, all_cells=True):
    """Cell Lock RPCs before and Cell Unlock RPCs after the RPCs in text (one XML file): every NR cell (NRCellDU) plus
    any other MO a change in text needs LOCKED (MOM 'Precondition:' of 25.Q2, e.g. NRCellDU sibType2 /
    secondaryCellOnly, NRCellCU transmitSib2 -> its NRCellDU) - a cell unlocked on the node made these RPCs fail
    (BGR583). Locking a LOCKED MO does nothing. MOs created in the file are left alone (created LOCKED by the XML).
    NRCellDU unlocks inside text (06 RIM deb) are taken out: the cells are unlocked only at the end.
    all_cells=False (07 VoNR on a site in service): only the MOs a change needs LOCKED, nothing if none.
    -> (lock_text, text, unlock_text)"""
    pre_all = _load(MOM_FILES.get(getattr(model, "circle", "KK"), MOM_DEFAULT)[1])
    mom, mos = model.mom, model.mos
    created, need, last_change, unlocked_at = set(), OrderedDict(), {}, {}
    for c in mos:
        if all_cells and _CELL.match(c) and c.startswith("gnbdufunction="):
            need[c] = "NR cell lock section"
            last_change[c] = -1
    for n, (mid, body) in enumerate(re.findall(r'<rpc message-id="([^"]+)"(.*?)</rpc>', text, re.S)):
        stack, struct = [], 0
        for tok in re.finditer(r"<(/?)([A-Za-z][\w-]*)((?:\s[^>]*)?)>(?:([^<]*)</\2>)?", body):
            close, tag, extra, val = tok.groups()
            if tag in ("edit-config", "target", "running", "config", "ManagedElement", "managedElementId"):
                continue
            if tag[0].isupper():
                if close:
                    stack.pop()
                elif val is None:
                    stack.append([tag, None, "create" in (extra or "")])
                continue
            if close:
                struct -= 1                       # end of a struct attribute
                continue
            if struct:                            # struct member
                struct += val is None
                continue
            if not stack:
                continue
            if val is None:
                struct += 1                       # struct attribute: <sibType2><siPeriodicity>..
            elif stack[-1][1] is None and tag.lower() == stack[-1][0].lower() + "id":
                stack[-1][1] = val
                if stack[-1][2]:
                    created.add(",".join(f"{c}={i}" for c, i, _ in stack).lower())
                continue
            k = ",".join(f"{c}={i}" for c, i, _ in stack).lower()
            if tag == "administrativeState":
                if val == "UNLOCKED":
                    unlocked_at[k] = n
                continue
            if k in created or k not in mos:
                continue
            p = pre_all.get(mom.class_key(mos[k]["ldn"]) or "", {}).get(tag)
            if not p:
                continue
            for t in _lock_targets(model, k, p):
                if t in mos and t not in created and mom.attr(mos[t]["key"], "administrativeState"):
                    if need.get(t, "NR cell lock section") == "NR cell lock section":
                        need[t] = f"{mos[k]['ldn']} {tag}: {p}"
                    last_change[t] = n
    for t in [t for t in need if t in created]:
        del need[t]
    if not need:
        return "", text, ""
    # NRCellDU unlocks inside the file move to the Cell Unlock section
    text = re.sub(r"(<NRCellDU>\s*<nRCellDUId>[^<]*</nRCellDUId>)\s*<administrativeState>UNLOCKED</administrativeState>",
                  r"\1", text)
    order = sorted(need, key=lambda t: 0 if _CELL.match(t) else 1)       # cells first, unlock the other way round

    def rpc(mid, t, state):
        parts = mos[t]["ldn"].split(",")
        body = "".join(f"<{c}><{c[0].lower() + c[1:]}Id>{escape(i)}</{c[0].lower() + c[1:]}Id>"
                       for c, _, i in (p.partition("=") for p in parts))
        body += f"<administrativeState>{state}</administrativeState>" + "".join(f"</{p.partition('=')[0]}>" for p in reversed(parts))
        return (f'<rpc message-id="{mid}" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n'
                '<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n<target>\n<running/>\n</target>\n'
                '<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">\n<ManagedElement>\n'
                f"<managedElementId>{escape(node)}</managedElementId>\n{body}\n</ManagedElement>\n</config>\n</edit-config>\n"
                "</rpc>\n]]>]]>\n")
    cls = lambda t: mos[t]["ldn"].rsplit(",", 1)[-1].split("=")[0]
    lock = "<!-- #####Start: Cell Lock ####### -->\n"
    for n, t in enumerate(order, 1):
        lock += f"<!-- needed for {need[t].replace('--', '- -')} -->\n" + rpc(f"{prefix}_Lock_{n:03d}_{cls(t)}", t, "LOCKED")
    lock += "<!-- #####end: Cell Lock ####### -->\n"
    todo = [t for t in reversed(order) if _CELL.match(t) or unlocked_at.get(t, -1) < last_change[t]]
    unlock = "<!-- #####Start: Cell Unlock ####### -->\n"
    unlock += "".join(rpc(f"{prefix}_Unlock_{n:03d}_{cls(t)}", t, "UNLOCKED") for n, t in enumerate(todo, 1))
    unlock += "<!-- #####end: Cell Unlock ####### -->\n"
    return lock, text, unlock


def amos_to_netconf_model(node, initial_xml, steps, system="KK", only_changes=(), pull_back=None):
    """amos_to_netconf + the final model (for lock_sections); only_changes: steps whose sets are written only where
    they change the value set before; pull_back {later step: earlier step}: see emit"""
    mom = Mom(_load(MOM_FILES.get(system, MOM_DEFAULT)[0]))
    sysdata = _load(f"system_mos_{system}.json.gz")["templates"]
    model = Model(mom, _system_templates(mom, sysdata))
    model.circle = system
    for text in initial_xml:
        load_netconf(model, text, "initial")
    for mo in model.mos.values():          # initial state: nothing is 'set by the scripts'
        mo["set"], mo["created"] = [], False
    rp = Replay(model)
    rp.only_changes = set(only_changes)
    for name, kind, text in steps:
        rp.step = name
        if kind == "xml":
            for ldn, a, why in load_netconf(model, text, "script", as_script=True, events=rp.events, step=name):
                rp.left(name, 0, f"{ldn} {a}", f"attribute {why} (25.Q2) - dropped from this XML")
        else:
            rp.run(list(enumerate(text.replace("\r\n", "\n").split("\n"), 1)), name)
    _node_rules(model, rp)
    xml_text, order_problems = emit(model, node, rp.events, rp.deleted_existing, pull_back)
    for ldn, a, target in order_problems:
        rp.left("XML", 0, f"{ldn} {a} -> {target}", "reference to an MO that is created later in the XML - check order")
    return xml_text, rp.leftover, rp.notes, model
