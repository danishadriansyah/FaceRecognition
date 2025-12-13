# Minggu 5: Complete Face Recognition System (File-Based)

## 🚀 Quick Setup

**Auto-setup dengan interactive menu:**
```bash
cd minggu-5-recognition-system
python setup_week5.py
```

Setup script akan:
- ✅ Create folder structure untuk lesson 1 & 2
- ✅ Interactive menu: **1) Capture faces** / **2) Copy dari Week 4** / **3) Skip**
- ✅ Auto-copy dataset jika pilih copy
- ✅ Show next steps untuk generate encodings

**Tinggal pilih nomor!** Script akan auto-copy atau launch camera.

---

## Tujuan Pembelajaran
- **Complete Recognition Pipeline:** Integrasikan Week 1-4 tanpa database
- Capture faces → Generate encodings → Real-time recognition
- File-based storage (pickle) untuk simplicity
- Production-ready recognition system
- Real-time webcam recognition dengan confidence scores

## Struktur Folder

```
minggu-5-recognition-system/
├── README.md
├── learning/          # Tutorial dan latihan
│   ├── README.md
│   ├── lesson-1/      # Capture & encode faces
│   │   ├── main.py
│   │   ├── known_faces/     # Foto yang di-capture
│   │   ├── encodings.pkl    # Face encodings
│   │   └── README.md
│   └── lesson-2/      # Real-time recognition
│       ├── main.py
│       ├── recognition_service.py
│       └── README.md
└── project/           # Module untuk progressive build
    ├── recognition_service.py (Complete pipeline)
    ├── test_recognition.py
    └── README.md
```

## 🔧 Tech Stack: Complete Integration

**Week 5 Focus: End-to-End Recognition**

File-based recognition system yang simple dan production-ready:

```
Capture Faces → Save Photos → Generate Encodings → Save to Pickle →
Load from Pickle → Real-time Recognition → Display Results
```

**Key Features:**
- ✅ No database needed (file-based storage)
- ✅ Capture faces langsung dari webcam
- ✅ Automatic encoding generation (DeepFace Facenet512)
- ✅ Real-time recognition dengan confidence scores
- ✅ Simple & portable (no SQL setup)

## Learning Goals

### Tutorial Materials (learning/)
1. **Lesson 1** - Capture & Encode Faces
   - Capture wajah dari webcam (10-20 foto per orang)
   - Generate 512-d encodings (DeepFace)
   - Simpan ke pickle file
   - Quality validation

2. **Lesson 2** - Real-time Recognition
   - Load encodings dari pickle
   - Real-time webcam recognition
   - Display name + confidence
   - FPS monitoring

### Konsep Utama
- **Face Capture:** Multi-angle capture untuk accuracy
- **Encoding Generation:** 512-dimensional embeddings
- **Pickle Storage:** Serialize/deserialize encodings
- **Real-time Recognition:** 6-9 FPS capable
- **Confidence Scoring:** Euclidean distance threshold
- **No Database:** Portable & easy deployment

## Project Development

### Module: `recognition_service.py`
Production-ready recognition service (file-based):

**Core Components:**
- `RecognitionService()` - Initialize dengan pickle file
- `capture_faces(name)` - Capture faces dari webcam
- `generate_encodings()` - Generate encodings untuk semua faces
- `save_encodings(filepath)` - Save ke pickle
- `load_encodings(filepath)` - Load dari pickle
- `recognize_face(image)` - Recognize single image
- `recognize_webcam()` - Real-time recognition
- `get_statistics()` - Performance stats

**Storage:**
- Folder: `known_faces/{name}/photo_001.jpg`
- Encodings: `encodings.pkl` (pickle file)
- No SQL required!

### Integration
Uses modules dari Week 1-3:
- `image_utils.py` (Week 1) - Image preprocessing
- `face_detector.py` (Week 2) - MediaPipe detection
- `face_recognizer.py` (Week 3) - DeepFace encoding

Module ini akan digunakan oleh:
- Week 6: Attendance system (recognition + recording)
- Week 7: Desktop GUI (real-time interface)

## Cara Penggunaan

### Learning (Tutorial)
```bash
cd minggu-5-recognition-system/learning

# Lesson 1: Database Integration
cd lesson-1
python main.py
# Learn about database connection and encoding loading

# Lesson 2: Recognition Service
cd ../lesson-2
python main.py
# Build and test recognition service
```

### Project Development
```bash
cd minggu-5-recognition-system/project

# Run tests
python test_recognition.py

# Use in your code
from recognition_service import RecognitionService

service = RecognitionService()
service.set_detector_recognizer(detector, recognizer)
result = service.process_image(image)
```

## Architecture - Database Integration

```
Input Image/Video
    ↓
Image Utils (preprocess)  [Week 1]
    ↓
Face Detection  [Week 2]
    ↓
Crop Face Regions
    ↓
Face Recognition - Generate Encoding  [Week 3]
    ↓
Database Manager - Load Known Encodings  [Week 4]
    ↓
Match Encoding to Database
    (Euclidean distance matching)
    ↓
Recognition Service  [Week 5]
    (Threshold comparison & confidence)
    ↓
Recognition Result + Confidence Score
```

**Integration Benefits:**
- ✅ Centralized database management
- ✅ Scalable to many people
- ✅ Easy to add new people
- ✅ Persistent storage
- ✅ Real-time recognition

