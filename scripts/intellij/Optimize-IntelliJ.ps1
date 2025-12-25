# Optimize-IntelliJ.ps1 - IntelliJ IDEA optimization and maintenance script
[CmdletBinding()]
param(
    [Parameter()]
    [switch]$ClearCache,
    
    [Parameter()]
    [switch]$OptimizeMemory,
    
    [Parameter()]
    [switch]$UpdatePlugins,
    
    [Parameter()]
    [switch]$BackupSettings,
    
    [Parameter()]
    [switch]$RestoreSettings,
    
    [Parameter()]
    [string]$BackupPath = ".\IntelliJ-Backup",
    
    [Parameter()]
    [switch]$All
)

$ErrorActionPreference = "Stop"

function Write-OptimizationBanner {
    Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║                 🔧 IntelliJ IDEA Optimizer                   ║
║                        A6-9V Edition                         ║
╚══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Magenta
}

function Get-IntelliJConfigPaths {
    $paths = @()
    
    # JetBrains Toolbox locations
    $toolboxPaths = Get-ChildItem -Path "$env:LOCALAPPDATA\JetBrains\Toolbox\apps\IDEA-*" -ErrorAction SilentlyContinue
    foreach ($path in $toolboxPaths) {
        $configPath = Get-ChildItem -Path "$($path.FullName)\ch-0\*" -ErrorAction SilentlyContinue | 
                      Sort-Object LastWriteTime -Descending | 
                      Select-Object -First 1
        if ($configPath) {
            $paths += $configPath.FullName
        }
    }
    
    # Standard installation locations
    $standardPaths = @(
        "$env:LOCALAPPDATA\JetBrains",
        "$env:APPDATA\JetBrains"
    )
    
    foreach ($basePath in $standardPaths) {
        $intellijDirs = Get-ChildItem -Path "$basePath\IntelliJIdea*" -ErrorAction SilentlyContinue
        foreach ($dir in $intellijDirs) {
            $paths += $dir.FullName
        }
    }
    
    return $paths
}

function Clear-IntelliJCaches {
    Write-Host "🧹 Clearing IntelliJ IDEA caches..." -ForegroundColor Yellow
    
    $configPaths = Get-IntelliJConfigPaths
    $clearedCount = 0
    
    foreach ($configPath in $configPaths) {
        Write-Host "📁 Checking: $configPath" -ForegroundColor Gray
        
        $cacheDirs = @("system", "caches", "logs", "tmp")
        foreach ($cacheDir in $cacheDirs) {
            $fullPath = Join-Path $configPath $cacheDir
            if (Test-Path $fullPath) {
                try {
                    Remove-Item -Path $fullPath -Recurse -Force -ErrorAction SilentlyContinue
                    Write-Host "  ✅ Cleared: $cacheDir" -ForegroundColor Green
                    $clearedCount++
                } catch {
                    Write-Warning "  ⚠️ Failed to clear: $cacheDir - $_"
                }
            }
        }
    }
    
    if ($clearedCount -gt 0) {
        Write-Host "✨ Cache cleanup completed! Cleared $clearedCount directories." -ForegroundColor Green
    } else {
        Write-Host "ℹ️ No caches found to clear." -ForegroundColor Blue
    }
}

