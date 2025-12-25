# Helper to install and run the Playwright exporter on Windows (pwsh)
# Edit $env:BROWSER_USER_DATA_DIR to point to your Chrome/Edge profile if you want to reuse signed-in session.

param()

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$exportDir = $scriptDir
$playwrightDir = Join-Path $exportDir 'export_notebooklm_playwright'

# Set this to your browser profile directory if you are signed in to Google there
# Example Chrome Default: C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default
# Example Edge Default:   C:\Users\<username>\AppData\Local\Microsoft\Edge\User Data\Default
$env:BROWSER_USER_DATA_DIR = $env:BROWSER_USER_DATA_DIR

Write-Host "Working directory: $exportDir"
Write-Host "Playwright folder: $playwrightDir"

if (-not (Test-Path $playwrightDir)) {
    Write-Host "Playwright folder missing: $playwrightDir"
    exit 1
}

Push-Location $playwrightDir

Write-Host "Installing npm dependencies (this may take a minute)..."
# Install dependencies
npm install

Write-Host "Running export script..."
npm run export

Pop-Location

Write-Host "Export complete. Check files in: $exportDir"