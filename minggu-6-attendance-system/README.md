# Minggu 6: Attendance System

## 🚀 Quick Setup (WAJIB BACA!)

### Setup Otomatis - Interactive Menu

**Jalankan setup script (HANYA SEKALI):**
```bash
cd minggu-6-attendance-system
python setup_week6.py
```

**Setup script akan:**
1. ✅ Create semua folder yang dibutuhkan (dataset, output, photos, reports)
2. ✅ Tampilkan menu pilihan:
   ```
   ╔═══════════════════════════════════════╗
   ║  Week 6 - Attendance System Setup    ║
   ╚═══════════════════════════════════════╝
   
   Dataset Population Options:
   [1] Copy dataset from Week 5 (recommended)
   [2] Copy dataset from Week 4
   [3] Capture new faces with camera
   [4] Skip (setup manual nanti)
   
   Pilih [1/2/3/4]:
   ```
3. ✅ **Pilih nomor 1, 2, 3, atau 4** - Script auto-copy dataset + encodings!
4. ✅ Show langkah selanjutnya untuk run program

**MUDAH!** Tinggal ketik `1` atau `2` untuk copy dataset otomatis dari week sebelumnya.

### Apa yang Di-Setup?
- `learning/lesson-1/dataset/` - Dataset untuk lesson 1 (real-time attendance)
- `learning/lesson-1/output/` - Output folder untuk attendance.csv & photos
- `learning/lesson-2/output/` - Output folder untuk reports JSON
- `project/dataset/` - Dataset untuk project testing

**PENTING:** Setelah setup, langsung bisa run `python main.py` di lesson folders!

---

## Tujuan Pembelajaran
- Build automated attendance tracking system
- Real-time attendance logging dengan hybrid recognition
- CSV/JSON file operations untuk attendance records
- Generate attendance reports & analytics
- Handle edge cases (late, early, multiple check-ins)

## Struktur Folder

```
minggu-6-attendance-system/
├── README.md
├── learning/          # Tutorial dan latihan
│   ├── README.md
│   ├── lesson-1/      # Attendance logic & real-time tracking
│   │   ├── main.py
│   │   ├── attendance_system.py
│   │   └── README.md
│   └── lesson-2/      # Reports & analytics
│       ├── main.py
│       ├── report_generator.py
│       └── README.md
└── project/           # Module untuk progressive build
    ├── attendance_system.py (NEW - Complete attendance logic)
    ├── recognition_service.py (from Week 5 - Hybrid recognition)
    ├── test_attendance.py
    └── README.md
```

## 🔧 Tech Stack: Hybrid Recognition

**Face Recognition Pipeline (from Week 5):**
- MediaPipe: Fast detection (10-15ms)
- DeepFace: Accurate recognition (97%+, 100-150ms)
- Total: Real-time capable (6-9 FPS)

**Storage (File-Based):**
- CSV files for attendance logs
- JSON files for reports
- Photo storage for verification
- Pickle for encodings (from Week 4-5)

**Week 6 Focus:**
- Attendance business logic
- Real-time check-in/check-out
- Reports & analytics

## Learning Goals

### Tutorial Materials (learning/)
1. **Lesson 1** - Attendance Logic & Real-time Tracking
   - AttendanceSystem class architecture
   - Real-time check-in dengan webcam
   - Business rules (working hours, duplicate prevention)
   - Status calculation (On Time, Late, Early Leave)

2. **Lesson 2** - Reports & Analytics
   - Daily attendance summary from CSV
   - Individual attendance history
   - Monthly statistics & trends
   - Export to JSON reports
   - CSV data processing

### Konsep Utama
- **Attendance Record:** timestamp, person_name, type, confidence, photo_path
- **CSV Storage:** logs/attendance.csv dengan semua records
- **Real-time Check-in:** Recognition → Verify threshold → Log to CSV
- **Duplicate Prevention:** One check-in per person per day (cache)
- **Photo Storage:** logs/photos/ untuk verification
- **Reporting:** CSV parsing, data aggregation, JSON export
- **Analytics:** Attendance rate, check-in/out statistics

## Project Development

### Modules:

