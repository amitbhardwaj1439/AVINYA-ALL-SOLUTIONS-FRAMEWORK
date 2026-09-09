"""Shared widgets for the Avinya All Solutions tabs.

The layout is the original gui.py's - same dark cards, file lists and log
console - recoloured to the Avinya identity. Every value below is sampled from
assets/avinya_logo.png rather than picked by eye, so the window and the logo
sit in the same colour space: the near-black backdrop, the gold of the 'A' and
the steel blue of the infinity ribbon.
"""
from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

# --- sampled from the logo ------------------------------------------------
GOLD = "#DBB362"          # the 'A' - weighted mean of its gold pixels
GOLD_BRIGHT = "#EFCB7C"   # its highlights, used for hover
GOLD_DEEP = "#A8853F"     # its shadow side, used for pressed/borders
BLUE = "#36719A"          # the infinity ribbon
BLUE_BRIGHT = "#4A8CBA"
BG_APP = "#03050B"        # the logo's backdrop, so the mark blends into it
BG_CARD = "#0C1220"       # one step up, to lift cards off that backdrop
BG_LIST = "#070B14"       # one step down, for inset lists and the console

# Gold is the primary action; blue carries selection and secondary emphasis.
ACCENT = GOLD
ACCENT_HOVER = GOLD_BRIGHT
SELECT = BLUE
MUTED = "#1B2436"
MUTED_HOVER = "#2A3854"
TEXT = "#E8EDF6"
TEXT_DIM = "#8FA0BC"

# Status colours, nudged toward the logo's warmth rather than stock pastels.
OK = "#7FD199"
WARN = GOLD_BRIGHT
ERR = "#E86A6A"


class FilePanel(ctk.CTkFrame):
    """Multi-file picker with add / remove / clear."""

    def __init__(self, parent, label: str, patterns=None, **kwargs):
        super().__init__(parent, fg_color=BG_CARD, corner_radius=10, **kwargs)
        self._patterns = patterns or [("Text files", "*.txt"), ("All files", "*.*")]

        ctk.CTkLabel(self, text=label, font=ctk.CTkFont(size=13, weight="bold")).pack(pady=(10, 4))

        # The button row is packed BEFORE the list: the list expands to fill
        # whatever is left, so if it were packed first a short panel would push
        # Add/Remove/Clear off the bottom entirely.
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(side="bottom", fill="x", padx=10, pady=(6, 10))
        ctk.CTkButton(row, text="+ Add Files", width=100, fg_color=SELECT,
                      hover_color=BLUE_BRIGHT, command=self._add).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="Remove", width=80, fg_color=MUTED,
                      hover_color=MUTED_HOVER, command=self._remove).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="Clear", width=60, fg_color=MUTED,
                      hover_color=MUTED_HOVER, command=self._clear).pack(side="left")

        list_frame = ctk.CTkFrame(self, fg_color=BG_LIST, corner_radius=6)
        list_frame.pack(fill="both", expand=True, padx=10)
        # tk.Scrollbar is not a CustomTkinter widget, so it needs colouring by
        # hand or it renders as a bright system-grey bar on the dark panel.
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", relief="flat",
                                 borderwidth=0, highlightthickness=0,
                                 troughcolor=BG_LIST, bg=MUTED,
                                 activebackground=MUTED_HOVER)
        self.listbox = tk.Listbox(
            # Selection uses the ribbon blue: gold on gold-tinted text would
            # collide with the Run button's meaning, and blue reads as "chosen".
            list_frame, selectmode=tk.EXTENDED, bg=BG_LIST, fg=TEXT,
            selectbackground=SELECT, selectforeground="white", relief="flat",
            highlightthickness=0, borderwidth=0, font=("Consolas", 9),
            # The tab body scrolls and does not stretch its children, so this
            # is the list's actual height. Six rows: enough to work with, and
            # small enough that the controls under it stay on screen on a
            # 1280x800 display at 150% scaling.
            height=6,
            yscrollcommand=scrollbar.set,
        )
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.pack(fill="both", expand=True, padx=4, pady=4)

    def _add(self) -> None:
        for p in filedialog.askopenfilenames(title="Select files", filetypes=self._patterns):
            if p not in self.listbox.get(0, tk.END):
                self.listbox.insert(tk.END, p)

    def _remove(self) -> None:
        for idx in reversed(self.listbox.curselection()):
            self.listbox.delete(idx)

    def _clear(self) -> None:
        self.listbox.delete(0, tk.END)

    def get_files(self) -> list[Path]:
        return [Path(self.listbox.get(i)) for i in range(self.listbox.size())]


