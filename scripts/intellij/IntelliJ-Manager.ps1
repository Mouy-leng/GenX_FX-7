# IntelliJ-Manager.ps1 - Master automation script for IntelliJ IDEA
param(
    [Parameter(Position = 0)]
    [ValidateSet("Start", "New", "Optimize", "Status", "Help")]
    [string]$Action = "Help",
    
    [Parameter(Position = 1)]
    [string]$ProjectName,
    
    [Parameter()]
    [ValidateSet("Java", "Maven", "Gradle", "Spring", "Kotlin")]
    [string]$ProjectType = "Maven",
    
    [Parameter()]
    [string]$ProjectPath,
    
    [Parameter()]
    [switch]$Fresh,
    
    [Parameter()]
    [switch]$DebugMode,
    
    [Parameter()]
    [int]$MaxMemory = 4096
)

$ErrorActionPreference = "Stop"

function Write-ManagerBanner {
    Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║                  🎯 IntelliJ IDEA Manager                    ║
║                       A6-9V Edition                          ║
║                All-in-One Development Tool                   ║
╚══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor DarkCyan
}

function Show-Help {
    Write-Host @"
IntelliJ IDEA Manager - A6-9V Edition

USAGE:
    .\IntelliJ-Manager.ps1 <Action> [Options]

ACTIONS:
    Start       Launch IntelliJ IDEA with optimizations
    New         Create a new project and open in IntelliJ
    Optimize    Run optimization and maintenance tasks
    Status      Show IntelliJ status and system info
    Help        Show this help message

EXAMPLES:
    # Start IntelliJ IDEA
    .\IntelliJ-Manager.ps1 Start

    # Start with specific project
    .\IntelliJ-Manager.ps1 Start -ProjectPath "C:\Projects\MyApp"

    # Create new Maven project
    .\IntelliJ-Manager.ps1 New "MyApp" -ProjectType Maven

    # Create new Spring Boot project
    .\IntelliJ-Manager.ps1 New "SpringDemo" -ProjectType Spring

    # Optimize IntelliJ with fresh cache clear
    .\IntelliJ-Manager.ps1 Optimize -Fresh

    # Check IntelliJ status
    .\IntelliJ-Manager.ps1 Status

OPTIONS:
    -ProjectName    Name of the new project to create
    -ProjectType    Type of project (Java, Maven, Gradle, Spring, Kotlin)
    -ProjectPath    Path to existing project to open
    -Fresh          Clear caches and start fresh
    -Debug          Enable debug mode
    -MaxMemory      Maximum memory allocation in MB (default: 4096)

KEYBOARD SHORTCUTS:
    Ctrl+Shift+A    Find Action
    Ctrl+Shift+F    Find in Files
    Ctrl+N          Find Class
    Ctrl+Shift+N    Find File
    Alt+Enter       Show Intention Actions
    Ctrl+/          Toggle Line Comment
    Ctrl+Shift+/    Toggle Block Comment
    Ctrl+D          Duplicate Line
    Ctrl+Y          Delete Line
    Ctrl+Shift+Up   Move Statement Up
    Ctrl+Shift+Down Move Statement Down

A6-9V TOOLS INTEGRATION:
    - Automatic project templates with A6-9V conventions
    - Optimized memory and performance settings
    - Pre-configured development environment
    - Git integration with A6-9V standards
    - DevContainer support for consistent environments

"@ -ForegroundColor White
}

function Test-Scripts {
    $scriptPath = $PSScriptRoot
    $requiredScripts = @(
        "Start-IntelliJ.ps1",
        "New-IntelliJProject.ps1",
        "Optimize-IntelliJ.ps1"
    )
    
    foreach ($script in $requiredScripts) {
        $fullPath = Join-Path $scriptPath $script
        if (-not (Test-Path $fullPath)) {
            Write-Error "❌ Required script not found: $script"
            Write-Host "Please ensure all A6-9V IntelliJ scripts are in the same directory." -ForegroundColor Yellow
            return $false
        }
    }
    return $true
}

function Invoke-StartAction {
    param($ProjectPath, $MaxMemory, $Fresh, $DebugMode)
    
    Write-Host "🚀 Starting IntelliJ IDEA..." -ForegroundColor Green
    
    $startScript = Join-Path $PSScriptRoot "Start-IntelliJ.ps1"
    $arguments = @()
    
    if ($ProjectPath) { $arguments += "-ProjectPath", $ProjectPath }
    if ($MaxMemory -ne 4096) { $arguments += "-MaxMemory", $MaxMemory }
    if ($Fresh) { $arguments += "-Fresh" }
    if ($DebugMode) { $arguments += "-Debug" }
    
    & $startScript @arguments
}

function Invoke-NewAction {
    param($ProjectName, $ProjectType)
    
    if (-not $ProjectName) {
        $ProjectName = Read-Host "Enter project name"
        if (-not $ProjectName) {
            Write-Error "❌ Project name is required"
            return
        }
    }
    
    Write-Host "📦 Creating new $ProjectType project: $ProjectName" -ForegroundColor Blue
    
    $newProjectScript = Join-Path $PSScriptRoot "New-IntelliJProject.ps1"
    $arguments = @($ProjectName, "-ProjectType", $ProjectType, "-GroupId", "com.a69v", "-OpenInIntelliJ")
    
    & $newProjectScript @arguments
}

function Invoke-OptimizeAction {
    param($Fresh)
    
    Write-Host "🔧 Optimizing IntelliJ IDEA..." -ForegroundColor Magenta
    
    $optimizeScript = Join-Path $PSScriptRoot "Optimize-IntelliJ.ps1"
    $arguments = @()
    $arguments += "-OptimizeMemory"
    $arguments += "-BackupSettings"
    
    if ($Fresh) {
        $arguments += "-ClearCache"
    }
    
    & $optimizeScript @arguments
}

