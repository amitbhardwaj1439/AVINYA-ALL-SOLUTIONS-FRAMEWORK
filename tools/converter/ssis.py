"""Reading Ericsson SSIS / CCR workbooks.

Every 'S_*' sheet in these workbooks shares one skeleton::

    row 0   'Site Specific'  + free-text hints
    row 1   the MO path each column writes to
    row 2   the #Template name
    row 3   the real column names          <- header
    row 4+  one row per site

while the loose planning tabs ('Sheet1', 'RIM TAG') are ordinary tables with
their header on row 0. `Sheet.header_row` is decided by the row-0 marker rather
than by sniffing, because a mis-detected header silently shifts every value.

The wide sheets repeat a block of columns once per cell/sector/radio - 'cellId'
appears at c10, c24, c38 ... - so a column name alone does not identify a value.
`Sheet.occurrences()` returns every column carrying a given name, left to right,
and the Nth entry belongs to the Nth block. That indexing is used instead of
computing a block width because the blocks are not all the same size (the
antenna blocks in S_Site Equipment nest sub-blocks of differing length), while
'the Nth cellId goes with the Nth earfcndl' holds throughout.
"""
from __future__ import annotations

import hashlib
import itertools
import pickle
import re
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

# Row 0 carries this marker on the structured sheets, and nothing else does.
SITE_SPECIFIC_MARKER = "site specific"
STRUCTURED_HEADER_ROW = 3
MO_PATH_ROW = 1

# Columns that name the site. Column 0 holds it on almost every sheet; 'RIM TAG'
# is the exception - its column 0 is a cell name and the site sits in 'site id'.
# 'site_id' is the same key with an underscore: the VI RF database and IP plan
# spell it that way, and without it their first column ('OrderId', 'Circle')
# would be taken as the key and the sheet would contribute no sites.
KEY_COLUMN_NAMES = ("site id", "site_id", "2g site id")

# How many leading rows are examined to find the sheet's used width. Every
# layout here puts its header within the first four.
HEADER_SCAN_ROWS = 10

# Parsed workbooks are cached here, keyed by content, because reading a large
# .xlsb costs minutes and the same file is read on every request.
CACHE_DIR = Path(__file__).resolve().parents[1] / ".cache"
# Bumped when the parse changes shape: v2 added 'site_id' to KEY_COLUMN_NAMES,
# so workbooks cached under v1 carry the wrong key column.
CACHE_VERSION = 2


def clean(v) -> str | None:
    """Cell -> the text it means, or None when blank.

    Excel hands back floats for every number, so whole floats lose the '.0'
    that would otherwise reach the template as '19356.0'.
    """
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    s = str(v).replace("_x000D_", " ").replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s or None


@dataclass(frozen=True)
class Naming:
    """How a circle spells its node names, so they reduce to one site id.

    Circle knowledge, declared by the mapping module and carried here rather
    than guessed, because the same shape means different things per circle:
    AP's 'LHY9532' is a node prefix over the site 'HY9532', while HR's 'LOOK48'
    is the site id itself.
    """

    # AP: the 4G node is L + site id ('LHY9532' -> 'HY9532'). Off for HR, whose
    # ids are already bare and several genuinely begin with L.
    strip_node_prefix: bool = True

    # DEL: the site id is the bare number and every node spells it with its own
    # one- or two-letter prefix - 'LD47793' (L900/L1800/TDD node), 'LU47793'
    # (L2100 node), 'X47793' (2G node) - which all stand for site 47793. Off
    # elsewhere: AP's 'HY9532' is 1-2 letters + digits too, and stripping there
    # would merge every circle site sharing a number.
    numeric_site_ids: bool = False


DEFAULT_NAMING = Naming()


def naming(value) -> Naming:
    """Accept either a `Naming` or the plain bool this used to take."""
    return value if isinstance(value, Naming) else Naming(strip_node_prefix=bool(value))


