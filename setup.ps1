#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Automated setup script for Geospatial Chatbot
.DESCRIPTION
    This script creates a virtual environment, installs all dependencies,
    and prepares the chatbot for use. Works across different PCs.
.PARAMETER GPU
    Install GPU-enabled PyTorch (requires NVIDIA GPU with CUDA 12.1+)
.EXAMPLE
    .\setup.ps1
    .\setup.ps1 -GPU
#>

param(
    [switch]$GPU = $false
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Geospatial Chatbot Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python version
Write-Host "[1/6] Checking Python version..." -ForegroundColor Yellow
$pythonCmd = "python"
$pythonVersion = & $pythonCmd --version 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found. Please install Python 3.11 or higher." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

Write-Host "Found: $pythonVersion" -ForegroundColor Green

# Check if version is 3.11 or higher
$versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
if ($versionMatch) {
    $major = [int]$matches[1]
    $minor = [int]$matches[2]
    
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 11)) {
        Write-Host "WARNING: Python 3.11+ recommended. You have Python $major.$minor" -ForegroundColor Yellow
        Write-Host "The chatbot may work but could have compatibility issues." -ForegroundColor Yellow
        $continue = Read-Host "Continue anyway? (y/n)"
        if ($continue -ne "y") {
            exit 1
        }
    }
}

# Step 2: Create virtual environment
Write-Host "`n[2/6] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists. Removing old one..." -ForegroundColor Yellow
    Remove-Item -Path ".venv" -Recurse -Force
}

& $pythonCmd -m venv .venv

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create virtual environment." -ForegroundColor Red
    exit 1
}

Write-Host "Virtual environment created successfully!" -ForegroundColor Green

# Step 3: Activate virtual environment
Write-Host "`n[3/6] Activating virtual environment..." -ForegroundColor Yellow
$activateScript = ".\.venv\Scripts\Activate.ps1"

if (-not (Test-Path $activateScript)) {
    Write-Host "ERROR: Activation script not found at $activateScript" -ForegroundColor Red
    exit 1
}

& $activateScript

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment." -ForegroundColor Red
    exit 1
}

Write-Host "Virtual environment activated!" -ForegroundColor Green

# Step 4: Upgrade pip
Write-Host "`n[4/6] Upgrading pip..." -ForegroundColor Yellow
& .\.venv\Scripts\python.exe -m pip install --upgrade pip --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Failed to upgrade pip, continuing anyway..." -ForegroundColor Yellow
} else {
    Write-Host "pip upgraded successfully!" -ForegroundColor Green
}

# Step 5: Install dependencies
Write-Host "`n[5/6] Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take several minutes on first run..." -ForegroundColor Cyan

if ($GPU) {
    Write-Host "Installing with GPU support (CUDA 12.1)..." -ForegroundColor Cyan
    
    # Install CPU packages first (except torch/torchvision/torchaudio)
    Write-Host "  -> Installing core dependencies..." -ForegroundColor Gray
    & .\.venv\Scripts\pip.exe install fastapi==0.109.2 uvicorn[standard]==0.27.1 pymupdf==1.23.26 langchain==0.1.20 langchain-community==0.0.38 langchain-core==0.1.52 faiss-cpu==1.8.0 pydantic==2.6.4 pydantic-core==2.16.3 requests==2.31.0 sentence-transformers==2.5.1 huggingface-hub==0.21.4 transformers==4.38.2 tokenizers==0.15.2 numpy==1.26.4 safetensors==0.4.2 regex==2023.12.25 filelock==3.13.1 fsspec==2024.2.0 typing-extensions==4.10.0 annotated-types==0.6.0 --quiet
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install core dependencies." -ForegroundColor Red
        exit 1
    }
    
    # Install GPU-enabled PyTorch
    Write-Host "  -> Installing GPU-enabled PyTorch (this is large, ~2.5GB)..." -ForegroundColor Gray
    & .\.venv\Scripts\pip.exe install torch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 --index-url https://download.pytorch.org/whl/cu121
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install GPU PyTorch." -ForegroundColor Red
        Write-Host "Your system may not support CUDA 12.1. Try running without -GPU flag." -ForegroundColor Red
        exit 1
    }
    
} else {
    Write-Host "Installing with CPU support..." -ForegroundColor Cyan
    & .\.venv\Scripts\pip.exe install -r requirements.txt --quiet
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install dependencies." -ForegroundColor Red
        exit 1
    }
}

Write-Host "All dependencies installed successfully!" -ForegroundColor Green

# Step 6: Verify installation
Write-Host "`n[6/6] Verifying installation..." -ForegroundColor Yellow

$verifyScript = @"
import sys
import importlib

packages = [
    'fastapi',
    'uvicorn',
    'fitz',  # PyMuPDF
    'langchain',
    'langchain_community',
    'faiss',
    'pydantic',
    'sentence_transformers',
    'transformers',
    'torch'
]

print('Checking packages...')
failed = []
for pkg in packages:
    try:
        importlib.import_module(pkg)
        print(f'  ✓ {pkg}')
    except Exception as e:
        print(f'  ✗ {pkg}: {e}')
        failed.append(pkg)

if failed:
    print(f'\nERROR: Failed to import: {", ".join(failed)}')
    sys.exit(1)
else:
    print('\nAll packages verified successfully!')
    
# Check GPU if requested
import torch
if torch.cuda.is_available():
    print(f'\n✓ GPU detected: {torch.cuda.get_device_name(0)}')
    print(f'  CUDA version: {torch.version.cuda}')
else:
    print('\n✓ Running in CPU mode')
"@

$verifyScript | & .\.venv\Scripts\python.exe -

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nERROR: Package verification failed." -ForegroundColor Red
    Write-Host "Some packages may not have installed correctly." -ForegroundColor Red
    exit 1
}

# Step 7: Check for data folder
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path "data\geospatial_book.pdf")) {
    Write-Host "⚠ WARNING: PDF file not found at data\geospatial_book.pdf" -ForegroundColor Yellow
    Write-Host "  Please place your PDF in the data folder before starting." -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "To start the chatbot, run:" -ForegroundColor Cyan
Write-Host "  .\start_chatbot.bat" -ForegroundColor White
Write-Host ""
Write-Host "Or manually:" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\python.exe app.py" -ForegroundColor White
Write-Host ""
