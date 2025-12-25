# A6-9V Simple MetaTrader Login Script
param(
    [string]$Platform = "both",
    [int]$WaitTime = 20
)

Write-Host "🚀 A6-9V MetaTrader Login Script" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Account configurations
$MT4_Login = "70559995"
$MT4_Password = "Leng12345@#`$01"
$MT4_Server = "Exness-Trail9"

$MT5_Login = "279260115"  
$MT5_Password = "Leng12345@#`$01"
$MT5_Server = "Exness-MT5Trail8"

Write-Host "🔧 Checking MetaTrader processes..." -ForegroundColor Cyan

# Check MT4
$MT4_Process = Get-Process -Name "terminal" -ErrorAction SilentlyContinue
if ($MT4_Process) {
    Write-Host "✅ MT4 Terminal detected (PID: $($MT4_Process.Id))" -ForegroundColor Green
} else {
    Write-Host "❌ MT4 Terminal not running" -ForegroundColor Red
}

# Check MT5  
$MT5_Process = Get-Process -Name "terminal64" -ErrorAction SilentlyContinue
if ($MT5_Process) {
    Write-Host "✅ MT5 Terminal detected (PID: $($MT5_Process.Id))" -ForegroundColor Green
} else {
    Write-Host "❌ MT5 Terminal not running" -ForegroundColor Red
}

Write-Host ""
Write-Host "🔐 Login Information Display:" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow

if ($Platform -eq "mt4" -or $Platform -eq "both") {
    Write-Host "MT4 EXNESS Account:" -ForegroundColor Magenta
    Write-Host "  Login    : $MT4_Login" -ForegroundColor White
    Write-Host "  Password : $MT4_Password" -ForegroundColor White  
    Write-Host "  Server   : $MT4_Server" -ForegroundColor White
    Write-Host ""
}

if ($Platform -eq "mt5" -or $Platform -eq "both") {
    Write-Host "MT5 EXNESS Account:" -ForegroundColor Magenta
    Write-Host "  Login    : $MT5_Login" -ForegroundColor White
    Write-Host "  Password : $MT5_Password" -ForegroundColor White
    Write-Host "  Server   : $MT5_Server" -ForegroundColor White
    Write-Host ""
}

Write-Host "⚠️ MANUAL LOGIN REQUIRED:" -ForegroundColor Yellow
Write-Host "1. Open MetaTrader 4/5 platforms" -ForegroundColor White
Write-Host "2. Click 'File' > 'Login to Trade Account'" -ForegroundColor White
Write-Host "3. Enter the credentials shown above" -ForegroundColor White
Write-Host "4. Enable Expert Advisors (Ctrl+E)" -ForegroundColor White
Write-Host "5. Ensure AutoTrading is enabled" -ForegroundColor White

Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Green
Write-Host "- Verify successful login" -ForegroundColor White
Write-Host "- Check connection status" -ForegroundColor White
Write-Host "- Enable auto-trading features" -ForegroundColor White
Write-Host "- Start trading activities" -ForegroundColor White

Write-Host ""
Write-Host "📊 Organization: A6-9V | Status: Ready" -ForegroundColor Green