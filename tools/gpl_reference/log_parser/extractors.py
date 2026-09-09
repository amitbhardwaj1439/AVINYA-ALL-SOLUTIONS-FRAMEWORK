import logging
import re
from pathlib import Path

import pandas as pd

from .reader import parse_all_commands_multi

log = logging.getLogger(__name__)


# hgetc prints a list-valued attribute with its element count in front:
#   csiRsActivePortConfig -> "i[2] = 2 4 (PORT_8 PORT_32)"
# The golden sheet writes the bare list ("2 4 (PORT_8 PORT_32)") and puts the
# count on the parameter NAME instead ("csiRsActivePortConfig[2]"), so the
# prefix has to come off before the two can be compared.
_ARRAY_PREFIX_RE = re.compile(r"^\s*\w*\[\d+\]\s*=\s*")


def _clean_value(val):
    if pd.isna(val):
        return val
    s = _ARRAY_PREFIX_RE.sub("", str(val))
    return re.sub(r"\s*\([^)]*\)", "", s).strip()


# `hgetc <scope> ^someStruct$@memberA$|memberB$` reads the members of a struct
# attribute. The struct name appears ONLY in the command — hgetc's own header
# prints the members bare ("MO;i11Restriction") — so the log alone cannot say
# which struct a member belongs to.
_STRUCT_RE = re.compile(r"\^?(\w+)\$?@")


def _qualify_struct_members(cmd: str, df: pd.DataFrame, id_vars: list[str]):
    """Second view of a struct command's table, columns renamed 'struct.member'.

    NRCellDU carries csiRsConfig4P, csiRsConfig8P and csiRsConfig32P, each with
    its own i11Restriction, and each read by its own command. All three print
    the same bare column name, so they collided on the (MO, Parameter) dedup key
    and only one survived — while the golden sheet, which spells them out as
    csiRsConfig8p.i11Restriction, matched none of them and reported all three
    Missing.

    Returned ALONGSIDE the bare-named view rather than replacing it: plenty of
    struct members are listed in the sheet under their bare name (the whole
    systemInformationBlock3 block, for one), and those must keep matching.
    Rows nobody's golden list names are simply never looked up.
    """
    m = _STRUCT_RE.search(cmd)
    if m is None:
        return None
    struct = m.group(1)
    prefix = struct.lower() + "."
    renames = {
        c: f"{struct}.{c}"
        for c in df.columns
        if c not in id_vars and not str(c).lower().startswith(prefix)
    }
    return df.rename(columns=renames) if renames else None


async def get_gpl_audit_data(
    commands: dict,
    file_paths: list[Path | str],
    keys: tuple[str, ...] = (
        "LTE_GPL_AUDIT", "NR_GPL_AUDIT", "GPL_AUDIT",
        # The golden workbook does not care which section a command was filed
        # under, so neither can this audit. These sections all carry rows the
        # reference sheets define, and reading only the two *_GPL_AUDIT ones
        # left them permanently "Missing" while the values sat in the log:
        #   EUTRANFREQRELATION_AUDIT   EUtranFreqRelation.pMax / tReselectionEutra / …
        #   GUTRANFREQRELATION_AUDIT   GUtranFreqRelation.b1ThrRsrpFreqOffset / qOffsetFreq / …
        #   CELLRELATION_AUDIT         EUtranCellRelation.isHoAllowed, NRCellRelation.sCellCandidate, …
        #   LTE_CELL_DATA              EUtranCellFDD.dlChannelBandwidth / ulChannelBandwidth, …
        #   EUTRANFREQUENCY_AUDIT      EUtranFrequency=*.arfcnValueEUtranDl
        # The rest contribute nothing today but are listed so a command moving
        # between sections can never silently drop out of the audit again.
        "EUTRANFREQRELATION_AUDIT", "GUTRANFREQRELATION_AUDIT", "GERANFREQRELATION_AUDIT",
        "CELLRELATION_AUDIT", "LTE_CELL_DATA", "NR_CELL_DATA",
        "EUTRANFREQUENCY_AUDIT", "SSBFREQUENCY_AUDIT",
        "ENBINFO_AUDIT", "GNBINFO_AUDIT",
    ),
) -> pd.DataFrame:
    """Every golden-parameter-list command, melted into one long
    (Node_ID, MO, Perameter, value) table.

    Section placement decides nothing here: LTE vs NR is settled per row by
    audits.py via reference.classify_mo_tree()/lookup_parameter_dual(), from
    the MO path itself. The commands file still keeps its separate sections so
    the SAME file can drive gpl_audit_tool_V2 (which does route by section) and
    one log capture can feed both tools.

    FEATURESTATE is deliberately absent — features are a different sheet with a
    different comparison (see get_feature_state_data / extract_state_code).

    A few commands are intentionally unscoped (e.g. bare ``^Paging=``) and can
    return the same physical row that a root-scoped sibling command also
    returns once every section is pulled together, so duplicates are dropped
    here."""
    gpl_commands = [c for key in keys for c in commands.get(key, [])]
    if not gpl_commands:
        log.warning("No commands found in section(s) %s — skipping.", ", ".join(keys))
        return pd.DataFrame()
    log.info(
        "GPL audit commands: %d from %s",
        len(gpl_commands),
        ", ".join(f"{k}={len(commands.get(k, []))}" for k in keys if commands.get(k)),
    )

    all_dfs = await parse_all_commands_multi(gpl_commands, file_paths)

        
    # exit(0)

    frames = []
    for cmd, df in all_dfs.items():
        if df.empty:
            continue
        if "MO" not in df.columns:
            log.warning("'MO' column missing for command: %s", cmd)
            continue
        id_vars = [c for c in ("Node_ID", "MO") if c in df.columns]
        frames.append(df.melt(id_vars=id_vars, var_name="Perameter"))

        qualified = _qualify_struct_members(cmd, df, id_vars)
        if qualified is not None:
            frames.append(qualified.melt(id_vars=id_vars, var_name="Perameter"))

    if not frames:
        log.warning("No valid data extracted from %s [%s]", file_paths, ", ".join(keys))
        return pd.DataFrame()

    result = pd.concat(frames, axis=0, ignore_index=True)
    dedup_cols = [c for c in ("Node_ID", "MO", "Perameter") if c in result.columns]
    if dedup_cols and "value" in result.columns:
        # A row can be duplicated across commands when one command is a
        # broader/unscoped pattern that happens to also match the same MO —
        # it captures that MO but not this particular attribute, while another
        # command captures the real value. Prefer the real value regardless of
        # which command happened to run first.
        #
        # "No value" is BLANK as often as it is NaN: reader._build_df pads a
        # short row out to the header width with "", so a command whose output
        # simply stops before this column yields "" and not NaN. Sorting on
        # isna() alone let those blanks win the dedup and blank out attributes
        # that another command had read correctly.
        result = result.sort_values(
            by="value",
            key=lambda s: s.isna() | (s.astype(str).str.strip() == ""),
            kind="stable",
        )
    
    return result.drop_duplicates(subset=dedup_cols, keep="first").reset_index(drop=True)


