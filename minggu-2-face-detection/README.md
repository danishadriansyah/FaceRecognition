# Minggu 2: Face Detection dengan MediaPipe

## Tujuan Pembelajaran
- Memahami konsep face detection
- Menggunakan MediaPipe Face Detection (Google's ML model)
- Mendeteksi wajah dari gambar dan webcam dengan 10-15ms performance
- Multiple face detection dengan confidence scores & keypoints

## Struktur Folder

```
minggu-2-face-detection/
├── README.md
├── learning/          # Tutorial dan latihan
│   ├── 01_face_detection_image.py
│   ├── 02_face_detection_webcam.py
│   ├── 03_eye_detection.py
│   ├── 04_advanced_detection.py
│   └── latihan.py
├── project/           # Module untuk progressive build
│   ├── face_detector.py
│   ├── test_detector.py
│   └── README.md
└── haarcascades/      # Pre-trained models
```

## Learning Goals

### Tutorial Materials (learning/)
1. **01_face_detection_image.py** - Face detection dari gambar statis
2. **02_face_detection_webcam.py** - Real-time face detection
3. **03_eye_detection.py** - Deteksi mata dari wajah
4. **04_advanced_detection.py** - Advanced detection features
5. **latihan.py** - Mini project face detection

### Konsep Utama
- MediaPipe Face Detection (Google's state-of-the-art ML model)
- Fast inference (10-15ms per frame on CPU)
- Confidence scoring (0.0-1.0 for each detection)
- Face keypoints (6 points: eyes, nose, mouth, ears)
- Model selection: short-range (0-2m) vs full-range (0-5m)
- Real-time capable (60+ FPS on webcam)

## Project Development

### Module: `face_detector.py`
Production-ready face detection module dengan MediaPipe:
- `FaceDetector` class - Face detection dengan MediaPipe
- `detect_faces()` - Detect faces dari image (returns bbox + confidence)
- `detect_faces_detailed()` - Detailed info with keypoints
- `detect_faces_webcam()` - Real-time detection
- `draw_detections()` - Draw bounding boxes dengan confidence & keypoints
- `get_face_regions()` - Extract face crops
- `validate_detection()` - Quality checks
- `get_face_regions()` - Extract face ROIs
- `validate_detection()` - Quality validation

### Integration
Module ini akan digunakan oleh:
- Week 3: Face recognition (preprocessing)
- Week 4: Dataset collection (validasi wajah)
- Week 5-6: Recognition system dan attendance
- Week 7-8: Desktop GUI application

## Cara Penggunaan

### Learning (Tutorial)
```bash
cd minggu-2-face-detection/learning

# Jalankan tutorial secara berurutan
python 01_face_detection_image.py
python 02_face_detection_webcam.py
python 03_eye_detection.py
python 04_advanced_detection.py

# Kerjakan latihan
python latihan.py
```

### Project Development
```bash
cd minggu-2-face-detection/project

# Test face detector module
python test_detector.py

# Integrate to main project
# Copy face_detector.py to ../../core/
```

## Konsep Penting

### Haar Cascade
- Machine Learning based object detection
- Pre-trained dengan ribuan images
- Fast detection (real-time capable)

### detectMultiScale Parameters
```python
faces = cascade.detectMultiScale(
    gray_image,
    scaleFactor=1.1,    # Scale reduction per iteration
    minNeighbors=5,     # Neighbors to retain detection
    minSize=(30, 30)    # Minimum face size
)
```

## Deliverables

### Learning
- Completed tutorial exercises
- Understanding of Haar Cascade
- Ability to detect faces in real-time

### Project
- `face_detector.py` - Reusable face detection module
- `test_detector.py` - Unit tests
- Integration-ready for main project

## Next Week Preview

**Minggu 3: Face Recognition**
- MediaPipe Face Recognition
- Face encodings
- Face comparison
- Recognition system basics

---

**Time Estimate:** 4-5 hours  
**Difficulty:** Intermediate