def site_candidates(name, naming_rules=DEFAULT_NAMING) -> set[str]:
    """Every id a site name could stand for.

    The same AP site is written three ways - 'LHY9532' (4G SSIS), 'HY9532'
    (GSM / RIM TAG) and 'AP-NLHY9532-1' (5G CCR) - so a node name also stands
    for the bare site id, and two names refer to one site when their candidate
    sets overlap. DEL spells one site four ways as well, but numerically:
    'LD47793', 'LU47793' and 'X47793' all stand for 47793.

    `naming_rules` is circle knowledge, set by the mapping module; see `Naming`.
    """
    rules = naming(naming_rules)
    s = clean(name)
    if s is None:
        return set()
    s = s.upper()
    out = {s}
    m = re.fullmatch(r"[A-Z]{2}-N?L(.+?)-\d+", s)          # 5G: AP-NLHY9532-1
    if m:
        out.add(m.group(1))
    if rules.strip_node_prefix and re.fullmatch(r"L[A-Z]{2,4}\d[A-Z0-9]*", s):
        out.add(s[1:])                                      # 4G node: LHY9532
    m = re.fullmatch(r"[A-Z]{1,2}(\d{4,})", s)              # DEL node: LD47793
    if rules.numeric_site_ids and m:
        out.add(m.group(1))
    return out


def canonical_site(candidates) -> str | None:
    """The id to call a site, given every id its spellings reduce to.

    The shortest: 'HY9532' rather than the node names 'LHY9532' /
    'AP-NLHY9532-1', but 'LOOK48' in a circle whose ids are not prefixed, where
    'OOK48' is never a candidate in the first place.
    """
    values = {clean(c).upper() for c in candidates if clean(c)}
    return min(values, key=lambda v: (len(v), v)) if values else None


@dataclass(frozen=True)
class Column:
    index: int
    name: str
    mo: str | None          # MO path from row 1, absent on the loose tabs


@dataclass
class Sheet:
    workbook: str
    name: str
    header_row: int
    columns: list[Column]
    rows: list[list]
    key_index: int

    @property
    def structured(self) -> bool:
        return self.header_row == STRUCTURED_HEADER_ROW

    def occurrences(self, column_name: str) -> list[Column]:
        """Every column carrying `column_name`, left to right.

        The Nth entry belongs to the Nth repeated block (cell, sector, radio).
        Matched case-insensitively - the same field is spelled 'userLabel',
        'User Lable' and 'USER LABLE' across these files.
        """
        want = column_name.strip().lower()
        return [c for c in self.columns if c.name.strip().lower() == want]

    def has(self, column_name: str) -> bool:
        return bool(self.occurrences(column_name))

    @property
    def site_bearing(self) -> bool:
        """Whether this sheet's key column actually names sites.

        The master workbooks carry scratch tabs whose first column is a number
        or a date; without this they contribute '2', '45238' and the like to the
        site list.
        """
        key = next((c.name for c in self.columns if c.index == self.key_index), "")
        key = key.strip().lower()
        return "site" in key or "name" in key or key in ("4g id", "2g")

    def _row_name(self, r: list) -> str | None:
        return r[self.key_index] if self.key_index < len(r) else None

    def rows_for(self, candidates: set[str], naming_rules=DEFAULT_NAMING) -> list[list]:
        """Every data row whose site name shares an id with `candidates`."""
        if not self.site_bearing:
            return []
        return [r for r in self.rows
                if site_candidates(self._row_name(r), naming_rules) & candidates]

    def ids_for(self, candidates: set[str], naming_rules=DEFAULT_NAMING) -> set[str]:
        """Every id the names this sheet uses for that site reduce to."""
        out = set()
        for r in self.rows:
            keys = site_candidates(self._row_name(r), naming_rules)
            if keys & candidates:
                out |= keys
        return out

    def site_names(self) -> set[str]:
        """Every site name written on this sheet, verbatim."""
        if not self.site_bearing:
            return set()
        return {n.upper() for n in (self._row_name(r) for r in self.rows) if n}


@dataclass
class Workbook:
    path: Path
    sheets: list[Sheet] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)   # sheet name -> why

    @property
    def name(self) -> str:
        return self.path.name


def _key_index(columns: list[Column]) -> int:
    """Which column identifies the site.

    Column 0 on nearly every sheet; 'RIM TAG' keys on 'site id' because its
    column 0 holds a cell name, and matching on that would attach one cell's
    row to the whole site.
    """
    for c in columns:
        if c.name.strip().lower() in KEY_COLUMN_NAMES:
            return c.index
    return 0


