"""Full PRE/POST comparison of two kget_mom logs.

Every MO of both logs is matched by its LDN (below ManagedElement) and every configurable attribute is compared
(readOnly state is only compared where the audit-only sections ask for it). PRE is the reference, POST is the site
being corrected. When PRE and POST are different sites the PRE names are moved onto the POST site first (node
name, site token in cell/profile names, own eNBId/gNBId in relation ids), so 'the same' MO compares as one.
"""
from __future__ import annotations

import re
from collections import OrderedDict
from dataclasses import dataclass, field

from .kget_parser import KgetData

# ---------------------------------------------------------------------------------------------------- sections
LTE_GPL, NR_GPL, FEATURE, EUTRAN_FREQ, SSB_FREQ = "LTE GPL", "NR GPL", "FeatureState", "Eutranfrequency", "ssbFrequency"
EUTRAN_FREQ_REL, GUTRAN_FREQ_REL, GERAN_FREQ_REL, CELL_REL = ("EutranfreqRelation", "GutranfreqRelation",
                                                              "GeranFreqRelation", "CellRelation")
OTHER = "Other"
CORRECTION_SECTIONS = [LTE_GPL, FEATURE, EUTRAN_FREQ, SSB_FREQ, EUTRAN_FREQ_REL, GUTRAN_FREQ_REL, GERAN_FREQ_REL,
                       CELL_REL, NR_GPL]

CELL_RELATIONS = {"EUtranCellRelation", "GUtranCellRelation", "GeranCellRelation", "NRCellRelation", "UtranCellRelation"}
NEIGHBOURS = {"ExternalENodeBFunction", "ExternalEUtranCellFDD", "ExternalEUtranCellTDD", "TermPointToENB",
              "ExternalGNodeBFunction", "ExternalGUtranCell", "TermPointToGNB", "ExternalGeranCell", "ExternalUtranCellFDD",
              "ExternalUtranCellTDD", "ExternalNRCellCU", "ExternalGNBCUCPFunction", "TermPointToGNodeB",
              "TermPointToENodeB", "ExternalBroadcastPLMNInfo", "ExternalGNBDUFunction", "TermPointToGNBDU"}
FREQ_CLASSES = {"EUtranFrequency", "GeranFrequency", "GeranFreqGroup", "UtranFrequency", "UtranFrequencyTDD"}
SSB_CLASSES = {"GUtranSyncSignalFrequency", "NRFrequency"}
NR_TOPS = {"GNBDUFunction", "GNBCUCPFunction", "GNBCUUPFunction"}
# links the node builds from live traffic / signalling - compared, never created
RUNTIME = {"TermPointToSGW", "GtpPath", "SctpAssociation", "X2ULink", "S1ULink", "RpUserPlaneLink", "XnULink",
           "F1ULink", "NgULink", "TermPointToAmf", "TermPointToMme"}
# values that belong to the site itself: audited, corrected only when PRE and POST are the same site
SITE_DATA = {"latitude", "longitude", "altitude", "cellid", "celllocalid", "nci", "enbid", "gnbid", "gnbidlength",
             "tac", "nrtac", "physicallayercellid", "physicallayercellidgroup", "physicallayersubcellid", "nrpci",
             "rachrootsequence", "earfcn", "earfcndl", "earfcnul", "arfcndl", "arfcnul", "ssbfrequency",
             "enodebplmnid", "plmnid", "userlabel", "primaryplmnreserved", "ipv4address", "ipv6address"}
# a cross-site value pointing into these is the site's own wiring (SectorCarrier rfBranchRxRef -> its AntennaUnitGroup)
SITE_REF_TOPS = ("Equipment=", "Transport=", "NodeSupport=", "SystemFunctions=")

