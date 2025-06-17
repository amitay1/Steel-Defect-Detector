@echo off
REM Activate virtual environment and run the YOLOv8 Metal Defect Detection app

echo 🔧 YOLOv8 Metal Defect Detection with Memory Bank
echo ==================================================

REM Check if virtual environment exists
if not exist ".env\Scripts\activate.bat" (
    echo ❌ Virtual environment not found in .env folder
    echo 💡 Create one with: python -m venv .env
    pause
    exit /b 1
)

echo 🐍 Activating virtual environment...
call .env\Scripts\activate.bat

echo 📦 Installing/updating requirements...
pip install -r requirements.txt

echo 🔍 Checking requirements...
python -c "import ultralytics, gradio, cv2, numpy; print('✅ All dependencies available')" 2>nul
if errorlevel 1 (
    echo ❌ Missing dependencies. Installing...
    pip install -r requirements.txt
)

echo 🚀 Initializing Memory Bank system...
python -c "import os; from memory_bank import MemoryBank; print('📊 Memory bank ready') if os.path.exists('memory_bank.db') else MemoryBank() and print('📊 Memory bank initialized')"

echo 🌐 Starting Gradio application...
echo 📱 Open your browser to the URL shown below
echo 💾 All detections will be stored in the memory bank
echo 📊 View statistics in the 'Memory Bank Statistics' tab
echo.
echo Press Ctrl+C to stop the application
echo.

python app.py

echo 👋 Application stopped
pause
