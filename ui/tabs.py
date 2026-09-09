"""The four tools, one class each.

Every tab exposes the same contract so the shell can drive any of them:

    build(parent)      -> lay the inputs out
    validate()         -> raise ValueError with a message the user can act on
    collect()          -> read the widgets into plain values
    run(params, log)   -> do the work, return a Result

`build`, `validate` and `collect` run on the UI thread; `run` runs on a worker
thread and must never touch a widget. Tk raises "main thread is not in main
loop" if a StringVar is read off the main thread, which is why `collect` exists
as a separate step rather than `run` reading the fields itself. Anything `run`
wants on screen goes through `log`, and its Result carries the artifact the
shell offers to open or save.

Every tool writes to the user's Downloads folder; none of them ask where to
put their output.
"""
from __future__ import annotations

import asyncio
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

import customtkinter as ctk

from .paths import downloads_dir
from .widgets import (ACCENT, BLUE_BRIGHT, SELECT, TEXT_DIM, FilePanel,
                      LabeledCombo, PathRow)

# The LTE generator's circles are the branches its runner actually implements.
LTE_CIRCLES = ["KK", "TN", "CHN", "AP", "RJ", "NE", "AS", "DEL", "DEL_Vi",
               "MAG_Vi", "UPW", "HR", "JK"]

EXCEL_PATTERNS = [("Excel files", "*.xlsx *.xlsb *.xlsm *.xls"), ("All files", "*.*")]


@dataclass
class Result:
    """What a finished run leaves behind."""

    message: str
    artifact: Path | None = None      # file offered via Save output as... / Open


class ToolTab:
    name = "Tool"
    description = ""
    run_label = "Run"

    def build(self, parent) -> None:
        raise NotImplementedError

    def validate(self) -> None:
        """Raise ValueError if the inputs are not runnable yet. UI thread."""

    def collect(self) -> dict:
        """Snapshot the widgets into plain values. UI thread."""
        return {}

    def run(self, params: dict, log) -> Result:
        """Do the work. Worker thread - no widget access."""
        raise NotImplementedError

    @staticmethod
    def _header(parent, text: str) -> None:
        ctk.CTkLabel(parent, text=text, anchor="w", justify="left",
                     text_color=TEXT_DIM, font=ctk.CTkFont(size=12)).pack(
                         fill="x", padx=4, pady=(0, 8))

    @staticmethod
    def _output_note(parent) -> None:
        """Pin the output-folder line to the bottom of the tab.

        Packed with side="bottom" and called BEFORE the file panel: a panel
        packed with expand=True claims whatever is left, so anything added
        after it gets squeezed to nothing. Reserving the fixed rows first is
        what keeps this line and the circle selector visible.
        """
        ctk.CTkLabel(parent, text=f"Output folder:  {downloads_dir()}", anchor="w",
                     text_color=TEXT_DIM, font=ctk.CTkFont(size=11)).pack(
                         side="bottom", fill="x", padx=4, pady=(8, 2))


class GplAuditTab(ToolTab):
    """PRE/POST log comparison - the tool this app started life as."""

    name = "GPL Audit"
    description = ("Compare PRE and POST node logs and produce the GPL audit workbook "
                   "plus correction scripts.")
    run_label = "Run Audit"

    def build(self, parent) -> None:
        self._header(parent, self.description)
        # No circle selector: the node name in the logs already starts with the
        # circle, so the audit reads it rather than asking.
        self._output_note(parent)

        panels = ctk.CTkFrame(parent, fg_color="transparent")
        panels.pack(fill="both", expand=True)
        self.pre = FilePanel(panels, "PRE logs")
        self.pre.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.post = FilePanel(panels, "POST logs")
        self.post.pack(side="left", fill="both", expand=True, padx=(5, 0))

    def validate(self) -> None:
        if not self.pre.get_files():
            raise ValueError("Add at least one PRE log file.")
        if not self.post.get_files():
            raise ValueError("Add at least one POST log file.")

    def collect(self) -> dict:
        return {"pre": self.pre.get_files(), "post": self.post.get_files(),
                "out_dir": downloads_dir()}

    def run(self, params: dict, log) -> Result:
        # These are contextvars and do NOT inherit into a new thread, so they
        # must be set here, on the thread that will read them back.
        from tools.gpl_audit.log_parser.config import (
            set_output_file, set_post_files, set_pre_files)
        from tools.gpl_audit.main import main as run_audit

        set_pre_files(params["pre"])
        set_post_files(params["post"])
        # main() takes only the parent from this; it names the file itself.
        set_output_file(params["out_dir"] / "GPL_AUDIT.xlsx")
        zip_path = Path(asyncio.run(run_audit()))
        return Result("Audit complete - " + zip_path.name, zip_path)