function Optimize-IntelliJMemory {
    Write-Host "⚡ Optimizing IntelliJ IDEA memory settings..." -ForegroundColor Yellow
    
    # Get available system memory
    $totalMemory = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 0)
    $recommendedHeap = [math]::Min([math]::Max($totalMemory * 0.25, 2), 8) * 1024
    
    Write-Host "🖥️ System RAM: ${totalMemory}GB, Recommended heap: ${recommendedHeap}MB" -ForegroundColor Cyan
    
    $configPaths = Get-IntelliJConfigPaths
    $optimizedCount = 0
    
    foreach ($configPath in $configPaths) {
        # Look for IntelliJ installation
        $installPath = $configPath
        if ($configPath -like "*Toolbox*") {
            $installPath = $configPath
        } else {
            # Try to find installation from config path
            $possibleInstalls = @(
                "${env:ProgramFiles}\JetBrains\IntelliJ IDEA*\bin",
                "${env:ProgramFiles(x86)}\JetBrains\IntelliJ IDEA*\bin"
            )
            
            foreach ($possibleInstall in $possibleInstalls) {
                $resolved = Get-ChildItem -Path $possibleInstall -ErrorAction SilentlyContinue | Select-Object -First 1
                if ($resolved) {
                    $installPath = $resolved.FullName
                    break
                }
            }
        }
        
        if ($installPath -and (Test-Path $installPath)) {
            $vmOptionsFiles = @(
                (Join-Path $installPath "idea64.exe.vmoptions"),
                (Join-Path $installPath "idea.exe.vmoptions")
            )
            
            foreach ($vmOptionsFile in $vmOptionsFiles) {
                if (Test-Path (Split-Path $vmOptionsFile -Parent)) {
                    Write-Host "📝 Updating: $vmOptionsFile" -ForegroundColor Gray
                    
                    $optimizedOptions = @(
                        "-Xmx${recommendedHeap}m",
                        "-Xms512m",
                        "-XX:ReservedCodeCacheSize=512m",
                        "-XX:+UseG1GC",
                        "-XX:SoftRefLRUPolicyMSPerMB=50",
                        "-XX:CICompilerCount=2",
                        "-XX:+HeapDumpOnOutOfMemoryError",
                        "-XX:-OmitStackTraceInFastThrow",
                        "-ea",
                        "-Dsun.io.useCanonPrefixCache=false",
                        "-Djdk.http.auth.tunneling.disabledSchemes=",
                        "-Djava.system.class.loader=com.intellij.util.lang.PathClassLoader",
                        "-Dfile.encoding=UTF-8"
                    )
                    
                    try {
                        Set-Content -Path $vmOptionsFile -Value $optimizedOptions -Force
                        Write-Host "  ✅ Memory settings optimized" -ForegroundColor Green
                        $optimizedCount++
                    } catch {
                        Write-Warning "  ⚠️ Failed to update VM options: $_"
                    }
                }
            }
        }
    }
    
    if ($optimizedCount -gt 0) {
        Write-Host "⚡ Memory optimization completed! Updated $optimizedCount configuration(s)." -ForegroundColor Green
    } else {
        Write-Host "ℹ️ No IntelliJ installations found to optimize." -ForegroundColor Blue
    }
}

function Update-IntelliJPlugins {
    Write-Host "🔌 Updating IntelliJ IDEA plugins..." -ForegroundColor Yellow
    
    # This would typically require IntelliJ to be running
    Write-Host "ℹ️ Plugin updates require IntelliJ IDEA to be running." -ForegroundColor Blue
    Write-Host "📋 Recommended plugins for A6-9V development:" -ForegroundColor Cyan
    
    $recommendedPlugins = @(
        "Maven Helper",
        "Gradle",
        "Spring Boot",
        "Lombok",
        "GitToolBox",
        "SonarLint",
        "CheckStyle-IDEA",
        "FindBugs-IDEA",
        "Docker",
        "AWS Toolkit",
        ".ignore",
        "Rainbow Brackets",
        "Key Promoter X"
    )
    
    foreach ($plugin in $recommendedPlugins) {
        Write-Host "  • $plugin" -ForegroundColor White
    }
    
    Write-Host "💡 Install these via File → Settings → Plugins in IntelliJ IDEA" -ForegroundColor Yellow
}

function Backup-IntelliJSettings {
    param([string]$BackupPath)
    
    Write-Host "💾 Backing up IntelliJ IDEA settings..." -ForegroundColor Yellow
    
    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $backupDir = Join-Path $BackupPath "IntelliJ-Backup-$timestamp"
    $null = New-Item -ItemType Directory -Path $backupDir -Force
    
    $configPaths = Get-IntelliJConfigPaths
    $backedUpCount = 0
    
    foreach ($configPath in $configPaths) {
        $configDir = Join-Path $configPath "config"
        if (Test-Path $configDir) {
            $versionName = Split-Path $configPath -Leaf
            $targetDir = Join-Path $backupDir $versionName
            
            try {
                Copy-Item -Path $configDir -Destination $targetDir -Recurse -Force
                Write-Host "  ✅ Backed up: $versionName" -ForegroundColor Green
                $backedUpCount++
            } catch {
                Write-Warning "  ⚠️ Failed to backup: $versionName - $_"
            }
        }
    }
    
    if ($backedUpCount -gt 0) {
        Write-Host "💾 Settings backup completed! Location: $backupDir" -ForegroundColor Green
        return $backupDir
    } else {
        Write-Host "ℹ️ No settings found to backup." -ForegroundColor Blue
        return $null
    }
}