function Show-Status {
    Write-Host "📊 IntelliJ IDEA System Status" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════" -ForegroundColor Gray
    
    # System Information
    $os = Get-CimInstance Win32_OperatingSystem
    $cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
    $memory = Get-CimInstance Win32_ComputerSystem
    
    Write-Host "🖥️ System Information:" -ForegroundColor Yellow
    Write-Host "   OS: $($os.Caption) $($os.Version)" -ForegroundColor White
    Write-Host "   CPU: $($cpu.Name)" -ForegroundColor White
    Write-Host "   RAM: $([math]::Round($memory.TotalPhysicalMemory / 1GB, 1))GB" -ForegroundColor White
    Write-Host ""
    
    # Java Information
    Write-Host "☕ Java Environment:" -ForegroundColor Yellow
    try {
        $javaVersion = java -version 2>&1 | Select-Object -First 1
        Write-Host "   $javaVersion" -ForegroundColor White
        
        $javaHome = $env:JAVA_HOME
        if ($javaHome) {
            Write-Host "   JAVA_HOME: $javaHome" -ForegroundColor White
        } else {
            Write-Host "   JAVA_HOME: Not set" -ForegroundColor Red
        }
    } catch {
        Write-Host "   Java: Not found or not in PATH" -ForegroundColor Red
    }
    Write-Host ""
    
    # IntelliJ Status
    Write-Host "🔧 IntelliJ IDEA:" -ForegroundColor Yellow
    $intellijProcesses = Get-Process -Name "*idea*" -ErrorAction SilentlyContinue
    if ($intellijProcesses) {
        Write-Host "   Status: Running ($($intellijProcesses.Count) process(es))" -ForegroundColor Green
        foreach ($process in $intellijProcesses) {
            $memory = [math]::Round($process.WorkingSet / 1MB, 0)
            Write-Host "     PID $($process.Id): ${memory}MB" -ForegroundColor Gray
        }
    } else {
        Write-Host "   Status: Not running" -ForegroundColor Yellow
    }
    Write-Host ""
    
    # Project Information
    Write-Host "📁 Current Directory Projects:" -ForegroundColor Yellow
    $currentDir = Get-Location
    $projectFiles = @()
    
    # Look for project indicators
    if (Test-Path "pom.xml") { $projectFiles += "Maven (pom.xml)" }
    if (Test-Path "build.gradle") { $projectFiles += "Gradle (build.gradle)" }
    if (Test-Path ".idea") { $projectFiles += "IntelliJ (.idea)" }
    if (Test-Path "src") { $projectFiles += "Source (src/)" }
    
    if ($projectFiles.Count -gt 0) {
        foreach ($file in $projectFiles) {
            Write-Host "   ✅ $file" -ForegroundColor Green
        }
    } else {
        Write-Host "   No project files detected" -ForegroundColor Gray
    }
    Write-Host ""
    
    # DevContainer Status
    Write-Host "🐳 DevContainer:" -ForegroundColor Yellow
    if (Test-Path ".devcontainer") {
        Write-Host "   ✅ DevContainer configuration found" -ForegroundColor Green
        if (Test-Path ".devcontainer/devcontainer.json") {
            Write-Host "   ✅ devcontainer.json present" -ForegroundColor Green
        }
        if (Test-Path ".devcontainer/Dockerfile") {
            Write-Host "   ✅ Dockerfile present" -ForegroundColor Green
        }
    } else {
        Write-Host "   ⚪ No DevContainer configuration" -ForegroundColor Gray
    }
    Write-Host ""
    
    # Git Status
    Write-Host "🔗 Git Repository:" -ForegroundColor Yellow
    try {
        if (Test-Path ".git") {
            $gitBranch = git rev-parse --abbrev-ref HEAD 2>$null
            $gitStatus = git status --porcelain 2>$null
            Write-Host "   ✅ Git repository (branch: $gitBranch)" -ForegroundColor Green
            
            if ($gitStatus) {
                $changes = ($gitStatus | Measure-Object).Count
                Write-Host "   📝 Uncommitted changes: $changes" -ForegroundColor Yellow
            } else {
                Write-Host "   ✅ Working directory clean" -ForegroundColor Green
            }
        } else {
            Write-Host "   ⚪ Not a Git repository" -ForegroundColor Gray
        }
    } catch {
        Write-Host "   ❌ Git not available" -ForegroundColor Red
    }
}

# Main execution
try {
    Write-ManagerBanner
    
    # Verify all required scripts are present
    if (-not (Test-Scripts)) {
        exit 1
    }
    
    switch ($Action.ToLower()) {
        "start" {
            Invoke-StartAction -ProjectPath $ProjectPath -MaxMemory $MaxMemory -Fresh $Fresh -DebugMode $DebugMode
        }
        "new" {
            Invoke-NewAction -ProjectName $ProjectName -ProjectType $ProjectType
        }
        "optimize" {
            Invoke-OptimizeAction -Fresh $Fresh
        }
        "status" {
            Show-Status
        }
        "help" {
            Show-Help
        }
        default {
            Write-Warning "❌ Unknown action: $Action"
            Show-Help
        }
    }
    
} catch {
    Write-Error "❌ Error executing action '$Action': $_"
    exit 1
}

# Quick access aliases
Write-Host ""
Write-Host "💡 Quick Commands:" -ForegroundColor DarkGray
Write-Host "   .\IntelliJ-Manager.ps1 Start" -ForegroundColor DarkGray
Write-Host "   .\IntelliJ-Manager.ps1 New MyApp" -ForegroundColor DarkGray
Write-Host "   .\IntelliJ-Manager.ps1 Optimize" -ForegroundColor DarkGray