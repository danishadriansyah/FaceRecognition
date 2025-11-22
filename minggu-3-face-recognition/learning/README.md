# Minggu 3 - Learning: Face Recognition

## 📚 Overview
Folder ini berisi **2 lessons** untuk belajar face recognition menggunakan **MediaPipe** library (updated dari face_recognition). Anda akan belajar cara mengenali dan membedakan wajah orang menggunakan face encodings (128-d vectors).

⚠️ **NOTE:** Project sudah migrate dari `face_recognition` ke `MediaPipe` karena:
- ✅ Tidak butuh compile C++ (no dlib!)
- ✅ Super cepat (30+ FPS)
- ✅ Google product (well-maintained)

## 📁 File Structure

```
learning/
├── README.md (file ini)
├── lesson-1/          # Face encoding & recognition (gambar)
│   ├── main.py
│   ├── README.md
│   ├── known_faces/   # Database known faces
│   ├── images/        # Test images
│   └── output/        # Recognition results
└── lesson-2/          # Real-time recognition (webcam)
    ├── main.py
    ├── README.md
    ├── known_faces/
    └── output/
```

---

## 🎯 Tutorial Lessons - Detailed Guide

### Lesson 1: Face Encoding & Recognition (Gambar)
**Lokasi:** `lesson-1/main.py`

**Tujuan:** Memahami face encodings dan bagaimana mengenali wajah dari static images

**Apa yang dipelajari:**
- Setup known faces database (folder per person)
- Generate face encodings (128-dimension vectors) dengan MediaPipe
- Load known faces dan build encodings database
- Recognize face dari test image
- Calculate distance & determine match
- Display results dengan confidence score

**Cara menggunakan:**
```bash
cd minggu-3-face-recognition/learning/lesson-1
python main.py
```

**Setup known faces:**
```
known_faces/
├── alice/
│   ├── photo1.jpg
│   └── photo2.jpg
└── bob/
    ├── photo1.jpg
    └── photo2.jpg
```

**Output yang diharapkan:**
- Console print: Recognition results
- Distance scores untuk setiap comparison
- Best match name dengan confidence
- Output images saved di `output/` folder

**Konsep penting:**
- MediaPipe FaceMesh - Extract facial landmarks & features
- Encoding adalah unique "fingerprint" untuk setiap wajah
- Encodings dapat disimpan dan di-load kembali
- Same person = similar encodings
- Different person = different encodings

**Code example (MediaPipe version):**
```python
import mediapipe as mp
import pickle
import cv2

# Load image
image = cv2.imread('person.jpg')
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Initialize MediaPipe
mp_face_detection = mp.solutions.face_detection
with mp_face_detection.FaceDetection() as face_detection:
    results = face_detection.process(rgb_image)
    
    if results.detections:
        # Face detected! Extract features
        # (Actual feature extraction handled by face_recognizer.py)
        print("Face detected!")
        
        # Save encoding (import from project folder)
        import sys
        sys.path.append('../project')
        from face_recognizer import FaceRecognizer
        
        recognizer = FaceRecognizer()
        encoding = recognizer.encode_face(image)
        
        with open('person.pkl', 'wb') as f:
            pickle.dump(encoding, f)
```

**Tips:**
- Always check if face was detected (len(encodings) > 0)
- Use high-quality frontal face images
- One encoding per face in image
- Store encodings dengan nama yang jelas

---

### Lesson 2: Real-Time Recognition dari Webcam
**Lokasi:** `lesson-2/main.py`

**Tujuan:** Real-time face recognition dari webcam stream

**Apa yang dipelajari:**
- Load known faces database dari lesson 1
- Real-time face detection & recognition
- Display names dan confidence scores
- Handle multiple faces simultaneously
- Performance optimization untuk smooth video (>15 FPS)

**Cara menggunakan:**
```bash
cd minggu-3-face-recognition/learning/lesson-2
python main.py
```

**Setup:**
- Gunakan known_faces dari lesson-1 (atau buat baru)
- Webcam harus terhubung dan working

**Output yang diharapkan:**
- Live video feed dengan rectangle boxes
- Names displayed above each detected face
- Confidence scores shown (e.g., "Alice 85%")
- "Unknown" untuk wajah yang tidak dikenali
- Smooth performance (>15 FPS)

**Keyboard controls:**
- ESC: Exit program
- SPACE: Save current frame snapshot
- R: Reset recognition cache

**Performance optimization tips:**
```python
# Process every Nth frame untuk speed
frame_count = 0
if frame_count % 3 == 0:  # Process every 3rd frame
    results = recognizer.recognize_faces_in_image(small_frame)

# Resize frame untuk faster processing
small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
```

