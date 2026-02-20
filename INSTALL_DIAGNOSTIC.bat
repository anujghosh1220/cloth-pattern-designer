@echo off
echo === Draping Threads Installation Diagnostic ===
echo.

echo Checking installer file...
if exist "Draping Threads Setup 1.0.0.exe" (
    echo [OK] Installer file found
    echo File size: 
    dir "Draping Threads Setup 1.0.0.exe" | find "Draping Threads Setup 1.0.0.exe"
) else (
    echo [ERROR] Installer file not found!
    pause
    exit /b 1
)

echo.
echo Checking Windows version...
ver

echo.
echo Checking available memory...
systeminfo | find "Total Physical Memory"

echo.
echo Checking disk space...
dir | find "bytes free"

echo.
echo Attempting to run installer...
echo If nothing happens, try these solutions:
echo.
echo 1. Right-click installer -^> Run as administrator
echo 2. Copy installer to Desktop first
echo 3. Check if antivirus is blocking it
echo 4. Try the other file: DrapingThreads.exe
echo.
echo Press any key to try running installer...
pause > nul
"Draping Threads Setup 1.0.0.exe"

echo.
echo If installer still doesn't work, try the unpacked version:
cd win-unpacked
"Draping Threads.exe"
pause