# audit-only sections (compared, never corrected) - the hgetc commands of the request, applied to the kget:
# MO pattern = regex on the RDN (on the LDN when it has a comma), attribute pattern = regex search on the name
INFO_SPECS = {
    "eNBInfo": [(r"enodebfunction=1$", r"enbid|enodebplmnid")],
    "gNBInfo": [(r"^GNB.*Function", r"pLMNId|gnbid")],
    "LTE_CELL_DATA": [
        (r"^EUtranCell.DD", r"^administrativeState$|^operationalState$|^tac$|^userlabel$|^freqband$|^dlChannelBandwidth"
                            r"|^earfcndl$|^ulChannelBandwidth|^earfcnul$|^channelBandwidth$|^earfcn$|^cellid$"
                            r"|^primaryPlmnReserved$|^physicalLayerCellId$|^physicalLayerCellIdGroup$"
                            r"|^physicalLayerSubCellId$|^rachRootSequence$|^noOfPucchSrUsers$|^cellSubscriptionCapacity$"),
        (r"ENodeBFunction=1,SectorCarrier=", r"reservedBy|noOfRxAntennas|noOfTxAntennas|configuredMaxTxPower|sectorFunctionRef"),
    ],
    "NR_CELL_DATA": [
        (r"NRCellDU=", r"^administrativeState$|^cellLocalId$|^ssbFrequency$|^bandListManual$|^operationalState$|^nRPCI$"
                       r"|^rachRootSequence$|^nRTAC$|^userLabel"),
        (r"^NRSectorCarrier=", r"reservedBy|noOfUsedRxAntennas$|noOfUsedTxAntennas$|configuredMaxTxPower"
                               r"|sectorEquipmentFunctionRef|arfcnDL$|^bSChannelBwDL$"),
    ],
}


def _mo_match(pattern: str, ldn: str) -> bool:
    """moshell rule (as in the KK XML engine): plain pattern = regex on the RDN, pattern with a comma = regex on the
    LDN with the match ending inside the MO's own RDN"""
    if "," in pattern:
        return re.search(f"(?:{pattern})[^,]*$", ldn, re.I) is not None
    return re.search(pattern, ldn.rsplit(",", 1)[-1], re.I) is not None


def classes_of(ldn: str) -> list[str]:
    return [p.split("=", 1)[0] for p in ldn.split(",")] if ldn else ["ManagedElement"]


def section_of(ldn: str) -> str:
    cls = classes_of(ldn)
    chain = set(cls)
    if cls[-1] == "FeatureState" and "Lm" in chain:
        return FEATURE
    if chain & (CELL_RELATIONS | NEIGHBOURS):
        return CELL_REL
    if "EUtranFreqRelation" in chain:
        return EUTRAN_FREQ_REL
    if chain & {"GUtranFreqRelation", "NRFreqRelation"}:
        return GUTRAN_FREQ_REL
    if chain & {"GeranFreqGroupRelation", "GeranFreqRelation"}:
        return GERAN_FREQ_REL
    if chain & SSB_CLASSES:
        return SSB_FREQ
    if chain & FREQ_CLASSES:
        return EUTRAN_FREQ
    if chain & RUNTIME:
        return OTHER
    if cls[0] == "ENodeBFunction":
        return LTE_GPL
    if cls[0] in NR_TOPS:
        return NR_GPL
    return OTHER


# ---------------------------------------------------------------------------------------------------- values
def text(v) -> str:
    """value -> one comparable / printable line (structs 'm=v,m=v', sequences space separated, struct lists ';')"""
    if v is None:
        return ""
    if isinstance(v, dict):
        return ",".join(f"{k}={text(x)}" for k, x in v.items())
    if isinstance(v, list):
        if v and isinstance(v[0], dict):
            return ";".join(text(x) for x in v)
        return " ".join(str(x) for x in v)
    return re.sub(r"\s+", " ", str(v)).strip()


def _subst(v, rules):
    if isinstance(v, dict):
        return OrderedDict((k, _subst(x, rules)) for k, x in v.items())
    if isinstance(v, list):
        return [_subst(x, rules) for x in v]
    if isinstance(v, str):
        for rx, rep in rules:
            v = rx.sub(rep, v)
    return v


def site_token(node: str) -> str:
    """'KK-NLAAZAD1-1' -> 'AAZAD1' (same rule as the LTE tool's site id)"""
    chunks = str(node).split("-")
    if len(chunks) >= 2 and chunks[1]:
        c = chunks[1]
        return c[2:] if c[:2].isalpha() and len(c) > 2 else c
    return ""


def _own_ids(data: KgetData):
    enb = str((data.mos.get("ENodeBFunction=1") or {}).get("eNBId", "")).strip()
    gnb = ""
    for top in ("GNBCUCPFunction=1", "GNBDUFunction=1", "GNBCUUPFunction=1"):
        gnb = str((data.mos.get(top) or {}).get("gNBId", "")).strip()
        if gnb:
            break
    return enb, gnb


