@echo off
title A6-9V Python Manager Launcher
echo Starting A6-9V Python Management System...
echo.

cd /d "C:\Users\lengk\Dropbox\OneDrive\Desktop"

echo [%time%] Checking dependencies...
"C:\Users\lengk\AppData\Local\Programs\Python\Python313\python.exe" "C:\Users\lengk\Dropbox\OneDrive\Desktop\launch_python_manager.py" --check-deps
if errorlevel 1 (
    echo Error: Dependencies check failed
    pause
    exit /b 1
)

echo [%time%] Starting Python Startup Manager...
start "Python Manager" "C:\Users\lengk\AppData\Local\Programs\Python\Python313\python.exe" "C:\Users\lengk\Dropbox\OneDrive\Desktop\python_startup_manager.py"

timeout /t 5 /nobreak >nul

echo [%time%] Starting Dashboard...
start "Dashboard" "C:\Users\lengk\AppData\Local\Programs\Python\Python313\python.exe" "C:\Users\lengk\Dropbox\OneDrive\Desktop\process_monitor_dashboard.py"

echo.
echo [SUCCESS] A6-9V Python Management System started successfully
echo.
echo Components running:
echo - Python Startup Manager (manages your Python applications)
echo - Process Monitor Dashboard (monitoring and control interface)
echo.
echo Check the dashboard window for real-time monitoring and control.
echo.
pause
