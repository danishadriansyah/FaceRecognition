# Minggu 4: Dataset Collection & Management (File-Based)

## 🚀 Quick Setup

**Auto-setup dengan interactive menu:**
```bash
cd minggu-4-dataset-database
python setup_week4.py
```

Setup script akan:
- ✅ Create folder structure (dataset, rejected, backups)
- ✅ Create template person folders
- ✅ Interactive menu: **1) Capture faces** atau **2) Skip**
- ✅ Show next steps untuk generate encodings

**Tinggal pilih nomor!** Script akan handle sisanya.

---

## Tujuan Pembelajaran
- Systematic face data collection dengan quality control
- Organize dataset dengan folder structure
- Store dataset ke file system dengan metadata (JSON/pickle)
- Data quality validation & organization

## Struktur Folder

```
minggu-4-dataset-database/
├── README.md
├── learning/          # Tutorial dan latihan
│   ├── README.md
│   ├── lesson-1/      # Face capture dengan quality check
│   │   ├── main.py
│   │   ├── README.md
│   │   ├── captured_faces/
│   │   └── rejected/
│   └── lesson-2/      # Generate encodings to pickle (NEW!)
│       ├── main.py
│       ├── README.md
│       └── output/
├── project/           # Module untuk progressive build
│   ├── dataset_manager.py
│   ├── face_detector.py
│   ├── face_recognizer.py
│   ├── image_utils.py
│   ├── test_dataset.py
│   └── README.md
└── tugas/             # Assignment
    ├── dataset_manager_template.py
    └── TUGAS.md
```

## Learning Goals

### Tutorial Materials (learning/)
1. **Lesson 1** - Face capture dengan quality validation
   - Webcam face capture systematic
   - Real-time quality checks (brightness, blur, face size)
   - Auto-organize per person
   - Reject bad photos automatically

2. **Lesson 2** - Generate face encodings to pickle
   - Generate face encodings dengan DeepFace Facenet512
   - Store encodings ke pickle file (.pkl)
   - Save metadata ke JSON file
   - Auto-load captured faces dari Lesson 1
   - **Benefit:** Encodings siap untuk recognition system Week 5-7!

### Konsep Utama
- Face capture dengan validation
- Multiple angles (frontal, left, right)
- Quality metrics (blur, brightness, size)
- **File organization:** dataset/person_name/images/
- **Pickle storage:** Face encodings saved to .pkl
- **JSON metadata:** Person info, timestamps, quality scores
- **Integration ready:** Files siap untuk recognition system

## Project Development

### Module: `dataset_manager.py`
Production-ready dataset management module (file-based):
- `DatasetManager` class - Manage face datasets locally
- `add_person(name, employee_id)` - Add new person dengan metadata JSON
- `capture_faces(person_id, count)` - Capture with validation
- `generate_encodings(model_name)` - Generate & save encodings to pickle
- `load_encodings()` - Load encodings from pickle
- `get_person_list()` - List all persons in dataset
- `get_statistics()` - Dataset statistics
- `export_metadata(output_file)` - Export dataset info to JSON

### Integration
Uses Week 2 `face_detector.py` (MediaPipe) and Week 3 `face_recognizer.py` (DeepFace).  
Module ini akan digunakan oleh:
- Week 5: Recognition system (load encodings)
- Week 6: Attendance system (recognition backend)
- Week 7: Desktop GUI (person registration)

## Cara Penggunaan

### Learning (Tutorial)
```bash
cd minggu-4-dataset-database/learning

# Lesson 1: Face Capture
cd lesson-1
python main.py
# Capture 20+ photos per person dengan quality check

# Lesson 2: Generate Face Encodings
cd ../lesson-2
python main.py
# Generate encodings from captured faces, save to pickle
```

### Project Development
```bash
cd minggu-4-dataset-database/project
python test_dataset.py
```

### Tugas (Assignment)
```bash
cd minggu-4-dataset-database/tugas
copy dataset_manager_template.py dataset_manager.py
# Isi 6 blanks, lihat TUGAS.md untuk hints
python dataset_manager.py
```

## Dataset Structure

```
dataset/
├── metadata.json           # Person info, image counts
├── encodings.pkl           # All face encodings (512-d vectors)
├── alice/
│   ├── alice_001.jpg
│   ├── alice_002.jpg
│   └── ...
└── bob/
    ├── bob_001.jpg
    └── ...
```

## Deliverables

### Learning
- ✅ Lesson 1: Captured faces dengan quality check (20+ photos per person)
- ✅ Lesson 2: Face encodings generated and saved to pickle

### Tugas
- ✅ `dataset_manager_template.py` - Fill 6 blanks untuk dataset operations

### Project
- ✅ `dataset_manager.py` - Production-ready file-based dataset management
- ✅ `test_dataset.py` - Unit tests for file operations
- ✅ Sample dataset: 3+ people, 20+ photos each
- ✅ Encodings: face_encodings.pkl with 512-d vectors

## Next Week Preview

**Minggu 5: Face Recognition System**
- Load encodings from pickle file
- Real-time recognition dengan MediaPipe + DeepFace
- Recognition service integration
- Build recognition service (97%+ accuracy)
- Real-time recognition pipeline

---

**Time Estimate:** 5-6 hours  
**Difficulty:** Intermediate
