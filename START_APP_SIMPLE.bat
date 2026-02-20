@echo off
title Draping Threads - Pattern Designer
color 0A
echo.
echo ========================================
echo    🧵 Draping Threads Pattern Designer
echo ========================================
echo.
echo Starting application...
echo This may take 30-60 seconds, please wait...
echo.

REM Change to the correct directory
cd /d "%~dp0"

REM Check if app.py exists
if not exist "app.py" (
    echo.
    echo ❌ ERROR: app.py not found!
    echo Please make sure you have all the files in the same folder.
    echo.
    pause
    exit /b 1
)

REM Try different Python commands
echo 🔍 Checking for Python...
set PYTHON_FOUND=0

REM Try bundled Python first
if exist "python\python.exe" (
    echo ✅ Found bundled Python
    set PYTHON_CMD=python\python.exe
    set PYTHON_FOUND=1
    goto :CHECK_FLASK
)

REM Try system Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Found Python: python
    set PYTHON_CMD=python
    set PYTHON_FOUND=1
    goto :CHECK_FLASK
)

REM Try python3
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Found Python: python3
    set PYTHON_CMD=python3
    set PYTHON_FOUND=1
    goto :CHECK_FLASK
)

REM Try py
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Found Python: py
    set PYTHON_CMD=py
    set PYTHON_FOUND=1
    goto :CHECK_FLASK
)

REM Try common installation paths
if exist "C:\Python39\python.exe" (
    echo ✅ Found Python: C:\Python39\python.exe
    set PYTHON_CMD=C:\Python39\python.exe
    set PYTHON_FOUND=1
    goto :CHECK_FLASK
)

if exist "C:\Python310\python.exe" (
    echo ✅ Found Python: C:\Python310\python.exe
    set PYTHON_CMD=C:\Python310\python.exe
    set PYTHON_FOUND=1
    goto :CHECK_FLASK
)

if exist "C:\Python311\python.exe" (
    echo ✅ Found Python: C:\Python311\python.exe
    set PYTHON_CMD=C:\Python311\python.exe
    set PYTHON_FOUND=1
    goto :CHECK_FLASK
)

if exist "C:\Python312\python.exe" (
    echo ✅ Found Python: C:\Python312\python.exe
    set PYTHON_CMD=C:\Python312\python.exe
    set PYTHON_FOUND=1
    goto :CHECK_FLASK
)

if exist "C:\Program Files\Python39\python.exe" (
    echo ✅ Found Python: C:\Program Files\Python39\python.exe
    set PYTHON_CMD="C:\Program Files\Python39\python.exe"
    set PYTHON_FOUND=1
    goto :CHECK_FLASK
)

if exist "C:\Program Files\Python310\python.exe" (
    echo ✅ Found Python: C:\Program Files\Python310\python.exe
    set PYTHON_CMD="C:\Program Files\Python310\python.exe"
    set PYTHON_FOUND=1
    goto :CHECK_FLASK
)

if exist "C:\Program Files\Python311\python.exe" (
    echo ✅ Found Python: C:\Program Files\Python311\python.exe
    set PYTHON_CMD="C:\Program Files\Python311\python.exe"
    set PYTHON_FOUND=1
    goto :CHECK_FLASK
)

if exist "C:\Program Files\Python312\python.exe" (
    echo ✅ Found Python: C:\Program Files\Python312\python.exe
    set PYTHON_CMD="C:\Program Files\Python312\python.exe"
    set PYTHON_FOUND=1
    goto :CHECK_FLASK
)

:PYTHON_NOT_FOUND
echo.
echo ❌ Python not found on your computer.
echo.
echo Python is required to run this application.
echo.
echo 📥 Please install Python from: https://www.python.org/downloads/
echo.
echo ⚠️  IMPORTANT: During installation, check "Add Python to PATH"
echo.
echo After installing Python, run this file again.
echo.
echo Press any key to open the Python download page...
pause >nul
start https://www.python.org/downloads/
exit /b 1

:CHECK_FLASK
echo.
echo 🔍 Checking for Flask...
%PYTHON_CMD% -c "import flask" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Flask is installed
    goto :START_APP
)

echo.
echo 📦 Installing Flask... This may take a few minutes...
echo Please wait...
echo.
%PYTHON_CMD% -m pip install flask
if %errorlevel% neq 0 (
    echo.
    echo ❌ Failed to install Flask automatically.
    echo.
    echo Please try installing Flask manually:
    echo 1. Open Command Prompt
    echo 2. Type: %PYTHON_CMD% -m pip install flask
    echo 3. Press Enter
    echo 4. Run this file again
    echo.
    pause
    exit /b 1
)
echo ✅ Flask installed successfully!

:START_APP
echo.
echo 🚀 Starting Draping Threads application...
echo.
echo The application will open in your web browser.
echo If browser doesn't open automatically, go to: http://localhost:5000
echo.
echo Login with:
echo Username: admin
echo Password: admin2214
echo.
echo Press Ctrl+C to stop the application when finished.
echo ========================================
echo.

REM Start the Flask application
%PYTHON_CMD% app.py

echo.
echo Application stopped.
echo Press any key to exit...
pause >nul
