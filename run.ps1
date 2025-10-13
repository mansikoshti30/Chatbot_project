# PowerShell script to run the Geospatial Chatbot

Write-Host "🌍 Starting Geospatial Information Chatbot..." -ForegroundColor Green
Write-Host ""

# Check if OpenAI API key is set
if (-not $env:OPENAI_API_KEY) {
    Write-Host "⚠️  WARNING: OPENAI_API_KEY is not set!" -ForegroundColor Yellow
    Write-Host "Please set it using: `$env:OPENAI_API_KEY='your-api-key'" -ForegroundColor Yellow
    Write-Host ""
}

# Check if PDF exists
if (-not (Test-Path "data\geospatial_book.pdf")) {
    Write-Host "⚠️  WARNING: PDF file not found at data\geospatial_book.pdf" -ForegroundColor Yellow
    Write-Host "Please add your PDF file to the data directory." -ForegroundColor Yellow
    Write-Host ""
}

# Check if dependencies are installed
Write-Host "📦 Checking dependencies..." -ForegroundColor Cyan
$result = python -c "import fastapi, uvicorn" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Dependencies not installed!" -ForegroundColor Red
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "🚀 Starting server on http://localhost:8000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the application
python app.py