def _own_cell_numbers(mos, enb: str) -> dict:
    """LDN of an own cell -> its global number: ECI (eNBId*256 + cellId) for LTE cells, nCI for NR cells.
    ANR/EN-DC ids of relations to the own cells are made from these ('auto51105546')."""
    out = {}
    for k, v in mos.items():
        if re.match(r"^ENodeBFunction=1,EUtranCell[FT]DD=[^,]+$", k) and enb.isdigit():
            cid = str(v.get("cellId", "")).strip()
            if cid.isdigit():
                out[k] = str(int(enb) * 256 + int(cid))
        elif re.match(r"^GNBCUCPFunction=1,NRCellCU=[^,]+$", k):
            nci = str(v.get("nCI", "")).strip()
            if nci.isdigit():
                out[k] = nci
    return out


def _number_rule(a: str, b: str):
    """whole-number occurrence of a (any zero padding) -> b with the same width"""
    return (re.compile(rf"(?<![0-9])0*{re.escape(a)}(?![0-9])"), lambda m, b=b: b.zfill(len(m.group(0))))


# ---------------------------------------------------------------------------------------------------- result
@dataclass
class Item:
    """one compared attribute (or struct member) of one MO"""
    section: str
    ldn: str
    attr: str
    member: str          # '' or struct member name
    pre: str
    post: str
    status: str          # OK | NOT OK | Missing
    info: str = ""       # audit-only sheet name, '' for correctable sections


@dataclass
class AuditResult:
    pre: KgetData
    post: KgetData
    pre_mos: "OrderedDict[str, OrderedDict]"      # PRE moved onto the POST site
    cross_site: bool
    items: list = field(default_factory=list)
    missing_mos: list = field(default_factory=list)     # LDNs only in PRE (eligible or not)
    new_mos: list = field(default_factory=list)         # LDNs only in POST
    skipped_neighbours: int = 0
    mapping: list = field(default_factory=list)         # (from, to) applied to PRE

    @property
    def node(self) -> str:
        return self.post.node


def _readonly(mom, ldn, attr) -> bool:
    info = mom.attr(mom.class_key(ldn), attr)
    return bool(info and "readOnly" in info[2])


def _is_key(mom, ldn, attr) -> bool:
    cls = classes_of(ldn)[-1]
    if attr.lower() == (cls[0].lower() + cls[1:] + "Id").lower():
        return True
    info = mom.attr(mom.class_key(ldn), attr)
    return bool(info and "key" in info[2])


def _intra_site(ldn: str, attrs: dict, own: set) -> bool:
    """cross-site: a relation / neighbour definition is comparable only if it points to the own site
    (own = POST eNBId, gNBId and the ECI/nCI of its cells, without leading zeros)"""
    cls = classes_of(ldn)
    rdns = ldn.split(",")
    ids = [r.split("=", 1)[1] for r, c in zip(rdns, cls) if c in CELL_RELATIONS | NEIGHBOURS]
    if "NRCellRelation" in cls:
        ref = text(attrs.get("nRCellRef", ""))
        return ",NRCellCU=" in ref and "External" not in ref
    if "GeranCellRelation" in cls or "ExternalGeranCell" in cls:
        return False
    for i in ids:
        parts = i.split("-")
        if len(parts) >= 2:                                   # 40445-<eNBId>-<cellId>, 40445-<gNBId>
            if parts[1].lstrip("0") in own:
                continue
            return False
        nums = [n.lstrip("0") for n in re.findall(r"\d+", i)]
        if i.lower().startswith("auto") and nums:             # auto404_45_2_<eNBId>, auto<ECI>
            if nums[-1] in own:
                continue
            return False
        # plain ids (ExternalBroadcastPLMNInfo=1, TermPointToENodeB=auto1): the parent decides
    return True


CELL_CLASSES = re.compile(r"^(?:ENodeBFunction=[^,]+,EUtranCell[FT]DD|GNBCUCPFunction=[^,]+,NRCellCU"
                          r"|GNBDUFunction=[^,]+,NRCellDU)=[^,]+$")


