# Minggu 3 - Learning: Face Recognition dengan MediaPipe FaceMesh

## 📚 Overview

Folder ini berisi **2 lesson files** untuk belajar face recognition menggunakan **MediaPipe FaceMesh** (production-grade face encoding). Anda akan belajar cara recognize wajah secara akurat menggunakan 1404-dimensional facial landmarks.

🚀 **MediaPipe FaceMesh Benefits:**
- ✅ **No dlib compilation needed** - Just `pip install`!
- ✅ **Super fast** - 30+ FPS real-time processing
- ✅ **More accurate** - 468 facial landmarks (3D coordinates)
- ✅ **Production-ready** - Google's face technology
- ✅ **Cross-platform** - Windows, Mac, Linux instantly

## 📁 File Structure

```
learning/
├── README.md (file ini)
├── lesson-1/
│   ├── main.py              # Static image recognition
│   ├── README.md
│   ├── images/              # Test images folder
│   ├── known_faces/         # Known people photos
│   └── output/              # Results folder
└── lesson-2/
    ├── main.py              # Real-time webcam
    ├── README.md
    ├── known_faces/         # Known people photos
    └── output/              # Captured frames folder
```

---

## 🎯 Lesson 1: Static Image Recognition

**Tujuan:** Memahami face encoding dengan MediaPipe FaceMesh dan recognition dari static images

**Apa yang dipelajari:**
- Generate 1404-d face encodings (468 landmarks × 3 coordinates)
- Load known faces dari database
- Recognize all faces in image
- Calculate confidence scores (cosine similarity)
- Visualize results dengan bounding boxes

**Cara menggunakan:**
```bash
cd lesson-1
python main.py
```

**Setup folder struktur:**
```
lesson-1/
├── known_faces/
│   ├── alice/
│   │   ├── alice1.jpg
│   │   └── alice2.jpg
│   └── bob/
│       └── bob1.jpg
├── images/
│   └── test.jpg          # Test image with faces
└── output/               # Results will be saved here
```

**Output yang diharapkan:**
- ✅ Konsol: progress indicators (1️⃣ 2️⃣ 3️⃣)
- ✅ Konsol: detected faces dengan names & confidence
- ✅ File: `output/recognized.jpg` - annotated image
- ✅ Window: Display hasil recognition dengan bounding boxes

**Konsep penting:**
- **MediaPipe FaceMesh:** Extract 468 facial landmarks dalam 3D
- **Encoding:** 1404-d vector (normalized)
- **Cosine Similarity:** Distance metric untuk matching
- **Confidence:** Direct conversion dari distance score
- **Multi-face:** Process semua faces in single pass

**How it works (under the hood):**
```python
from face_recognizer import FaceRecognizer
import cv2

# Initialize recognizer dengan MediaPipe FaceMesh
recognizer = FaceRecognizer(tolerance=0.5)

# Load known faces
img = cv2.imread('alice/alice1.jpg')
encoding = recognizer.encode_face(img)  # 1404-d vector
recognizer.add_known_face(encoding, 'Alice')

# Recognize in test image
test_img = cv2.imread('test.jpg')
results = recognizer.recognize_faces_in_image(test_img)

# Results: [{'name': 'Alice', 'confidence': 0.92, 'bbox': (x,y,w,h), ...}]
```

**Key differences from old face_recognition:**
```
OLD: 128-d encoding (simplified)
NEW: 1404-d encoding (468 landmarks × 3 coords: x, y, z)

OLD: Euclidean distance
NEW: Cosine similarity (more stable for normalized vectors)

OLD: Sequential face crop + encoding
NEW: Direct FaceMesh landmark extraction (faster)
```

**Tips untuk hasil terbaik:**
- ✅ Use high-quality frontal face images (min 100x100 pixels)
- ✅ Add 2-3 photos per person untuk robustness
- ✅ Ensure consistent lighting dalam known_faces folder
- ✅ Test images sebaiknya sama format (jpg/png) dengan known faces

---

## 🎯 Lesson 2: Real-Time Webcam Recognition

**Tujuan:** Real-time face recognition dari webcam dengan live statistics

**Apa yang dipelajari:**
- Load known faces database
- Real-time detection & recognition
- FPS calculation & monitoring
- Frame caching untuk performance optimization
- Live statistics display
- Capture snapshots

**Cara menggunakan:**
```bash
cd lesson-2
python main.py
```

**Keyboard Controls:**
- `SPACE` - Capture screenshot
- `ESC` atau `Q` - Exit

**Setup (same as lesson-1):**
```
lesson-2/
├── known_faces/
│   ├── alice/
│   │   ├── alice1.jpg
│   │   └── alice2.jpg
│   └── bob/
│       └── bob1.jpg
└── output/              # Screenshots saved here
```

**Output yang diharapkan:**
- ✅ Live webcam feed dengan face boxes
- ✅ Names & confidence scores displayed
- ✅ FPS counter di top-left
- ✅ Face counter & frame counter
- ✅ Color-coded boxes (green=matched, red=unknown)
- ✅ ~30 FPS performance

**Konsep penting:**

