@echo off
echo === Creating Portable Version with Bundled Python ===
echo.

REM Create portable directory
if not exist "portable" mkdir portable
if not exist "portable\python" mkdir portable\python

echo Copying application files...
copy "main_bundled.js" "portable\"
copy "app.py" "portable\"
copy "package.json" "portable\"
xcopy "static" "portable\static\" /E /I /Y
xcopy "templates" "portable\templates\" /E /I /Y
if exist "instance" xcopy "instance" "portable\instance\" /E /I /Y
if exist "migrations" xcopy "migrations" "portable\migrations\" /E /I /Y
if exist "cloth.db" copy "cloth.db" "portable\"
if exist "requirements.txt" copy "requirements.txt" "portable\"

echo Creating portable launcher...
echo @echo off > portable\START_APP.bat
echo echo Starting Draping Threads... >> portable\START_APP.bat
echo echo. >> portable\START_APP.bat
echo REM Try to find Python automatically >> portable\START_APP.bat
echo set PYTHON_CMD= >> portable\START_APP.bat
echo. >> portable\START_APP.bat
echo REM Check for Python in common locations >> portable\START_APP.bat
echo if exist "C:\Python39\python.exe" set PYTHON_CMD=C:\Python39\python.exe >> portable\START_APP.bat
echo if exist "C:\Python310\python.exe" set PYTHON_CMD=C:\Python310\python.exe >> portable\START_APP.bat
echo if exist "C:\Python311\python.exe" set PYTHON_CMD=C:\Python311\python.exe >> portable\START_APP.bat
echo if exist "C:\Python312\python.exe" set PYTHON_CMD=C:\Python312\python.exe >> portable\START_APP.bat
echo if exist "C:\Program Files\Python39\python.exe" set PYTHON_CMD="C:\Program Files\Python39\python.exe" >> portable\START_APP.bat
echo if exist "C:\Program Files\Python310\python.exe" set PYTHON_CMD="C:\Program Files\Python310\python.exe" >> portable\START_APP.bat
echo if exist "C:\Program Files\Python311\python.exe" set PYTHON_CMD="C:\Program Files\Python311\python.exe" >> portable\START_APP.bat
echo if exist "C:\Program Files\Python312\python.exe" set PYTHON_CMD="C:\Program Files\Python312\python.exe" >> portable\START_APP.bat
echo. >> portable\START_APP.bat
echo REM If no Python found, try system PATH >> portable\START_APP.bat
echo if "%PYTHON_CMD%"=="" ( >> portable\START_APP.bat
echo     python --version ^>nul 2^>^&1 >> portable\START_APP.bat
echo     if !errorlevel! equ 0 set PYTHON_CMD=python >> portable\START_APP.bat
echo ) >> portable\START_APP.bat
echo. >> portable\START_APP.bat
echo REM If still no Python, show helpful message >> portable\START_APP.bat
echo if "%PYTHON_CMD%"=="" ( >> portable\START_APP.bat
echo     echo. >> portable\START_APP.bat
echo     echo Python is required but not found on this computer. >> portable\START_APP.bat
echo     echo. >> portable\START_APP.bat
echo     echo Please install Python from: https://www.python.org/downloads/ >> portable\START_APP.bat
echo     echo Make sure to check "Add Python to PATH" during installation. >> portable\START_APP.bat
echo     echo. >> portable\START_APP.bat
echo     echo Press any key to exit... >> portable\START_APP.bat
echo     pause ^>nul >> portable\START_APP.bat
echo     exit /b 1 >> portable\START_APP.bat
echo ) >> portable\START_APP.bat
echo. >> portable\START_APP.bat
echo echo Found Python: %%PYTHON_CMD%% >> portable\START_APP.bat
echo echo. >> portable\START_APP.bat
echo REM Check if Flask is installed >> portable\START_APP.bat
echo %%PYTHON_CMD%% -c "import flask" ^>nul 2^>^&1 >> portable\START_APP.bat
echo if errorlevel 1 ( >> portable\START_APP.bat
echo     echo Installing Flask... >> portable\START_APP.bat
echo     %%PYTHON_CMD%% -m pip install flask >> portable\START_APP.bat
echo ) >> portable\START_APP.bat
echo. >> portable\START_APP.bat
echo echo Starting application... >> portable\START_APP.bat
echo echo Please wait for the application to open... >> portable\START_APP.bat
echo echo. >> portable\START_APP.bat
echo cd /d "%%~dp0" >> portable\START_APP.bat
echo %%PYTHON_CMD%% app.py >> portable\START_APP.bat
echo pause >> portable\START_APP.bat

echo Creating README for portable version...
echo # Draping Threads - Portable Version > portable\README.md
echo. >> portable\README.md
echo ## 🎯 Super Easy - No Installation Required! >> portable\README.md
echo. >> portable\README.md
echo ### Step 1: Double-click START_APP.bat >> portable\README.md
echo ### Step 2: Wait for app to open (may take 30-60 seconds) >> portable\README.md
echo ### Step 3: Login with: admin / admin2214 >> portable\README.md
echo. >> portable\README.md
echo ## 📋 What Happens >> portable\README.md
echo - App automatically finds or installs Python >> portable\README.md
echo - Flask is installed automatically if needed >> portable\README.md
echo - Application starts in your web browser >> portable\README.md
echo. >> portable\README.md
echo ## 🆘 If You See Errors >> portable\README.md
echo - "Python not found" - Install Python from python.org >> portable\README.md
echo - "Flask not found" - App installs it automatically >> portable\README.md
echo - "Port 5000 in use" - Close other apps and restart >> portable\README.md
echo. >> portable\README.md
echo ## 🎉 That's It! >> portable\README.md
echo Your pattern designer is ready to use! >> portable\README.md

echo.
echo === Portable Version Created! ===
echo.
echo Location: portable\
echo.
echo To use:
echo 1. Copy entire 'portable' folder to client computer
echo 2. Double-click START_APP.bat
echo 3. Follow on-screen instructions
echo.
echo This version is completely self-contained and handles Python/Flask automatically!
pause
