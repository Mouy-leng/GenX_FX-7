# A6-9V MetaTrader Auto-Login Script
# Organization: A6-9V
# Purpose: Automated login for MT4/5 trading platforms

param(
    [string]$Platform = "both",
    [int]$WaitTime = 30
)

Write-Host "🚀 A6-9V MetaTrader Auto-Login Script" -ForegroundColor Green
Write-Host "═══════════════════════════════════════=" -ForegroundColor Green

# Trading Account Configurations
$MT4_CONFIG = @{
    Login = "70559995"
    Password = "Leng12345@#`$01"
    Server = "Exness-Trail9"
    ProcessName = "terminal.exe"
    WindowTitle = "*MetaTrader 4*"
}

$MT5_CONFIG = @{
    Login = "279260115"
    Password = "Leng12345@#`$01"
    Server = "Exness-MT5Trail8"
    ProcessName = "terminal64.exe"
    WindowTitle = "*MetaTrader 5*"
}

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

function Send-KeysToWindow {
    param(
        [string]$WindowTitle,
        [string]$Keys,
        [int]$Delay = 500
    )
    
    try {
        $window = Get-Process | Where-Object { $_.MainWindowTitle -like $WindowTitle } | Select-Object -First 1
        if ($window) {
            $handle = $window.MainWindowHandle
            if ($handle -ne [System.IntPtr]::Zero) {
                [Microsoft.VisualBasic.Interaction]::AppActivate($window.Id)
                Start-Sleep -Milliseconds $Delay
                [System.Windows.Forms.SendKeys]::SendWait($Keys)
                return $true
            }
        }
    }
    catch {
        Write-Warning "Failed to send keys to window: $($_.Exception.Message)"
    }
    return $false
}

function Login-MetaTrader {
    param(
        [hashtable]$Config,
        [string]$PlatformName
    )
    
    Write-Host "🔑 Attempting login for $PlatformName..." -ForegroundColor Yellow
    
    # Wait for platform to load
    Write-Host "   ⏳ Waiting for $PlatformName to initialize..." -ForegroundColor Cyan
    Start-Sleep -Seconds $WaitTime
    
    # Check if process is running
    $processName = $Config.ProcessName -replace '\.exe$', ''
    $process = Get-Process -Name $processName -ErrorAction SilentlyContinue
    if (-not $process) {
        Write-Warning "   ❌ $PlatformName process not found!"
        return $false
    }
    
    Write-Host "   ✅ $PlatformName process detected" -ForegroundColor Green
    
    # Try to access login dialog
    Start-Sleep -Seconds 5
    
    # Send Ctrl+O to open login dialog (standard MT4/5 shortcut)
    if (Send-KeysToWindow -WindowTitle $Config.WindowTitle -Keys "^o" -Delay 1000) {
        Write-Host "   📋 Login dialog opened" -ForegroundColor Cyan
        
        # Clear any existing text and enter login
        Send-KeysToWindow -WindowTitle $Config.WindowTitle -Keys "^a" -Delay 300
        Send-KeysToWindow -WindowTitle $Config.WindowTitle -Keys $Config.Login -Delay 500
        
        # Tab to password field
        Send-KeysToWindow -WindowTitle $Config.WindowTitle -Keys "{TAB}" -Delay 300
        
        # Clear and enter password
        Send-KeysToWindow -WindowTitle $Config.WindowTitle -Keys "^a" -Delay 300
        Send-KeysToWindow -WindowTitle $Config.WindowTitle -Keys $Config.Password -Delay 500
        
        # Tab to server field
        Send-KeysToWindow -WindowTitle $Config.WindowTitle -Keys "{TAB}" -Delay 300
        
        # Clear and enter server
        Send-KeysToWindow -WindowTitle $Config.WindowTitle -Keys "^a" -Delay 300
        Send-KeysToWindow -WindowTitle $Config.WindowTitle -Keys $Config.Server -Delay 500
        
        # Press Enter to login
        Send-KeysToWindow -WindowTitle $Config.WindowTitle -Keys "{ENTER}" -Delay 1000
        
        Write-Host "   🎯 Login credentials submitted for $PlatformName" -ForegroundColor Green
        
        # Wait for login to complete
        Start-Sleep -Seconds 10
        
        return $true
    }
    else {
        Write-Warning "   ❌ Could not access $PlatformName login dialog"
        return $false
    }
}

function Enable-AutoTrading {
    param(
        [hashtable]$Config,
        [string]$PlatformName
    )
    
    Write-Host "🤖 Enabling auto-trading for $PlatformName..." -ForegroundColor Yellow
    
    # Enable Expert Advisors (Ctrl+E)
    if (Send-KeysToWindow -WindowTitle $Config.WindowTitle -Keys "^e" -Delay 1000) {
        Write-Host "   ✅ Expert Advisors enabled for $PlatformName" -ForegroundColor Green
    }
    
    # Enable AutoTrading button (if needed)
    Start-Sleep -Seconds 2
}

# Main execution
Write-Host "🔧 Initializing auto-login process..." -ForegroundColor Cyan
Write-Host "   Platform: $Platform" -ForegroundColor White
Write-Host "   Wait Time: $WaitTime seconds" -ForegroundColor White
Write-Host ""

# Add required assemblies for SendKeys
Add-Type -AssemblyName Microsoft.VisualBasic

$success = $false

if ($Platform -eq "mt4" -or $Platform -eq "both") {
    Write-Host "📈 Processing MT4 Login..." -ForegroundColor Magenta
    if (Login-MetaTrader -Config $MT4_CONFIG -PlatformName "MT4") {
        Enable-AutoTrading -Config $MT4_CONFIG -PlatformName "MT4"
        $success = $true
    }
}

if ($Platform -eq "mt5" -or $Platform -eq "both") {
    Write-Host "📊 Processing MT5 Login..." -ForegroundColor Magenta
    if (Login-MetaTrader -Config $MT5_CONFIG -PlatformName "MT5") {
        Enable-AutoTrading -Config $MT5_CONFIG -PlatformName "MT5"
        $success = $true
    }
}

# Final status
Write-Host ""
Write-Host "═══════════════════════════════════════=" -ForegroundColor Green
if ($success) {
    Write-Host "✅ A6-9V Auto-Login Process Completed!" -ForegroundColor Green
    Write-Host "🎯 Trading platforms are ready for automated trading" -ForegroundColor Yellow
} else {
    Write-Host "⚠️ Some issues occurred during login process" -ForegroundColor Yellow
    Write-Host "📝 Manual verification recommended" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🔐 MANUAL VERIFICATION REQUIRED:" -ForegroundColor Red
Write-Host "   • Check MT4/5 connection status" -ForegroundColor White
Write-Host "   • Verify Expert Advisors are enabled" -ForegroundColor White
Write-Host "   • Confirm auto-trading is active" -ForegroundColor White
Write-Host ""
Write-Host "📊 Organization: A6-9V | Status Ready" -ForegroundColor Green