#### `attendance_system.py` (NEW)
Complete attendance tracking system (file-based):

**Core Methods:**
- `AttendanceSystem(dataset_path, log_dir)` - Initialize with file storage
- `check_in(name, confidence, photo)` - Record check-in to CSV
- `check_out(name, confidence, photo)` - Record check-out to CSV
- `get_today_attendance()` - Today's records from cache
- `get_attendance_by_date(date)` - Load records for specific date
- `get_person_attendance_summary(name, start, end)` - Person history
- `export_report(start_date, end_date)` - Export to JSON
- `process_camera_attendance(mode)` - Real-time camera processing

**Storage:**
- CSV file: logs/attendance.csv
- Photos: logs/photos/
- Reports: logs/reports/ (JSON)
- Today's cache: in-memory for fast duplicate checking

### Integration
Uses modules from previous weeks:
- `recognition_service.py` (Week 5) - Hybrid recognition untuk identify person
- Dataset encodings (Week 4) - Pickle file dengan face encodings

**Attendance Flow:**
```
Webcam Frame → RecognitionService (Week 5) → name + confidence → 
AttendanceSystem.check_in() → Validate confidence → Save to CSV → Save photo
```

Module ini akan digunakan oleh:
- Week 7: Desktop GUI for attendance management interface

## Cara Penggunaan

### Learning (Tutorial)
```bash
cd minggu-6-attendance-system/learning

# Lesson 1: Attendance Logic
cd lesson-1
python main.py
# Real-time attendance dengan webcam + business rules

# Lesson 2: Reports & Analytics
cd ../lesson-2
python main.py
# Generate daily/monthly reports from CSV, export to JSON
```

### Project Development
```bash
cd minggu-6-attendance-system/project
python test_attendance.py

# Run attendance system
python attendance_system.py
```

## File Structure (Storage)

```
logs/
├── attendance.csv        # All attendance records
│   Columns: timestamp, date, time, person_name, type, 
│            confidence, photo_path, location, notes
├── photos/              # Verification photos
│   ├── alice_20251212_100530.jpg
│   └── bob_20251212_100645.jpg
└── reports/             # JSON reports
    ├── daily_2025-12-12.json
    └── monthly_2025_12.json

dataset/                 # From Week 4-5
├── encodings.pkl        # Face encodings
└── metadata.json        # Person info
```

## Deliverables

### Learning
- Attendance business logic implementation
- Real-time check-in system dengan webcam
- Daily & monthly reports from CSV
- JSON export functionality

### Project
- `attendance_system.py` - Complete file-based attendance logic
- `test_attendance.py` - Unit tests untuk attendance
- Sample CSV logs with attendance records
- Sample JSON reports
- Performance logs

## Next Week Preview

**Minggu 7: Desktop GUI Development**
- Tkinter GUI development
- Multi-window application
- Webcam integration
- User interface design

---

**Time Estimate:** 6-7 hours  
**Difficulty:** Advanced
---

## ⚙️ Configuration & Tuning

### 📍 Confidence Parameter Locations

#### **Learning Files**

**Lesson 1 (Real-time Attendance):**  
[learning/lesson-1/main.py](learning/lesson-1/main.py)

```python
# Line ~25-35 di function generate_encodings_from_dataset()

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.3  # ← UBAH DI SINI (encoding generation)
)
```

#### **Project Files (Shared Modules)**

**Recognition Service (Week 5):**  
[../minggu-5-recognition-system/project/recognition_service.py](../minggu-5-recognition-system/project/recognition_service.py)

```python
# Line ~67-72 di __init__()

# Initialize MediaPipe Face Detection
self.face_detection = self.mp_face_detection.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.3  # ← UBAH DI SINI (real-time detection)
)

# Line ~76-82
# Initialize MediaPipe Face Mesh
self.face_mesh = self.mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=5,
    refine_landmarks=True,
    min_detection_confidence=0.3,  # ← UBAH DI SINI (face mesh detection)
    min_tracking_confidence=0.3     # ← UBAH DI SINI (tracking)
)
```

