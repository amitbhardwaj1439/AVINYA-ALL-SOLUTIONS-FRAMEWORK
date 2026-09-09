"""Everything the input workbooks hold about one site, in one object.

A site's data is scattered across several workbooks - the LTE SSIS carries the
cells and transport, the GSM SSIS the ABIS addressing, a per-sector delta file
the extra sector, the CCR the 5G side - so the mapping rules would otherwise
each have to know which file to look in. `SiteData` collects every sheet that
has a row for the site and exposes lookups by column name, letting a rule ask
for 'eNBId' without naming a workbook.

Where two workbooks disagree, the sheet whose values are read first wins, and
`SiteData.sources` records which sheet each value came from so the coverage
report can show it.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .ssis import (DEFAULT_NAMING, Sheet, Workbook, canonical_site,
                   load_workbook, site_candidates)


@dataclass
class SheetHit:
    """One sheet that carries rows for the site."""
    sheet: Sheet
    rows: list[list]

    @property
    def label(self) -> str:
        return f"{self.sheet.workbook}::{self.sheet.name}"


_SEGMENT_CACHE: dict[int, list[dict]] = {}


def _segments(sheet: Sheet) -> list[dict]:
    """Split a sheet's columns into the repeating blocks it is built from.

    A new block starts at the first column name already used in the block being
    built. That segments the sheet without knowing any block's width, which
    matters because the widths differ even within one sheet - the FDD cell block
    is 14 columns (it splits earfcn into dl/ul), the TDD block 13 - and because
    the trailing MO groups (noOfTxAntennas + sectorFunctionRef per sector, then
    the MME termpoints) are narrower again.

    Indexing by "the Nth occurrence of a name" cannot do this: it makes the Nth
    TDD cell read the Nth *FDD* cell's sectorCarrierRef, since both share one
    pool of columns.
    """
    cached = _SEGMENT_CACHE.get(id(sheet))
    if cached is not None:
        return cached

    blocks, current = [], {}
    for col in sheet.columns:
        key = col.name.strip().lower()
        if key in current:
            blocks.append(current)
            current = {}
        current[key] = col
    if current:
        blocks.append(current)

    _SEGMENT_CACHE[id(sheet)] = blocks
    return blocks


_WINDOW_CACHE: dict[tuple[int, str], list] = {}


def _anchor_windows(sheet: Sheet, anchor: str) -> list[tuple[dict, "Column"]]:
    """One fixed-width column window per repeat of `anchor`.

    `_segments` alone gets the last block wrong: a block only ends when a name
    repeats, so the final cell absorbs whatever follows it - on the RN sheet
    that is the per-sector `sectorFunctionRef` group, which handed the last cell
    another sector's name. The first block is inflated the same way by the
    sheet's Name/Node Type/#Template prefix.

    So the repeat is measured instead: the block size and the anchor's offset
    within it are taken from the blocks that agree (the middle ones, which no
    prefix or tail distorts), and every anchor is then given a window of exactly
    that shape. Sizes are measured per anchor name because one sheet mixes
    widths - the FDD cell block splits earfcn into dl/ul and so is one column
    wider than the TDD block beside it.
    """
    key = (id(sheet), anchor.strip().lower())
    cached = _WINDOW_CACHE.get(key)
    if cached is not None:
        return cached

    want = anchor.strip().lower()
    columns = sheet.columns
    positions = [i for i, c in enumerate(columns) if c.name.strip().lower() == want]

    # The gap between consecutive anchors is the block width, and is exact -
    # unlike the segment sizes, which the prefix and tail distort. With only one
    # anchor the sheet holds one block per row (the per-sector delta files), so
    # the whole row is the block.
    if len(positions) >= 2:
        gaps = [b - a for a, b in zip(positions, positions[1:])]
        size = max(set(gaps), key=gaps.count)
    else:
        size = len(columns)

    # Where the anchor sits inside its block, learned from the segments that
    # already have the block's width.
    lead = 0
    for block in _segments(sheet):
        col = block.get(want)
        if col is None or len(block) != size:
            continue
        start = min(columns.index(c) for c in block.values())
        lead = columns.index(col) - start
        break

    windows = []
    for p in positions:
        start = max(0, p - lead)
        window = {c.name.strip().lower(): c for c in columns[start:start + size]}
        # Never let a window that overlaps the next block hand back that
        # block's anchor: this repeat is defined by its own anchor column.
        window[want] = columns[p]
        windows.append((window, columns[p]))

    _WINDOW_CACHE[key] = windows
    return windows


@dataclass
class Block:
    """One cell / radio / MO instance, and the columns that describe it."""
    hit: SheetHit
    row: int
    columns: dict

    def get(self, column_name: str) -> str | None:
        """This block's value for `column_name`.

        Falls back to a sheet-wide value only when every populated occurrence of
        the name agrees - which covers the genuinely node-level fields (eNBId
        appears once; noOfTxAntennas is stated per sector but identically) while
        refusing to hand a cell another cell's value. Without that guard a TDD
        block, which has no 'earfcndl' of its own, would be given an FDD cell's.
        """
        key = column_name.strip().lower()
        r = self.hit.rows[self.row]
        col = self.columns.get(key)
        if col is not None:
            return r[col.index] if col.index < len(r) else None

        values = {r[c.index] for c in self.hit.sheet.occurrences(column_name)
                  if c.index < len(r) and r[c.index] is not None}
        return values.pop() if len(values) == 1 else None


@dataclass
class SiteData:
    key: str                       # normalised site id, e.g. HY9532
    requested: str                 # what the user typed
    hits: list[SheetHit] = field(default_factory=list)
    sources: dict[str, str] = field(default_factory=dict)

    # -- discovery ---------------------------------------------------------

    def sheets_matching(self, *name_fragments: str) -> list[SheetHit]:
        """Hits whose sheet name contains any fragment (case-insensitive).

        Sheet names vary per file - 'S_RN', 'S_RN - 3 sector_FD+TD+FD900_20M',
        'S_RN_1-N_Sec' are all the radio-network sheet - so rules select by
        fragment rather than by exact name.

        Ordered by the fragment that matched, so a rule can express preference:
        HR's 'Script Data' and 'Ericcson Shared Data' describe the same cells
        but disagree (one names the Ericsson eNB, the other ZTE's), and the
        first-listed fragment should win.
        """
        want = [f.lower() for f in name_fragments]
        ranked = []
        for hit in self.hits:
            name = hit.sheet.name.lower()
            rank = next((i for i, f in enumerate(want) if f in name), None)
            if rank is not None:
                ranked.append((rank, len(ranked), hit))
        return [h for _, _, h in sorted(ranked, key=lambda t: (t[0], t[1]))]

    def sheets_with(self, column_name: str) -> list[SheetHit]:
        """Hits whose sheet carries `column_name`."""
        return [h for h in self.hits if h.sheet.has(column_name)]

    # -- value lookup ------------------------------------------------------

    def value(self, column_name: str, occurrence: int = 0,
              sheet_fragments: tuple[str, ...] = (), row: int = 0,
              record_as: str | None = None) -> str | None:
        """First non-empty value for `column_name`.

        `occurrence` picks which repeat of the column to read - the Nth block
        on a wide sheet. `sheet_fragments` restricts the search to sheets whose
        name matches, for fields that appear in more than one file with
        different meanings.
        """
        pool = self.sheets_matching(*sheet_fragments) if sheet_fragments else self.hits
        for hit in pool:
            cols = hit.sheet.occurrences(column_name)
            if occurrence >= len(cols) or row >= len(hit.rows):
                continue
            col = cols[occurrence]
            r = hit.rows[row]
            if col.index >= len(r):
                continue
            v = r[col.index]
            if v is not None:
                self.sources[record_as or column_name] = hit.label
                return v
        return None

    def value_by_mo(self, mo_pattern: str, sheet_fragments: tuple[str, ...] = (),
                    row: int = 0, record_as: str | None = None) -> str | None:
        """First value whose MO path matches `mo_pattern`.

        The transport columns are all named 'address' or 'vlanId' and are told
        apart only by the MO they write to - Router(1) vs Router(2), the
        interface address vs the route's next hop - so they are selected on the
        MO path rather than on name and position.
        """
        rx = re.compile(mo_pattern, re.IGNORECASE)
        pool = self.sheets_matching(*sheet_fragments) if sheet_fragments else self.hits
        for hit in pool:
            if row >= len(hit.rows):
                continue
            r = hit.rows[row]
            for col in hit.sheet.columns:
                if not col.mo or not rx.search(col.mo):
                    continue
                if col.index < len(r) and r[col.index] is not None:
                    self.sources[record_as or mo_pattern] = hit.label
                    return r[col.index]
        return None

    def occurrence_count(self, column_name: str,
                         sheet_fragments: tuple[str, ...] = ()) -> int:
        """How many repeats of `column_name` carry a value for this site.

        This is what decides how many cells / radios to emit: the template needs
        one output row per block, and trailing blocks are frequently empty
        because the sheet is sized for the largest configuration in the circle.
        """
        pool = self.sheets_matching(*sheet_fragments) if sheet_fragments else self.hits
        total = 0
        for hit in pool:
            for n, col in enumerate(hit.sheet.occurrences(column_name)):
                for r in hit.rows:
                    if col.index < len(r) and r[col.index] is not None:
                        total += 1
                        break
        return total

    def blocks(self, anchor: str, sheet_fragments: tuple[str, ...] = ()):
        """Yield a `Block` for every populated repeat of `anchor`.

        A 'block' is one cell, one radio or one MO instance. The sheets carry
        them horizontally (repeated column groups, one row per site) and
        vertically (one row per cell, as in the 4th-sector delta files), so both
        are walked and the anchor decides whether a block holds data.
        """
        pool = self.sheets_matching(*sheet_fragments) if sheet_fragments else self.sheets_with(anchor)
        for hit in pool:
            windows = _anchor_windows(hit.sheet, anchor)
            for ri, r in enumerate(hit.rows):
                for columns, col in windows:
                    if col.index < len(r) and r[col.index] is not None:
                        yield Block(hit=hit, row=ri, columns=columns)

    def block_value(self, block: "Block", column_name: str) -> str | None:
        return block.get(column_name)


def collect(site: str, inputs: list[Path],
            naming_rules=DEFAULT_NAMING) -> tuple[SiteData, list[Workbook]]:
    """Load every input workbook and gather the sheets holding `site`."""
    candidates = site_candidates(site, naming_rules)
    if not candidates:
        raise ValueError(f"Could not read a site name from {site!r}")

    workbooks, hits, ids = [], [], set(candidates)
    for path in inputs:
        wb = load_workbook(path)
        workbooks.append(wb)
        for sheet in wb.sheets:
            rows = sheet.rows_for(candidates, naming_rules)
            if rows:
                hits.append(SheetHit(sheet=sheet, rows=rows))
                ids |= sheet.ids_for(candidates, naming_rules)

    data = SiteData(key=canonical_site(ids) or site.upper(), requested=site)
    data.hits = hits
    return data, workbooks


def available_sites(workbooks: list[Workbook],
                    naming_rules=DEFAULT_NAMING) -> set[str]:
    """One id per site across every workbook.

    Spellings are grouped by shared id first, so a site written three ways is
    listed once, under the id the others reduce to.
    """
    names = set()
    for wb in workbooks:
        for sheet in wb.sheets:
            names |= sheet.site_names()

    groups: dict[str, set[str]] = {}
    for name in names:
        keys = site_candidates(name, naming_rules)
        merged = set(keys)
        for existing in [k for k, v in groups.items() if v & keys]:
            merged |= groups.pop(existing)
        for k in merged:
            groups[k] = merged

    return {canonical_site(g) for g in {frozenset(v) for v in groups.values()}}
