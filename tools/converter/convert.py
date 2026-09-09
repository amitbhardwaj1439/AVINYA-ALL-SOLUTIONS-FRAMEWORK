"""Orchestration: site + circle + input folder -> one template workbook.

`convert_site()` is the whole public API and takes no Django objects, so
LTE_Integration_Scripting_Automtion can call it from a view later by handing
over the uploaded files' paths.
"""
from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from . import template as tpl
from .sitedata import SiteData, available_sites, collect
from .ssis import Naming, discover_inputs, site_candidates
from .writer import write_workbook

# circle -> mapping module, named relative to this package so the same code
# imports cleanly whether it is reached as 'converter' (the CLI puts the folder
# on sys.path) or as 'Converter.converter' (the Django app). One module per
# circle because the source documents themselves differ, not just the column
# spellings: AP delivers wide SSIS exports, HR circle-wide master RF data, DEL
# tall SSIS exports with two 4G nodes per site.
MAPPINGS = {"AP": ".mapping_ap", "HR": ".mapping_hr", "DEL": ".mapping_del",
            "DEL_VI": ".mapping_del_vi", "MAG_VI": ".mapping_mag_vi"}


def _naming(mapping) -> Naming:
    """How this circle's mapping says its node names spell the site id."""
    return Naming(
        strip_node_prefix=bool(getattr(mapping, "STRIP_NODE_PREFIX", True)),
        numeric_site_ids=bool(getattr(mapping, "NUMERIC_SITE_IDS", False)),
    )


def naming_for(circle: str) -> Naming:
    """`Naming` for a circle, for callers that list sites before converting."""
    try:
        return _naming(_load_mapping(circle))
    except UnknownCircle:
        return Naming()


class UnknownCircle(Exception):
    pass


class SiteNotFound(Exception):
    pass


@dataclass
class ColumnCoverage:
    sheet: str
    column: str
    filled: int
    total: int
    note: str = ""

    @property
    def state(self) -> str:
        if self.total == 0:
            return "no rows"
        if self.filled == self.total:
            return "filled"
        return "empty" if self.filled == 0 else f"{self.filled}/{self.total} rows"

    @property
    def is_gap(self) -> bool:
        """True only when no row got a value.

        A partly-filled column is normal rather than a gap: Site_Basic carries
        one row per node, so the 4G transport columns are empty on the 5G row
        and vice versa, and TDD cells have no earfcnul.
        """
        return self.total > 0 and self.filled == 0

    @property
    def is_partial(self) -> bool:
        return 0 < self.filled < self.total


@dataclass
class ConversionResult:
    site: str                      # the site id, e.g. HY9532
    circle: str
    output: Path
    rows: dict[str, int]
    requested: str = ""            # what the caller passed, if it differed
    coverage: list[ColumnCoverage] = field(default_factory=list)
    sources: dict[str, str] = field(default_factory=dict)

    def report(self) -> str:
        asked = (f"   (from {self.requested})"
                 if self.requested and self.requested.upper() != self.site else "")
        lines = [
            f"site   : {self.site}{asked}   circle: {self.circle}",
            f"output : {self.output}",
            "",
            "rows written:",
        ]
        for sheet, n in self.rows.items():
            lines.append(f"  {sheet:<12} {n}")

        lines += ["", "coverage:"]
        for sheet in self.rows:
            cov = [c for c in self.coverage if c.sheet == sheet]
            gaps = [c for c in cov if c.is_gap]
            partial = [c for c in cov if c.is_partial]
            if not self.rows[sheet]:
                why = next((c.note for c in cov if c.note), "")
                lines.append(f"  {sheet} - no rows"
                             + (f" - {why}" if why else
                                " (site has no data of this kind)"))
                continue
            lines.append(f"  {sheet} - {len(cov) - len(gaps)}/{len(cov)} columns carry data")
            for c in gaps:
                note = f"  - {c.note}" if c.note else ""
                lines.append(f"      EMPTY  {c.column:<26}{note}")
            for c in partial:
                lines.append(f"      part   {c.column:<26}  {c.state}")
        return "\n".join(lines)


