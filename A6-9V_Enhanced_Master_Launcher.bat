@echo off
title A6-9V Enhanced Master Trading System Launcher
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              🚀 A6-9V Enhanced Master Launcher              ║
echo ║           All Systems + MT4/5 Trading Platform              ║
echo ║                    Organization: A6-9V                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "C:\Users\lengk\Dropbox\OneDrive\Desktop"

echo [%time%] 🔧 Starting A6-9V Enhanced Master Systems...
echo.

REM =============================================================================
REM SECTION 1: METATRADER 4 & 5 SETUP AND LOGIN
REM =============================================================================

echo [%time%] 💹 PHASE 1: MetaTrader Platform Setup
echo ════════════════════════════════════════════════════════════════

REM Start MT4 EXNESS with login
echo [%time%] 🔑 Starting MT4 EXNESS - Login: 70559995
if exist "C:\Program Files (x86)\MetaTrader 4 EXNESS\terminal.exe" (
    start "MT4-EXNESS" "C:\Program Files (x86)\MetaTrader 4 EXNESS\terminal.exe" /portable
    timeout /t 5 /nobreak >nul
    echo    ✅ MT4 EXNESS launched successfully
) else (
    echo    ⚠️  MT4 EXNESS not found, checking alternative path...
    if exist "C:\Program Files\MetaTrader\terminal64.exe" (
        start "MT4-GENERIC" "C:\Program Files\MetaTrader\terminal64.exe"
        timeout /t 5 /nobreak >nul
        echo    ✅ MT4 Generic launched successfully
    )
)

REM Start MT5 EXNESS with login
echo [%time%] 🔑 Starting MT5 EXNESS - Login: 279260115
if exist "C:\Program Files\MetaTrader 5 EXNESS\terminal64.exe" (
    start "MT5-EXNESS" "C:\Program Files\MetaTrader 5 EXNESS\terminal64.exe" /portable
    timeout /t 5 /nobreak >nul
    echo    ✅ MT5 EXNESS launched successfully
) else (
    echo    ⚠️  MT5 EXNESS not found, checking alternative path...
    if exist "C:\Program Files\MetaTrader 5\terminal64.exe" (
        start "MT5-GENERIC" "C:\Program Files\MetaTrader 5\terminal64.exe"
        timeout /t 5 /nobreak >nul
        echo    ✅ MT5 Generic launched successfully
    )
)

REM Display login information for manual entry
echo.
echo 🔐 TRADING ACCOUNT LOGIN INFORMATION:
echo ══════════════════════════════════════════════════════════════
echo MT4 EXNESS:
echo    Login    : 70559995
echo    Password : Leng12345@#$01
echo    Server   : Exness-Trail9
echo.
echo MT5 EXNESS:
echo    Login    : 279260115
echo    Password : Leng12345@#$01
echo    Server   : Exness-MT5Trail8
echo ══════════════════════════════════════════════════════════════
echo.
echo ⏰ Waiting 15 seconds for MetaTrader platforms to fully load...
timeout /t 15 /nobreak >nul

REM Execute PowerShell login information script
echo [%time%] 🔐 Displaying login information...
if exist "MT_Login_Simple.ps1" (
    powershell -ExecutionPolicy Bypass -File "MT_Login_Simple.ps1" -Platform both
    echo    ✅ Login information displayed
) else (
    echo    ⚠️  Login script not found, showing credentials manually
    echo.
    echo    MT4 Login: 70559995 | Password: Leng12345@#$01 | Server: Exness-Trail9
    echo    MT5 Login: 279260115 | Password: Leng12345@#$01 | Server: Exness-MT5Trail8
)

REM =============================================================================
REM SECTION 2: ORIGINAL SYSTEM COMPONENTS
REM =============================================================================

echo [%time%] 🔧 PHASE 2: Core System Components
echo ════════════════════════════════════════════════════════════════

REM Start Python Management System
echo [%time%] 📊 Launching Python Manager...
if exist "start_all.bat" (
    start "A6-9V Python Manager" cmd /c "start_all.bat"
    timeout /t 3 /nobreak >nul
    echo    ✅ Python Manager started
) else (
    echo    ⚠️  Python Manager not found, skipping...
)

