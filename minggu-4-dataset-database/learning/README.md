# Minggu 4 - Learning: Dataset Collection & Face Encoding

## 📚 Overview
Folder ini berisi 2 lessons: (1) face capture dengan quality control, (2) generate face encodings dari dataset dan save ke pickle file. **Minggu 4 ini fokus pada data collection dan encoding generation** untuk recognition system di minggu 5-7.

## 📁 File Structure

```
learning/
├── README.md (file ini)
├── lesson-1/          # Face capture dengan quality check
│   ├── main.py
│   ├── README.md
│   └── dataset/        # Captured faces per person
└── lesson-2/          # Generate face encodings
    ├── main.py
    ├── README.md
    └── output/        # encodings.pkl + metadata.json
```

---

## 🎯 Lessons - Detailed Guide

### Lesson 1: Face Capture dengan Quality Check
**File:** `lesson-1/main.py`

**Tujuan:** Systematic face capture dari webcam dengan automatic quality validation

**Apa yang dipelajari:**
- Capture multiple photos per person dari webcam
- Real-time quality checks (brightness, blur, face size)
- Auto-reject bad quality photos
- Organize captured faces per person
- Progress tracking

**💡 RECOMMENDED:** Use setup script instead!
```bash
cd minggu-4-dataset-database
python setup_week4.py
# Pilih opsi [1] Capture faces
```

**Atau jalankan lesson langsung:**
```bash
cd minggu-4-dataset-database/learning/lesson-1
python main.py
```

**Workflow:**
1. Input nama person (Alice, Bob, etc)
2. Webcam akan terbuka
3. Press **SPACE** untuk capture photo
4. Target: 20+ photos per person
5. Gerakkan wajah (frontal, kiri, kanan) untuk variasi
6. Photos tersimpan di `dataset/person_name/`

**Quality Checks:**
- ✅ Minimum face size: 100x100 pixels
- ✅ Brightness range: 40-220 (tidak terlalu gelap/terang)
- ✅ Sharpness (Laplacian): >100 (tidak blur)
- ✅ Single face only (reject jika ada multiple faces)

**Output yang diharapkan:**
```
dataset/
├── alice/
│   ├── alice_001.jpg  ✅ Good
│   ├── alice_002.jpg  ✅ Good
│   └── ...
└── bob/
    └── bob_001.jpg
    └── ...
```

**Tips untuk capture bagus:**
- 💡 Lighting bagus (cahaya dari depan)
- 💡 Vary angles: frontal, left, right
- 💡 Vary expressions: neutral, smile
- 💡 Keep face centered di frame
- 💡 Target minimal 20 photos per person

---

### Lesson 2: Generate Face Encodings
**File:** `lesson-2/main.py`

**Tujuan:** Convert captured faces menjadi 512-dimensional face embeddings using DeepFace

**Apa yang dipelajari:**
1. **Face Encoding**
   - Load images dari dataset
   - Generate embeddings menggunakan DeepFace (Facenet512)
   - Save ke pickle file format
   - Create metadata file (JSON)

2. **File-Based Storage**
   - Understand pickle format untuk encoding
   - JSON metadata untuk person info
   - Efficient encoding storage

3. **Encoding Verification**
   - Check berapa banyak encodings
   - Verify file integrity
   - Load dan inspect encodings

2. **Store Dataset to Database**
   - Load captured faces dari Lesson 1
   - Create Person records dengan metadata
   - Store face images as BLOB atau file path
   - Organize data dengan relational structure

3. **Database Operations**
   - Basic CRUD (Create, Read, Update, Delete)
   - Query persons by name/ID
   - Count faces per person
   - Data validation

**Cara menggunakan:**
```bash
# Setup database dulu (one-time)
# 1. Install MySQL Server
# 2. Create database: face_recognition_db

cd minggu-4-dataset-database/learning/lesson-2
python main.py
```

**Workflow:**
1. Connect to MySQL database
2. Create tables dari models (Person, FaceImage)
3. Scan `captured_faces/` dari Lesson 1
4. Untuk setiap person:
   - Create Person record (name, employee_id, department)
   - Store each face image to FaceImage table
   - Generate metadata & timestamps
5. Display database statistics

**Database Schema:**
```sql
-- Person Table
CREATE TABLE persons (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id VARCHAR(50) UNIQUE,
    name VARCHAR(100),
    department VARCHAR(100),
    email VARCHAR(100),
    created_at DATETIME,
    updated_at DATETIME
);

-- FaceImage Table
CREATE TABLE face_images (
    id INT PRIMARY KEY AUTO_INCREMENT,
    person_id INT,
    image_path VARCHAR(255),
    image_data BLOB,  -- Optional: store image binary
    quality_score FLOAT,
    capture_date DATETIME,
    FOREIGN KEY (person_id) REFERENCES persons(id)
);

-- FaceEncoding Table (akan diisi di Minggu 5)
CREATE TABLE face_encodings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    person_id INT,
    encoding BLOB,  -- 512-d vector from DeepFace
    model VARCHAR(50),  -- 'Facenet512'
    created_at DATETIME,
    FOREIGN KEY (person_id) REFERENCES persons(id)
);
```

