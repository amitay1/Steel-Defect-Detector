@echo off
REM Simple script to activate the virtual environment

echo 🐍 Activating virtual environment...
call .env\Scripts\activate.bat

echo ✅ Virtual environment activated!
echo 💡 You can now run:
echo    - python app.py (to start the application)
echo    - python memory_bank_cli.py stats (to view statistics)
echo    - python start.py (full startup with checks)
echo.
echo 🔧 Current environment:
python --version
echo.

cmd /k
