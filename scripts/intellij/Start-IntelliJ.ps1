# Start-IntelliJ.ps1 - Launch IntelliJ IDEA with optimizations
param(
    [Parameter(Position = 0)]
    [string]$ProjectPath,
    
    [Parameter()]
    [ValidateSet("Community", "Ultimate")]
    [string]$Edition = "Ultimate",
    
    [Parameter()]
    [int]$MaxMemory = 4096,
    
    [Parameter()]
    [switch]$DebugMode,
    
    [Parameter()]
    [switch]$Fresh
)

$ErrorActionPreference = "Stop"

# Configuration
$IntelliJPaths = @{
    "Ultimate" = @(
        "$env:LOCALAPPDATA\JetBrains\Toolbox\apps\IDEA-U\ch-0\*\bin\idea64.exe",
        "${env:ProgramFiles}\JetBrains\IntelliJ IDEA*\bin\idea64.exe",
        "${env:ProgramFiles(x86)}\JetBrains\IntelliJ IDEA*\bin\idea64.exe"
    )
    "Community" = @(
        "$env:LOCALAPPDATA\JetBrains\Toolbox\apps\IDEA-C\ch-0\*\bin\idea64.exe",
        "${env:ProgramFiles}\JetBrains\IntelliJ IDEA Community Edition*\bin\idea64.exe"
    )
}

function Write-Banner {
    Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║                    🚀 IntelliJ IDEA Launcher                 ║
║                         A6-9V Edition                        ║
╚══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan
}

function Find-IntelliJExecutable {
    param([string]$Edition)
    
    Write-Host "🔍 Looking for IntelliJ IDEA $Edition..." -ForegroundColor Yellow
    
    foreach ($path in $IntelliJPaths[$Edition]) {
        $resolved = Get-ChildItem -Path $path -ErrorAction SilentlyContinue | 
                   Sort-Object LastWriteTime -Descending | 
                   Select-Object -First 1
        
        if ($resolved) {
            Write-Host "✅ Found: $($resolved.FullName)" -ForegroundColor Green
            return $resolved.FullName
        }
    }
    
    throw "❌ IntelliJ IDEA $Edition not found. Please install it first."
}

function Set-IntelliJMemory {
    param([string]$IntelliJPath, [int]$MaxMemory)
    
    $configDir = Split-Path -Parent $IntelliJPath
    $vmoptions = Join-Path $configDir "idea64.exe.vmoptions"
    
    if (-not (Test-Path $vmoptions)) {
        Write-Host "📝 Creating VM options file..." -ForegroundColor Yellow
        $null = New-Item -ItemType File -Path $vmoptions -Force
    }
    
    $optimizedSettings = @(
        "-Xmx${MaxMemory}m",
        "-Xms512m",
        "-XX:ReservedCodeCacheSize=512m",
        "-XX:+UseConcMarkSweepGC",
        "-XX:SoftRefLRUPolicyMSPerMB=50",
        "-ea",
        "-XX:CICompilerCount=2",
        "-Dsun.io.useCanonPrefixCache=false",
        "-Djdk.http.auth.tunneling.disabledSchemes=",
        "-XX:+HeapDumpOnOutOfMemoryError",
        "-XX:-OmitStackTraceInFastThrow",
        "-Djb.vmOptionsFile=$vmoptions",
        "-Djava.system.class.loader=com.intellij.util.lang.PathClassLoader"
    )
    
    Set-Content -Path $vmoptions -Value $optimizedSettings -Force
    Write-Host "⚡ Optimized memory settings applied (Max: ${MaxMemory}MB)" -ForegroundColor Green
}

function Start-IntelliJWithProject {
    param([string]$IntelliJPath, [string]$ProjectPath, [bool]$DebugMode)
    
    $arguments = @()
    
    if ($ProjectPath) {
        if (Test-Path $ProjectPath) {
            $arguments += $ProjectPath
            Write-Host "📁 Opening project: $ProjectPath" -ForegroundColor Green
        } else {
            Write-Warning "⚠️ Project path not found: $ProjectPath"
        }
    }
    
    if ($DebugMode) {
        $arguments += "--debug"
        Write-Host "🐛 Debug mode enabled" -ForegroundColor Magenta
    }
    
    Write-Host "🚀 Starting IntelliJ IDEA..." -ForegroundColor Green
    Start-Process -FilePath $IntelliJPath -ArgumentList $arguments -NoNewWindow
}

function Clear-IntelliJCache {
    $cacheLocations = @(
        "$env:LOCALAPPDATA\JetBrains\IntelliJIdea*",
        "$env:APPDATA\JetBrains\IntelliJIdea*"
    )
    
    Write-Host "🧹 Clearing IntelliJ cache and system files..." -ForegroundColor Yellow
    
    foreach ($location in $cacheLocations) {
        $paths = Get-ChildItem -Path $location -ErrorAction SilentlyContinue
        foreach ($path in $paths) {
            $systemPath = Join-Path $path.FullName "system"
            if (Test-Path $systemPath) {
                Remove-Item -Path $systemPath -Recurse -Force -ErrorAction SilentlyContinue
                Write-Host "✅ Cleared: $systemPath" -ForegroundColor Green
            }
        }
    }
}

# Main execution
try {
    Write-Banner
    
    if ($Fresh) {
        Clear-IntelliJCache
    }
    
    $intellijPath = Find-IntelliJExecutable -Edition $Edition
    Set-IntelliJMemory -IntelliJPath $intellijPath -MaxMemory $MaxMemory
    Start-IntelliJWithProject -IntelliJPath $intellijPath -ProjectPath $ProjectPath -DebugMode $DebugMode
    
    Write-Host "✨ IntelliJ IDEA is starting up!" -ForegroundColor Cyan
    
} catch {
    Write-Error "❌ Failed to start IntelliJ IDEA: $_"
    exit 1
}

# Example usage:
# .\Start-IntelliJ.ps1
# .\Start-IntelliJ.ps1 -ProjectPath "C:\Projects\MyProject"
# .\Start-IntelliJ.ps1 -MaxMemory 8192 -Debug
# .\Start-IntelliJ.ps1 -Fresh