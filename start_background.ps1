# Start Chatbot in Background (Hidden Window)
# This keeps the server running even if you close the PowerShell window

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Geospatial Chatbot" -ForegroundColor Green
Write-Host "  (Background Mode)" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get the virtual environment Python path
$pythonPath = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
$appPath = Join-Path $PSScriptRoot "app.py"

# Check if already running
$existingProcess = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.Path -eq $pythonPath
}

if ($existingProcess) {
    Write-Host "⚠️  Chatbot is already running!" -ForegroundColor Yellow
    Write-Host "   Process ID: $($existingProcess.Id)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "To stop it, run: stop_chatbot.ps1" -ForegroundColor Cyan
} else {
    # Start in background (hidden window)
    $processInfo = Start-Process -FilePath $pythonPath `
                                  -ArgumentList $appPath `
                                  -WorkingDirectory $PSScriptRoot `
                                  -WindowStyle Hidden `
                                  -PassThru

    Write-Host "✅ Chatbot started in background!" -ForegroundColor Green
    Write-Host "   Process ID: $($processInfo.Id)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "📱 Access your chatbot at:" -ForegroundColor Cyan
    Write-Host "   http://localhost:8000" -ForegroundColor White
    Write-Host ""
    Write-Host "⏹️  To stop the server, run:" -ForegroundColor Yellow
    Write-Host "   .\stop_chatbot.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 The server will keep running even if you close this window!" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Wait for server to start
Write-Host "⏳ Waiting for server to initialize (30 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check if server is responding
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Server is ready and responding!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Opening browser..." -ForegroundColor Cyan
    Start-Process "http://localhost:8000"
} catch {
    Write-Host "⚠️  Server might still be loading. Give it another minute." -ForegroundColor Yellow
    Write-Host "   Then visit: http://localhost:8000" -ForegroundColor White
}

Write-Host ""
Read-Host "Press Enter to exit this window (server will keep running)"
