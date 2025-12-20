# Minggu 7: Desktop GUI Development

## 🚀 Quick Setup

**Auto-setup dengan interactive menu:**
```bash
cd minggu-7-desktop-gui
python setup_week7.py
```

Setup script akan:
- ✅ Create folder structure (dataset, logs, reports, snapshots)
- ✅ Interactive menu: **1) Week 6** / **2) Week 5** / **3) Week 4** / **4) Capture** / **5) Skip**
- ✅ Auto-copy dataset + encodings dari week lain
- ✅ Show next steps untuk launch GUI

**Tinggal pilih nomor!** Script akan auto-copy dari week manapun.

---

## Tujuan Pembelajaran
- Build **pure desktop application** dengan Tkinter (NO WEB/FLASK!)
- GUI design principles & event-driven programming
- Multi-window application (Main, Register, Attendance, Reports)
- Real-time webcam preview di GUI
- Integrate semua modules dari Week 1-6

## Struktur Folder

```
minggu-7-desktop-gui/
├── README.md
├── setup_week7.py
├── learning/          # Tutorial dan latihan
│   ├── README.md
│   ├── lesson-1/      # Tkinter basics
│   ├── lesson-2/      # Complete GUI integration
│   └── lesson-3/      # Testing & deployment
└── project/           # Production-ready desktop app
    ├── gui/           # ✨ GUI modules (NEW!)
    │   ├── __init__.py
    │   ├── main_window.py         # Main dashboard
    │   ├── register_window.py     # Register persons
    │   ├── attendance_window.py   # Mark attendance
    │   └── reports_window.py      # View/export reports
    ├── main_app.py               # ✨ Main entry point
    ├── test_gui.py               # ✨ GUI testing
    ├── attendance_system.py      # Backend (from Week 6)
    ├── recognition_service.py    # Recognition (from Week 5)
    ├── dataset_manager.py        # Dataset ops (from Week 4)
    ├── face_detector.py          # Detection (from Week 2)
    ├── face_recognizer.py        # Recognition (from Week 3)
    ├── image_utils.py            # Utils (from Week 1)
    ├── dataset/                  # Face dataset
    ├── logs/                     # Attendance logs
    ├── reports/                  # Generated reports
    └── snapshots/                # Captured photos
```

## 🔧 Tech Stack: Pure Desktop Application

**GUI Framework:**
- ✅ Tkinter (built-in Python) - NO Flask/Web!
- ✅ PIL/Pillow for image display
- ✅ Threading for non-blocking UI
- ✅ Multi-window management

**Face Recognition (Hybrid):**
- MediaPipe: Fast face detection (10-15ms)
- DeepFace: Accurate recognition (97%+, Facenet512)
- Real-time pipeline: 6-9 FPS

**Backend (File-Based):**
- CSV: Attendance logging
- JSON: Reports & metadata
- Pickle: Face encodings
- No database required!

## Learning Goals

### Tutorial Materials (learning/)

**Lesson 1: Tkinter Basics**
- Build basic GUI window dengan menu bar
- Add buttons, labels, frames
- Event handling (clicks, actions)
- Layout management (pack, grid)

**Lesson 2: Complete GUI Integration**
- Integrate all backend modules (Week 1-6)
- Add webcam preview ke GUI
- Real-time face recognition display
- Complete attendance system GUI

**Lesson 3: Testing & Deployment**
- Test all GUI components
- Debug & performance testing
- Camera detection & selection
- Package as executable (optional)

### Key Concepts
- Tkinter widgets (Button, Label, Entry, Frame, Canvas)
- Layout managers (pack, grid, place)
- Event-driven programming
- Threading untuk webcam (non-blocking)
- PIL/Pillow untuk image display
- Dialog boxes (messagebox, filedialog)
- Multi-window management

## Project Structure (Desktop App)

### GUI Windows:

#### 🏠 Main Window (`gui/main_window.py`)
- **Left:** Live webcam dengan face detection boxes
- **Right:** Dashboard stats, action buttons
- **Features:** Real-time preview, statistics, navigation
- **Menu:** File, View, Help

#### 📝 Register Window (`gui/register_window.py`)
- **Form:** Name, ID, Department, Email
- **Webcam:** Preview untuk capture 20 photos
- **Progress:** Photo count & progress bar
- **Auto-capture:** Automatic photo capture dengan face detection

#### 📸 Attendance Window (`gui/attendance_window.py`)
- **Webcam:** Real-time recognition & marking
- **Auto-mark:** Automatic check-in/out saat face recognized
- **Manual:** Fallback manual entry
- **Records:** Today's attendance list

#### 📊 Reports Window (`gui/reports_window.py`)
- **Filter:** By date range (today/week/month/all)
- **Search:** Find by name
- **Table:** Scrollable attendance records
- **Export:** CSV export & text reports

