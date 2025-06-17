---
title: Yolov8 Metal Defect Detection with Memory Bank
emoji: �
colorFrom: indigo
colorTo: gray
sdk: gradio
sdk_version: 5.29.0
app_file: app.py
pinned: false
---

# 🔧 YOLOv8 Metal Defect Detection with Memory Bank

An advanced metal surface defect detection system using YOLOv8 with integrated memory bank functionality for tracking detection history, performance metrics, and building knowledge base.

## Features

### 🎯 Defect Detection
- Real-time detection of metal surface defects
- Support for multiple defect types (crazing, scratches, pitting, inclusion, patches, rolled-in scale)
- Confidence scoring and bounding box visualization

### 🧠 Memory Bank System
- **Detection History**: Store and retrieve all detection results
- **Performance Tracking**: Monitor model performance over time
- **Knowledge Base**: Build expertise database from detection patterns
- **Statistics Dashboard**: Comprehensive analytics and reporting
- **Data Export**: Export detection data for analysis
- **Automatic Cleanup**: Manage storage with configurable data retention

### 📊 Analytics Features
- Detection confidence statistics
- Defect type distribution analysis
- Daily/weekly performance trends
- Similar detection matching
- User feedback integration

## Quick Start

1. **Initialize Memory Bank**:
   ```bash
   python memory_bank_cli.py init
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **View Statistics**:
   ```bash
   python memory_bank_cli.py stats
   ```

## Memory Bank CLI Commands

- `python memory_bank_cli.py init` - Initialize database
- `python memory_bank_cli.py stats` - Show statistics  
- `python memory_bank_cli.py export output.json` - Export data
- `python memory_bank_cli.py cleanup --days 30` - Clean old data

## Configuration

Edit `config.json` to customize:
- Model confidence thresholds
- Data retention periods
- Defect type definitions
- Performance parameters

## Database Schema

The memory bank uses SQLite with tables for:
- `defect_detections` - Individual detection records
- `model_performance` - Performance metrics over time
- `user_sessions` - User interaction tracking
- `knowledge_base` - Defect pattern information

## API Integration

The memory bank can be integrated into other applications:

```python
from memory_bank import MemoryBank, DefectDetection

# Initialize
memory_bank = MemoryBank()

# Store detection
detection = DefectDetection(...)
memory_bank.store_detection(detection)

# Query history
history = memory_bank.get_detection_history(defect_type="scratch")
```

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

## 🐍 Virtual Environment Setup

This project is configured to use a Python virtual environment located in the `.env` folder.

### Quick Start with Virtual Environment

**Option 1: Use the startup scripts**
```bash
# Windows Batch
start.bat

# Windows PowerShell  
.\start.ps1

# Cross-platform Python
python start.py
```

**Option 2: Manual activation**
```bash
# Windows
.env\Scripts\activate.bat

# Linux/Mac
source .env/bin/activate

# Then run the app
python app.py
```

### Virtual Environment Management

```bash
# Check venv status
python venv_manager.py status

# Install requirements in venv
python venv_manager.py install

# Run commands in venv
python venv_manager.py run app.py
```
