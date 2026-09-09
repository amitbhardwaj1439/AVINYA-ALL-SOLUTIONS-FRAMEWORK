"""The output schema, read from the template workbook itself.

The sheet names and column order are taken from a real
*_RF_Data_Scripting_Template_4G_5G_*.xlsx at run time rather than hardcoded, so
a column added to the template reaches the output without a code change - and
the four sheet names stay exactly as LTE_Integration_Scripting_Automtion's
views.py parses them ('Site_Basic', 'Radio_HW', 'LTE-CELL', 'NR-CELL').
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

TEMPLATE_GLOB = "*RF_Data_Scripting_Template*.xlsx"

# Where the template lives: a fixture of the app, not sample data, since both
# the output schema and its formatting are read from it on every run.
REFERENCE_DIR = Path(__file__).resolve().parents[1] / "reference"

# Sheets views.py::generate_integration_script parses. Kept as a check so a
# template with a renamed tab fails here rather than deep inside script
# generation.
REQUIRED_SHEETS = ("Site_Basic", "Radio_HW", "LTE-CELL", "NR-CELL")

OUTPUT_NAME = "{site}_RF_Data_Scripting_Template_4G_5G_{circle}.xlsx"


@dataclass(frozen=True)
class TemplateSchema:
    path: Path
    sheets: dict[str, list[str]]      # sheet name -> column names, in order

    def columns(self, sheet: str) -> list[str]:
        return self.sheets[sheet]


def find_template(*folders: Path) -> Path:
    """The template workbook, searched through `folders` in order.

    Defaults to the app's reference/ folder. Any file matching the template name
    pattern will do - the shipped one is named for NWG007/RJ, but only its
    header rows and formatting are read, never its data.
    """
    candidates = [Path(f) for f in folders if f] or [REFERENCE_DIR]
    for folder in candidates:
        matches = [p for p in sorted(folder.glob(TEMPLATE_GLOB))
                   if not p.name.startswith("~$")]
        if matches:
            return matches[0]
    raise FileNotFoundError(
        f"No template matching {TEMPLATE_GLOB!r} in "
        f"{', '.join(str(c) for c in candidates)}. "
        "The converter reads its output schema and formatting from that file."
    )


def load_schema(path: Path) -> TemplateSchema:
    xl = pd.ExcelFile(path)
    sheets = {}
    for name in xl.sheet_names:
        raw = xl.parse(name, header=None, nrows=1, dtype=object)
        if raw.empty:
            continue
        cols = []
        for v in raw.iloc[0].tolist():
            if v is None or (isinstance(v, float) and pd.isna(v)):
                continue
            cols.append(re.sub(r"\s+", " ", str(v)).strip())
        if cols:
            sheets[name] = cols

    missing = [s for s in REQUIRED_SHEETS if s not in sheets]
    if missing:
        raise ValueError(
            f"Template {path.name} is missing sheet(s) {missing}. "
            f"LTE_Integration_Scripting_Automtion parses {list(REQUIRED_SHEETS)}."
        )
    return TemplateSchema(path=path, sheets=sheets)


def output_filename(site: str, circle: str) -> str:
    """'HY9532', 'AP' -> 'HY9532_RF_Data_Scripting_Template_4G_5G_AP.xlsx'.

    `site` is the site id, not a node name: 'LHY9532' is the LTE node and
    'AP-NLHY9532-1' the NR node, and the workbook covers both.
    """
    return OUTPUT_NAME.format(site=site.strip().upper(), circle=circle.strip().upper())
