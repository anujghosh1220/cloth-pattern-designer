@echo off 
echo Starting Draping Threads... 
echo. 
REM Try to find Python automatically 
set PYTHON_CMD= 
 
REM Check for Python in common locations 
if exist "C:\Python39\python.exe" set PYTHON_CMD=C:\Python39\python.exe 
if exist "C:\Python310\python.exe" set PYTHON_CMD=C:\Python310\python.exe 
if exist "C:\Python311\python.exe" set PYTHON_CMD=C:\Python311\python.exe 
if exist "C:\Python312\python.exe" set PYTHON_CMD=C:\Python312\python.exe 
if exist "C:\Program Files\Python39\python.exe" set PYTHON_CMD="C:\Program Files\Python39\python.exe" 
if exist "C:\Program Files\Python310\python.exe" set PYTHON_CMD="C:\Program Files\Python310\python.exe" 
if exist "C:\Program Files\Python311\python.exe" set PYTHON_CMD="C:\Program Files\Python311\python.exe" 
if exist "C:\Program Files\Python312\python.exe" set PYTHON_CMD="C:\Program Files\Python312\python.exe" 
 
REM If no Python found, try system PATH 
if ""=="" ( 
    python --version >nul 2>&1 
    if !errorlevel! equ 0 set PYTHON_CMD=python 
) 
 
REM If still no Python, show helpful message 
if ""=="" ( 
    echo. 
    echo Python is required but not found on this computer. 
    echo. 
    echo Please install Python from: https://www.python.org/downloads/ 
    echo Make sure to check "Add Python to PATH" during installation. 
    echo. 
    echo Press any key to exit... 
    pause >nul 
    exit /b 1 
) 
 
echo Found Python: %PYTHON_CMD% 
echo. 
REM Check if Flask is installed 
%PYTHON_CMD% -c "import flask" >nul 2>&1 
if errorlevel 1 ( 
    echo Installing Flask... 
    %PYTHON_CMD% -m pip install flask 
) 
 
echo Starting application... 
echo Please wait for the application to open... 
echo. 
cd /d "%~dp0" 
%PYTHON_CMD% app.py 
pause 
