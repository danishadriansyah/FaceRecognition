# Week 8 - Complete Guide
## Face Recognition Attendance System - Final Project

Comprehensive guide untuk Final Capstone Project yang mengintegrasikan semua pembelajaran Week 1-7 menjadi production-ready attendance system.

---

## 🚀 Quick Start

```bash
cd minggu-8-final-project/project
python main_app.py
```

**That's it!** Desktop application akan langsung berjalan dengan:
- ✅ Teachable Machine model (Danis & Bella sudah trained)
- ✅ Face detection & recognition
- ✅ Attendance tracking
- ✅ Reports & analytics

---

## 📋 Project Overview

### Integration Summary

Week 8 mengintegrasikan semua modul dari Week 1-7:

- **Week 1:** Image processing utilities (`image_utils.py`)
- **Week 2:** Face detection dengan MediaPipe
- **Week 3:** Face recognition (MediaPipe Face Mesh)
- **Week 4:** Dataset management (pickle + JSON)
- **Week 5:** Recognition service integration
- **Week 6:** Attendance system & CSV logging
- **Week 7:** Desktop GUI dengan Tkinter

**Result:** Production-ready system yang siap deploy!

### Key Features

#### 1. Dashboard
- Live webcam preview dengan real-time face detection
- Statistics: total persons, today's attendance, system status
- Quick navigation ke semua fitur

#### 2. Person Registration
- Register person baru dengan detail (nama, ID, department, email)
- Auto-capture 20 photos dengan face detection
- Quality validation (blur, brightness, face size)
- **Duplicate detection** - checks existing model classes
- Export photos untuk Teachable Machine training

#### 3. Attendance Marking
- Real-time face recognition dari webcam
- Auto check-in/out dengan confidence threshold
- Manual fallback untuk unknown faces
- Cooldown timer (5 detik) prevent duplicate entries
- Visual feedback (bounding boxes, labels, confidence)

#### 4. Reports & Analytics
- Filter by date range (today, week, month, all)
- Search by name or ID
- Export to CSV
- Sortable columns dengan statistics

#### 5. System Management
- Model management (import, switch, rename, delete)
- Settings configuration
- System logs viewer
- Data validation & integrity checks

---

## 🎓 Teachable Machine Integration

### What is Teachable Machine?

Google's Teachable Machine adalah tool untuk train custom image classification models tanpa coding. Week 8 menggunakan TM untuk:

- ✅ Custom face recognition untuk orang-orang spesifik
- ✅ Fast training (1-3 menit)
- ✅ Easy re-training saat ada orang baru
- ✅ Lightweight & real-time capable

### Current Model

**Model Location:** `project/models/default_*/`
- `keras_model.h5` - Trained model
- `labels.txt` - Class labels

**Classes:** 
- Danis
- Bella

**Configuration:**
- Input size: 224x224 RGB
- Confidence threshold: 70% (adjustable)
- Framework: TensorFlow/Keras

### How It Works

```
Camera Frame
    ↓
MediaPipe Face Detection ← Detect faces in frame
    ↓
Crop Face Region ← Extract face bounding box
    ↓
Resize to 224x224 ← TM input size
    ↓
Keras Model Prediction ← Run through trained model
    ↓
Get Class + Confidence ← "Danis" (85%)
    ↓
Display Result ← Show with bounding box
```

### Switching Modes

**Teachable Machine Mode** (Default):
```python
# config.py
use_teachable_machine: bool = True
```

**MediaPipe Encoding Mode** (Alternative):
```python
use_teachable_machine: bool = False
```

**Comparison:**

| Feature | Teachable Machine | MediaPipe |
|---------|-------------------|-----------|
| Adding people | Re-train model | Dynamic (no retrain) |
| Speed | Very fast (30-60 FPS) | Fast (15-30 FPS) |
| Accuracy | High (trained) | Good (landmarks) |
| Setup | Need training | Auto-generate encodings |
| Best for | Fixed team | Changing visitors |

---

## 👤 Person Registration Workflow

### Complete Flow