function Restore-IntelliJSettings {
    param([string]$BackupPath)
    
    Write-Host "🔄 Restoring IntelliJ IDEA settings..." -ForegroundColor Yellow
    
    if (-not (Test-Path $BackupPath)) {
        Write-Error "❌ Backup path not found: $BackupPath"
        return
    }
    
    # List available backups
    $backups = Get-ChildItem -Path $BackupPath -Directory | Sort-Object LastWriteTime -Descending
    
    if ($backups.Count -eq 0) {
        Write-Error "❌ No backups found in: $BackupPath"
        return
    }
    
    Write-Host "📋 Available backups:" -ForegroundColor Cyan
    for ($i = 0; $i -lt $backups.Count; $i++) {
        Write-Host "  $($i + 1). $($backups[$i].Name)" -ForegroundColor White
    }
    
    $selection = Read-Host "Select backup to restore (1-$($backups.Count))"
    try {
        $selectedIndex = [int]$selection - 1
        if ($selectedIndex -ge 0 -and $selectedIndex -lt $backups.Count) {
            $selectedBackup = $backups[$selectedIndex]
            Write-Host "🔄 Restoring from: $($selectedBackup.Name)" -ForegroundColor Yellow
            
            $configPaths = Get-IntelliJConfigPaths
            $restoredCount = 0
            
            foreach ($configPath in $configPaths) {
                $configDir = Join-Path $configPath "config"
                $versionName = Split-Path $configPath -Leaf
                $backupConfigDir = Join-Path $selectedBackup.FullName $versionName
                
                if (Test-Path $backupConfigDir) {
                    try {
                        if (Test-Path $configDir) {
                            Remove-Item -Path $configDir -Recurse -Force
                        }
                        Copy-Item -Path $backupConfigDir -Destination $configDir -Recurse -Force
                        Write-Host "  ✅ Restored: $versionName" -ForegroundColor Green
                        $restoredCount++
                    } catch {
                        Write-Warning "  ⚠️ Failed to restore: $versionName - $_"
                    }
                }
            }
            
            if ($restoredCount -gt 0) {
                Write-Host "🔄 Settings restoration completed! Restored $restoredCount configuration(s)." -ForegroundColor Green
            } else {
                Write-Host "ℹ️ No matching configurations found to restore." -ForegroundColor Blue
            }
        } else {
            Write-Error "❌ Invalid selection: $selection"
        }
    } catch {
        Write-Error "❌ Invalid selection: $selection"
    }
}

function Show-IntelliJStatus {
    Write-Host "📊 IntelliJ IDEA Status Report" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════" -ForegroundColor Gray
    
    $configPaths = Get-IntelliJConfigPaths
    if ($configPaths.Count -eq 0) {
        Write-Host "❌ No IntelliJ IDEA installations found" -ForegroundColor Red
        return
    }
    
    foreach ($configPath in $configPaths) {
        $versionName = Split-Path $configPath -Leaf
        Write-Host "📁 $versionName" -ForegroundColor White
        
        # Check cache sizes
        $cacheDirs = @("system", "caches", "logs", "tmp")
        $totalSize = 0
        foreach ($cacheDir in $cacheDirs) {
            $fullPath = Join-Path $configPath $cacheDir
            if (Test-Path $fullPath) {
                $size = (Get-ChildItem -Path $fullPath -Recurse -ErrorAction SilentlyContinue | 
                        Measure-Object -Property Length -Sum).Sum / 1MB
                $totalSize += $size
                Write-Host "  $cacheDir`: $([math]::Round($size, 2)) MB" -ForegroundColor Gray
            }
        }
        Write-Host "  Total Cache: $([math]::Round($totalSize, 2)) MB" -ForegroundColor Yellow
        Write-Host ""
    }
}

# Main execution
try {
    Write-OptimizationBanner
    
    if ($All) {
        $ClearCache = $true
        $OptimizeMemory = $true
        $BackupSettings = $true
    }
    
    Show-IntelliJStatus
    
    if ($BackupSettings) {
        $backupLocation = Backup-IntelliJSettings -BackupPath $BackupPath
        if ($backupLocation) {
            Write-Host "💾 Backup saved to: $backupLocation" -ForegroundColor Green
        }
    }
    
    if ($RestoreSettings) {
        Restore-IntelliJSettings -BackupPath $BackupPath
    }
    
    if ($ClearCache) {
        Clear-IntelliJCaches
    }
    
    if ($OptimizeMemory) {
        Optimize-IntelliJMemory
    }
    
    if ($UpdatePlugins) {
        Update-IntelliJPlugins
    }
    
    Write-Host "✨ IntelliJ IDEA optimization completed!" -ForegroundColor Green
    Write-Host "💡 Restart IntelliJ IDEA to apply all changes." -ForegroundColor Yellow
    
} catch {
    Write-Error "❌ Optimization failed: $_"
    exit 1
}

# Example usage:
# .\Optimize-IntelliJ.ps1 -All
# .\Optimize-IntelliJ.ps1 -ClearCache -OptimizeMemory
# .\Optimize-IntelliJ.ps1 -BackupSettings -BackupPath "D:\Backups"