## Deliverables

### Learning
- Database integration tutorial
- Encoding loading & matching
- Error handling

### Project
- `recognition_service.py` - Complete service module
- `test_recognition.py` - Integration tests (8 test cases)
- Working database connection

## Workflow Integration

**Week 4 → Week 5 Flow:**
1. Week 4 creates dataset in MySQL database
2. Week 4 generates & stores face encodings
3. Week 5 loads encodings from database
4. Week 5 performs real-time matching
5. Week 5 tracks statistics

**Complete Pipeline (Weeks 1-5):**
```
Raw Image/Video
  ↓
Week 1: Image Utils (preprocess)
  ↓
Week 2: Face Detector (find faces)
  ↓
Week 3: Face Recognizer (create encodings)
  ↓
Week 4: Dataset Manager (store in database)
  ↓
Week 5: Recognition Service (match & recognize)
```

## Next Week Preview

**Minggu 6: Attendance System**
- Attendance recording
- Person logging
- Time tracking
- Reports

---

**Time Estimate:** 4-5 hours  
**Difficulty:** Intermediate


   - Setup DeepFace dengan Facenet512
   - Generate face encodings dari database
   - Compare accuracy: Basic vs Hybrid

2. **Lesson 2** - Recognition Service & Optimization
   - Build RecognitionService class
   - Real-time webcam recognition (6-9 FPS)
   - Batch processing untuk multiple faces
   - Caching & performance optimization

### Konsep Utama
- **Hybrid Pipeline:** Fast detection + Accurate recognition
- **DeepFace Models:** Facenet512, ArcFace, SFace comparison
- **Face Encodings:** 512-dimensional embeddings
- **Distance Metrics:** Euclidean distance untuk matching
- **Threshold Tuning:** Balance false positives vs false negatives
- **Real-time Processing:** Frame skipping, caching strategies
- **Performance Metrics:** FPS, accuracy, latency monitoring

## Project Development

### Module: `recognition_service.py`
Production-ready recognition service dengan hybrid approach:

**Core Methods:**
- `RecognitionService(model='Facenet512')` - Initialize hybrid system
- `load_database()` - Load encodings dari MySQL database (Week 4)
- `encode_face(image, bbox)` - Generate 512-d encoding dengan DeepFace
- `recognize_face(image, bbox, threshold=0.6)` - Identify person dengan confidence
- `process_webcam()` - Real-time recognition (6-9 FPS)
- `batch_recognize(images)` - Process multiple images efficiently
- `get_statistics()` - Performance metrics (FPS, accuracy, latency)

**Hybrid Pipeline:**
```
Input Frame → MediaPipe Detection (10ms) → DeepFace Recognition (100ms) → Name + Confidence
```

**Performance:**
- Detection: 10-15ms per frame (MediaPipe)
- Recognition: 100-150ms per face (DeepFace Facenet512)
- Total: 110-165ms per face
- Real-time: 6-9 FPS dengan single face

### Integration
Uses modules from Week 1-4:
- `image_utils.py` (Week 1) - Image preprocessing
- `face_detector.py` (Week 2) - Haar Cascade backup
- `face_recognizer.py` (Week 3-4) - **UPGRADED: Hybrid MediaPipe + DeepFace**
- `database.py` + `models.py` (Week 4) - Load persons & encodings from MySQL

**NEW Dependencies:**
- DeepFace 0.0.89 - Face recognition
- TensorFlow 2.15.0 - DeepFace backend

Module ini akan digunakan oleh:
- Week 6: Attendance system backend (recognition + logging)
- Week 7: Desktop GUI application (real-time recognition)

## Cara Penggunaan

### Learning (Tutorial)
```bash
cd minggu-5-recognition-system/learning

# Lesson 1: Hybrid Introduction
cd lesson-1
python main.py
# Learn hybrid approach, generate encodings with DeepFace

# Lesson 2: Recognition Service
cd ../lesson-2
python main.py
# Real-time recognition dengan webcam (6-9 FPS)
```

### Project Development
```bash
cd minggu-5-recognition-system/project
python test_service.py

# Integrate to main project
# Copy recognition_service.py to ../../core/
```

## Architecture - Hybrid Pipeline

```
Input Image/Video
    ↓
Image Utils (preprocess)
    ↓
MediaPipe Detection (10-15ms)
    ⚡ Fast bounding boxes
    ↓
Crop Face Regions
    ↓
DeepFace Recognition (100-150ms per face)
    🎯 Accurate identification (97%+)
    ↓
Dataset Manager (match to database)
    ↓
Recognition Result + Confidence
```

**Hybrid Benefits:**
- ✅ 2x faster than pure DeepFace
- ✅ Production-ready accuracy (97%+)
- ✅ Real-time capable
- ✅ Scalable to multiple faces

## Deliverables

### Learning
- Complete recognition pipeline
- Optimized performance
- Error handling

### Project
- `recognition_service.py` - Complete service module
- `test_service.py` - Integration tests
- Performance benchmarks

## Next Week Preview

**Minggu 6: Database & Attendance System**
- MySQL database setup
- Attendance records
- CRUD operations
- Reports generation

---

**Time Estimate:** 6-7 hours  
**Difficulty:** Advanced
