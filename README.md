# AI-Based Face Recognition Attendance System
## Progressive Learning - 7 Minggu Pembelajaran Terstruktur

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8.1-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-red.svg)

Sistem absensi berbasis face recognition yang dikembangkan secara progressive dalam 7 minggu pembelajaran terstruktur. Menggunakan **MediaPipe Face Detection + Face Mesh** untuk performa real-time yang cepat dan akurat.

---

## 🎯 Fitur Utama

- ✅ **MediaPipe Face Recognition:** Detection + Face Mesh (1404-dim landmarks)
- ✅ **Super Fast:** 60+ FPS real-time (0.01s per face)
- ✅ **High Accuracy:** Cosine similarity matching
- ✅ **Lightweight:** ~150MB install (no TensorFlow!)
- ✅ **File-Based Storage:** Pickle + JSON + CSV (no database needed!)
- ✅ Real-time attendance tracking via webcam
- ✅ Desktop GUI dengan Tkinter
- ✅ Export reports ke CSV/JSON
- ✅ Support 100-200+ persons
- ✅ Berjalan offline - no internet needed

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.11+**
```bash
python --version  # Harus 3.11 atau lebih
```
Download: https://python.org/downloads/ (Centang "Add to PATH"!)

2. **Webcam** - Built-in atau USB camera

### Installation

```bash
# 1. Clone/Download project
git clone <repo-url>
cd ExtraQueensya

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify
python -c "import cv2, mediapipe; print('✅ Ready!')"
```

**Setup per-week dengan Interactive Menu:**
```bash
# Week 4-7: Auto-setup dataset
cd minggu-X-xxxxx
python setup_weekX.py
# Interactive menu akan muncul dengan pilihan:
#   [1] Copy dataset dari week sebelumnya (otomatis!)
#   [2] Capture faces dengan camera
#   [3] Skip (populate manual nanti)
# Tinggal ketik nomor, no manual commands needed!
```

**Setup All Weeks (4-7) Sekaligus:**
```bash
python setup_all_weeks.py
# Create folder structure untuk semua week
# Kemudian run setup_weekX.py untuk interactive dataset population
```

---

## 📚 Learning Path (7 Minggu)

```
minggu-1-python-basics/       ← START: OpenCV basics
├── learning/                 ← Tutorial & teori
├── project/                  ← Implementation & tests
└── README.md

minggu-2-face-detection/      ← Face detection (MediaPipe)
minggu-3-face-recognition/    ← Face recognition (MediaPipe Face Mesh)
minggu-4-dataset-database/    ← Dataset management
minggu-5-recognition-system/  ← Recognition service integration
minggu-6-attendance-system/   ← Attendance logic & reports
minggu-7-desktop-gui/         ← Desktop application
```

### Cara Belajar

**Setiap minggu:**
1. Baca `learning/README.md` → Pahami konsep
2. Jalankan tutorial files di `learning/` → Praktik
3. Baca `project/README.md` → Understand implementation
4. Run tests di `project/` → Validasi

**Timeline:** 2-3 jam/hari × 7 minggu = Complete attendance system

---

## 🏗️ Tech Stack

**Core:**
- **Python 3.11** - Programming language
- **OpenCV 4.8.1** - Image processing & video capture
- **MediaPipe 0.10.9** - Face Detection + Face Mesh
  - Face Detection: `min_detection_confidence=0.3` (configurable)
  - Face Mesh: 468 landmarks × 3 coordinates = 1404-dim encoding
- **NumPy 1.26.2** - Cosine similarity matching

**Storage & Export:**
- Pickle (face encodings - 1404-dim vectors)
- JSON (metadata)
- CSV (attendance logs)
- Tkinter (GUI)

**Why MediaPipe?**
- ✅ Super fast: 60+ FPS real-time (25x faster than DeepFace)
- ✅ Lightweight: ~150MB install vs ~500MB with TensorFlow
- ✅ No heavy dependencies
- ✅ Easy setup: 2-3 min install
- ✅ Google-maintained, production-ready

---

## 📖 Week-by-Week Roadmap

| Week | Topic | Files | Output | Time |
|------|-------|-------|--------|------|
| 1 | Python & OpenCV | 5 tutorials | `image_utils.py` | 6-7 hari |
| 2 | Face Detection | 4 tutorials | `face_detector.py` | 6-7 hari |
| 3 | Face Recognition | 3 tutorials | `face_recognizer.py` (MediaPipe) | 7-8 hari |
| 4 | Dataset Management | 3 tutorials | `dataset_manager.py` | 6-7 hari |
| 5 | System Integration | 2 tutorials | `recognition_service.py` | 6-7 hari |
| 6 | Attendance System | 2 lessons | `attendance_system.py` | 6-7 hari |
| 7 | Desktop GUI | 2 lessons | `main_app.py` | 5-6 hari |