class PathRow(ctk.CTkFrame):
    """One labelled path entry with a Browse button.

    `mode` picks the dialog: an existing file, a directory, or a save target.
    """

    def __init__(self, parent, label: str, mode: str = "open",
                 initial: str = "", patterns=None, initialfile: str = "",
                 action: tuple[str, object] | None = None, **kwargs):
        super().__init__(parent, fg_color=BG_CARD, corner_radius=8, **kwargs)
        self.mode = mode
        self._patterns = patterns or [("All files", "*.*")]
        self._initialfile = initialfile
        self.var = tk.StringVar(value=initial)

        ctk.CTkLabel(self, text=label, width=132, anchor="w",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(12, 6), pady=10)
        ctk.CTkEntry(self, textvariable=self.var, fg_color=BG_LIST, text_color=TEXT,
                     border_color=MUTED_HOVER, border_width=1).pack(
            side="left", fill="x", expand=True, pady=10,
            padx=(0, 12) if mode == "text" else 0)
        # "text" values are typed, not picked - a site id has no file dialog.
        if mode != "text":
            ctk.CTkButton(self, text="Browse", width=80, fg_color=MUTED, hover_color=MUTED_HOVER,
                          command=self._browse).pack(side="left", padx=10, pady=10)
        # Optional companion button, e.g. "List sites" beside the site id, so a
        # lookup does not need a row of its own.
        if action is not None:
            text, command = action
            ctk.CTkButton(self, text=text, width=100, fg_color=SELECT,
                          hover_color=BLUE_BRIGHT, command=command).pack(
                              side="left", padx=10, pady=10)

    def _browse(self) -> None:
        if self.mode == "dir":
            path = filedialog.askdirectory(title="Select folder")
        elif self.mode == "save":
            path = filedialog.asksaveasfilename(
                title="Select output file", defaultextension=".xlsx",
                filetypes=self._patterns, initialfile=self._initialfile)
        else:
            path = filedialog.askopenfilename(title="Select file", filetypes=self._patterns)
        if path:
            self.var.set(path)

    def get(self) -> str:
        return self.var.get().strip()


class LabeledCombo(ctk.CTkFrame):
    """A labelled dropdown, e.g. the circle selector."""

    def __init__(self, parent, label: str, values: list[str], initial: str = "", **kwargs):
        super().__init__(parent, fg_color=BG_CARD, corner_radius=8, **kwargs)
        self.var = tk.StringVar(value=initial or (values[0] if values else ""))
        # A minimum height so the row still renders its full control if the
        # surrounding layout gets tight.
        self.configure(height=56)
        self.pack_propagate(False)

        ctk.CTkLabel(self, text=label, width=132, anchor="w",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(12, 6), pady=10)
        ctk.CTkComboBox(self, values=values, variable=self.var, width=260, height=32,
                        fg_color=BG_LIST, border_color=MUTED_HOVER,
                        button_color=SELECT, button_hover_color=BLUE_BRIGHT,
                        dropdown_fg_color=BG_LIST, dropdown_hover_color=SELECT,
                        dropdown_text_color=TEXT, text_color=TEXT,
                        font=ctk.CTkFont(size=13)).pack(side="left", pady=12)

    def get(self) -> str:
        return self.var.get().strip()