async def get_nr_cell_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "NR_CELL_DATA",
) -> pd.DataFrame:
    nr_commands = commands.get(key)
    if not nr_commands:
        log.warning("Section '%s' not found in commands — skipping.", key)
        return pd.DataFrame()

    all_dfs = await parse_all_commands_multi(nr_commands, file_paths)

    frames = []
    for cmd, df in all_dfs.items():
        if df.empty:
            continue
        if "MO" not in df.columns:
            log.warning("'MO' column missing for command: %s", cmd)
            continue
        frames.append(df)

    if not frames:
        log.warning("No valid data extracted from %s [%s]", file_paths, key)
        return pd.DataFrame()

    result = frames[0].reset_index(drop=True)
    for i, df in enumerate(frames[1:], 1):
        df = df.reset_index(drop=True).rename(columns={"MO": f"MO_{i}"})
        df = df.drop(columns=["Node_ID"], errors="ignore")
        result = pd.concat([result, df], axis=1)
    return result


async def _get_lte_wide_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str,
) -> pd.DataFrame:
    """Concat all DataFrames for a section vertically (wide / non-melted)."""
    lte_commands = commands.get(key)
    if not lte_commands:
        log.warning("Section '%s' not found in commands — skipping.", key)
        return pd.DataFrame()

    all_dfs = await parse_all_commands_multi(lte_commands, file_paths)


    frames = []
    for cmd, df in all_dfs.items():
        if df.empty:
            continue
        if "MO" not in df.columns:
            log.warning("'MO' column missing for command: %s", cmd)
            continue
        frames.append(df)

    if not frames:
        log.warning("No valid data extracted from %s [%s]", file_paths, key)
        return pd.DataFrame()

    return pd.concat(frames, axis=0, ignore_index=True)


async def get_lte_enbinfo_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "ENBINFO_AUDIT",
) -> pd.DataFrame:
    return await _get_lte_wide_data(commands, file_paths, key)

async def get_nr_gnbinfo_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "GNBINFO_AUDIT",
) -> pd.DataFrame:
    df = await _get_lte_wide_data(commands, file_paths, key)
    if not df.empty:
        # hgetc splits some MOs (e.g. GNBCUUPFunction, whose pLMNId is a
        # struct attribute) across two physical output lines: one line has
        # gNBId/gNBIdLength populated with mcc/mnc blank, the next has it the
        # other way round. Coalesce rows sharing the same Node_ID+MO into one
        # logical row, keeping the first non-blank value per column.
        group_cols = [c for c in ("Node_ID", "MO") if c in df.columns]
        if group_cols:
            def _coalesce(s: pd.Series):
                for v in s:
                    if pd.notna(v) and str(v).strip() != "":
                        return v
                return s.iloc[0]

            df = df.groupby(group_cols, as_index=False, sort=False).agg(_coalesce)
    return df




