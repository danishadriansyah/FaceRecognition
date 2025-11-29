# Minggu 4: Dataset Collection & Database Setup

## Tujuan Pembelajaran
- Systematic face data collection dengan quality control
- Setup MySQL database untuk face recognition
- Store dataset ke database dengan metadata
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
│   └── lesson-2/      # Database setup + Store dataset to DB (NEW!)
│       ├── main.py
│       ├── README.md
│       ├── database.py
│       ├── models.py
│       └── dataset/
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

2. **Lesson 2** - Database setup & store dataset (NEW COMBINED!)
   - Setup MySQL database
   - Create database models (Person, FaceImage, FaceEncoding)
   - Store captured faces to database
   - Generate metadata & basic CRUD
   - **Benefit:** Dataset langsung tersimpan di database untuk week 5-7!

### Konsep Utama
- Face capture dengan validation
- Multiple angles (frontal, left, right)
- Quality metrics (blur, brightness, size)
- **Database design:** Person, FaceImage, FaceEncoding tables
- **SQLAlchemy ORM:** Object-relational mapping
- **Data persistence:** Store images & metadata to MySQL
- **Integration ready:** Database siap untuk recognition system

## Project Development

### Module: `dataset_manager.py`
Production-ready dataset management module dengan fungsi:
- `DatasetManager` class - Manage face datasets
- `capture_face()` - Capture with validation
- `add_person()` - Add new person to dataset
- `remove_person()` - Remove person from dataset
- `get_person_images()` - Get all images for person
- `validate_dataset()` - Check dataset quality
- `export_encodings()` - Generate encodings for dataset

### Integration
Uses Week 2 `face_detector.py` and Week 3 `face_recognizer.py`.  
Module ini akan digunakan oleh:
- Week 5: Recognition system training
- Week 6: Attendance database seeding
- Week 7-8: Desktop GUI for person registration

## Cara Penggunaan

### Learning (Tutorial)
```bash
cd minggu-4-dataset-database/learning

# Lesson 1: Face Capture
cd lesson-1
python main.py
# Capture 20+ photos per person dengan quality check

# Lesson 2: Database Setup & Store Dataset
cd ../lesson-2
python main.py
# Setup database, store captured faces, generate metadata
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
├── person_1/
│   ├── frontal_1.jpg
│   ├── frontal_2.jpg
│   ├── left_angle.jpg
│   ├── right_angle.jpg
│   └── encodings.pkl
├── person_2/
│   └── ...
└── metadata.json
```

## Deliverables

### Learning
- ✅ Lesson 1: Captured faces dengan quality check (20+ photos per person)
- ✅ Lesson 2: MySQL database setup + faces stored to database

### Tugas
- ✅ `dataset_manager_template.py` - Fill 6 blanks untuk dataset + database operations

### Project
- ✅ `dataset_manager.py` - Production-ready dataset + database management
- ✅ `database.py` - Database connection & session management
- ✅ `models.py` - SQLAlchemy models (Person, FaceImage, FaceEncoding)
- ✅ `test_dataset.py` - Unit tests
- ✅ Sample dataset: 3+ people, 20+ photos each, stored in MySQL

## Next Week Preview

**Minggu 5: Face Recognition with Hybrid Approach**
- Introduction to Hybrid (MediaPipe + DeepFace)
- Generate face encodings dengan Facenet512
- Build recognition service (97%+ accuracy)
- Real-time recognition pipeline

---

**Time Estimate:** 5-6 hours  
**Difficulty:** Intermediate
