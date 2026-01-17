# Minggu 8: Final Capstone Project

## 🎯 Face Recognition Attendance System - Production Ready

Complete integration dari semua pembelajaran Week 1-7 menjadi production-ready attendance system dengan desktop GUI.

---

## 🚀 Quick Start

```bash
cd minggu-8-final-project/project
python main_app.py
```

**That's it!** Desktop application akan langsung berjalan.

---

## 📋 What You'll Build

Production-ready attendance system yang mengintegrasikan:

- ✅ **Week 1-3:** Image processing, face detection & recognition
- ✅ **Week 4-5:** Dataset management & recognition service
- ✅ **Week 6:** Attendance tracking & logging
- ✅ **Week 7:** Desktop GUI
- ✅ **Week 8:** Production deployment dengan Teachable Machine integration

---

## 🎨 Key Features

1. **Dashboard** - Live webcam preview dengan statistics
2. **Person Registration** - Auto-capture 20 photos dengan duplicate detection
3. **Attendance Marking** - Real-time face recognition & auto check-in/out
4. **Reports & Analytics** - Filter, search, export to CSV
5. **Model Management** - Import, switch, manage Teachable Machine models

---

## 📚 Documentation

### Complete Guide
**See:** [WEEK-8-COMPLETE-GUIDE.md](WEEK-8-COMPLETE-GUIDE.md) - Comprehensive documentation dengan:
- Teachable Machine integration
- Person registration workflow
- Model training guide
- Troubleshooting
- Configuration tips

### Quick Reference
**See:** [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Commands & shortcuts

---

## 🏗️ Project Structure

```
minggu-8-final-project/
├── README.md                    # This file (quick overview)
├── QUICK_REFERENCE.md          # Command reference
├── WEEK-8-COMPLETE-GUIDE.md    # Comprehensive guide
│
├── dataset_export/              # For Teachable Machine training
├── dataset/                     # Backup storage
│
└── project/                     # Main application
    ├── main_app.py             # Entry point
    ├── config.py               # Configuration
    ├── core/                   # Backend modules (Week 1-6)
    ├── gui/                    # Desktop GUI (Week 7)
    └── models/                 # Trained Teachable Machine models
```

---

## ⚙️ System Requirements

**Hardware:**
- Camera: Webcam (built-in or USB)
- CPU: Dual-core 2.0GHz+
- RAM: 4GB minimum, 8GB recommended

**Software:**
- OS: Windows 10/11, macOS, Linux
- Python: 3.8, 3.9, 3.10, or 3.11

---

## 🎓 Teachable Machine Integration

Week 8 menggunakan **Google Teachable Machine** untuk custom face recognition:

**Current Model Classes:**
- Danis
- Bella

**To Add New People:**
1. Register di aplikasi → Photos saved to `dataset_export/`
2. Train di [Teachable Machine](https://teachablemachine.withgoogle.com/train/image)
3. Import model kembali ke aplikasi

**See:** [WEEK-8-COMPLETE-GUIDE.md](WEEK-8-COMPLETE-GUIDE.md#model-training-guide) untuk detailed training steps.

---

## 🔧 Configuration

Edit `project/config.py`:

```python
# Teachable Machine settings
use_teachable_machine: bool = True  # Switch to MediaPipe if False
teachable_confidence: float = 0.7   # 70% confidence minimum

# Attendance settings 
cooldown_seconds: int = 5  # Prevent duplicate entries
```

---

## ⚡ Usage

### Run Application
```bash
cd project
python main_app.py
```

### Register New Person
1. Click "Register Person"
2. Enter details
3. Capture 20 photos
4. Follow training instructions

### Mark Attendance
1. Click "Mark Attendance"
2. Face camera
3. Auto check-in ✅

### View Reports
1. Click "View Reports"
2. Filter by date
3. Export to CSV

---

## 🐛 Troubleshooting

**Common Issues:**

| Problem | Solution |
|---------|----------|
| Black screen di camera preview | Restart app, check camera permissions |
| Person not recognized | Lower confidence to 0.6, check lighting |
| Model not found | Import model via "Models" → "Import Model" |

**See:** [WEEK-8-COMPLETE-GUIDE.md](WEEK-8-COMPLETE-GUIDE.md#troubleshooting) untuk comprehensive troubleshooting guide.

---

## 🎉 Congratulations!

You've completed **Week 8 - Final Capstone Project!**

**What You've Accomplished:**
- ✅ Built production-ready face recognition system
- ✅ Integrated 8 weeks of learning
- ✅ Created deployable desktop application
- ✅ Mastered Computer Vision, ML, and GUI development

**Skills Gained:**
- Python, OpenCV, MediaPipe
- Machine Learning (Teachable Machine)
- Desktop GUI (Tkinter)
- Software Engineering & Testing
- Production Deployment

---

**📘 Full Documentation:** [WEEK-8-COMPLETE-GUIDE.md](WEEK-8-COMPLETE-GUIDE.md)  
**⚡ Quick Commands:** [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

**Time Estimate:** 8-10 hours (integration, testing, documentation)  
**Difficulty:** Advanced  
**Status:** Production-Ready ✅
