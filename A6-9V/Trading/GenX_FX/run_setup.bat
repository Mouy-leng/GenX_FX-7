@echo off
echo ========================================
echo GenX-FX Complete Setup Script
echo ========================================
echo.

echo Starting comprehensive setup...
echo.

REM Run the complete setup script
python scripts/complete_setup.py

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Review config/consolidated_secrets.env
echo 2. Update missing API keys
echo 3. Run: python main.py
echo.
pause