def _pair_cells(pre_mos, post_mos, token: str) -> list:
    """PRE cells without a POST cell of the same name -> the POST cell of the same class with the same site id and
    sector suffix (KK_5_EE_T1_OM_6_xxxxBGR583_A = KK_5_EE_T1_OM_5_xxxxBGR583_A: site BGR583, 1st sector). Only a
    unique match on both sides is taken, so cells of two bands on one sector (KK_E_F1_.._A / KK_E_F3_.._A) are never
    paired by this rule."""
    if not token:
        return []

    def key(ldn):
        cls, _, cid = ldn.rpartition("=")              # cls = 'GNBCUCPFunction=1,NRCellCU'
        m = re.search(r"_([A-Za-z0-9])$", cid)
        return (cls, m.group(1).upper()) if token in cid and m else None

    lone_pre = [k for k in pre_mos if CELL_CLASSES.match(k) and k not in post_mos]
    lone_post = [k for k in post_mos if CELL_CLASSES.match(k) and k not in pre_mos]
    by_pre, by_post = {}, {}
    for k in lone_pre:
        by_pre.setdefault(key(k), []).append(k)
    for k in lone_post:
        by_post.setdefault(key(k), []).append(k)
    return [(a[0], by_post[g][0]) for g, a in by_pre.items() if g and len(a) == 1 and len(by_post.get(g, [])) == 1]


RELATION_TARGET = {"NRCellRelation": "nRCellRef", "EUtranCellRelation": "neighborCellRef",
                   "GUtranCellRelation": "neighborCellRef", "GeranCellRelation": "neighborCellRef"}


def _pair_relations(pre_mos, post_mos) -> list:
    """PRE relations without a POST relation of the same id -> the POST relation under the same parent pointing to the
    same cell (unique on both sides)"""
    def key(ldn, attrs):
        cls = classes_of(ldn)[-1]
        if cls not in RELATION_TARGET:
            return None
        target = text(attrs.get(RELATION_TARGET[cls], ""))
        return (ldn.rsplit(",", 1)[0], cls, target) if target else None

    by_pre, by_post = {}, {}
    for k, v in pre_mos.items():
        if k not in post_mos:
            g = key(k, v)
            if g:
                by_pre.setdefault(g, []).append(k)
    for k, v in post_mos.items():
        if k not in pre_mos:
            g = key(k, v)
            if g:
                by_post.setdefault(g, []).append(k)
    return [(a[0], by_post[g][0]) for g, a in by_pre.items() if len(a) == 1 and len(by_post.get(g, [])) == 1]


