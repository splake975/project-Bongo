@echo off
REM Check for Python installation
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python 3.12.4...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
    echo Python 3.12.4 installed successfully.
) else (
    echo Python is already installed.
)

REM Check for pyenv-win installation
where pyenv >nul 2>&1
if %errorlevel% neq 0 (
    echo pyenv-win is not installed. Installing pyenv-win...
    curl -o install-pyenv-win.ps1 https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1
    powershell -ExecutionPolicy Bypass -File install-pyenv-win.ps1
    del install-pyenv-win.ps1
    echo pyenv-win installed successfully.

    REM Add pyenv-win to PATH
    setx PATH "%USERPROFILE%\.pyenv\pyenv-win\bin;%USERPROFILE%\.pyenv\pyenv-win\shims;%PATH%"
    echo pyenv-win added to PATH.
) else (
    echo pyenv-win is already installed.
)

timeout /t 5
@REM exit