**Face Recognizer (Week 3):**  
[../minggu-3-face-recognition/project/face_recognizer.py](../minggu-3-face-recognition/project/face_recognizer.py)

```python
# Line ~44-49 di __init__()

self.face_mesh = self.mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.3  # ← UBAH DI SINI
)
```

### 📊 Confidence Values & Effects

#### **Detection Confidence (`min_detection_confidence`)**

| Value | Effect | Use Case |
|-------|--------|----------|
| **0.1 - 0.2** | **Sangat Sensitif** | Lighting buruk, wajah miring, jarak jauh<br>⚠️ **Banyak false positives** |
| **0.3 - 0.4** | **Sensitif (✅ Recommended)** | Kondisi normal, indoor lighting<br>✅ **Balance optimal** |
| **0.5 - 0.6** | **Standard (Default)** | Good lighting, wajah frontal<br>⚠️ Bisa miss beberapa faces |
| **0.7 - 0.9** | **Ketat** | Perfect conditions only<br>⚠️ **Banyak missed detections** |

#### **Tracking Confidence (`min_tracking_confidence`)**

| Value | Effect | Use Case |
|-------|--------|----------|
| **0.1 - 0.3** | **Smooth tracking** | Fast movement, low-end webcam, shaky video |
| **0.4 - 0.6** | **✅ Balanced** | Normal movement, standard webcam |
| **0.7 - 0.9** | **Strict tracking** | Minimal movement, high-end camera |

#### **Recognition Tolerance (`tolerance` in FaceRecognizer)**

[../minggu-3-face-recognition/project/face_recognizer.py](../minggu-3-face-recognition/project/face_recognizer.py)
```python
# Line di __init__()
def __init__(self, tolerance: float = 0.6):  # ← UBAH DI SINI
    self.tolerance = tolerance
```

| Value | Effect | Use Case |
|-------|--------|----------|
| **0.3 - 0.4** | **Sangat Ketat** | Kembar identik, high security<br>⚠️ Same person bisa ditolak |
| **0.5 - 0.6** | **✅ Standard** | Normal use case, office attendance<br>✅ **Balance optimal** |
| **0.7 - 0.8** | **Toleran** | Variasi appearance, lighting changes<br>⚠️ Bisa salah recognize |
| **0.9+** | **Sangat Toleran** | Testing only<br>⚠️ **Banyak false matches** |

### 🎯 Recommended Settings by Scenario

#### **Scenario 1: Office Attendance (Indoor, Good Lighting)**
```python
# Detection
min_detection_confidence = 0.4
min_tracking_confidence = 0.4

# Recognition
tolerance = 0.6
```
**Result:** Balance antara speed & accuracy, minimal false positives

#### **Scenario 2: Outdoor/Variable Lighting**
```python
# Detection
min_detection_confidence = 0.3  # More sensitive
min_tracking_confidence = 0.3

# Recognition
tolerance = 0.65  # Slightly more tolerant
```
**Result:** Better detection di kondisi lighting bervariasi

#### **Scenario 3: High Security (Bank, Lab)**
```python
# Detection
min_detection_confidence = 0.5
min_tracking_confidence = 0.5

# Recognition
tolerance = 0.5  # Stricter matching
```
**Result:** Minimize false accepts, maximize security

#### **Scenario 4: Low-End Webcam/Laptop**
```python
# Detection
min_detection_confidence = 0.3  # Compensate for low quality
min_tracking_confidence = 0.2   # Smooth tracking

# Recognition
tolerance = 0.65  # More tolerant for poor image quality
```
**Result:** Better performance dengan hardware terbatas

### 🔧 How to Test & Tune

#### **Step 1: Test Current Settings**
```bash
cd minggu-6-attendance-system/learning/lesson-1
python main.py
```

**Observe:**
- Face detected atau tidak?
- Berapa FPS (kecepatan)?
- Recognition accuracy?

#### **Step 2: Adjust Detection Confidence**

**If: Face tidak terdeteksi (missed detections)**
```python
# Lower the confidence (more sensitive)
min_detection_confidence = 0.3  # dari 0.5
min_detection_confidence = 0.2  # jika masih missed
```