```
1. Click "Register Person"
        ↓
2. Enter person details
        ↓
3. Click "Start Capture"
        ↓
4. System checks for duplicates
   ├─ Duplicate found → Show warning → User decides
   └─ New name → Show info → Continue
        ↓
5. Auto-capture 20 photos (0.5s interval)
        ↓
6. Click "Save Person"
        ↓
7. Photos saved to:
   • dataset_export/[Name]/ (for TM training)
   • dataset/[Name]/ (backup)
        ↓
8. Training instructions dialog appears
        ↓
9. User trains on Teachable Machine
        ↓
10. Import updated model
        ↓
11. Ready for recognition! ✅
```

### Duplicate Detection Feature

When starting capture, system automatically:
- ✅ Checks if name exists in active model
- ✅ Shows all existing classes
- ✅ Prompts user:
  - **YES:** Re-train with new photos (updates person)
  - **NO:** Cancel and choose different name

**Example Dialog:**
```
⚠️ The name 'Danis' already exists!

Existing classes:
  • Danis
  • Bella

Do you want to:
  YES - Re-train model with new photos
  NO - Cancel and choose a different name
```

### Directory Structure

```
minggu-8-final-project/
├── dataset_export/              ← For TM training
│   ├── Danis/
│   │   └── Danis_01.jpg ... Danis_20.jpg
│   ├── Bella/
│   └── NewPerson/
│
├── dataset/                     ← Backup
│   ├── Danis/
│   │   ├── metadata.json
│   │   └── photos...
│   └── ...
│
└── project/
    └── models/                  ← Trained models
        ├── default_20250115_143022/
        │   ├── keras_model.h5
        │   └── labels.txt
        └── models_metadata.json
```

---

## 🎯 Model Training Guide

### Step-by-Step Training Process

#### 1. Register Person in App
1. Open application
2. Click "Register Person"
3. Enter details (name, ID, department, email)
4. Click "Start Capture" → 20 photos captured
5. Click "Save Person"
6. Dialog shows training instructions

#### 2. Prepare Training Data
Photos automatically saved to `dataset_export/[Name]/`

#### 3. Train on Teachable Machine

**A. Open Teachable Machine**
- URL: https://teachablemachine.withgoogle.com/train/image
- Click "Get Started"
- Choose "Image Project" → "Standard image model"

**B. Import ALL Existing Classes** ⚠️ CRITICAL
For EACH person already in model:
1. Click "Add a class" 
2. Name it (e.g., "Danis")
3. Upload ALL photos from `dataset_export/Danis/`
4. Repeat for ALL existing people

**C. Add New Person**
1. Click "Add a class"
2. Name it (e.g., "NewPerson")
3. Upload photos from `dataset_export/NewPerson/`

**D. Train the Model**
1. Click "Train Model" 
2. Wait 1-3 minutes
3. Test with webcam (optional)

**E. Export the Model**
1. Click "Export Model" tab
2. Select "Tensorflow" → "Keras"
3. Click "Download my model"
4. Extract ZIP file

#### 4. Import to Application
1. In app: "Models" → "Import Model"
2. Select folder containing:
   - keras_model.h5
   - labels.txt
3. Enter model name
4. Click "Import"
5. Model auto-set as active ✅

### Important Notes

> [!WARNING]
> **ALWAYS Include ALL Classes When Re-training**
> 
> If you only upload the new person, model will FORGET everyone else!
> Keep `dataset_export/` organized with all person folders.

> [!TIP]
> **Recommended Workflow:**
> ```
> dataset_export/
> ├── Person1/  ← Keep existing
> ├── Person2/  ← Keep existing
> ├── Person3/  ← Keep existing
> └── NewPerson/  ← Add new
> ```
> Upload ALL folders to Teachable Machine!

### Model Quality Tips

**Photo Requirements:**
- Quantity: 20-30 photos per person
- Clarity: Clear, well-lit faces
- Variety: Different angles, expressions, lighting
- Background: Varied backgrounds

**Training Tips:**
- Balanced classes (similar photo counts)
- Train 2-3 times, keep best model
- Test before exporting
- Optional: Add "Unknown" class for better rejection

---

## 🏗️ Project Structure