**SQLAlchemy Models:**
```python
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Person(Base):
    __tablename__ = 'persons'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(String(50), unique=True)
    name = Column(String(100))
    department = Column(String(100))
    email = Column(String(100))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # Relationships
    face_images = relationship("FaceImage", back_populates="person")
    face_encodings = relationship("FaceEncoding", back_populates="person")

class FaceImage(Base):
    __tablename__ = 'face_images'
    
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'))
    image_path = Column(String(255))
    quality_score = Column(Float)
    capture_date = Column(DateTime)
    
    person = relationship("Person", back_populates="face_images")
```

**Output:**
```
✅ Database connected: mysql://localhost/face_recognition_db
✅ Tables created: persons, face_images, face_encodings

Processing person: alice
  ├─ Created Person ID: 1
  ├─ Stored 24 face images
  └─ Average quality: 0.92

Processing person: bob
  ├─ Created Person ID: 2
  ├─ Stored 22 face images
  └─ Average quality: 0.88

=== Database Statistics ===
Total Persons: 2
Total Face Images: 46
Database Size: 15.2 MB
Ready for recognition system! ✅
```

**Why This Matters:**
- ✅ Data persistence: Dataset tersimpan permanen
- ✅ Scalability: Easy untuk manage ratusan persons
- ✅ Integration: Database siap untuk minggu 5-7
- ✅ Production-ready: Struktur data yang proper
- ✅ Query capability: Search, filter, analytics

---

## 🎓 Best Practices

### Data Collection (Lesson 1)
- **Quantity:** 20-30 photos per person minimum
- **Variety:** Different angles (frontal ±30°, slight up/down)
- **Quality:** Well-lit, sharp, single face
- **Consistency:** Same lighting conditions jika memungkinkan

### Dataset Organization (Lesson 2)
- **Naming:** `person_ID_name` format untuk consistency
- **Metadata:** Selalu include capture info
- **Backups:** Auto-backup sebelum perubahan besar
- **Versioning:** Date-stamped backups

### Quality Control
- **Trust the automation:** Quality checks sudah tuned
- **Manual review:** Spot-check beberapa samples
- **Re-capture:** Jangan ragu recapture jika hasil kurang bagus
- **Goal:** >80% pass rate untuk quality checks

---

## ✅ Checklist Progress

```
[ ] Lesson 1: Captured 3+ people dengan 20+ photos each
[ ] Quality check passed >80% (check rejected/ folder)
[ ] Lesson 2: Dataset organized dengan proper structure
[ ] Metadata generated untuk semua person
[ ] Backup created successfully
[ ] Dataset statistics reviewed
```

---

## 🐛 Common Issues & Solutions

**Webcam tidak terbuka:**
- Check apakah webcam sudah digunakan aplikasi lain
- Coba restart Python script
- Check `cv2.VideoCapture(0)` - ubah 0 menjadi 1 jika perlu

**Semua foto masuk rejected/:**
- Check lighting - perlu cahaya yang cukup
- Lower quality thresholds di code
- Manual review rejected photos

**Dataset organization error:**
- Pastikan sudah run Lesson 1 dulu
- Check `captured_faces/` folder ada isinya
- Check permissions untuk create folders

---

## 📖 Code Concepts

**Quality Check Implementation:**
```python
# Blur detection
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
is_sharp = laplacian_var > 100

# Brightness check
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
brightness = np.mean(hsv[:,:,2])
is_good_light = 40 <= brightness <= 220

# Face size check
x, y, w, h = face_bbox
is_large_enough = w >= 100 and h >= 100
```

**Metadata Generation:**
```python
import json
from datetime import datetime

metadata = {
    'person_id': '001',
    'name': person_name,
    'photo_count': len(photos),
    'capture_date': datetime.now().strftime('%Y-%m-%d')
}

with open('metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
```

**Backup Creation:**
```python
import shutil
from datetime import datetime

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_file = f'backups/dataset_backup_{timestamp}'
shutil.make_archive(backup_file, 'zip', 'dataset/')
```

---

## ⏭️ Next Steps

Setelah menyelesaikan minggu 4:

1. ✅ Dataset dengan 3+ people, 20+ photos each
2. ✅ Quality validated (>80% good photos)
3. ✅ Proper folder structure dengan metadata
4. ✅ Backups created
5. ✅ Ready untuk **Minggu 5: Recognition System**



---

**Great dataset = Great recognition! 📸**

*Quality data is foundation of good AI. Take time to do this right!*
