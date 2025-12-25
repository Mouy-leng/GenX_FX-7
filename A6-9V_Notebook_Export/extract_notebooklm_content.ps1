# A6-9V NotebookLM Content Extractor
# PowerShell script to help extract and organize NotebookLM content

Write-Host "A6-9V NotebookLM Content Extraction Tool" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host ""

$notebookUrl = "https://notebooklm.google.com/notebook/4824ad0b-4f53-4b06-a641-cb8f3bd90622"
$exportDir = "C:\Users\lengk\Dropbox\OneDrive\Desktop\A6-9V_Notebook_Export"

Write-Host "Target Notebook URL: $notebookUrl" -ForegroundColor Yellow
Write-Host "Export Directory: $exportDir" -ForegroundColor Yellow
Write-Host ""

Write-Host "INSTRUCTIONS:" -ForegroundColor Cyan
Write-Host "1. Open the NotebookLM URL in your browser (link saved to clipboard)"
Write-Host "2. In NotebookLM, look for Export or Download options"
Write-Host "3. Download the content as Text, Markdown, or JSON format"
Write-Host "4. Save the downloaded file to: $exportDir"
Write-Host "5. Run this script again to organize the content"
Write-Host ""

# Copy URL to clipboard
Set-Clipboard -Value $notebookUrl
Write-Host "✓ NotebookLM URL copied to clipboard!" -ForegroundColor Green
Write-Host ""

# Check if any files have been downloaded
$downloadedFiles = Get-ChildItem -Path $exportDir -File | Where-Object { $_.Name -notlike "*.ps1" -and $_.Name -notlike "*.md" }

if ($downloadedFiles.Count -gt 0) {
    Write-Host "Downloaded files found:" -ForegroundColor Green
    foreach ($file in $downloadedFiles) {
        Write-Host "  - $($file.Name)" -ForegroundColor White
    }
    Write-Host ""
    
    # Ask user if they want to organize the content
    $organize = Read-Host "Do you want to organize the content by place and environment? (Y/N)"
    
    if ($organize -match '^[Yy]') {
        Write-Host "Organizing content..." -ForegroundColor Yellow
        
        # Create organization structure
        $directories = @(
            "01_Places",
            "02_Environments", 
            "03_Development",
            "04_Production", 
            "05_Testing",
            "06_Documentation",
            "07_A6-9V_Organization"
        )
        
        foreach ($dir in $directories) {
            $fullPath = Join-Path $exportDir $dir
            if (-not (Test-Path $fullPath)) {
                New-Item -ItemType Directory -Path $fullPath | Out-Null
                Write-Host "✓ Created directory: $dir" -ForegroundColor Green
            }
        }
        
        Write-Host ""
        Write-Host "Organization structure created!" -ForegroundColor Green
        Write-Host "Please manually sort your content into the appropriate directories:" -ForegroundColor Yellow
        foreach ($dir in $directories) {
            Write-Host "  - $dir" -ForegroundColor White
        }
    }
} else {
    Write-Host "No downloaded files found yet." -ForegroundColor Yellow
    Write-Host "Please download content from NotebookLM first." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")