**If: Terlalu banyak false positives (bukan wajah terdeteksi)**
```python
# Raise the confidence (more strict)
min_detection_confidence = 0.5  # dari 0.3
min_detection_confidence = 0.6  # jika masih banyak FP
```

#### **Step 3: Adjust Recognition Tolerance**

**If: Salah recognize (Wrong person match)**
```python
# Lower tolerance (stricter matching)
tolerance = 0.5  # dari 0.6
tolerance = 0.4  # jika masih salah
```

**If: Orang yang sama tidak dikenali (Unknown person)**
```python
# Raise tolerance (more lenient)
tolerance = 0.7  # dari 0.6
tolerance = 0.75 # jika masih Unknown
```

#### **Step 4: Re-generate Encodings (If Changed Detection)**

Jika ubah `min_detection_confidence` di encoding generation:
```bash
cd minggu-6-attendance-system/learning/lesson-1

# Backup old encodings
Move-Item dataset/encodings.pkl dataset/encodings_old.pkl

# Generate new encodings
python -c "from main import generate_encodings_from_dataset; generate_encodings_from_dataset('dataset', 'dataset')"
```

### 📈 Performance Trade-offs

| Setting | Detection Speed | Accuracy | False Positives | Missed Detections |
|---------|----------------|----------|-----------------|-------------------|
| **Low Confidence (0.2-0.3)** | Fast ⚡ | Medium 😐 | High ⚠️ | Low ✅ |
| **Medium Confidence (0.4-0.5)** | Fast ⚡ | Good ✅ | Low ✅ | Medium 😐 |
| **High Confidence (0.6-0.8)** | Medium 😐 | High ✅ | Very Low ✅ | High ⚠️ |

### 💡 Tips & Best Practices

#### ✅ DO:
1. **Start with recommended defaults** (0.3-0.4 detection, 0.6 tolerance)
2. **Test in target environment** (actual lighting, camera, distance)
3. **Adjust gradually** (0.1 increments)
4. **Document changes** (note what settings work best)
5. **Re-generate encodings** after detection changes

#### ❌ DON'T:
1. **Set too low** (< 0.2) → Too many false positives
2. **Set too high** (> 0.7) → Miss real faces
3. **Change without testing** → Unknown behavior
4. **Forget to re-generate encodings** → Inconsistent results
5. **Use different settings** for encoding vs recognition

### 🔍 Common Issues & Solutions

#### Problem: "No face detected"
```python
# Solution 1: Lower detection confidence
min_detection_confidence = 0.2  # Very sensitive

# Solution 2: Check lighting & distance
# - Add more light
# - Move closer (50-100cm)
# - Face camera directly

# Solution 3: Check image quality
# - Increase camera resolution
# - Clean camera lens
```

#### Problem: "Wrong person detected"
```python
# Solution 1: Lower tolerance (stricter)
tolerance = 0.5  # More strict

# Solution 2: Add more training images
# - Capture 30-50 images per person
# - Different angles & expressions
# - Similar lighting conditions

# Solution 3: Re-generate encodings
# - Delete old encodings.pkl
# - Generate with better images
```

#### Problem: "Laggy/Slow detection"
```python
# Solution 1: Raise detection confidence
min_detection_confidence = 0.5  # Less processing

# Solution 2: Reduce max_num_faces
max_num_faces = 1  # Process only 1 face

# Solution 3: Lower video resolution
# - Use 640x480 instead of 1920x1080
```

### 📝 Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│ CONFIDENCE QUICK REFERENCE                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Detection (min_detection_confidence):                   │
│   • Indoor/Good Light:    0.4                          │
│   • Outdoor/Variable:     0.3                          │
│   • Low-End Camera:       0.3                          │
│   • High Security:        0.5                          │
│                                                         │
│ Tracking (min_tracking_confidence):                    │
│   • Normal Movement:      0.4                          │
│   • Fast Movement:        0.3                          │
│   • Minimal Movement:     0.5                          │
│                                                         │
│ Recognition (tolerance):                               │
│   • Standard:             0.6                          │
│   • High Security:        0.5                          │
│   • Variable Conditions:  0.65                         │
│   • Testing:              0.7                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```