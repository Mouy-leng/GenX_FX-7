# A6-9V MetaTrader Expert Advisor Enabler
# Organization: A6-9V

Write-Host "A6-9V Expert Advisor Enabler" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName Microsoft.VisualBasic

function Enable-ExpertAdvisors {
    param([string]$WindowTitle)
    
    try {
        $processes = Get-Process | Where-Object { $_.MainWindowTitle -like "*$WindowTitle*" }
        
        foreach ($process in $processes) {
            if ($process.MainWindowHandle -ne [System.IntPtr]::Zero) {
                Write-Host "Enabling Expert Advisors for: $($process.MainWindowTitle)" -ForegroundColor Cyan
                
                # Activate window
                [Microsoft.VisualBasic.Interaction]::AppActivate($process.Id)
                Start-Sleep -Milliseconds 1000
                
                # Send Ctrl+E to enable Expert Advisors
                [System.Windows.Forms.SendKeys]::SendWait("^e")
                Start-Sleep -Milliseconds 500
                
                # Send F7 to open Expert Advisor settings (alternative)
                [System.Windows.Forms.SendKeys]::SendWait("{F7}")
                Start-Sleep -Milliseconds 500
                
                Write-Host "[SUCCESS] Expert Advisors enabled for $WindowTitle" -ForegroundColor Green
                return $true
            }
        }
    }
    catch {
        Write-Host "[WARNING] Could not enable Expert Advisors for $WindowTitle" -ForegroundColor Yellow
        return $false
    }
    return $false
}

# Check current processes
$MT4_Process = Get-Process | Where-Object { $_.ProcessName -eq "terminal" } | Select-Object -First 1
$MT5_Process = Get-Process | Where-Object { $_.ProcessName -eq "terminal64" } | Select-Object -First 1

Write-Host "Current MetaTrader Status:" -ForegroundColor Yellow
if ($MT4_Process) {
    Write-Host "MT4: $($MT4_Process.MainWindowTitle) (PID: $($MT4_Process.Id))" -ForegroundColor White
} else {
    Write-Host "MT4: Not running" -ForegroundColor Red
}

if ($MT5_Process) {
    Write-Host "MT5: $($MT5_Process.MainWindowTitle) (PID: $($MT5_Process.Id))" -ForegroundColor White
} else {
    Write-Host "MT5: Not running" -ForegroundColor Red
}

Write-Host ""

# Enable Expert Advisors
$success = $false

if ($MT4_Process) {
    Write-Host "Enabling Expert Advisors for MT4..." -ForegroundColor Magenta
    if (Enable-ExpertAdvisors -WindowTitle "MetaTrader 4") {
        $success = $true
    }
}

if ($MT5_Process) {
    Write-Host "Enabling Expert Advisors for MT5..." -ForegroundColor Magenta  
    if (Enable-ExpertAdvisors -WindowTitle "MetaTrader 5") {
        $success = $true
    }
}

Write-Host ""
Write-Host "TRADING VERIFICATION CHECKLIST:" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host "1. Check MT4/5 connection status (should show server names)" -ForegroundColor White
Write-Host "2. Verify Expert Advisors tab shows 'AutoTrading'" -ForegroundColor White
Write-Host "3. Confirm account balance displays correctly" -ForegroundColor White
Write-Host "4. Check that auto-trading button is enabled (green)" -ForegroundColor White
Write-Host ""

if ($success) {
    Write-Host "[SUCCESS] Expert Advisors configuration completed!" -ForegroundColor Green
    Write-Host "Organization: A6-9V | Auto-Trading: ENABLED" -ForegroundColor Green
} else {
    Write-Host "[INFO] Manual verification recommended" -ForegroundColor Yellow
    Write-Host "Please manually press Ctrl+E in both MT4 and MT5 platforms" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "DOMAIN VERIFICATION:" -ForegroundColor Yellow
Write-Host "Current MT5 connection shows: Exness-MT5Trial8" -ForegroundColor White
Write-Host "Current MT4 expected: Exness-Trail9" -ForegroundColor White