### Backend Integration
Menggunakan SEMUA modules dari Week 1-6:
- **Week 1:** `image_utils.py` - Image processing
- **Week 2:** `face_detector.py` - MediaPipe detection
- **Week 3:** `face_recognizer.py` - DeepFace recognition
- **Week 4:** `dataset_manager.py` - Dataset management
- **Week 5:** `recognition_service.py` - Hybrid pipeline
- **Week 6:** `attendance_system.py` - Attendance logic

**GUI Pipeline:**
```
Tkinter GUI → OpenCV Webcam → MediaPipe Detection → 
DeepFace Recognition → AttendanceSystem → CSV Log → 
UI Update → Report Generation
```

## Cara Penggunaan

### 1. Setup (WAJIB!)
```bash
cd minggu-7-desktop-gui
python setup_week7.py

# Pilih option 1-5 untuk dataset
```

### 2. Learning (Tutorial)
```bash
cd learning

# Lesson 1 - Tkinter basics
cd lesson-1
python main.py

# Lesson 2 - Complete integration
cd ../lesson-2
python main.py

# Lesson 3 - Testing
cd ../lesson-3
python main.py
```

### 3. Run Desktop Application
```bash
cd project

# Test dulu (OPTIONAL tapi recommended)
python test_gui.py

# Launch aplikasi desktop
python main_app.py
```

**Aplikasi akan:**
1. ✅ Check requirements (OpenCV, Pillow, MediaPipe, dataset)
2. ✅ Load face encodings
3. ✅ Start webcam preview
4. ✅ Show main dashboard
5. ✅ Ready untuk register/attendance/reports!

### 4. Menggunakan Aplikasi

**Register Person:**
1. Click "📝 Register Person"
2. Isi form (Name wajib, yang lain optional)
3. Click "Start Capture" 
4. Tunggu 20 photos auto-captured
5. Click "Save Person"
6. Done! Encodings auto-generated

**Mark Attendance:**
1. Click "📸 Mark Attendance"
2. Pilih Check In / Check Out
3. Face ke camera - auto recognize & mark!
4. Atau manual entry jika recognition gagal

**View Reports:**
1. Click "📊 View Reports"
2. Filter by date (today/week/month/all)
3. Search by name
4. Export to CSV atau generate text report

---

## ⚙️ Requirements

### Python Packages
```txt
opencv-python>=4.8.0
mediapipe>=0.10.0
deepface>=0.0.79
pillow>=10.0.0
numpy>=1.24.0
```

Install semua:
```bash
pip install -r requirements.txt
```

### Hardware
- 💻 Webcam (built-in atau external)
- 🧠 RAM minimum 4GB (recommended 8GB)
- ⚡ CPU: Multi-core recommended

---

## 🎯 Features

✅ **Complete Desktop GUI** - Pure Tkinter, no web required!
✅ **Real-time Recognition** - MediaPipe + DeepFace hybrid
✅ **Auto Attendance** - Face detection auto mark
✅ **Multi-window** - Main, Register, Attendance, Reports
✅ **CSV Logging** - Simple file-based storage
✅ **Report Generation** - Export CSV & text reports
✅ **Manual Fallback** - Manual entry jika recognition gagal
✅ **Live Stats** - Real-time dashboard statistics
✅ **Thread-safe** - Non-blocking UI dengan threading

---

## 📚 What You'll Learn

1. **Tkinter Mastery:** Build production-ready desktop apps
2. **Multi-threading:** Non-blocking webcam in GUI
3. **Event-driven:** Handle user interactions
4. **Integration:** Combine 6 weeks of modules into one app
5. **File I/O:** CSV, JSON, Pickle operations
6. **Image Display:** PIL/Pillow dalam Tkinter
7. **Error Handling:** User-friendly error messages
8. **Testing:** Component & integration testing

---

## 🐛 Troubleshooting

**Webcam tidak muncul:**
```bash
# Test webcam
python -c "import cv2; cap=cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'FAIL')"
```

**Import errors:**
```bash
pip install --upgrade opencv-python pillow mediapipe deepface
```

**Dataset kosong:**
```bash
# Re-run setup
python setup_week7.py
# Pilih option 1 atau 2
```

**Performance lambat:**
- Close aplikasi lain yang pakai webcam
- Lower FPS di code (default 30 FPS)
- Pastikan lighting cukup

---

## 🎉 Next Steps

Setelah Week 7, kamu akan:
1. ✅ Punya production-ready desktop application
2. ✅ Menguasai Tkinter GUI development
3. ✅ Integrate 7 weeks of learning
4. ✅ Siap build custom attendance systems!

**Final Project:** Build your own complete attendance system from scratch!