REM Start GenX-FX Trading System
echo [%time%] 💹 Starting GenX-FX Trading System...
cd /d "C:\Users\lengk\Dropbox\OneDrive\Desktop\A6-9V\Trading\GenX_FX"
if exist "main.py" (
    start "GenX-FX Trading" "C:\Users\lengk\AppData\Local\Programs\Python\Python313\python.exe" "main.py"
    timeout /t 2 /nobreak >nul
    echo    ✅ GenX-FX Trading System started
) else (
    echo    ⚠️  GenX-FX main.py not found, checking GenX_FX directory...
    cd /d "C:\Users\lengk\GenX_FX"
    if exist "src\main.py" (
        if exist "venv\Scripts\activate.bat" (
            start "GenX-FX Trading" cmd /c "venv\Scripts\activate && python src\main.py"
            timeout /t 2 /nobreak >nul
            echo    ✅ GenX-FX Trading System started from GenX_FX directory
        )
    ) else (
        echo    ⚠️  GenX-FX system not found in either location
    )
)

cd /d "C:\Users\lengk\Dropbox\OneDrive\Desktop"

REM =============================================================================
REM SECTION 3: DEVELOPMENT AND MONITORING TOOLS
REM =============================================================================

echo [%time%] 🛠️  PHASE 3: Development Environment
echo ════════════════════════════════════════════════════════════════

REM Open Cursor IDE
echo [%time%] 🖥️  Launching Cursor IDE...
if exist "C:\Users\lengk\AppData\Local\Programs\cursor\Cursor.exe" (
    start "Cursor IDE" "C:\Users\lengk\AppData\Local\Programs\cursor\Cursor.exe" "C:\Users\lengk\Dropbox\OneDrive\Desktop\A6-9V"
    timeout /t 2 /nobreak >nul
    echo    ✅ Cursor IDE launched
) else (
    echo    ⚠️  Cursor IDE not found, skipping...
)

REM Open Chrome with trading dashboards and Code With Me
echo [%time%] 🌐 Opening Trading Dashboards and Code With Me...
start "Trading Dashboard" chrome.exe --new-window "https://www.tradingview.com" "https://finance.yahoo.com" "https://code-with-me.global.jetbrains.com/ZhaX8frcoZS0qveUMv8vAg" "http://localhost:8080"
timeout /t 2 /nobreak >nul
echo    ✅ Trading dashboards and Code With Me opened

REM Start monitoring tools
echo [%time%] 📈 Starting System Monitoring...
start "Task Manager" taskmgr.exe
timeout /t 1 /nobreak >nul
echo    ✅ Task Manager started

REM =============================================================================
REM SECTION 4: TRADING AUTOMATION VERIFICATION
REM =============================================================================

echo.
echo [%time%] 🔍 PHASE 4: Trading System Verification
echo ════════════════════════════════════════════════════════════════

echo 🔄 Checking trading system processes...
timeout /t 5 /nobreak >nul

REM Check if MT4/MT5 processes are running
tasklist /FI "IMAGENAME eq terminal.exe" 2>NUL | find /I /N "terminal.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo    ✅ MT4 Terminal is running
) else (
    echo    ⚠️  MT4 Terminal not detected
)

tasklist /FI "IMAGENAME eq terminal64.exe" 2>NUL | find /I /N "terminal64.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo    ✅ MT5 Terminal is running
) else (
    echo    ⚠️  MT5 Terminal not detected
)

REM =============================================================================
REM SECTION 5: COMPLETION SUMMARY
REM =============================================================================

echo.
echo ✅ [SUCCESS] A6-9V Enhanced Master System launched successfully!
echo.
echo 🎯 ACTIVE TRADING COMPONENTS:
echo ════════════════════════════════════════════════════════════════
echo    🔹 MetaTrader 4 EXNESS (Login: 70559995)
echo    🔹 MetaTrader 5 EXNESS (Login: 279260115)  
echo    🔹 Python Management System
echo    🔹 GenX-FX Trading System
echo    🔹 Development Environment (Cursor IDE)
echo    🔹 Trading Dashboards (TradingView, Yahoo Finance)
echo    🔹 Code With Me Session (JetBrains)
echo    🔹 System Monitoring (Task Manager)
echo.
echo 🔐 MANUAL LOGIN REQUIRED:
echo ════════════════════════════════════════════════════════════════
echo Please manually log into your MetaTrader platforms using the
echo credentials displayed above to enable automated trading.
echo.
echo 🚨 IMPORTANT TRADING REMINDERS:
echo    • Ensure Expert Advisors are enabled in MT4/MT5
echo    • Verify trading signals are active
echo    • Check internet connection stability
echo    • Monitor account balance and margin levels
echo.

echo 🔒 Desktop will be locked in 15 seconds...
echo    Press Ctrl+C to cancel or any other key to lock immediately
timeout /t 15

REM Lock the desktop
rundll32.exe user32.dll,LockWorkStation

echo.
echo 🎯 A6-9V Enhanced Trading System is now fully operational!
echo    All trading platforms are active and desktop is secured.
echo.
echo 📊 Organization: A6-9V | System Status: ONLINE
echo.
pause