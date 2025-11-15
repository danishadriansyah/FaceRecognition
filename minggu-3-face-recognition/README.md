# Minggu 3: Face Recognition Fundamentals

## Tujuan Pembelajaran
- Memahami face recognition vs face detection
- Menggunakan face_recognition library
- Face encodings dan comparison
- Build recognition system

## Struktur Folder

```
minggu-3-face-recognition/
├── README.md
├── learning/          # Tutorial dan latihan
│   ├── 01_face_encodings.py
│   ├── 02_face_comparison.py
│   ├── 03_recognition_webcam.py
│   ├── 04_multiple_faces.py
│   └── latihan.py
└── project/           # Module untuk progressive build
    ├── face_recognizer.py
    ├── test_recognizer.py
    └── README.md
```

## Learning Goals

### Tutorial Materials (learning/)
1. **01_face_encodings.py** - Generate face encodings
2. **02_face_comparison.py** - Compare face encodings
3. **03_recognition_webcam.py** - Real-time recognition
4. **04_multiple_faces.py** - Multiple face recognition
5. **latihan.py** - Build simple recognition system

### Konsep Utama
- Face encodings (128-dimension vectors)
- face_distance() dan face_compare()
- Tolerance levels
- Known faces database
- Recognition confidence

## Project Development

### Module: `face_recognizer.py`
Production-ready face recognition module dengan fungsi:
- `FaceRecognizer` class - Main recognition engine
- `encode_face()` - Generate face encoding
- `recognize_face()` - Identify person from encoding
- `add_known_face()` - Add to known faces database
- `get_all_encodings()` - Export encodings
- `calculate_confidence()` - Recognition confidence score

### Integration
Uses Week 2 `face_detector.py` for preprocessing.  
Module ini akan digunakan oleh:
- Week 4: Dataset collection
- Week 5: Full recognition system
- Week 6: Attendance system
- Week 7-8: Desktop GUI application

## Cara Penggunaan

### Learning (Tutorial)
```bash
cd minggu-3-face-recognition/learning
python 01_face_encodings.py
python 02_face_comparison.py
python 03_recognition_webcam.py
python 04_multiple_faces.py
python latihan.py
```

### Project Development
```bash
cd minggu-3-face-recognition/project
python test_recognizer.py

# Integrate to main project
# Copy face_recognizer.py to ../../core/
```

## Konsep Penting

### Face Encodings
- 128-dimension vector representation
- Unique untuk setiap wajah
- Invariant terhadap lighting, angle (dengan batasan)

### Face Distance
```python
distance = face_recognition.face_distance(known_encodings, unknown_encoding)
# Lower distance = more similar
# Typical threshold: 0.6
```

## Deliverables

### Learning
- Understanding face encodings
- Recognition from webcam
- Database of known faces

### Project
- `face_recognizer.py` - Core recognition module
- `test_recognizer.py` - Comprehensive tests
- Known faces database structure

## Next Week Preview

**Minggu 4: Dataset Collection**
- Systematic face data collection
- Multiple angles and lighting
- Dataset management
- Data quality validation

---

**Time Estimate:** 5-6 hours  
**Difficulty:** Intermediate
