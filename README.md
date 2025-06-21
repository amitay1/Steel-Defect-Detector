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

## 🚀 Quick Start - הפעלה מהירה

### אופציה 1: הפעלה מהירה (מומלץ)
```batch
launch.bat
```

### אופציה 2: הפעלה ישירה
```bash
python app.py
```

המערכת תיפתח בדפדפן ב-http://localhost:7860

## מה תקבל

ממשק אינטרנטי מקצועי עם:

1. **🖼️ העלאת תמונות** - גרור ושחרר תמונות של מתכת
2. **⚙️ הגדרות חומר** - בחירת סוג מתכת, עובי ודרגת איכות
3. **🎯 ניתוח אוטומטי** - זיהוי פגמים עם בינה מלאכותית
4. **🟡 הדגשה צהובה** - פגמים מודגשים בדיוק פיקסל
5. **📊 דוחות מקצועיים** - ציונים, המלצות ועמידה בתקנים
6. **📁 הורדת קבצים** - דוחות JSON ותמונות מעובדות

**Direct Python (Any OS):**
```bash
python launcher.py
```

The unified launcher provides a professional menu with options for:
- 🔧 ASTM Defect Analysis System (Complete defect detection with standards compliance)
- 📋 Reference Card Manager (Generate ASTM reference cards)
- 🎯 Maximum Recall Detection (100% defect detection guarantee)
- 🎓 Model Training Pipeline
- 📊 System Information

For detailed instructions, see [QUICK_START.md](QUICK_START.md)

### 3. **View Statistics**:
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
Let's get it in order, first of all all the systems are nice and all but that's not what I need I need one system that knows how to do the following:
Knows how to receive an image to analyze it using our smart model
What the model will do The model will return to us with great accuracy the following: The image that was uploaded to it with all the defects in it highlighted in yellow It is very important that it be accurate, that is, an area where there is no defect will not be touched Let's color it at all
The model will also return what type of defect it is from the knowledge and training it has done If it did not recognize the defect it will write the message, I was not trained on this type of defect
The model will also return what type of defect it is from the knowledge and training it has done If it did not recognize the defect it will write the message, I was not trained on this type of defect
The model will also return Does the image meet the international standard How will it do this, the model will have access to the table that I sent before the model or you will use code to cross-reference the data you received through the user's website This data will give you a certain number like in the table itself, this number is the key to the success of the entire program, so like this The three pieces of data are the type of metal found in the image I uploaded, the thickness of the metal, and the type of defect that the model will have to identify using the learning system and all the images it received that it worked on, and our model is already trained for this. Maybe it needs to be reinforced for certain defects, that is, trained more. Okay, let's continue with the combination of these three pieces of data. It will bring you to a folder where we will find 8 images whose names are from 1 to 8. Now for the most important part of the program. Remember that I said earlier that you will receive a number from the table I also sent here with these instructions. This number will be the image that you or the model will use to compare. Now note that this is where it gets complicated. All we have done so far was so that you or the model would know for each type of data that the users will enter, of course, according to what we have defined for them. According to this, you will simply know which image to compare with which image. Okay, after we have received the correct image in front of us, we compare here, the difficulty comes in. Each image from 1 to 8 will be fine in terms of how big the defect is. The system cannot simply return an answer based on whether the circle in the image I sent is larger or smaller than the comparison image. It is much more complex than that. The system will have to calculate a square of pixels within the image that was sent and actually scan the entire image. It is enough that in one of the squares that you scanned there is a defect that is much larger in size than the square where the defect is located in the comparison image. The system will consider this as a FAIL, meaning that the image you sent did not pass the international standard test. Of course, everything will be written below in a professional result that is suitable for large and professional enterprises.
I ask you that this thing is very, very complex, so we will have to build it in stages. Please prepare a plan of how many steps you think need to be done to get through this accurately and professionally. We need to reach perfection without errors, so you can start successfully.