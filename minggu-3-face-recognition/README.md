# Minggu 3: Face Recognition Fundamentals

## Tujuan Pembelajaran
- Memahami face recognition vs face detection
- Menggunakan MediaPipe untuk face recognition
- Face encodings dan comparison
- Build recognition system

## Struktur Folder

```
minggu-3-face-recognition/
├── README.md
├── learning/          # Tutorial dan latihan
│   ├── lesson-1/     # Face encoding & recognition (gambar)
│   │   ├── main.py
│   │   ├── README.md
│   │   ├── known_faces/
│   │   ├── images/
│   │   └── output/
│   ├── lesson-2/     # Real-time recognition (webcam)
│   │   ├── main.py
│   │   ├── README.md
│   │   ├── known_faces/
│   │   └── output/
│   └── README.md
├── project/           # Module untuk progressive build
│   ├── face_detector.py
│   ├── face_recognizer.py
│   ├── image_utils.py
│   ├── test_recognizer.py
│   ├── test_images/
│   ├── output/
│   └── README.md
└── tugas/
    └── README.md
```

## Learning Goals

### Tutorial Materials (learning/)
1. **lesson-1/** - Face encoding & recognition dari gambar
   - Generate face encodings dengan MediaPipe
   - Compare encodings untuk recognize
   - Build known faces database
   - Recognition dari static images

2. **lesson-2/** - Real-time recognition dari webcam
   - Load known faces database
   - Real-time face detection & recognition
   - Display names dan confidence scores
   - Performance optimization

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
# Lesson 1: Face encoding dari gambar
cd minggu-3-face-recognition/learning/lesson-1
python main.py

# Lesson 2: Real-time recognition
cd minggu-3-face-recognition/learning/lesson-2
python main.py
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
import numpy as np

# Calculate Euclidean distance
distances = [np.linalg.norm(known_enc - unknown_encoding) for known_enc in known_encodings]
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

**Time Estimate:** 3-4 hours  
**Difficulty:** Intermediate