def run_audit(pre: KgetData, post: KgetData) -> AuditResult:
    cross = pre.node != post.node
    rules, mapping = [], []
    if cross:
        rules.append((re.compile(re.escape(pre.node)), post.node))
        mapping.append((pre.node, post.node))
        pt, qt = site_token(pre.node), site_token(post.node)
        if len(pt) >= 4 and len(qt) >= 4 and pt != qt:
            rules.append((re.compile(re.escape(pt)), qt))
            mapping.append((pt, qt))
    named = OrderedDict((_subst(k, rules), _subst(v, rules)) for k, v in pre.mos.items()) if rules else pre.mos
    cell_renames = _pair_cells(named, post.mos, site_token(post.node))
    if cell_renames:
        # the cell name wherever it is a whole word: cell LDNs and ids made from it (UeCC=1,CgSwitch=<cell name>)
        names = sorted({(a.rsplit("=", 1)[1], b.rsplit("=", 1)[1]) for a, b in cell_renames}, key=lambda ab: -len(ab[0]))
        cell_rules = [(re.compile(rf"(?<![\w-]){re.escape(a)}(?![\w-])"), b) for a, b in names]
        named = OrderedDict((_subst(k, cell_rules), _subst(v, cell_rules)) for k, v in named.items())
        mapping += [(a.rsplit(",", 1)[-1], b.rsplit(",", 1)[-1]) for a, b in cell_renames]
    if cross:
        # own eNBId / gNBId / cell numbers wherever they appear as a whole number: relation ids (40445-<id>-12,
        # auto404_45_2_<id>, auto<ECI>), struct members (pciDetectingCell enbId=<id>), plain values (eNodeBId)
        (pe, pg), (qe, qg) = _own_ids(pre), _own_ids(post)
        nums = []
        pre_cells, post_cells = _own_cell_numbers(named, pe), _own_cell_numbers(post.mos, qe)
        for k, a in pre_cells.items():
            b = post_cells.get(k)
            if b and a != b:
                nums.append((a, b))
        nums += [(a, b) for a, b in ((pe, qe), (pg, qg)) if a and b and a != b and len(a) >= 4]
        nums.sort(key=lambda ab: -len(ab[0]))          # longest first: an ECI never loses digits to the eNBId rule
        if nums:
            num_rules = [_number_rule(a, b) for a, b in nums]
            named = OrderedDict((_subst(k, num_rules), _subst(v, num_rules)) for k, v in named.items())
            mapping += [(a, b) for a, b in nums if (a, b) in ((pe, qe), (pg, qg))]
            mapping.append((f"{sum(1 for a, b in nums if (a, b) not in ((pe, qe), (pg, qg)))} own cell ECI/NCI", "POST values"))
    # an MO whose id differs only in case is the same profile (PRE PrefUeGroupSelectionProfile=QCI6 = POST qci6: the
    # node refuses a second one with the same prefUeGroupId/priority) - PRE takes the POST id, references included
    post_lower = {k.lower(): k for k in post.mos}
    renames = [(k, post_lower[k.lower()]) for k in named
               if k not in post.mos and k.lower() in post_lower and post_lower[k.lower()] not in named]
    if renames:
        rename_rules = [(re.compile(re.escape(a) + r"(?=,|$)"), b) for a, b in sorted(renames, key=lambda ab: -len(ab[0]))]
        named = OrderedDict((_subst(k, rename_rules), _subst(v, rename_rules)) for k, v in named.items())
        mapping += [(a.rsplit(",", 1)[-1], b.rsplit(",", 1)[-1]) for a, b in renames]
    # a relation to the same cell under another id is the same relation (PRE ANR 'auto<nCI>' = POST manual
    # '40445-<gNBId>-<cellLocalId>': the node refuses two relations with the same nRCellRef)
    rel_renames = _pair_relations(named, post.mos)
    if rel_renames:
        rel_rules = [(re.compile(re.escape(a) + r"(?=,|$)"), b) for a, b in sorted(rel_renames, key=lambda ab: -len(ab[0]))]
        named = OrderedDict((_subst(k, rel_rules), _subst(v, rel_rules)) for k, v in named.items())
        mapping.append((f"{len(rel_renames)} cell relations", "POST relation to the same cell"))
    pre_mos = OrderedDict(named)
    res = AuditResult(pre=pre, post=post, pre_mos=pre_mos, cross_site=cross, mapping=mapping)
    enb, gnb = _own_ids(post)
    own = {x.lstrip("0") for x in [enb, gnb, *_own_cell_numbers(post.mos, enb).values()] if x}
    mom = post.mom

    def info_sheet(ldn, attr):
        for sheet, specs in INFO_SPECS.items():
            for mo_rx, attr_rx in specs:
                if _mo_match(mo_rx, ldn) and re.search(attr_rx, attr, re.I):
                    return sheet
        return ""

    for ldn in list(pre_mos) + [k for k in post.mos if k not in pre_mos]:
        if not ldn:
            continue
        section = section_of(ldn)
        a_pre, a_post = pre_mos.get(ldn), post.mos.get(ldn)
        if cross and section == CELL_REL and not _intra_site(ldn, a_pre or a_post, own):
            res.skipped_neighbours += 1
            continue
        if a_post is None:
            res.missing_mos.append(ldn)
            continue
        if a_pre is None:
            res.new_mos.append(ldn)
            continue
        for attr in list(a_pre) + [a for a in a_post if a not in a_pre]:
            sheet = info_sheet(ldn, attr)
            if not sheet and (_readonly(mom, ldn, attr) or _is_key(mom, ldn, attr)):
                continue
            if attr not in a_pre:
                continue                                   # new attribute of the POST software: not a finding
            vp, vq = a_pre[attr], a_post.get(attr)
            if isinstance(vp, dict) and (vq is None or isinstance(vq, dict)):
                for m, x in vp.items():
                    y = None if vq is None else vq.get(m)
                    res.items.append(Item(section, ldn, attr, m, text(x), "" if y is None else text(y),
                                          "Missing" if y is None else ("OK" if text(x) == text(y) else "NOT OK"), sheet))
                continue
            st = "Missing" if vq is None else ("OK" if text(vp) == text(vq) else "NOT OK")
            res.items.append(Item(section, ldn, attr, "", text(vp), "" if vq is None else text(vq), st, sheet))
    return res
