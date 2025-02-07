@echo off

call pyenv update
REM Install Python 3.12.4 using pyenv-win
echo Installing Python 3.12.4 using pyenv-win...
call pyenv install 3.12.4 

echo Python 3.12.4 installed successfully.

REM Set Python 3.12.4 as the local version
call pyenv local 3.12.4

REM Create a virtual environment named 'venvOCR'
echo Creating virtual environment 'venvOCR'...
call python -m venv venvOCR
if %errorlevel% neq 0 (
    echo Failed to create virtual environment.
    timeout /t 1
    exit /b 1
)
echo Virtual environment 'venvOCR' created successfully.

echo Setup complete. Activate the virtual environment using:
echo   .\venvOCR\Scripts\activate
call .\venvOCR\scripts\activate
call pip install -r ./requirementsOCR.txt
call deactivate
timeout 1

:: Batch file to install Microsoft Visual C++ Redistributable

@REM echo Downloading Visual C++ Redistributable x64...
@REM call curl -o vc_redist.x64.exe https://aka.ms/vs/16/release/vc_redist.x64.exe

@REM echo Downloading Visual C++ Redistributable x86...
@REM call curl -o vc_redist.x86.exe https://aka.ms/vs/16/release/vc_redist.x86.exe

echo Installing Visual C++ Redistributable x64...
start /wait vc_redist.x64.exe /install /quiet /norestart

echo Installing Visual C++ Redistributable x86...
start /wait vc_redist.x86.exe /install /quiet /norestart

echo Installation completed.

:: Set the paths to the installers
set "VC_REDIST_X64=vc_redist.x64.exe"
set "VC_REDIST_X86=vc_redist.x86.exe"

:: Check if the installers exist
if not exist "%VC_REDIST_X86%" (
    echo %VC_REDIST_X86% not found. Please ensure the file is in the same directory as this script.
    pause
    exit /b 1
)

if not exist "%VC_REDIST_X64%" (
    echo %VC_REDIST_X64% not found. Please ensure the file is in the same directory as this script.
    pause
    exit /b 1
)

:: Install the x86 version
echo Installing Microsoft Visual C++ Redistributable (x86)...
start /wait %VC_REDIST_X86% /install /quiet /norestart
if %errorlevel% equ 0 (
    echo x86 installation completed successfully.
) else (
    echo x86 installation failed with error code %errorlevel%.
)

:: Install the x64 version
echo Installing Microsoft Visual C++ Redistributable (x64)...
start /wait %VC_REDIST_X64% /install /quiet /norestart
if %errorlevel% equ 0 (
    echo x64 installation completed successfully.
) else (
    echo x64 installation failed with error code %errorlevel%.
)

call .\venvOCR\scripts\activate
call python ./ocrProd/pyFiles/ocrServerInit.py

:: End of script
echo Installation process completed.
pause

timeout /t 1
exit