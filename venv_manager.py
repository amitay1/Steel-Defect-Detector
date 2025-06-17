#!/usr/bin/env python3
"""
Virtual Environment Management Script for YOLOv8 Metal Defect Detection
"""

import os
import sys
import subprocess
from pathlib import Path

def create_venv():
    """Create a new virtual environment"""
    print("🐍 Creating virtual environment in .env folder...")
    
    try:
        subprocess.run([sys.executable, "-m", "venv", ".env"], check=True)
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating virtual environment: {e}")
        return False

def install_requirements():
    """Install requirements in the virtual environment"""
    print("📦 Installing requirements...")
    
    venv_python = get_venv_python()
    if not venv_python:
        return False
    
    try:
        subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def get_venv_python():
    """Get the path to Python in the virtual environment"""
    if os.name == 'nt':  # Windows
        venv_python = Path(".env/Scripts/python.exe")
    else:  # Linux/Mac
        venv_python = Path(".env/bin/python")
    
    if venv_python.exists():
        return str(venv_python)
    else:
        print("❌ Virtual environment Python not found")
        return None

def check_venv_status():
    """Check the status of the virtual environment"""
    print("🔍 Checking virtual environment status...")
    
    venv_path = Path(".env")
    if not venv_path.exists():
        print("❌ Virtual environment not found")
        return False
    
    venv_python = get_venv_python()
    if not venv_python:
        return False
    
    print("✅ Virtual environment found")
    
    # Check Python version
    try:
        result = subprocess.run([venv_python, "--version"], capture_output=True, text=True, check=True)
        print(f"🐍 Python version: {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("⚠️  Could not get Python version")
    
    # Check installed packages
    try:
        result = subprocess.run([venv_python, "-m", "pip", "list"], capture_output=True, text=True, check=True)
        packages = result.stdout.split('\n')
        print(f"📦 Installed packages: {len(packages) - 2}")  # -2 for header lines
        
        # Check for required packages
        required = ['ultralytics', 'gradio', 'opencv-python', 'numpy']
        installed_packages = result.stdout.lower()
        
        for package in required:
            if package in installed_packages:
                print(f"  ✅ {package}")
            else:
                print(f"  ❌ {package} (missing)")
    
    except subprocess.CalledProcessError:
        print("⚠️  Could not list installed packages")
    
    return True

def run_in_venv(command):
    """Run a command in the virtual environment"""
    venv_python = get_venv_python()
    if not venv_python:
        return False
    
    try:
        subprocess.run([venv_python] + command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {e}")
        return False

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("🔧 Virtual Environment Management")
        print("=" * 35)
        print("Usage:")
        print("  python venv_manager.py create     - Create virtual environment")
        print("  python venv_manager.py install    - Install requirements")
        print("  python venv_manager.py status     - Check venv status")
        print("  python venv_manager.py run <cmd>  - Run command in venv")
        return
    
    command = sys.argv[1].lower()
    
    if command == "create":
        create_venv()
    elif command == "install":
        install_requirements()
    elif command == "status":
        check_venv_status()
    elif command == "run":
        if len(sys.argv) > 2:
            run_in_venv(sys.argv[2:])
        else:
            print("❌ No command specified to run")
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()