**Konsep penting:**
- **Real-time vs Batch:** Video needs speed, optimize aggressively
- **Frame skipping:** Process every 2-3 frames, reuse results
- **Resize strategy:** 1/4 size (0.25 scale) = 16x faster
- **MediaPipe advantage:** Already optimized for real-time!

---

## 🎓 Cara Belajar yang Efektif

### Step 1: Setup Known Faces Database
```bash
cd minggu-3-face-recognition/learning/lesson-1
```

Buat folder `known_faces/` dengan struktur:
```
known_faces/
├── alice/
│   ├── photo1.jpg
│   └── photo2.jpg
├── bob/
│   ├── photo1.jpg
│   └── photo2.jpg
└── charlie/
    ├── photo1.jpg
    └── photo2.jpg
```

### Step 2: Learn Face Encoding & Recognition
```bash
python main.py
```
- Pahami bagaimana face encodings di-generate
- Lihat distance calculation dan matching
- Eksperimen dengan berbagai test images

### Step 3: Real-time Recognition
```bash
cd ../lesson-2
python main.py
```
- Test dengan wajah known dan unknown
- Perhatikan performance (FPS)
- Coba multiple faces simultaneously

### Step 4: Optimization
- Adjust tolerance threshold (0.5 - 0.7)
- Test different frame skip rates
- Try different resize scales

---

## ✅ Checklist Progress

```
[ ] Lesson 1 completed - Static image recognition working
[ ] Built known_faces database dengan 3+ people
[ ] Recognition accuracy >85% di lesson 1
[ ] Lesson 2 completed - Real-time recognition smooth
[ ] Performance >15 FPS di lesson 2
[ ] Understand tolerance tuning
[ ] Can handle multiple faces
[ ] Ready untuk minggu 4!
```

---

## 🐛 Common Issues & Solutions

**No face detected in image:**
- Ensure face is clear and frontal
- Check image quality (not too blurry)
- Face should be large enough in frame
- MediaPipe works best with well-lit faces

**Recognition returns "Unknown" for known person:**
- Check if person exists di known_faces database
- Try adding more photos of that person (2-3 minimum)
- Lower tolerance threshold (try 0.5)
- Ensure photos are good quality

**Wrong person recognized:**
- Increase tolerance strictness (try 0.5 instead of 0.6)
- Use better quality enrollment photos
- Check for similar-looking people in database
- Add more varied photos per person

**Slow performance on webcam (Lesson 2):**
- Increase frame skip rate (process every 3-5 frames)
- Reduce frame resize scale (try 0.2 instead of 0.25)
- Reduce number of known faces if possible
- Close other applications using webcam

**Import error: No module named 'mediapipe':**
```bash
pip install mediapipe opencv-python numpy
```

**Webcam not opening:**
- Check if other apps using webcam
- Try different camera index: `cv2.VideoCapture(1)`
- Verify webcam permissions

---

## 📚 Key Concepts Summary

### Face Encodings
- 128-dimension numerical vector
- Unique "fingerprint" untuk setiap wajah
- Generated by deep neural network
- Dapat disimpan dan di-load
- Fast to compare (vector math)

### Face Recognition Process
1. Detect face locations
2. Generate encodings untuk each face
3. Compare dengan known encodings
4. Find best match berdasarkan distance
5. Apply tolerance threshold

### Distance vs Similarity
- Lower distance = More similar
- Distance 0.0 = Identical (same photo)
- Distance < 0.4 = Very likely same person
- Distance 0.4-0.6 = Likely same person
- Distance > 0.6 = Probably different person

### Tolerance Setting
```python
# Strict (low false positives, might miss matches)
tolerance = 0.4

# Balanced (recommended)
tolerance = 0.6

# Loose (more matches, more false positives)
tolerance = 0.7
```

---

## 📖 Additional Resources

- **MediaPipe:** https://mediapipe.dev/
- **How it works:** MediaPipe FaceMesh - 468 facial landmarks
- **Theory:** FaceNet/VGGFace2 embeddings (128-d vectors)
- **Previous:** face_recognition library (now replaced with MediaPipe)

---

## ⏭️ Next Steps

Setelah selesai kedua lessons:

1. ✅ Can recognize faces dari static images (Lesson 1)
2. ✅ Real-time recognition working smoothly (Lesson 2)
3. ✅ Recognition accuracy >85%
4. ✅ Performance >15 FPS di webcam
5. ✅ Review code di `../project/face_recognizer.py` module
6. ✅ Run tests: `python ../project/test_recognizer.py`
7. ✅ Complete tugas di `../tugas/README.md`
8. ✅ Lanjut ke **Minggu 4: Dataset Collection & Management**

---

**Awesome work! 🚀**

*Face recognition adalah core AI capability. Master ini untuk build attendance system!*