def _looks_like_header(row: list) -> bool:
    """Whether a row reads as column names rather than as data.

    The SSIS sheets put their header on a known row, but the HR master
    workbooks lead with a formula/example row ('Formula', 'HR_BB1_Formula', 1.0,
    ...) and only put the real names on the row below. A header row is mostly
    non-numeric and mostly distinct, which separates the two reliably.
    """
    values = [v for v in row if v is not None]
    if len(values) < 4:
        return False
    numeric = 0
    for v in values:
        try:
            float(str(v).replace(",", ""))
            numeric += 1
        except ValueError:
            pass
    if numeric > len(values) * 0.3:
        return False
    return len({str(v).strip().lower() for v in values}) >= len(values) * 0.7


def _header_row(rows: list[list]) -> int:
    """Index of the header row.

    The 'Site Specific' marker pins the SSIS layout exactly; everything else is
    sniffed over the first few rows so a leading formula row does not become the
    header and shift every value by one.
    """
    marker = rows[0][0] if rows and rows[0] else None
    if marker and str(marker).strip().lower() == SITE_SPECIFIC_MARKER:
        return STRUCTURED_HEADER_ROW
    for i in range(min(3, len(rows))):
        if _looks_like_header(rows[i]):
            return i
    return 0


def _read_sheet(workbook_name: str, sheet_name: str, rows: list[list]) -> Sheet | None:
    if not rows:
        return None

    header_row = _header_row(rows)
    if len(rows) <= header_row:
        return None
    structured = header_row == STRUCTURED_HEADER_ROW

    header = rows[header_row]
    mo_row = rows[MO_PATH_ROW] if structured and len(rows) > MO_PATH_ROW else []

    columns = []
    for i, h in enumerate(header):
        if h is None:
            continue
        mo = mo_row[i] if i < len(mo_row) else None
        columns.append(Column(index=i, name=h, mo=mo))
    if not columns:
        return None

    body = [r for r in rows[header_row + 1:] if any(v is not None for v in r)]

    return Sheet(workbook=workbook_name, name=sheet_name, header_row=header_row,
                 columns=columns, rows=body, key_index=_key_index(columns))


def _rows_xlsx(path: Path, sheet_name: str, xl: pd.ExcelFile) -> list[list]:
    raw = xl.parse(sheet_name, header=None, dtype=object)
    if raw.empty or raw.shape[1] == 0:
        return []
    return [[clean(v) for v in r] for r in raw.itertuples(index=False, name=None)]


def _rows_xlsb(sheet) -> list[list]:
    """Rows of a .xlsb sheet, streamed.

    pyxlsb is read directly rather than through pandas, whose pyxlsb path is
    slower still.

    Some sheets carry whole-row formatting that materialises a cell record for
    every column out to Excel's limit: HR's 'RF Data Sheet' is 23,175 rows of
    16,382 cells with only 47 populated. Scanning every one of those 380M
    records costs minutes, so the used width is measured over the first rows -
    which is where every layout here puts its header - and later rows are sliced
    to it. A column past the header has no name and no rule can reference it, so
    nothing is lost by not reading it.

    The remaining cost is inside pyxlsb's own row iteration and cannot be
    avoided; `load_workbook` caches the parse so it is paid once per file.
    """
    rows = sheet.rows()
    head = []
    for row in rows:
        head.append(row)
        if len(head) >= HEADER_SCAN_ROWS:
            break

    width = 0
    for row in head:
        for c in row:
            if c.v is not None and c.v != "" and c.c >= width:
                width = c.c + 1
    if not width:
        return []

    out = []
    for row in itertools.chain(head, rows):
        values = [None] * width
        for c in row[:width]:
            values[c.c] = clean(c.v)
        out.append(values)
    return out


def _content_key(path: Path) -> str:
    """Cache key: the file's content, not its name or place.

    Hashed rather than stat'ed so the same workbook uploaded to a fresh job
    folder on every API call still hits the cache.
    """
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return f"{digest.hexdigest()}-v{CACHE_VERSION}"


