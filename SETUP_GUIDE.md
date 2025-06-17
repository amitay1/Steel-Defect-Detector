# 🚀 Setup Guide for YOLOv8 Metal Defect Detection with Memory Bank

## Prerequisites
- Python 3.8+ installed on your system
- Git (optional, for version control)

## Setup Instructions

### 1. Virtual Environment (Already Created ✅)
Your project already has a virtual environment in the `.env` folder with all dependencies installed.

### 2. Quick Start Options

#### Option A: Automated Startup (Recommended)
```bash
# Windows Command Prompt
start.bat

# Windows PowerShell
.\start.ps1

# Any platform with Python
python start.py
```

#### Option B: Manual Steps
```bash
# 1. Activate virtual environment
.env\Scripts\activate.bat          # Windows
# source .env/bin/activate         # Linux/Mac

# 2. Initialize memory bank (first time only)
python memory_bank_cli.py init

# 3. Start application
python app.py
```

### 3. Verify Installation
```bash
# Check virtual environment status
python venv_manager.py status

# Test memory bank functionality  
python test_memory_bank.py

# View current statistics
python memory_bank_cli.py stats
```

## 📱 Using the Application

1. **Start the application** using one of the methods above
2. **Open your browser** to the URL displayed (usually http://127.0.0.1:7860)
3. **Upload an image** of metal surface in the "Defect Detection" tab
4. **View results** with detected defects highlighted
5. **Check statistics** in the "Memory Bank Statistics" tab

## 🔧 Management Commands

```bash
# View detection statistics
python memory_bank_cli.py stats

# Export detection data
python memory_bank_cli.py export results.json

# Clean old data (older than 30 days)
python memory_bank_cli.py cleanup --days 30

# Check virtual environment
python venv_manager.py status

# Install/update requirements
python venv_manager.py install
```

## 📊 Memory Bank Features

- **Automatic Storage**: All detections are automatically saved
- **Performance Tracking**: Monitor model accuracy over time
- **Statistics Dashboard**: View comprehensive analytics
- **Data Export**: Export results for external analysis
- **Duplicate Detection**: Avoid processing the same image twice
- **Configurable Retention**: Automatic cleanup of old data

## 🛠️ Troubleshooting

### Virtual Environment Issues
```bash
# Check if venv is working
python venv_manager.py status

# Recreate virtual environment if needed
rmdir /s .env                    # Windows
python -m venv .env
.env\Scripts\activate.bat
pip install -r requirements.txt
```

### Missing Dependencies
```bash
# Reinstall requirements
python venv_manager.py install
```

### Database Issues
```bash
# Reinitialize memory bank
del memory_bank.db               # Windows
python memory_bank_cli.py init
```

### Model File Missing
- Ensure `yolov8_model.pt` exists in the project folder
- Download or train your YOLOv8 model if missing

## 📂 Project Structure
```
yolov8-metal-defect-detection/
├── .env/                    # Virtual environment
├── app.py                   # Main Gradio application
├── memory_bank.py          # Memory bank core functionality
├── memory_bank_cli.py      # Command-line management
├── config.json             # Configuration settings
├── start.py/.bat/.ps1      # Startup scripts
├── venv_manager.py         # Virtual environment management
├── yolov8_model.pt         # Trained YOLOv8 model
├── memory_bank.db          # SQLite database (created automatically)
└── requirements.txt        # Python dependencies
```

## 🎯 Next Steps

1. **Test with sample images** to verify detection works
2. **Monitor statistics** to understand model performance
3. **Export data** periodically for backup
4. **Customize settings** in `config.json` as needed
5. **Set up regular cleanup** with scheduled tasks

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all files are present and model file exists
3. Ensure Python 3.8+ is installed
4. Try recreating the virtual environment

---

✅ **Your setup is complete and ready to use!**