**Performance Optimization:**
```python
# Frame caching untuk speed
cache_interval = 3  # Detect setiap 3 frames
if frame_count % cache_interval == 0:
    results = recognizer.recognize_faces_in_image(frame)
# Reuse results untuk intermediate frames
```

**Cosine Similarity (NEW from Euclidean):**
```python
# OLD: Euclidean distance = √Σ(a-b)²
# NEW: Cosine similarity = 1 - (a·b)/(‖a‖‖b‖)

# Benefit: More stable untuk normalized vectors
# Range: [0, 2] vs Euclidean [0, ∞)
```

**Tolerance Tuning:**
- `0.4`: Very strict (rarely false positives)
- `0.5`: Default, recommended
- `0.6`: More lenient (more matches)
- `0.7`: Very loose (many false positives)

**Tips untuk smooth real-time:**
- ✅ Frame caching (detect every Nth frame)
- ✅ Use consistent lighting
- ✅ Keep faces ~30cm dari camera
- ✅ Frontal face position lebih baik

---

## 📊 Technical Comparison: Old vs New

| Aspect | Old (face_recognition) | New (MediaPipe FaceMesh) |
|--------|------------------------|--------------------------|
| **Encoding** | 128-d (simplified) | 1404-d (full landmarks) |
| **Landmarks** | Implicit features | 468 explicit 3D coords |
| **Similarity** | Euclidean distance | Cosine similarity |
| **Performance** | 15-20 FPS | 30+ FPS |
| **Multi-face** | Sequential crop | Parallel processing |
| **Dependencies** | dlib (C++ compile) | MediaPipe only |
| **Install** | Complex | Simple (pip install) |
| **Accuracy** | Good | Excellent (3D geometry) |

---

## 🎓 Cara Belajar yang Efektif

### Step 1: Setup Known Faces
Create `known_faces/` folder structure dengan 2-3 orang

### Step 2: Run Lesson 1
```bash
cd lesson-1
python main.py
```
Understand static image recognition

### Step 3: Run Lesson 2
```bash
cd lesson-2
python main.py
```
Test real-time webcam recognition

### Step 4: Experiment
- Change tolerance (0.4 to 0.7)
- Add more known faces
- Test berbagai lighting conditions
- Observe FPS changes

---

## ✅ Checklist Progress

```
[ ] lesson-1/main.py - Static recognition tested
[ ] lesson-2/main.py - Real-time recognition tested
[ ] Created known_faces/ dengan 2+ people
[ ] Recognition accuracy >85%
[ ] Real-time performance >20 FPS
[ ] Understood tolerance tuning
[ ] Captures working correctly
```

---

## 🐛 Common Issues & Solutions

**No face detected in image:**
- Ensure face is clear and frontal
- Check image quality (not too blurry)
- Try different image
- Verify image loaded correctly
- MediaPipe usually detects faces well, so quality matters!

**Encoding returns None:**
- Face tidak terdeteksi di image
- Coba dengan gambar yang lebih jelas
- Pastikan wajah cukup besar di foto
- Gunakan MediaPipe FaceMesh, bukan hanya detection

**Wrong person recognized:**
- Lower tolerance (try 0.5)
- Use better quality enrollment photos
- Add more photos per person
- Check for similar-looking people

**Slow performance on webcam:**
- Resize frame to smaller size
- Process every 2-3 frames only
- Reduce number of known faces
- MediaPipe sudah fast, tapi frame cache membantu

**Import error: No module named 'mediapipe':**
```bash
pip install -r ../../requirements.txt
```

---

## 📚 Key Concepts Summary

### Face Encodings
- 1404-dimension numerical vector
- Unique "fingerprint" untuk setiap wajah
- Generated by MediaPipe FaceMesh landmarks
- Dapat disimpan dan di-load
- Fast to compare (vector math)

### Face Recognition Process
1. Detect face locations menggunakan FaceMesh
2. Generate encodings untuk each face (1404-d)
3. Compare dengan known encodings (cosine similarity)
4. Find best match berdasarkan distance
5. Apply tolerance threshold

### Distance vs Similarity
- Lower distance = More similar
- Distance 0.0 = Identical (same photo)
- Distance < 0.4 = Very likely same person
- Distance 0.4-0.5 = Likely same person
- Distance > 0.5 = Probably different person

### Tolerance Setting
```python
# Strict (low false positives, might miss matches)
tolerance = 0.4

# Balanced (recommended)
tolerance = 0.5

# Loose (more matches, more false positives)
tolerance = 0.6
```

---

## 📖 Additional Resources

- **MediaPipe:** https://mediapipe.dev/
- **FaceMesh Details:** 468 facial landmarks
- **Theory:** Facial embeddings (similarity metric)
- **Previous:** face_recognition library (now replaced with MediaPipe)

---

## ⏭️ Next Steps

Setelah selesai learning:

1. ✅ Can generate face encodings reliably
2. ✅ Recognition accuracy >85%
3. ✅ Real-time working smoothly (>20 FPS)
4. ✅ Pindah ke ../project/
5. ✅ Review face_recognizer.py module
6. ✅ Run tests: `python ../project/test_recognizer.py`
7. ✅ Lanjut ke **Minggu 4: Dataset Collection**

---

**Awesome work! 🚀**

*Face recognition adalah core AI capability. Master ini untuk build attendance system!*