```
minggu-8-final-project/
├── README.md                    # Quick reference
├── QUICK_REFERENCE.md          # Command reference
├── WEEK-8-COMPLETE-GUIDE.md    # This file
│
├── dataset_export/              # For TM training
├── dataset/                     # Backup storage
├── logs/                        # Application logs
│
└── project/                     # Main application
    ├── main_app.py             # Entry point
    ├── config.py               # Configuration
    │
    ├── core/                   # Backend modules
    │   ├── image_utils.py
    │   ├── face_detector.py
    │   ├── face_recognizer.py
    │   ├── teachable_recognizer.py
    │   ├── dataset_manager.py
    │   ├── recognition_service.py
    │   ├── attendance_system.py
    │   └── model_manager.py
    │
    ├── gui/                    # Desktop GUI
    │   ├── main_window.py
    │   ├── register_window.py
    │   ├── attendance_window.py
    │   ├── reports_window.py
    │   └── model_manager_window.py
    │
    ├── models/                 # Trained models
    │   └── default_*/
    │       ├── keras_model.h5
    │       └── labels.txt
    │
    └── docs/                   # Documentation
```

---

## ⚙️ Configuration

### File: `project/config.py`

```python
@dataclass
class RecognitionConfig:
    # Teachable Machine settings
    use_teachable_machine: bool = True
    teachable_model_path: str = "models/keras_model.h5"
    teachable_labels_path: str = "models/labels.txt"
    teachable_confidence: float = 0.7  # 70%
    
    # MediaPipe settings (if TM disabled)
    threshold: float = 0.6
    detection_confidence: float = 0.5

@dataclass
class AttendanceConfig:
    cooldown_seconds: int = 5  # Prevent duplicates
    
@dataclass
class PerformanceConfig:
    frame_skip: int = 2  # Process every N frames
    max_detection_size: int = 640
```

### Tuning Tips

**Recognition Too Strict (many unknowns):**
- Lower `teachable_confidence` to 0.6 or 0.5
- Ensure good lighting

**Recognition Too Permissive (false positives):**
- Raise `teachable_confidence` to 0.8
- Re-train with more varied photos

**Performance Issues:**
- Increase `frame_skip` (process fewer frames)
- Reduce `max_detection_size` to 480

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Model Not Found Error
**Symptoms:** "Failed to load model" or "Model not found"

**Solutions:**
- Check if `project/models/keras_model.h5` exists
- Import at least one model via "Models" → "Import Model"
- Verify `models_metadata.json` is not corrupted

#### 2. TensorFlow Not Installed
**Symptoms:** "Cannot import tensorflow"

**Solution:**
```bash
pip install tensorflow==2.15.0 keras==2.15.0
```

#### 3. Recognition Always Shows "Unknown"
**Symptoms:** Model doesn't recognize registered people

**Solutions:**
- Lower confidence: `teachable_confidence = 0.6`
- Check lighting conditions
- Re-train with more varied photos
- Ensure person exists in active model classes

#### 4. Webcam Not Detected
**Symptoms:** Black screen or "Cannot open webcam"

**Solutions:**
- Check camera permissions
- Try different camera index (0, 1, 2)
- Restart application
- Update camera drivers (Windows)

#### 5. Person Forgot After Re-training
**Symptoms:** Previously recognized person now shows "Unknown"

**Solution:**
- You forgot to include their class when re-training!
- Re-train again with ALL classes from `dataset_export/`

#### 6. Duplicate Attendance Entries
**Symptoms:** Same person checked in multiple times

**Solutions:**
- Increase `cooldown_seconds` to 10 or 15
- Check system time accuracy
- Review attendance logs for manual cleanup

### Performance Issues

**Slow FPS / Laggy Camera:**
- Increase `frame_skip` (default: 2 → try 3 or 4)
- Reduce `max_detection_size` (default: 640 → try 480)
- Close other applications
- Consider GPU acceleration:
  ```bash
  pip install tensorflow-gpu==2.15.0
  ```

---

## 📊 Testing & Verification

### Run Integration Tests
```bash
cd project/tests
python test_integration.py
```