class GplParserTab(ToolTab):
    """Parse-only: log files straight to Excel, no PRE/POST pairing.

    The desktop face of gpl_audit_tool_V2's /parse/ endpoint.
    """

    name = "GPL Parser"
    description = ("Extract the raw parameters from one set of node logs into a workbook. "
                   "No PRE/POST comparison and no audit verdict - just the parsed data.")
    run_label = "Parse Files"

    def build(self, parent) -> None:
        self._header(parent, self.description)
        self._output_note(parent)
        self.inputs = FilePanel(parent, "Log files")
        self.inputs.pack(fill="both", expand=True)

    def validate(self) -> None:
        if not self.inputs.get_files():
            raise ValueError("Add at least one log file to parse.")

    def collect(self) -> dict:
        return {"files": self.inputs.get_files(), "out_dir": downloads_dir()}

    def run(self, params: dict, log) -> Result:
        # The parse pipeline reads its input through get_pre_files(); there is
        # no POST side. Same wiring the /parse/ endpoint uses.
        from tools.gpl_audit.log_parser.config import set_output_file, set_pre_files
        from tools.gpl_audit.main import main_parse_only

        set_pre_files(params["files"])
        set_output_file(params["out_dir"] / "PARSED.xlsx")
        excel_path = Path(asyncio.run(main_parse_only()))
        return Result("Parsed - " + excel_path.name, excel_path)


class GplReferenceTab(ToolTab):
    """Audit node logs against the golden-parameter reference workbooks."""

    name = "GPL Reference Audit"
    description = ("Audit node logs against the LTE/NR golden parameter references. "
                   "The circle selects which reference sheet is used.")
    run_label = "Run Reference Audit"

    def build(self, parent) -> None:
        self._header(parent, self.description)
        self._output_note(parent)
        self.circle = LabeledCombo(parent, "Circle", self._circles(), "")
        self.circle.pack(side="bottom", fill="x", pady=(8, 0))

        self.inputs = FilePanel(parent, "Node logs")
        self.inputs.pack(fill="both", expand=True)

    @staticmethod
    def _circles() -> list[str]:
        """Circles the reference workbooks actually carry a sheet for.

        Read from the workbooks themselves rather than hardcoded, so adding an
        'LTE <CIRCLE>' sheet to the reference file is all it takes to offer it.
        """
        from tools.gpl_reference.log_parser.reference import list_available_circles
        try:
            return sorted(list_available_circles()) or [""]
        except Exception:                             # noqa: BLE001 - missing/locked workbook
            return [""]

    def validate(self) -> None:
        if not self.inputs.get_files():
            raise ValueError("Add at least one node log file.")
        if not self.circle.get():
            raise ValueError("Select a circle - it decides which reference sheet is used.")

    def collect(self) -> dict:
        return {"inputs": self.inputs.get_files(), "circle": self.circle.get(),
                "out_dir": downloads_dir()}

    def run(self, params: dict, log) -> Result:
        from tools.gpl_reference.log_parser.config import (
            set_circle, set_input_files, set_output_file)
        from tools.gpl_reference.main import main as run_reference

        set_input_files(params["inputs"])
        set_circle(params["circle"])
        set_output_file(params["out_dir"] / "GPL_REFERENCE_AUDIT.xlsx")
        zip_path = Path(asyncio.run(run_reference()))
        return Result("Reference audit complete - " + zip_path.name, zip_path)