def _parse_workbook(path: Path) -> Workbook:
    wb = Workbook(path=path)
    if path.suffix.lower() == ".xlsb":
        from pyxlsb import open_workbook as open_xlsb
        with open_xlsb(str(path)) as book:
            for sheet_name in book.sheets:
                with book.get_sheet(sheet_name) as sh:
                    rows = _rows_xlsb(sh)
                sheet = _read_sheet(path.name, sheet_name, rows)
                if sheet is not None:
                    wb.sheets.append(sheet)
        return wb

    xl = pd.ExcelFile(path)
    for sheet_name in xl.sheet_names:
        sheet = _read_sheet(path.name, sheet_name, _rows_xlsx(path, sheet_name, xl))
        if sheet is not None:
            wb.sheets.append(sheet)
    return wb


def _to_plain(wb: Workbook) -> dict:
    """Workbook -> plain builtins.

    Deliberately not a pickle of the dataclasses: this package is imported as
    'converter' by the CLI and as 'Converter.converter' by Django, so pickled
    instances written under one name fail to load under the other - and the
    failure path would delete the cache, leaving the two contexts destroying
    each other's work.
    """
    return {
        "name": wb.name,
        "sheets": [{
            "name": s.name,
            "header_row": s.header_row,
            "key_index": s.key_index,
            "columns": [(c.index, c.name, c.mo) for c in s.columns],
            "rows": s.rows,
        } for s in wb.sheets],
    }


def _from_plain(data: dict, path: Path) -> Workbook:
    wb = Workbook(path=path)
    for s in data["sheets"]:
        wb.sheets.append(Sheet(
            workbook=data["name"], name=s["name"], header_row=s["header_row"],
            columns=[Column(index=i, name=n, mo=m) for i, n, m in s["columns"]],
            rows=s["rows"], key_index=s["key_index"],
        ))
    return wb


def load_workbook(path: Path, use_cache: bool = True) -> Workbook:
    """Parse a workbook, reusing a cached parse of the same content.

    A circle-wide .xlsb takes minutes to read once and is read on every request,
    so the parsed sheets are cached on disk under the file's content hash - by
    content, not path, so the same workbook uploaded into a fresh job folder on
    each API call still hits it. Delete `Converter/.cache/` to force a re-read.
    """
    if not use_cache:
        return _parse_workbook(path)

    cache_file = CACHE_DIR / f"{_content_key(path)}.pkl"
    if cache_file.exists():
        try:
            with open(cache_file, "rb") as fh:
                return _from_plain(pickle.load(fh), path)
        except Exception:
            cache_file.unlink(missing_ok=True)   # unreadable or stale format

    wb = _parse_workbook(path)
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        tmp = cache_file.with_suffix(".tmp")
        with open(tmp, "wb") as fh:
            pickle.dump(_to_plain(wb), fh, protocol=pickle.HIGHEST_PROTOCOL)
        tmp.replace(cache_file)
    except Exception:
        pass                        # caching is an optimisation, never required
    return wb


def discover_inputs(folder: Path, template: Path | None = None) -> list[Path]:
    """Input workbooks in `folder`, newest last.

    Skips Excel's '~$' lock files - they are not readable while the workbook is
    open, and one appearing mid-run would otherwise abort the conversion - plus
    the template itself and anything already written to output/.

    Templates are excluded by name as well as by path: over the API the inputs
    are uploaded into a job folder, so a template uploaded along with them is a
    different file from the one supplying the schema and would otherwise be read
    as input.
    """
    out = []
    # .xls as well as .xlsx/.xlsb: DEL's CCR forms are still saved in the old
    # BIFF format, which pandas reads through xlrd.
    candidates = sorted(list(folder.glob("*.xlsx")) + list(folder.glob("*.xlsb"))
                        + list(folder.glob("*.xls")))
    for p in candidates:
        if p.name.startswith("~$") or p.name.startswith("."):
            continue
        if template is not None and p.resolve() == template.resolve():
            continue
        # Covers the reference template and any previously generated output,
        # both of which are template-shaped rather than input data.
        if "RF_Data_Scripting_Template" in p.name:
            continue
        out.append(p)
    return out
