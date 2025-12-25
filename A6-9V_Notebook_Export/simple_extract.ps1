# A6-9V NotebookLM Simple Extractor
Write-Host "A6-9V NotebookLM Content Tool" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Green

$notebookUrl = "https://notebooklm.google.com/notebook/4824ad0b-4f53-4b06-a641-cb8f3bd90622"
$exportDir = "C:\Users\lengk\Dropbox\OneDrive\Desktop\A6-9V_Notebook_Export"

# Copy URL to clipboard and open browser
Set-Clipboard -Value $notebookUrl
Write-Host "URL copied to clipboard: $notebookUrl" -ForegroundColor Yellow
Start-Process $notebookUrl

# Create organization folders
$folders = @("01_Places", "02_Environments", "03_Development", "04_Production", "05_Testing", "06_A6-9V_Docs")

foreach ($folder in $folders) {
    $path = Join-Path $exportDir $folder
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force
        Write-Host "Created: $folder" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host "1. Browser opened to NotebookLM" -ForegroundColor White
Write-Host "2. Look for Export/Download options in NotebookLM" -ForegroundColor White  
Write-Host "3. Save exported files to: $exportDir" -ForegroundColor White
Write-Host "4. Organize content into the created folders" -ForegroundColor White

Write-Host ""
Write-Host "Organization folders created for A6-9V:" -ForegroundColor Yellow
foreach ($folder in $folders) {
    Write-Host "  - $folder" -ForegroundColor White
}