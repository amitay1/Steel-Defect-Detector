#!/usr/bin/env python3
"""
Startup script for YOLOv8 Metal Defect Detection with Memory Bank
Designed to work with virtual environment in .env folder
"""

import os
import sys
import subprocess
from pathlib import Path

def check_venv():
    """Check if we're running in the virtual environment"""
    venv_path = Path(".env")
    if not venv_path.exists():
        print("❌ Virtual environment not found in .env folder")
        print("💡 Create one with: python -m venv .env")
        return False
    
    # Check if we're in the venv by looking at sys.prefix
    expected_venv = str(venv_path.resolve())
    current_prefix = str(Path(sys.prefix).resolve())
    
    if expected_venv not in current_prefix:
        print("⚠️  Not running in virtual environment")
        print("💡 Run: .env\\Scripts\\activate.bat (Windows) or source .env/bin/activate (Linux/Mac)")
        print("💡 Or use: start.bat (Windows)")
        return False
    
    print("✅ Virtual environment active")
    return True

def check_requirements():
    """Check if all required files and dependencies are available"""
    print("🔍 Checking requirements...")
    
    required_files = [
        "yolov8_model.pt",
        "app.py", 
        "memory_bank.py",
        "config.json"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    try:
        import ultralytics
        import gradio
        import cv2
        import numpy as np
        import sqlite3
        print("✅ All dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Install with: pip install -r requirements.txt")
        return False

def initialize_system():
    """Initialize the memory bank system"""
    print("🚀 Initializing Memory Bank system...")
    
    from memory_bank import MemoryBank
    
    # Initialize memory bank if it doesn't exist
    if not os.path.exists("memory_bank.db"):
        print("📊 Creating new memory bank database...")
        memory_bank = MemoryBank()
        print("✅ Memory bank initialized")
    else:
        print("✅ Memory bank database found")
    
    return True

def start_application():
    """Start the Gradio application"""
    print("🌐 Starting Gradio application...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "app.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting application: {e}")
        return False
    except KeyboardInterrupt:
        print("👋 Application stopped by user")
        return True

def main():
    """Main startup function"""
    print("🔧 YOLOv8 Metal Defect Detection with Memory Bank")
    print("=" * 50)
    
    # Check virtual environment
    if not check_venv():
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Initialize system
    if not initialize_system():
        sys.exit(1)
    
    # Start application
    print("\n🎯 System ready! Starting application...")
    print("📱 Open your browser to the URL shown below")
    print("💾 All detections will be stored in the memory bank")
    print("📊 View statistics in the 'Memory Bank Statistics' tab")
    print("\nPress Ctrl+C to stop the application\n")
    
    start_application()

if __name__ == "__main__":
    main()
