# Face Recognition Attendance System
### Week 8 - Final Capstone Project

🎉 **Complete Production-Ready System** - Integration dari Week 1-7

---

## ✨ Highlights

- ✅ **Desktop GUI Application** dengan Tkinter
- ✅ **Real-Time Face Recognition** dengan MediaPipe + DeepFace
- ✅ **Automated Attendance** - Check-in/Check-out otomatis
- ✅ **Person Management** - Register, update, delete persons
- ✅ **Reports & Analytics** - Filter, search, export to CSV
- ✅ **File-Based Storage** - No database required (pickle + JSON + CSV)
- ✅ **Production-Ready** - Error handling, logging, backups

---

## 🚀 Quick Start

```bash
# Install dependencies (from root workspace)
cd c:\Ngoding\Kerja\ExtraQueensya
pip install -r requirements.txt

# Run application
cd minggu-8-final-project\project
python main_app.py
```

---

## 📂 Project Structure

```
project/
├── main_app.py              # Entry point
├── config.py                # Configuration
├── requirements.txt         # Dependencies
│
├── core/                    # Week 1-6 modules
│   ├── image_utils.py      # Image processing
│   ├── face_detector.py    # Face detection
│   ├── face_recognizer.py  # Face recognition
│   ├── dataset_manager.py  # Dataset management
│   ├── recognition_service.py  # Recognition pipeline
│   └── attendance_system.py    # Attendance logging
│
├── gui/                     # Week 7 GUI
│   ├── main_window.py      # Dashboard
│   ├── register_window.py  # Registration
│   ├── attendance_window.py # Attendance
│   └── reports_window.py   # Reports
│
├── dataset/                 # Data storage
├── logs/                    # System logs
├── backups/                 # Auto backups
├── tests/                   # Test suite
└── docs/                    # Documentation
```

---

## 🎯 Features

### 1. Dashboard
- Live webcam preview dengan face detection
- System statistics (persons, attendance, status)
- Quick navigation

### 2. Person Registration
- Form input (name, ID, department)
- Auto-capture 20 photos
- Quality validation
- Instant encoding generation

### 3. Attendance Marking
- Real-time face recognition
- Auto check-in/check-out
- Cooldown timer (5s)
- Manual fallback
- Visual feedback

### 4. Reports
- Date range filters
- Search by name/ID
- Export to CSV
- Sortable columns

---

## 📊 Performance

| Operation | Time | FPS |
|-----------|------|-----|
| Face Detection | 10-15ms | 60-100 |
| Face Recognition | 100-150ms | 6-10 |
| Complete Pipeline | 110-165ms | 6-9 |

**Tested:** Intel i5, 8GB RAM

---

## 🧪 Testing

```bash
cd tests
python test_integration.py    # Integration tests
python test_performance.py    # Performance benchmarks
python test_gui.py            # GUI tests
```

---

## 📚 Documentation

- **[User Guide](docs/USER_GUIDE.md)** - Complete usage instructions
- **[Project README](project/README.md)** - Technical details
- **[Main README](README.md)** - Project overview

---

## 💻 System Requirements

**Hardware:**
- Camera: Webcam (built-in or USB)
- CPU: Dual-core 2.0GHz+
- RAM: 4GB minimum, 8GB recommended

**Software:**
- Python 3.8-3.11
- Windows 10/11, macOS, or Linux

---

## 🎓 Learning Outcomes

This project integrates **8 weeks of learning**:

1. ✅ **Week 1:** Python & Image Processing
2. ✅ **Week 2:** Face Detection (MediaPipe)
3. ✅ **Week 3:** Face Recognition (DeepFace)
4. ✅ **Week 4:** Dataset Management
5. ✅ **Week 5:** Recognition Service
6. ✅ **Week 6:** Attendance System
7. ✅ **Week 7:** Desktop GUI (Tkinter)
8. ✅ **Week 8:** Final Integration ← **You are here!**

**Skills Mastered:**
- Computer Vision
- Machine Learning
- GUI Development
- Software Engineering
- Production Deployment

---

## 🔧 Troubleshooting

**Camera not working?**
- Check permissions
- Try different camera index
- Restart application

**Recognition failing?**
- Check lighting
- Adjust threshold in config
- Re-register with better photos

**Performance issues?**
- Increase frame skip
- Reduce resolution
- Close other apps

**See [User Guide](docs/USER_GUIDE.md) for detailed troubleshooting.**

---

## 🎉 Congratulations!

You've completed the entire Face Recognition Attendance System course!

**Next Steps:**
- ✅ Add to portfolio/GitHub
- ✅ Create demo video
- ✅ Customize for your needs
- ✅ Deploy to production

---

## 📝 License

Educational project - Free to use and modify

---

**Week 8 - Final Project ✅**  
**Status: Production-Ready**  
**Time Investment: 40-50 hours (Week 1-8)**