async def get_feature_state_data(
    commands: dict,
    file_paths: list[Path | str],
    keys: tuple[str, ...] = ("FEATURESTATE_AUDIT", "NR_FEATURESTATE_AUDIT"),
) -> pd.DataFrame:
    """Every featurestate row in the log, LTE and NR together.

    Today the commands file has a single "FeatureState Audit" section covering
    both; NR_FEATURESTATE_AUDIT is picked up too if one is ever added, since
    the audit treats all features as one list either way.
    """
    frames = []
    for key in keys:
        if key not in commands:
            continue
        df = await _get_lte_wide_data(commands, file_paths, key)
        if not df.empty:
            frames.append(df)

    if not frames:
        return pd.DataFrame()

    df = pd.concat(frames, axis=0, ignore_index=True)
    # The section mixes a broad "Lm=1,FeatureState" command with individual CXC
    # commands that overlap — deduplicate keeping the first occurrence per MO.
    return df.drop_duplicates(subset=["MO"], keep="first").reset_index(drop=True)


async def get_lte_eutran_freq_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "EUTRANFREQUENCY_AUDIT",
) -> pd.DataFrame:
    return await _get_lte_wide_data(commands, file_paths, key)


async def get_lte_eutran_freq_relation_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "EUTRANFREQRELATION_AUDIT",
) -> pd.DataFrame:
    df = await _get_lte_wide_data(commands, file_paths, key)
    if not df.empty:
        # Command 2 uses EutranFreqToQciProfileRelation@ (a child object), so its
        # MO column has an extra ",EutranFreqToQciProfileRelation=N" suffix.
        # Strip it so all 4 commands align to the same parent EUtranFreqRelation MO,
        # then groupby.first() merges columns across commands into one row per MO.
        df["MO"] = df["MO"].str.replace(
            r",EutranFreqToQciProfileRelation=\S+$", "", regex=True
        )
        df = df.groupby("MO", as_index=False).first()
    return df

async def get_nr_gutran_freq_relation_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "GUTRANFREQRELATION_AUDIT",
) -> pd.DataFrame:
    df = await _get_lte_wide_data(commands, file_paths, key)
    if not df.empty:
        # Command 2 uses EutranFreqToQciProfileRelation@ (a child object), so its
        # MO column has an extra ",EutranFreqToQciProfileRelation=N" suffix.
        # Strip it so all 4 commands align to the same parent EUtranFreqRelation MO,
        # then groupby.first() merges columns across commands into one row per MO.
        df["MO"] = df["MO"].str.replace(
            r",EutranFreqToQciProfileRelation=\S+$", "", regex=True
        )
        df = df.groupby("MO", as_index=False).first()
    return df


async def get_lte_cell_relation_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "CELLRELATION_AUDIT",
) -> pd.DataFrame:
    df = await _get_lte_wide_data(commands, file_paths, key)


    if not df.empty:
        # The section includes EUtranCell and ExternalGeranCell rows alongside
        # EUtranCellRelation rows.  Keep only the relation rows.
        df = df[df["MO"].str.contains("EUtranCellRelation", na=False)].reset_index(drop=True)
        # The audit dump batches both a "_PRE"/"_POST" file and an "_NR_5G_PRE"/
        # "_NR_5G_POST" file, and both contain the same LTE CellRelation section —
        # dedupe by MO like get_lte_eutran_freq_relation_data does.
        df = df.drop_duplicates(subset=["MO"], keep="first").reset_index(drop=True)
        # earfcndl/physicalLayerCellIdGroup/physicalLayerSubCellId/tac come from
        # the section's EUtranCellFDD command, and rimAssociationStatus/rimCapable
        # from its ExternalGeranCell command — both filtered out above, so these
        # columns are always empty once only EUtranCellRelation rows remain.
        df = df.drop(columns=[
            "earfcndl", "physicalLayerCellIdGroup", "physicalLayerSubCellId", "tac",
            "rimAssociationStatus", "rimCapable",
        ], errors="ignore")
    return df


async def get_lte_cell_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "LTE_CELL_DATA",
) -> pd.DataFrame:
    lte_commands = commands.get(key)

    if not lte_commands:
        log.warning("Section '%s' not found in commands — skipping.", key)
        return pd.DataFrame()

    all_dfs = await parse_all_commands_multi(lte_commands, file_paths)



    frames = []
    for cmd, df in all_dfs.items():
        if df.empty:
            continue
        if "MO" not in df.columns:
            log.warning("'MO' column missing for command: %s", cmd)
            continue
        frames.append(df)

    if not frames:
        log.warning("No valid data extracted from %s [%s]", file_paths, key)
        return pd.DataFrame()

    result = frames[0].reset_index(drop=True)
    for i, df in enumerate(frames[1:], 1):
        df = df.reset_index(drop=True).rename(columns={"MO": f"MO_{i}"})
        df = df.drop(columns=["Node_ID"], errors="ignore")
        result = pd.concat([result, df], axis=1)

    return result
