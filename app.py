"""Avinya All Solutions - one desktop front end for the four RAN tools.

Each tool keeps its own inputs on its own tab, but they share the run button,
the status line and the log console at the bottom, so a run looks the same
whichever tool produced it. Everything runs in this process: no Django, no
web server and no database are involved.

    python app.py
"""
from __future__ import annotations

import logging
import os
import queue
import shutil
import subprocess
import sys
import threading
import tkinter as tk
import traceback
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

# Importing a tool must work no matter where the app is launched from.
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from ui.tabs import ALL_TABS, Result  # noqa: E402
from ui.widgets import (ACCENT, ACCENT_HOVER, BG_APP, BG_CARD, BG_LIST,  # noqa: E402
                        BLUE_BRIGHT, ERR, GOLD_DEEP, MUTED, MUTED_HOVER, OK,
                        SELECT, TEXT, TEXT_DIM, WARN)

APP_NAME = "Avinya All Solutions"
TAGLINE = "Innovate  •  Automate  •  Elevate"
ASSETS = APP_DIR / "assets"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class _QueueHandler(logging.Handler):
    """Logging handler that pushes formatted records into a queue."""

    def __init__(self, q: queue.Queue):
        super().__init__()
        self.q = q

    def emit(self, record: logging.LogRecord) -> None:
        self.q.put(self.format(record))


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self._size_to_screen(preferred=(1080, 880), smallest=(900, 620))
        self.configure(fg_color=BG_APP)
        self._set_window_icon()

        self._log_queue: queue.Queue = queue.Queue()
        self._artifact: Path | None = None
        self._artifact_display = tk.StringVar(value="Nothing generated yet.")
        self._busy = False

        self._tabs: dict[str, object] = {}
        self._setup_logging()
        self._build_ui()
        self._poll_logs()

    # ------------------------------------------------------------------ setup

    def _size_to_screen(self, preferred: tuple[int, int], smallest: tuple[int, int]) -> None:
        """Open at `preferred`, but never taller or wider than the screen.

        CustomTkinter geometry is in logical pixels while winfo_screen* report
        physical ones, so on a scaled display (150% here) a fixed size can open
        a window taller than the monitor and push the Run button behind the
        taskbar. The margin leaves room for the taskbar and title bar.
        """
        try:
            scaling = ctk.ScalingTracker.get_window_scaling(self)
        except Exception:                             # noqa: BLE001 - older customtkinter
            scaling = 1.0
        avail_w = int(self.winfo_screenwidth() / scaling) - 40
        avail_h = int(self.winfo_screenheight() / scaling) - 90

        width = max(min(preferred[0], avail_w), 640)
        height = max(min(preferred[1], avail_h), 480)
        self.geometry(f"{width}x{height}")
        self.minsize(min(smallest[0], width), min(smallest[1], height))

    def _set_window_icon(self) -> None:
        """Title bar and taskbar icon. Never fatal - it is decoration."""
        try:
            icon = ASSETS / "avinya.ico"
            if icon.exists():
                self.iconbitmap(default=str(icon))
        except Exception:                             # noqa: BLE001 - e.g. no window manager
            pass

    def _load_mark(self, height: int):
        """The logo emblem for the title bar, or None if it cannot be loaded.

        Pillow ships with customtkinter, but the app must still start if the
        asset is missing from a trimmed-down copy.
        """
        try:
            from PIL import Image
            path = ASSETS / "avinya_mark.png"
            if not path.exists():
                return None
            img = Image.open(path)
            width = round(img.width * height / img.height)
            return ctk.CTkImage(light_image=img, dark_image=img, size=(width, height))
        except Exception:                             # noqa: BLE001 - decoration only
            return None

    def _setup_logging(self) -> None:
        handler = _QueueHandler(self._log_queue)
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S"))
        root_log = logging.getLogger()
        root_log.setLevel(logging.INFO)
        # Each tool calls logging.basicConfig at import time, which adds its own
        # StreamHandler. Replace the lot so output lands in the GUI console only.
        root_log.handlers.clear()
        root_log.addHandler(handler)

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Title bar sits on the logo's own backdrop so the mark has no visible
        # edge - the emblem's PNG background and BG_APP are the same colour.
        title_bar = ctk.CTkFrame(self, fg_color=BG_APP, corner_radius=0, height=64)
        title_bar.grid(row=0, column=0, sticky="ew")
        title_bar.grid_propagate(False)

        brand = ctk.CTkFrame(title_bar, fg_color="transparent")
        brand.pack(side="left", padx=(16, 0), pady=6)

        self._mark = self._load_mark(46)
        if self._mark is not None:
            ctk.CTkLabel(brand, image=self._mark, text="").pack(side="left", padx=(0, 14))

        words = ctk.CTkFrame(brand, fg_color="transparent")
        words.pack(side="left")
        ctk.CTkLabel(words, text="AVINYA", text_color=ACCENT, anchor="w",
                     font=ctk.CTkFont(size=19, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(words, text=TAGLINE, text_color=SELECT, anchor="w",
                     font=ctk.CTkFont(size=11)).pack(anchor="w")

        ctk.CTkLabel(title_bar, text="RAN audit, conversion and scripting tools",
                     text_color=TEXT_DIM).pack(side="right", padx=22)

        # A gold hairline under the header, echoing the logo's horizon line.
        ctk.CTkFrame(self, fg_color=GOLD_DEEP, corner_radius=0, height=2).grid(
            row=0, column=0, sticky="sew")

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=14, pady=(12, 0))
        content.grid_columnconfigure(0, weight=1)
        # The floor is sized for the busiest tab (Converter: circle, file list,
        # site id, hint line, output note). Without it the file list is the
        # only widget that can give, and it collapses to nothing.
        # Modest floors: this display gives the app only ~530 logical px of height
        # at 150% scaling, so a large floor would push the log or the run bar
        # off-screen. The tab body scrolls, so it copes with the remainder.
        content.grid_rowconfigure(0, weight=6, minsize=200)
        content.grid_rowconfigure(1, weight=2, minsize=90)

        # The ribbon blue marks the active tool. A segmented button shares one
        # text colour across every segment, so a gold selection would force
        # dark text on the unselected tabs too and make them unreadable; gold
        # stays on the Run button, where it means "this starts work".
        self.tabview = ctk.CTkTabview(
            content, fg_color=BG_CARD, border_color=MUTED, border_width=1,
            segmented_button_fg_color=BG_LIST,
            segmented_button_selected_color=SELECT,
            segmented_button_selected_hover_color=BLUE_BRIGHT,
            segmented_button_unselected_color=BG_LIST,
            segmented_button_unselected_hover_color=MUTED_HOVER,
            text_color=TEXT, command=self._on_tab_change)
        self.tabview.grid(row=0, column=0, sticky="nsew")
        for tab_cls in ALL_TABS:
            tool = tab_cls()
            frame = self.tabview.add(tool.name)
            # Scrollable: the busiest tab has five stacked rows, and on a
            # 150%-scaled display they no longer fit a small window. Letting
            # the body scroll means a control is never clipped, whatever the
            # window size or DPI setting.
            holder = ctk.CTkScrollableFrame(frame, fg_color="transparent",
                                            scrollbar_button_color=MUTED,
                                            scrollbar_button_hover_color=MUTED_HOVER)
            holder.pack(fill="both", expand=True, padx=8, pady=8)
            tool.build(holder)
            self._tabs[tool.name] = tool

        log_card = ctk.CTkFrame(content, fg_color=BG_CARD, corner_radius=10,
                                border_color=MUTED, border_width=1)
        log_card.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        header = ctk.CTkFrame(log_card, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(10, 4))
        ctk.CTkLabel(header, text="Log", text_color=ACCENT,
                     font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
        ctk.CTkButton(header, text="Clear", width=64, fg_color=MUTED,
                      hover_color=MUTED_HOVER, command=self._clear_log).pack(side="right")
        # An explicit height, or the textbox's default 200px request wins over
        # the row weights and the log ends up larger than the tab above it.
        self.log_box = ctk.CTkTextbox(log_card, fg_color=BG_LIST, text_color=TEXT,
                                      height=90, font=("Consolas", 10))
        self.log_box.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.log_box.configure(state="disabled")

        bottom = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0, height=58)
        bottom.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        bottom.grid_propagate(False)

        # Gold, on dark text: the one button that starts work.
        self.run_btn = ctk.CTkButton(bottom, text="Run", width=190, height=38,
                                     fg_color=ACCENT, hover_color=ACCENT_HOVER,
                                     text_color=BG_APP,
                                     font=ctk.CTkFont(size=14, weight="bold"),
                                     command=self._on_run)
        self.run_btn.pack(side="left", padx=16, pady=14)
        self.save_btn = ctk.CTkButton(bottom, text="Save output as...", width=150, height=38,
                                      fg_color=MUTED, hover_color=MUTED_HOVER,
                                      state="disabled", command=self._save_artifact)
        self.save_btn.pack(side="left", pady=14)
        self.open_btn = ctk.CTkButton(bottom, text="Open folder", width=120, height=38,
                                      fg_color=MUTED, hover_color=MUTED_HOVER,
                                      state="disabled", command=self._open_artifact_dir)
        self.open_btn.pack(side="left", padx=10, pady=14)

        ctk.CTkLabel(bottom, textvariable=self._artifact_display,
                     text_color=TEXT_DIM).pack(side="left", padx=10)
        self.status_label = ctk.CTkLabel(bottom, text="Ready", text_color=TEXT_DIM,
                                         font=ctk.CTkFont(size=13, weight="bold"))
        self.status_label.pack(side="right", padx=18)

        self._on_tab_change()

    # ------------------------------------------------------------------ state

    @property
    def _current(self):
        return self._tabs[self.tabview.get()]

    def _on_tab_change(self) -> None:
        """Each tool names its own action, so the run button follows the tab."""
        if self._busy:
            return
        self.run_btn.configure(text=self._current.run_label)

    def _clear_log(self) -> None:
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", tk.END)
        self.log_box.configure(state="disabled")

    def _append(self, line: str) -> None:
        self.log_box.configure(state="normal")
        self.log_box.insert(tk.END, line + "\n")
        self.log_box.see(tk.END)
        self.log_box.configure(state="disabled")

    # -------------------------------------------------------------------- run

    def _on_run(self) -> None:
        tool = self._current
        try:
            tool.validate()
            # Widgets must be read here: Tk refuses variable access from the
            # worker thread ("main thread is not in main loop").
            params = tool.collect()
        except ValueError as exc:
            messagebox.showerror(f"{tool.name} - check the inputs", str(exc))
            return

        self._busy = True
        self.run_btn.configure(state="disabled", text="Running...")
        self.save_btn.configure(state="disabled")
        self.open_btn.configure(state="disabled")
        self._artifact = None
        self._artifact_display.set("Working...")
        self.status_label.configure(text=f"{tool.name} running", text_color=WARN)
        self._clear_log()

        threading.Thread(target=self._worker, args=(tool, params), daemon=True).start()

    def _worker(self, tool, params: dict) -> None:
        try:
            result = tool.run(params, lambda msg: self._log_queue.put(str(msg)))
            self._log_queue.put(("__DONE__", result))
        except Exception as exc:                      # noqa: BLE001 - surfaced in the GUI
            logging.getLogger(__name__).debug("run failed", exc_info=True)
            self._log_queue.put(("__FAIL__", exc, traceback.format_exc()))

    def _poll_logs(self) -> None:
        try:
            while True:
                msg = self._log_queue.get_nowait()
                if isinstance(msg, tuple) and msg[0] == "__DONE__":
                    self._finish_ok(msg[1])
                elif isinstance(msg, tuple) and msg[0] == "__FAIL__":
                    self._finish_err(msg[1], msg[2])
                else:
                    self._append(str(msg))
        except queue.Empty:
            pass
        self.after(80, self._poll_logs)

    def _reset_buttons(self) -> None:
        self._busy = False
        self.run_btn.configure(state="normal", text=self._current.run_label)

    def _finish_ok(self, result: Result) -> None:
        self._reset_buttons()
        self.status_label.configure(text="Done", text_color=OK)
        self._append(result.message)
        artifact = result.artifact
        if artifact and Path(artifact).exists():
            self._artifact = Path(artifact)
            self._artifact_display.set(self._artifact.name)
            self.save_btn.configure(state="normal")
            self.open_btn.configure(state="normal")
        else:
            self._artifact_display.set("Finished, no file to save.")

    def _finish_err(self, exc: Exception, tb: str) -> None:
        self._reset_buttons()
        self.status_label.configure(text="Failed", text_color=ERR)
        self._artifact_display.set("Nothing generated.")
        self._append(f"ERROR: {exc}")
        self._append(tb)
        messagebox.showerror("Run failed", str(exc))

    # -------------------------------------------------------------- artifacts

    def _save_artifact(self) -> None:
        if not self._artifact or not self._artifact.exists():
            messagebox.showerror("Not found", "Nothing to save. Run a tool first.")
            return
        dest = filedialog.asksaveasfilename(
            title="Save output", defaultextension=self._artifact.suffix,
            initialfile=self._artifact.name,
            filetypes=[(f"{self._artifact.suffix.lstrip('.').upper()} files",
                        f"*{self._artifact.suffix}"), ("All files", "*.*")])
        if not dest:
            return
        try:
            shutil.copy2(self._artifact, dest)
            messagebox.showinfo("Saved", f"Saved to:\n{dest}")
        except OSError as exc:
            messagebox.showerror("Save failed", str(exc))

    def _open_artifact_dir(self) -> None:
        if not self._artifact or not self._artifact.exists():
            messagebox.showerror("Not found", "Nothing to open. Run a tool first.")
            return
        folder = str(self._artifact.parent)
        try:
            if sys.platform.startswith("win"):
                os.startfile(folder)  # noqa: S606 - opening the user's own output
            elif sys.platform == "darwin":
                subprocess.run(["open", folder], check=False)
            else:
                subprocess.run(["xdg-open", folder], check=False)
        except OSError as exc:
            messagebox.showerror("Could not open folder", str(exc))


def main() -> None:
    App().mainloop()


if __name__ == "__main__":
    main()