class ConverterTab(ToolTab):
    """RF database / SSIS workbooks -> the integration script template."""

    name = "Converter"
    description = ("Turn a circle's RF database and IP plan into the filled "
                   "RF_Data_Scripting_Template for one site.")
    run_label = "Convert Site"

    def build(self, parent) -> None:
        self._header(parent, self.description)
        from tools.converter.convert import MAPPINGS
        circles = sorted(MAPPINGS)
        self.circle = LabeledCombo(parent, "Circle", circles, circles[0])
        self.circle.pack(fill="x", pady=(0, 6))

        # Fixed rows reserved from the bottom up, then the file list expands.
        self._output_note(parent)

        # Site id and its lookup share a row - the tab has enough fixed rows
        # already, and every one of them steals height from the file list.
        self._sites_label = ctk.CTkLabel(parent, text="", anchor="w", text_color=TEXT_DIM)
        self._sites_label.pack(side="bottom", fill="x", padx=4, pady=(2, 0))

        self.site = PathRow(parent, "Site id", mode="text",
                            action=("List sites", self._list_sites))
        self.site.pack(side="bottom", fill="x", pady=(6, 0))

        self.inputs = FilePanel(parent, "Input files  (RF database, IP plan, SSIS/CCR)",
                                patterns=EXCEL_PATTERNS)
        self.inputs.pack(fill="both", expand=True)

    @staticmethod
    def _stage(files: list[Path]) -> Path:
        """convert_site() scans a folder, so gather the chosen files into one.

        Copied rather than linked: the sources may sit on different drives or
        network shares, and the parse reads them repeatedly.
        """
        staged = Path(tempfile.mkdtemp(prefix="avinya_convert_"))
        for f in files:
            shutil.copy2(f, staged / f.name)
        return staged

    def _list_sites(self) -> None:
        """A site is spelled differently in each source; show the normalised ids."""
        from tkinter import messagebox
        try:
            from tools.converter.convert import naming_for
            from tools.converter.sitedata import available_sites
            from tools.converter.ssis import load_workbook
            files = self.inputs.get_files()
            if not files:
                raise ValueError("Add the input files first.")
            books = [load_workbook(p) for p in files]
            sites = sorted(available_sites(books, naming_for(self.circle.get())))
            shown = ", ".join(sites[:8]) + (" ..." if len(sites) > 8 else "")
            self._sites_label.configure(text=f"{len(sites)} site(s): {shown}")
            if sites and not self.site.get():
                self.site.var.set(sites[0])
        except Exception as exc:                      # noqa: BLE001 - shown to the user
            messagebox.showerror("Could not list sites", str(exc))

    def validate(self) -> None:
        if not self.inputs.get_files():
            raise ValueError("Add the RF database / IP plan files.")
        if not self.site.get():
            raise ValueError("Enter a site id - use 'List sites' if you are unsure.")

    def collect(self) -> dict:
        return {"circle": self.circle.get(), "site": self.site.get(),
                "files": self.inputs.get_files(), "out_dir": downloads_dir()}

    def run(self, params: dict, log) -> Result:
        from tools.converter.convert import convert_site
        staged = self._stage(params["files"])
        try:
            res = convert_site(params["site"], params["circle"], staged, params["out_dir"])
        finally:
            shutil.rmtree(staged, ignore_errors=True)
        # report() covers rows written and per-column coverage - worth showing.
        for line in res.report().splitlines():
            log(line)
        path = Path(res.output)
        return Result(f"Converted {res.site} ({res.circle}) - {path.name}", path)


class IntegrationScriptingTab(ToolTab):
    """Integration workbook -> commissioning + integration scripts, zipped."""

    name = "Integration Scripting"
    description = ("Generate integration and commissioning scripts for every node in an "
                   "integration workbook, packaged as a zip.")
    run_label = "Generate Scripts"

    def build(self, parent) -> None:
        self._header(parent, self.description)
        self.workbook = PathRow(parent, "Integration file", mode="open",
                                patterns=EXCEL_PATTERNS)
        self.workbook.pack(fill="x", pady=(0, 6))

        self.circle = LabeledCombo(parent, "Circle", LTE_CIRCLES, "KK")
        self.circle.pack(fill="x", pady=(0, 6))

        from tools.lte.runner import DEFAULT_TEMPLATE
        self.template = PathRow(parent, "Validation template", mode="open",
                                initial=str(DEFAULT_TEMPLATE),
                                patterns=[("Excel files", "*.xlsx")])
        self.template.pack(fill="x")
        self._output_note(parent)

    def validate(self) -> None:
        workbook = self.workbook.get()
        if not workbook or not Path(workbook).is_file():
            raise ValueError("Choose the filled integration workbook.")
        if not self.circle.get():
            raise ValueError("Select a circle.")

    def collect(self) -> dict:
        return {"workbook": self.workbook.get(), "circle": self.circle.get(),
                "out_dir": str(downloads_dir()), "template": self.template.get() or None}

    def run(self, params: dict, log) -> Result:
        from tools.lte.runner import generate_integration_scripts
        res = generate_integration_scripts(
            params["workbook"], params["circle"], params["out_dir"],
            template_path=params["template"])
        zip_path = Path(res["zip_path"])
        log(f"Site {res['site_id']} - scripts written to {res['scripts_dir']}")
        return Result(f"{res['message']} ({zip_path.name})", zip_path)


ALL_TABS: list[type[ToolTab]] = [GplParserTab, GplAuditTab, GplReferenceTab,
                                 ConverterTab, IntegrationScriptingTab]
