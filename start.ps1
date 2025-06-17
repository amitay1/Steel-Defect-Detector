# PowerShell script to run YOLOv8 Metal Defect Detection with Memory Bank

Write-Host "🔧 YOLOv8 Metal Defect Detection with Memory Bank" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Check if virtual environment exists
if (-not (Test-Path ".env\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found in .env folder" -ForegroundColor Red
    Write-Host "💡 Create one with: python -m venv .env" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "🐍 Activating virtual environment..." -ForegroundColor Green
& ".env\Scripts\Activate.ps1"

Write-Host "📦 Installing/updating requirements..." -ForegroundColor Green
pip install -r requirements.txt

Write-Host "🔍 Checking requirements..." -ForegroundColor Green
$checkCmd = "import ultralytics, gradio, cv2, numpy; print('✅ All dependencies available')"
try {
    python -c $checkCmd
} catch {
    Write-Host "❌ Missing dependencies. Installing..." -ForegroundColor Red
    pip install -r requirements.txt
}

Write-Host "🚀 Initializing Memory Bank system..." -ForegroundColor Green
$initCmd = @"
import os
from memory_bank import MemoryBank
if os.path.exists('memory_bank.db'):
    print('📊 Memory bank ready')
else:
    MemoryBank()
    print('📊 Memory bank initialized')
"@
python -c $initCmd

Write-Host "🌐 Starting Gradio application..." -ForegroundColor Green
Write-Host "📱 Open your browser to the URL shown below" -ForegroundColor Yellow
Write-Host "💾 All detections will be stored in the memory bank" -ForegroundColor Yellow
Write-Host "📊 View statistics in the 'Memory Bank Statistics' tab" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host ""

python app.py

Write-Host "👋 Application stopped" -ForegroundColor Green
Read-Host "Press Enter to exit"
