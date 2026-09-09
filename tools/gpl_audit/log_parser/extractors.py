import logging
import re
from pathlib import Path

import pandas as pd

from .reader import parse_all_commands_multi

log = logging.getLogger(__name__)


def _clean_value(val):
    if pd.isna(val):
        return val
    return re.sub(r"\s*\([^)]*\)", "", str(val)).strip()


# `hgetc <scope> ^someStruct$@memberA$|memberB$` reads the members of a struct
# attribute. The struct name appears ONLY in the command — hgetc's own header
# prints the members bare ("MO;hysteresis") — so the log alone cannot say which
# struct a member belongs to.
_STRUCT_RE = re.compile(r"\^?(\w+)\$?@")


def _qualify_struct_members(cmd: str, df: pd.DataFrame, id_vars: list[str]) -> pd.DataFrame:
    """Rename a struct command's value columns to 'struct.member'.

    Several structs under one MO can each carry a member of the same name —
    McpcPSCellProfileUeCfg has more than one 'hysteresis', 'threshold' and
    'timeToTrigger' — and each is read by its own command. Printed bare, they
    all collapse onto one (MO, Perameter) key, which is exactly the key
    audits._build_audit_df merges pre and post on. The merge then pairs every
    pre row with every post row for that key, so a log compared against ITSELF
    reported 148 NOT OK: pre=20 matched against post=10 for a 'hysteresis' that
    belonged to a different struct.

    Qualifying makes the key unique again. Unlike the reference tool — which
    keeps both spellings because its golden sheet uses both — the diff has no
    external names to satisfy and simply needs pre and post keyed identically,
    so the bare name is REPLACED, not duplicated.
    """
    m = _STRUCT_RE.search(cmd)
    if m is None:
        return df
    struct = m.group(1)
    prefix = struct.lower() + "."
    renames = {
        c: f"{struct}.{c}"
        for c in df.columns
        if c not in id_vars and not str(c).lower().startswith(prefix)
    }
    return df.rename(columns=renames) if renames else df


def _melt_indexing_repeats(df: pd.DataFrame, id_vars: list[str]) -> pd.DataFrame:
    """Melt, numbering the elements of list-valued attributes.

    A sequence attribute prints one row per element under an unchanged MO —
    DESManagementFunction's esNotAllowedTimePeriod has 7, and one of them holds
    a different startTime from the rest. All 7 share the (MO, Perameter) merge
    key, so pre and post cross-join and the odd element is compared against the
    others, reporting a difference between a file and itself.

    Elements are positional and the node prints them in model order, so the
    row's position within its MO is the only thing that identifies it. Rows are
    tagged 'attr[i]' — but ONLY where an MO actually repeats, so the ordinary
    one-row-per-MO case keeps its plain parameter names.
    """
    if df.empty:
        return df.melt(id_vars=id_vars, var_name="Perameter")
    group = [c for c in id_vars if c in df.columns] or ["MO"]
    occ = df.groupby(group, sort=False).cumcount()
    repeats = df.groupby(group, sort=False)["MO"].transform("size") > 1
    df = df.assign(__occ=occ, __rep=repeats)

    melted = df.melt(id_vars=id_vars + ["__occ", "__rep"], var_name="Perameter")
    mask = melted["__rep"]
    melted.loc[mask, "Perameter"] = (
        melted.loc[mask, "Perameter"] + "[" + melted.loc[mask, "__occ"].astype(str) + "]"
    )
    return melted.drop(columns=["__occ", "__rep"])


def _prefer_real_values(df: pd.DataFrame) -> pd.DataFrame:
    """One row per (Node_ID, MO, Perameter), preferring a row that has a value.

    An attribute can be produced twice for the same MO by two commands, once
    with the real reading and once as an empty placeholder — a wide-table union
    artifact, since a command whose regex matches several MO classes gets every
    requested attribute name as a column on ALL of them. Left alone, the pre/post
    merge pairs the blank copy on one side with the real copy on the other and
    invents a difference.
    """
    if df.empty or "value" not in df.columns:
        return df
    subset = [c for c in ("Node_ID", "MO", "Perameter") if c in df.columns]
    blank = df["value"].isna() | (df["value"].astype(str).str.strip() == "")
    return (df.assign(__blank=blank)
              .sort_values("__blank", kind="stable")
              .drop_duplicates(subset=subset, keep="first")
              .drop(columns="__blank")
              .sort_index()
              .reset_index(drop=True))


async def get_nr_baseline_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "NR_GPL_AUDIT",
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
        id_vars = [c for c in ("Node_ID", "MO") if c in df.columns]
        df = _qualify_struct_members(cmd, df, id_vars)
        frames.append(_melt_indexing_repeats(df, id_vars))

    if not frames:
        log.warning("No valid data extracted from %s [%s]", file_paths, key)
        return pd.DataFrame()

    return _prefer_real_values(pd.concat(frames, axis=0, ignore_index=True))


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


async def get_lte_gpl_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "LTE_GPL_AUDIT",
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
        id_vars = [c for c in ("Node_ID", "MO") if c in df.columns]
        df = _qualify_struct_members(cmd, df, id_vars)
        frames.append(_melt_indexing_repeats(df, id_vars))

    if not frames:
        log.warning("No valid data extracted from %s [%s]", file_paths, key)
        return pd.DataFrame()

    return _prefer_real_values(pd.concat(frames, axis=0, ignore_index=True))


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




async def get_lte_feature_state_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "FEATURESTATE_AUDIT",
) -> pd.DataFrame:
    df = await _get_lte_wide_data(commands, file_paths, key)
    # The section mixes a broad "Lm=1,FeatureState" command with individual CXC
    # commands that overlap — deduplicate keeping the first occurrence per MO.
    if not df.empty:
        df = df.drop_duplicates(subset=["MO"], keep="first").reset_index(drop=True)
    return df


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