def _load_mapping(circle: str):
    circle = circle.strip().upper()
    if circle not in MAPPINGS:
        raise UnknownCircle(
            f"No mapping for circle {circle!r}. Available: {sorted(MAPPINGS)}. "
            "Add one by copying converter/mapping_ap.py."
        )
    return importlib.import_module(MAPPINGS[circle], package=__package__)


def _frame(columns: list[str], rows: list[dict]) -> pd.DataFrame:
    """Rows as a frame with exactly the template's columns, in order."""
    return pd.DataFrame([{c: r.get(c) for c in columns} for r in rows],
                        columns=columns)


def _coverage(sheet: str, columns: list[str], df: pd.DataFrame,
              unmapped: dict) -> list[ColumnCoverage]:
    out = []
    for c in columns:
        filled = int(df[c].notna().sum()) if len(df) else 0
        notes = unmapped.get(sheet, {})
        # '*' gives one reason for a whole sheet, for circles whose inputs
        # cannot fill it at all.
        out.append(ColumnCoverage(sheet=sheet, column=c, filled=filled,
                                  total=len(df),
                                  note=notes.get(c) or notes.get("*", "")))
    return out


def convert_site(site: str, circle: str, input_folder: Path,
                 output_folder: Path | None = None,
                 template_path: Path | None = None) -> ConversionResult:
    """Convert one site's data into the integration-script template.

    `input_folder` is scanned for every .xlsx except the template and Excel's
    '~$' lock files, so adding another SSIS file for the circle needs no
    argument change.
    """
    input_folder = Path(input_folder)
    # reference/ first: over the API the inputs are uploaded into a job folder
    # that has no template, and a template uploaded alongside them is not the
    # fixture this app formats its output from.
    template_path = (Path(template_path) if template_path
                     else tpl.find_template(tpl.REFERENCE_DIR, input_folder))
    schema = tpl.load_schema(template_path)
    mapping = _load_mapping(circle)

    inputs = discover_inputs(input_folder, template=template_path)
    if not inputs:
        raise FileNotFoundError(f"No input workbooks found in {input_folder}")

    rules = _naming(mapping)
    data, workbooks = collect(site, inputs, rules)
    if not data.hits:
        known = sorted(available_sites(workbooks, rules))
        raise SiteNotFound(
            f"Site {site!r} (matched as {sorted(site_candidates(site, rules))}) is not in any input "
            f"workbook in {input_folder}.\nSites present: {known}"
        )

    output_folder = Path(output_folder) if output_folder else input_folder / "output"
    output_folder.mkdir(parents=True, exist_ok=True)
    # Named for the site id, never for whatever spelling the caller used:
    # 'LHY9532' is the LTE node and 'AP-NLHY9532-1' the NR node, so naming the
    # file after either would label a site-level artefact with one node's name.
    out_path = output_folder / tpl.output_filename(data.key, circle)

    sheet_rows, sheet_columns, coverage, row_counts = {}, {}, [], {}
    for sheet in tpl.REQUIRED_SHEETS:
        columns = schema.columns(sheet)
        rows = mapping.BUILDERS[sheet](data)
        sheet_rows[sheet] = rows
        sheet_columns[sheet] = columns
        row_counts[sheet] = len(rows)
        coverage += _coverage(sheet, columns, _frame(columns, rows),
                              mapping.UNMAPPED)

    # Written by cloning the template so its colours, fonts, borders, column
    # widths and freeze panes carry over; pandas' writer would drop all of it.
    write_workbook(template_path, out_path, sheet_rows, sheet_columns)

    return ConversionResult(site=data.key, requested=site, circle=circle.upper(),
                            output=out_path, rows=row_counts, coverage=coverage,
                            sources=dict(data.sources))