**Expected:** All core modules load successfully

### Test Teachable Machine Module
```bash
cd project/core
python teachable_recognizer.py
```

- Opens webcam
- Press **SPACE** to recognize
- Press **Q** to quit

### Manual Testing Checklist

- [ ] Application starts without errors
- [ ] Webcam preview shows in dashboard
- [ ] Face detection works (green boxes appear)
- [ ] Recognition works for existing people
- [ ] Registration can capture photos
- [ ] Training instructions show after save
- [ ] Model import works
- [ ] Attendance marking records to CSV
- [ ] Reports filter and export correctly

---

## 🎯 Usage Examples

### Scenario 1: Fresh Installation
```bash
1. cd minggu-8-final-project/project
2. python main_app.py
3. Model auto-loads (Danis & Bella)
4. Click "Mark Attendance"
5. Face camera → auto check-in ✅
```

### Scenario 2: Adding New Person
```bash
1. Click "Register Person"
2. Enter "Charlie" as name
3. System shows: "New person. Existing: Danis, Bella"
4. Capture 20 photos
5. Click "Save"
6. Follow training instructions
7. Train on TM with ALL 3 classes (Danis, Bella, Charlie)
8. Import new model
9. Charlie now recognized! ✅
```

### Scenario 3: Updating Existing Person
```bash
1. Click "Register Person"
2. Enter "Danis"
3. Warning: "Name exists! Re-train?"
4. Choose YES
5. Capture 20 NEW photos
6. Train on TM with updated Danis photos
7. Import new model
8. Danis now recognized with new photos ✅
```

---

## 🚀 Deployment

### Option 1: Direct Python (Development)
```bash
python main_app.py
```

### Option 2: Executable (Production)
```bash
pip install pyinstaller

pyinstaller --onefile --windowed \
  --add-data "models:models" \
  --add-data "core:core" \
  --add-data "gui:gui" \
  main_app.py

# Output: dist/main_app.exe
```

### Option 3: Installer (Distribution)
Use Inno Setup (Windows) untuk create installer package

---

## 💡 Advanced Tips

### Hybrid Approach
- Use Teachable Machine untuk karyawan tetap
- Use MediaPipe mode untuk tamu/pengunjung sementara
- Switch via config: `use_teachable_machine = True/False`

### Model Versioning
- Models auto-timestamped: `name_YYYYMMDD_HHMMSS`
- Keep multiple models and switch via "Manage Models"
- Test new models before replacing active

### Backup Strategy
- `dataset_export/` → For re-training
- `dataset/` → Backup with metadata
- `models/` → All trained models
- `logs/attendance.csv` → Attendance records

Regular backup: Copy entire `minggu-8-final-project/` folder

---

## 📚 Additional Resources

**Documentation:**
- Main README: Overview & quick start
- QUICK_REFERENCE.md: Commands & shortcuts
- WEEK-8-COMPLETE-GUIDE.md: This comprehensive guide

**External Links:**
- [Teachable Machine](https://teachablemachine.withgoogle.com/)
- [MediaPipe Docs](https://google.github.io/mediapipe/)
- [TensorFlow/Keras](https://www.tensorflow.org/guide/keras)

---

## 🎉 Completion Checklist

### Learning Completed
- [x] Week 1: Image processing
- [x] Week 2: Face detection
- [x] Week 3: Face recognition
- [x] Week 4: Dataset management
- [x] Week 5: Recognition service
- [x] Week 6: Attendance system
- [x] Week 7: Desktop GUI
- [x] Week 8: Production integration ← **You are here!**

### Skills Mastered
- ✅ Python programming
- ✅ Computer Vision (OpenCV)
- ✅ Machine Learning (Teachable Machine, MediaPipe)
- ✅ Face Detection & Recognition
- ✅ GUI Development (Tkinter)
- ✅ Software Engineering (modular design, testing)
- ✅ Production Deployment

**Congratulations! 🎉**

You've completed the entire Face Recognition Attendance System course and built a production-ready application!

---

**Last Updated:** January 13, 2026  
**Version:** 2.0  
**Status:** Production Ready ✅
