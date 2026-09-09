"""Where this machine keeps its Downloads folder.

`Path.home() / "Downloads"` is wrong often enough to matter: OneDrive's Known
Folder Move redirects Downloads into the OneDrive tree, and a user can point it
anywhere from Explorer. Windows records the real location, so ask it rather
than guess - otherwise a colleague running this app finds their output in a
folder Explorer does not show them.

Resolution order, first hit wins:

1. SHGetKnownFolderPath(FOLDERID_Downloads) - the API Explorer itself uses
2. the User Shell Folders registry value, expanded for %USERPROFILE% etc.
3. ~/Downloads, then ~ - for non-Windows and for a stripped-down Windows
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# FOLDERID_Downloads, from KnownFolders.h
_DOWNLOADS_GUID = "{374DE290-123F-4565-9164-39C4925E467B}"


def _via_known_folder_api() -> Path | None:
    """Ask Windows itself. Correct even when Downloads has been redirected."""
    if not sys.platform.startswith("win"):
        return None
    try:
        import ctypes
        from ctypes import wintypes

        class GUID(ctypes.Structure):
            _fields_ = [("Data1", wintypes.DWORD), ("Data2", wintypes.WORD),
                        ("Data3", wintypes.WORD), ("Data4", ctypes.c_byte * 8)]

        shell32 = ctypes.windll.shell32
        ole32 = ctypes.windll.ole32
        guid = GUID()
        if ole32.CLSIDFromString(ctypes.c_wchar_p(_DOWNLOADS_GUID), ctypes.byref(guid)) != 0:
            return None

        out = ctypes.c_wchar_p()
        if shell32.SHGetKnownFolderPath(ctypes.byref(guid), 0, None, ctypes.byref(out)) != 0:
            return None
        try:
            return Path(out.value) if out.value else None
        finally:
            ole32.CoTaskMemFree(out)
    except Exception:                                 # noqa: BLE001 - fall through
        return None


def _via_registry() -> Path | None:
    """The same value Explorer stores, for when the API call is unavailable."""
    if not sys.platform.startswith("win"):
        return None
    try:
        import winreg
        key = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as handle:
            raw, _ = winreg.QueryValueEx(handle, _DOWNLOADS_GUID)
        # Stored as REG_EXPAND_SZ, e.g. "%USERPROFILE%\Downloads"
        return Path(os.path.expandvars(raw))
    except Exception:                                 # noqa: BLE001 - fall through
        return None


def downloads_dir() -> Path:
    """This machine's Downloads folder, created if it does not exist yet.

    Never raises: if every lookup fails the home folder is used, so a run still
    has somewhere to write.
    """
    for candidate in (_via_known_folder_api(), _via_registry(),
                      Path.home() / "Downloads", Path.home()):
        if candidate is None:
            continue
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            if candidate.is_dir() and os.access(candidate, os.W_OK):
                return candidate
        except OSError:
            continue
    return Path.cwd()
