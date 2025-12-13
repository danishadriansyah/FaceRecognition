# Minggu 6 - Learning: Attendance System (File-Based)

## 📚 Overview
Folder ini berisi 2 tutorial lessons untuk build attendance system dengan file-based storage (CSV, JSON, Pickle).

## 🚀 Quick Start

**1. Setup dulu (WAJIB!):**
```bash
cd minggu-6-attendance-system
python setup_week6.py
# Pilih [1] Copy dari Week 5 (termudah!)
```

**2. Run lessons:**
```bash
cd learning/lesson-1
python main.py  # Real-time attendance

cd ../lesson-2
python main.py  # Reports & analytics
```

## 📁 Structure

```
learning/
├── README.md (file ini)
├── lesson-1/           # Real-time attendance tracking
│   ├── main.py
│   ├── dataset/        # Face encodings (auto-copied by setup)
│   └── output/         # attendance.csv + photos
└── lesson-2/           # Reports & analytics
    ├── main.py
    └── output/reports/ # JSON exports
```

---

## 📖 Lessons

### Lesson 1: Real-time Attendance
**File:** `lesson-1/main.py`

**Belajar:**
- Load encodings dari file (pickle)
- Real-time face recognition dari webcam
- Auto check-in dengan confidence threshold
- Save ke CSV + capture photos
- Duplicate prevention

**Run:**
```bash
cd lesson-1
python main.py
```

**Output:**
- `output/attendance.csv` - Log semua check-ins
- `output/photos/` - Verification photos

---

### Lesson 2: Reports & Analytics
**File:** `lesson-2/main.py`

**Belajar:**
- Parse CSV dengan pandas
- Generate daily/monthly reports
- Calculate attendance statistics
- Export ke JSON
- Data aggregation

**Run:**
```bash
cd lesson-2
python main.py
```

**Output:**
- `output/reports/daily_YYYY-MM-DD.json`
- `output/reports/monthly_YYYY_MM.json`

---

## 🎯 Learning Path

1. **Week 4:** Dataset management (encodings.pkl)
2. **Week 5:** Recognition service (hybrid detection)
3. **Week 6 Lesson 1:** ⬅️ YOU ARE HERE - Attendance logging
4. **Week 6 Lesson 2:** Reports & analytics
5. **Week 7:** Desktop GUI

---

## ⚙️ Tech Stack

**Storage (File-Based):**
- Pickle (.pkl) - Face encodings
- CSV - Attendance logs
- JSON - Reports
- Photos - Verification images

**Recognition:**
- MediaPipe - Fast detection
- DeepFace - Accurate recognition

**No Database!** Semua file-based, mudah di-backup dan portable
