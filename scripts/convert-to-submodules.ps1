<#
.SYNOPSIS
  Convert nested Projects into git submodules and push nested repos to provided remotes.

.DESCRIPTION
  This script performs a safe conversion of the two nested projects Projects/A69VTestApp
  and Projects/ProductionApp into git submodules. It will create a backup, add the provided
  remotes to the nested repositories, push them, untrack the directories in the top-level
  repo, add submodules, commit, and push the top-level changes.

.PARAMETER A69VUrl
  HTTPS clone URL for the A69VTestApp repository (e.g. https://github.com/username/A69VTestApp.git)

.PARAMETER ProdUrl
  HTTPS clone URL for the ProductionApp repository (e.g. https://github.com/username/ProductionApp.git)

.PARAMETER Run
  If supplied, the script performs the operations. By default the script runs in dry-run mode.

Examples:
  # Dry-run (default)
  .\convert-to-submodules.ps1 -A69VUrl https://github.com/Mouy-leng/A69VTestApp.git -ProdUrl https://github.com/Mouy-leng/ProductionApp.git

  # Execute for real
  .\convert-to-submodules.ps1 -A69VUrl https://github.com/Mouy-leng/A69VTestApp.git -ProdUrl https://github.com/Mouy-leng/ProductionApp.git -Run
#>

param(
  [Parameter(Mandatory=$true)] [string] $A69VUrl,
  [Parameter(Mandatory=$true)] [string] $ProdUrl,
  [switch] $Run
)

function Log { param($m) Write-Host "[convert-submodules] $m" }

# Determine script root reliably
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if ($PSScriptRoot) { $scriptDir = $PSScriptRoot }
$root = Resolve-Path -Path (Join-Path $scriptDir '..')
Log "Workspace root: $root"

# Ensure git is available
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "git is not installed or not in PATH. Please install Git and retry."
}

$projectsDir = Join-Path $root 'Projects'
if (-not (Test-Path $projectsDir)) { throw "Projects directory not found at $projectsDir" }

$backup = Join-Path $root 'Projects-backup.zip'
Log "Creating backup of Projects -> $backup"
Compress-Archive -Path $projectsDir -DestinationPath $backup -Force

function RunIf([scriptblock]$scriptblock) {
  $text = $scriptblock.ToString().Trim()
  if ($Run) {
    Log "EXEC: $text"
    & $scriptblock
    if ($LASTEXITCODE -ne 0) { Log "Command exited with code $LASTEXITCODE" }
  } else {
    Log "DRY RUN: $text"
  }
}

function AddRemoteAndPush($path, $url) {
    if (-not (Test-Path $path)) { throw "Path not found: $path" }
    Log "Processing nested repo: $path"
  Push-Location $path
    try {
        # ensure it's a git repository
    if (-not (Test-Path '.git')) { throw "Not a git repository: $path" }

    $existing = git config --get remote.origin.url 2>$null
    if ([string]::IsNullOrWhiteSpace($existing) -or $LASTEXITCODE -ne 0) {
      Log "No existing origin remote. Will add origin -> $url"
      RunIf { git remote add origin $url }
    } else {
      Log "Existing remote.origin.url = $existing"
    }

    # ensure branch main exists and push
    Log "Ensure branch 'main' and push to origin"
    RunIf { git branch -M main }
    RunIf { git push -u origin main }
    } finally { Pop-Location }
}

# Add remotes and push nested repos
AddRemoteAndPush (Join-Path $projectsDir 'A69VTestApp') $A69VUrl
AddRemoteAndPush (Join-Path $projectsDir 'ProductionApp') $ProdUrl

# Convert top-level repo
Push-Location $root
try {
  Log "Untracking nested project folders (git rm --cached -r)"
  RunIf { git rm --cached -r --ignore-unmatch Projects/A69VTestApp Projects/ProductionApp }

  # commit if there are staged changes
  RunIf { if (-not (git diff --cached --quiet)) { git commit -m "chore: stop tracking nested project folders; prepare for submodules" } }

  Log "Adding submodules"
  RunIf { git submodule add $A69VUrl Projects/A69VTestApp }
  RunIf { git submodule add $ProdUrl Projects/ProductionApp }

  RunIf { git add .gitmodules } 
  RunIf { if (-not (git diff --cached --quiet)) { git commit -m "chore: add Projects/* as submodules" } }
  RunIf { git push origin main }
} finally { Pop-Location }

Log "Done. If you ran in dry-run mode, re-run with -Run to execute." 
