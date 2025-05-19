@echo off



:: Set the paths to the installers
set "cairoInstall=gtk-2.12.9-win32-2.exe"


:: Check if the installers exist
if not exist "%cairoInstall%" (
    echo %cairoInstall% not found. Please ensure the file is in the same directory as this script.
    pause
    exit /b 1
)


:: Install the x86 version
echo Installing cairo binaries...
start /wait %cairoInstall% /install /quiet /norestart
if %errorlevel% equ 0 (
    echo cairo installation completed successfully.
) else (
    echo cairo installation failed with error code %errorlevel%.
)


exit