Param(
  [switch]$Dev
)

Write-Host "Bootstrapping A6-9V Trading Workspace..."

# Ensure Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Write-Error "Git is required. Install Git and re-run."
  exit 1
}

# Python optional
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  Write-Host "Python not found. Skipping Python env."
} else {
  Write-Host "Python $(python --version) detected."
}

# Create local env sample
$envFile = ".env.sample"
if (-not (Test-Path $envFile)) {
  @(
    "# Copy to .env and fill values",
    "GITHUB_APP_ID=",
    "GITHUB_APP_INSTALLATION_ID=",
    "GITHUB_APP_PRIVATE_KEY=",
    "GITHUB_APP_WEBHOOK_SECRET="
  ) | Set-Content -NoNewline:$false $envFile
  Write-Host "Created $envFile"
}

Write-Host "Bootstrap complete. Review docs in docs/TRADING_SYSTEM and docs/GITHUB_APP_SETUP.md"


