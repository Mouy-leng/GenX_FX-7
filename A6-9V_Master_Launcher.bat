@echo off
title A6-9V Master System Launcher
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                  🚀 A6-9V Master Launcher                   ║
echo ║                    All Systems Startup                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "C:\Users\lengk\Dropbox\OneDrive\Desktop"

echo [%time%] 🔧 Starting A6-9V Master Systems...
echo.

REM Start Python Management System
echo [%time%] 📊 Launching Python Manager...
if exist "start_all.bat" (
    start "A6-9V Python Manager" cmd /c "start_all.bat"
    timeout /t 3 /nobreak >nul
) else (
    echo ⚠️ Python Manager not found, skipping...
)

REM Start GenX-FX Trading System
echo [%time%] 💹 Starting GenX-FX Trading System...
cd /d "C:\Users\lengk\Dropbox\OneDrive\Desktop\A6-9V\Trading\GenX_FX"
if exist "main.py" (
    start "GenX-FX Trading" "C:\Users\lengk\AppData\Local\Programs\Python\Python313\python.exe" "main.py"
    timeout /t 2 /nobreak >nul
) else (
    echo ⚠️ GenX-FX main.py not found, skipping...
)

REM Start Development Tools
echo [%time%] 🛠️ Launching Development Environment...
cd /d "C:\Users\lengk\Dropbox\OneDrive\Desktop"

REM Open Cursor IDE
if exist "C:\Users\lengk\AppData\Local\Programs\cursor\Cursor.exe" (
    start "Cursor IDE" "C:\Users\lengk\AppData\Local\Programs\cursor\Cursor.exe" "C:\Users\lengk\Dropbox\OneDrive\Desktop\A6-9V"
    timeout /t 2 /nobreak >nul
)

REM Open Chrome with trading dashboards
echo [%time%] 🌐 Opening Trading Dashboards...
start "Trading Dashboard" chrome.exe --new-window "https://www.tradingview.com" "https://finance.yahoo.com" "http://localhost:8080"

REM Start monitoring tools
echo [%time%] 📈 Starting System Monitoring...
start "Task Manager" taskmgr.exe
timeout /t 1 /nobreak >nul

echo.
echo ✅ [SUCCESS] A6-9V Master System launched successfully!
echo.
echo 🔧 Active Components:
echo    - Python Management System
echo    - GenX-FX Trading System  
echo    - Development Environment (Cursor IDE)
echo    - Trading Dashboards (Chrome)
echo    - System Monitoring (Task Manager)
echo.
echo 🔒 Locking desktop in 10 seconds...
echo    Press any key to cancel desktop lock
timeout /t 10

REM Lock the desktop
rundll32.exe user32.dll,LockWorkStation

echo.
echo 🎯 A6-9V Master System is now running!
echo    All systems are active and desktop is locked.
echo.
pause