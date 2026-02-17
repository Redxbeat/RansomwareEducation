@echo off
title Ransomware Simulation - Transfer to VM
color 0A
echo ==============================================
echo    COPYING FILES TO USB FOR VM TRANSFER
echo ==============================================
echo.

REM Check for USB drive (common letters)
set USB_FOUND=0
for %%D in (F G H I E D) do (
    if exist "%%D:\" (
        if not exist "%%D:\Windows\" (
            echo Found USB drive: %%D:\
            set USB_DRIVE=%%D:
            set USB_FOUND=1
            goto :found
        )
    )
)

:found
if %USB_FOUND%==0 (
    echo ❌ No USB drive found!
    echo Please insert a USB drive and try again.
    goto :end
)

echo 📁 Source: %CD%\transfer\
echo 📁 Destination: %USB_DRIVE%\RansomwareSim\
echo.

REM Create destination folder
if not exist "%USB_DRIVE%\RansomwareSim" mkdir "%USB_DRIVE%\RansomwareSim"

REM Copy files
echo Copying files...
xcopy /E /I /Y "%~dp0transfer\*" "%USB_DRIVE%\RansomwareSim\" >nul

if errorlevel 1 (
    echo ❌ Copy failed!
) else (
    echo ✅ Files copied successfully!
    echo.
    echo Files transferred:
    dir "%USB_DRIVE%\RansomwareSim\"
)

echo.
echo ==============================================
echo NEXT STEPS:
echo 1. In VirtualBox: Devices → USB → Select your USB
echo 2. In VM: Copy from USB to C:\RansomwareSim\
echo 3. In VM: Run the simulation
echo ==============================================

:end
echo.
pause