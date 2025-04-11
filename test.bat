@REM @echo off
:: Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Change directory to the batch file's location
cd /d "%~dp0"

:: Your commands here
echo Running in %cd%
@REM start "" cmd "client.exe > errorlogs.txt 2>&1"
client.exe > errorlogs.txt 2>&1