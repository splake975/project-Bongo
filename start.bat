REM @echo off
setlocal enabledelayedexpansion

REM === Make sure errorlogs folder exists ===
cd /d %~dp0
if not exist errorlogs mkdir errorlogs

:loop
REM === Get timestamp (locale-independent) ===
for /f "tokens=1-6 delims=/-: " %%a in (
    'wmic path win32_localtime get /format:list ^| findstr "="'
) do (
    set /a "yyyy=%%a, mm=%%b+100, dd=%%c+100, hh=%%d+100, min=%%e+100, sec=%%f+100"
)
set "timestamp=%yyyy%-%mm:~1%-%dd:~1%_%hh:~1%-%min:~1%-%sec:~1%"

REM === Launch exe and redirect output ===
echo Starting exe at %timestamp%
start "" /B cmd /c "client.exe > %CD%\errorlogs\output_%timestamp%.log 2>&1"

REM === Get PID with retries ===
set "pid="
for /L %%i in (1,1,10) do (
    if not defined pid (
        for /f "tokens=2 delims=," %%a in (
            'wmic process where "name='client.exe'" get processid /format:csv ^| findstr "[0-9]"'
        ) do set "pid=%%a"
        timeout /t 1 >nul
    )
)
if not defined pid (
    echo Error: Could not find PID of client.exe
    exit /b 1
)

REM === Wait for keypress or timeout (30 min) ===
echo Press any key to STOP the program, or wait 30 min...
set "wait_seconds=10"
set /a "elapsed=0"

:wait_loop
timeout /t 1 >nul
set /a elapsed+=1

REM === Check for 'Q' keypress ===
choice /c QN /n /t 1 /d N >nul
if %errorlevel% equ 1 (
    echo [Q] pressed, stopping gracefully...
    goto graceful_exit
)

if %elapsed% geq %wait_seconds% goto graceful_exit
goto wait_loop

:graceful_exit
REM === Kill process with retries ===
set "max_retries=10"
set "retry_count=0"

:kill_loop
set /a "retry_count+=1"
if %retry_count% gtr %max_retries% (
    echo Failed to kill process %pid% after %max_retries% attempts.
    exit /b 1
)

taskkill /PID %pid% /T /F >nul 2>&1
timeout /t 3 >nul
tasklist /fi "PID eq %pid%" | findstr "%pid%" >nul && goto kill_loop

echo Process %pid% stopped successfully.
exit /b