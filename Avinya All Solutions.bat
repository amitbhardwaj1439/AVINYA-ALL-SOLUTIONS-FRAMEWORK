@echo off
rem ---------------------------------------------------------------------------
rem  Avinya All Solutions - launcher
rem
rem  Runs from wherever this folder is copied to, on any machine, including
rem  paths containing spaces. Everything resolves relative to %~dp0 (the folder
rem  holding this file), so nothing is tied to the machine it was built on.
rem
rem  Interpreter - first one that actually works:
rem    1. avenv\    the venv shipped inside this folder. A venv stores an
rem                 absolute path to its base Python, so this only works on the
rem                 machine that created it.
rem    2. .venv\    a venv this script built here on an earlier run.
rem    3. bootstrap build .venv from the system Python and install
rem                 requirements.txt. First run on a new machine only.
rem ---------------------------------------------------------------------------
setlocal EnableExtensions
cd /d "%~dp0"

set "APP=%~dp0app.py"
set "REQ=%~dp0requirements.txt"
set "SHIPPED=%~dp0avenv\Scripts"
set "LOCAL=%~dp0.venv\Scripts"

rem -- 1. the shipped venv, if its base Python exists on this machine ---------
if exist "%SHIPPED%\python.exe" (
    "%SHIPPED%\python.exe" -c "import customtkinter, pandas" >nul 2>&1
    if not errorlevel 1 (
        start "" "%SHIPPED%\pythonw.exe" "%APP%"
        exit /b 0
    )
)

rem -- 2. a venv built here by an earlier run ---------------------------------
if exist "%LOCAL%\python.exe" (
    "%LOCAL%\python.exe" -c "import customtkinter, pandas" >nul 2>&1
    if not errorlevel 1 (
        start "" "%LOCAL%\pythonw.exe" "%APP%"
        exit /b 0
    )
)

rem -- 3. first run on this machine: build .venv ------------------------------
echo.
echo  Avinya All Solutions - first run on this machine.
echo  Setting up a local Python environment. This happens once.
echo.

set "SYSPY="
py -3 -c "import sys" >nul 2>&1
if not errorlevel 1 set "SYSPY=py -3"
if not defined SYSPY (
    python -c "import sys" >nul 2>&1
    if not errorlevel 1 set "SYSPY=python"
)
if not defined SYSPY goto :nopython

if not exist "%LOCAL%\python.exe" (
    %SYSPY% -m venv "%~dp0.venv"
    if errorlevel 1 goto :venvfailed
)

"%LOCAL%\python.exe" -m pip install --upgrade pip --quiet
"%LOCAL%\python.exe" -m pip install -r "%REQ%" --quiet
"%LOCAL%\python.exe" -c "import customtkinter, pandas" >nul 2>&1
if errorlevel 1 goto :pipfailed

echo  Setup complete - starting.
start "" "%LOCAL%\pythonw.exe" "%APP%"
exit /b 0

:nopython
echo  ERROR: Python 3 was not found on this machine.
echo.
echo  Install Python 3.10 or newer from https://www.python.org/downloads/
echo  ticking "Add python.exe to PATH" during setup, then run this file again.
echo.
pause
exit /b 1

:venvfailed
echo  ERROR: could not create the Python environment in
echo         "%~dp0.venv"
echo  Check that this folder is writable and not blocked by policy.
echo.
pause
exit /b 1

:pipfailed
echo  ERROR: the required Python packages could not be installed.
echo  If this machine sits behind a proxy, pip may need it configured.
echo  Retry manually with:
echo      "%LOCAL%\python.exe" -m pip install -r "%REQ%"
echo.
pause
exit /b 1