**Total:** ~50 hari pembelajaran terstruktur

---

## 🎮 Running the Application

### Week 1-3: Learning Mode
```bash
cd minggu-X-xxxxx/learning
python lesson-X/main.py
```

### Week 4+: Project Mode
```bash
# Setup dataset first
cd minggu-X-xxxxx
python setup_weekX.py

# Run learning
cd learning/lesson-1
python main.py
```

### Week 7: Desktop App
```bash
cd minggu-7-desktop-gui/project
python main_app.py
```

---

## ❓ FAQ

**Q: Harus mulai dari Week 1?**  
A: Pemula → Ya. Intermediate → Skip ke Week 3. Advanced → Week 5.

**Q: Berapa lama per minggu?**  
A: Flexible! 2-3 jam/hari santai, atau 1-2 hari intensif.

**Q: Kenapa pakai MediaPipe?**  
A: Super fast (60+ FPS), lightweight (~150MB), no heavy dependencies, Google-maintained.

**Q: Bisa offline?**  
A: Ya! Semua berjalan lokal, no cloud/internet needed.

**Q: Face detection tidak akurat?**  
A: Check lighting, distance (50-100cm), frontal face. Atau tuning confidence di Week 6 README.

**Q: Cara tuning sensitivity/confidence?**  
A: Lihat section "⚙️ Configuration & Tuning" di `minggu-6-attendance-system/README.md`.

---

## 📂 Progressive Modules Architecture

Setiap minggu **standalone** dengan copy modules dari minggu sebelumnya:
- Week 1: `image_utils.py`
- Week 2: Week 1 + `face_detector.py`
- Week 3: Week 2 + `face_recognizer.py` (MediaPipe Face Mesh)
- Week 4: Week 3 + `dataset_manager.py`
- Week 5: Week 4 + `recognition_service.py`
- Week 6: Week 5 + `attendance_system.py`
- Week 7: Week 6 + GUI (`main_app.py`)

**Why Duplicate?** Student bisa langsung run tanpa import issues atau dependency ke folder lain. Setiap week bisa dibuka sebagai standalone project.

---

## 🎯 Expected Results

Setelah 7 minggu, kamu akan punya:
- ✅ Working attendance system dengan face recognition
- ✅ Desktop application dengan GUI
- ✅ Super fast real-time recognition (60+ FPS)
- ✅ Report export (CSV/JSON)
- ✅ Portfolio-ready project
- ✅ Understanding of confidence tuning & optimization
- ✅ Skills: Python, OpenCV, MediaPipe, AI, Computer Vision, GUI

---

## 📞 Resources

### Documentation
- **Main README** (ini) - Overview & quick start
- **Weekly READMEs** - 14 detailed READMEs (learning + project per minggu)
- **KUNCI_JAWABAN_TUGAS.md** - Answer keys untuk tugas (after trying!)
- **Setup Scripts** - `setup_week4.py` sampai `setup_week7.py` dengan interactive menus
- **Configuration Guide** - Week 6 README section "⚙️ Configuration & Tuning"

### External
- OpenCV Docs: https://docs.opencv.org/
- MediaPipe Docs: https://google.github.io/mediapipe/
- MediaPipe Face Detection: https://google.github.io/mediapipe/solutions/face_detection
- MediaPipe Face Mesh: https://google.github.io/mediapipe/solutions/face_mesh

### Need Help?
1. Baca README di week yang sedang dikerjakan
2. Run `python setup_weekX.py` untuk interactive setup
3. Check Week 6 README untuk confidence tuning
4. Google error message
5. Review tutorial files di `learning/`

---

## 💪 Tips untuk Sukses

1. **Consistency > Intensity** - 2 jam/hari lebih baik dari 14 jam/weekend
2. **Understand > Memorize** - Pahami konsep, jangan hafal code
3. **Test Everything** - Run test setelah setiap perubahan
4. **Take Notes** - Catat konsep penting & insights
5. **Build Portfolio** - Screenshot, demo video, write blog
6. **Ask for Help** - Stuck > 1 jam? Take break atau cari bantuan

---

## 🚀 Ready to Start?

### Complete Beginner:
```bash
cd minggu-1-python-basics/learning
python lesson-1/main.py
```

### Intermediate:
```bash
cd minggu-3-face-recognition/learning
python lesson-1/main.py
```

### Want Quick Demo:
```bash
# Setup Week 6 first
cd minggu-6-attendance-system
python setup_week6.py  # Pilih [1] Copy dari Week 5

# Run attendance demo
cd learning/lesson-1
python main.py
```

---

**Happy Learning! 🎉**

*Remember: Everyone starts from zero. Keep learning, don't give up!*

---

**Last Updated:** December 13, 2025  
**Version:** 3.0  
**License:** Educational purposes
