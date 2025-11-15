# Minggu 2 - Learning: Face Detection

##  Overview
Folder ini berisi 4 tutorial files untuk belajar face detection menggunakan Haar Cascade Classifier. Anda akan belajar cara mendeteksi wajah dari gambar statis dan real-time webcam.

##  File Structure

```
learning/
 README.md (file ini)
 01_face_detection_image.py
 02_face_detection_webcam.py
 03_detection_parameters.py
 04_optimizing_detection.py
```

---

##  Tutorial Files - Detailed Guide

### 01_face_detection_image.py
**Tujuan:** Face detection dasar dari gambar statis

**Apa yang dipelajari:**
- Load Haar Cascade classifier
- Detect faces dari image file
- Draw bounding boxes di sekitar wajah
- Understand cascade classifier parameters
- Save hasil detection

**Cara menggunakan:**
```bash
cd minggu-2-face-detection/learning
python 01_face_detection_image.py
```

**Output yang diharapkan:**
- Window menampilkan image dengan bounding boxes
- Console print: jumlah wajah terdeteksi
- Rectangle hijau mengelilingi setiap wajah
- Koordinat dan ukuran setiap detection

**Konsep penting:**
- cv2.CascadeClassifier() - Load pre-trained model
- detectMultiScale() - Main detection function
- Bounding box format: (x, y, w, h)
- Grayscale conversion untuk performa
- scaleFactor: image pyramid scale
- minNeighbors: detection quality threshold

**Tips:**
- Convert ke grayscale dulu sebelum detect
- Haar Cascade works best dengan frontal faces
- Adjust parameters untuk balance speed vs accuracy

---

### 02_face_detection_webcam.py
**Tujuan:** Real-time face detection dari webcam

**Apa yang dipelajari:**
- Integrate face detection dengan webcam
- Process frames in real-time
- Display FPS (frames per second)
- Handle multiple faces simultaneously
- Optimize untuk performance

**Cara menggunakan:**
```bash
python 02_face_detection_webcam.py
```

**Output yang diharapkan:**
- Live webcam dengan rectangles di wajah
- FPS counter di corner
- Multiple faces detected bersamaan
- Smooth real-time detection
- Press 'q' untuk quit

**Konsep penting:**
- Frame-by-frame processing
- Performance optimization
- Real-time constraints (maintain >15 FPS)
- Multi-face detection
- Drawing on live frames

**Performance tips:**
- Resize frame ke 640x480 untuk speed
- Process every Nth frame jika lambat
- Use threading untuk camera I/O
- Optimize scaleFactor dan minNeighbors

**Troubleshooting:**
- Slow FPS: Reduce resolution atau skip frames
- False detections: Increase minNeighbors
- Missed faces: Decrease minNeighbors atau scaleFactor

---

### 03_detection_parameters.py
**Tujuan:** Understand dan tune detection parameters

**Apa yang dipelajari:**
- scaleFactor effect pada detection
- minNeighbors untuk quality control
- minSize dan maxSize untuk filtering
- Compare different parameter combinations
- Visual comparison tool

**Cara menggunakan:**
```bash
python 03_detection_parameters.py
```

**Output yang diharapkan:**
- Multiple windows dengan different parameters
- Side-by-side comparison
- Console print: detection counts
- Best parameter recommendations

**Parameters explained:**

**scaleFactor (1.1 - 1.5):**
- Smaller (1.1): More thorough, slower, more detections
- Larger (1.3): Faster, fewer detections, might miss faces
- Recommended: 1.1 - 1.2 untuk accuracy

**minNeighbors (3 - 6):**
- Lower (3): More detections, more false positives
- Higher (6): Fewer false positives, might miss real faces
- Recommended: 5 untuk balance

**minSize (30, 30):**
- Minimum face size to detect (pixels)
- Filter out tiny false detections
- Adjust based on camera distance

**Experiments to try:**
```python
# Conservative (high quality, slower)
faces = cascade.detectMultiScale(gray, 1.1, 6, minSize=(50,50))

# Aggressive (fast, more false positives)
faces = cascade.detectMultiScale(gray, 1.3, 3, minSize=(30,30))

# Balanced (recommended)
faces = cascade.detectMultiScale(gray, 1.2, 5, minSize=(40,40))
```

---

### 04_optimizing_detection.py
**Tujuan:** Advanced optimization techniques

**Apa yang dipelajari:**
- Frame skipping untuk speed
- Region of Interest (ROI) detection
- Multi-scale detection strategies
- Tracking untuk stability
- Performance benchmarking

**Cara menggunakan:**
```bash
python 04_optimizing_detection.py
```

**Output yang diharapkan:**
- Benchmarks untuk different methods
- FPS comparisons
- Optimized real-time detection
- Resource usage stats

**Optimization techniques:**

**1. Frame Skipping:**
```python
frame_count = 0
if frame_count % 3 == 0:  # Detect every 3rd frame
    faces = detect_faces(frame)
frame_count += 1
```

**2. ROI Detection:**
```python
# Only detect in center region
h, w = frame.shape[:2]
roi = frame[h//4:3*h//4, w//4:3*w//4]
faces = detect_faces(roi)
```

**3. Resolution Reduction:**
```python
small_frame = cv2.resize(frame, (320, 240))
faces = detect_faces(small_frame)
# Scale coordinates back to original size
```

**Performance metrics:**
- Full resolution: ~10 FPS
- Reduced resolution: ~25 FPS
- Frame skipping: ~30 FPS
- ROI only: ~35 FPS

---

##  Cara Belajar yang Efektif

### Step 1: Understand Haar Cascade
- Baca tentang Haar-like features
- Pahami cascade of classifiers concept
- Review pre-trained models available

### Step 2: Run Basic Detection
```bash
python 01_face_detection_image.py
```

### Step 3: Try Real-time
```bash
python 02_face_detection_webcam.py
```

### Step 4: Experiment Parameters
```bash
python 03_detection_parameters.py
```
Coba berbagai kombinasi untuk tau effect-nya

### Step 5: Optimize
```bash
python 04_optimizing_detection.py
```
Test performa dan cari balance terbaik

---

##  Checklist Progress

```
[ ] 01_face_detection_image.py - Understood & tested
[ ] 02_face_detection_webcam.py - Real-time working smoothly
[ ] 03_detection_parameters.py - Parameters tuned properly
[ ] 04_optimizing_detection.py - Optimization techniques mastered
[ ] Can detect faces reliably (>90% accuracy)
[ ] Achieving good FPS (>15 FPS real-time)
```

---

##  Common Issues & Solutions

**No faces detected:**
- Check if face is frontal (not profile)
- Ensure good lighting
- Lower minNeighbors (try 3)
- Decrease scaleFactor (try 1.1)

**Too many false positives:**
- Increase minNeighbors (try 6-8)
- Increase minSize
- Ensure proper lighting

**Low FPS / Laggy:**
- Reduce camera resolution
- Skip frames (detect every 3rd frame)
- Increase scaleFactor
- Use ROI detection only

**Rectangle flickering:**
- Implement tracking between frames
- Smooth coordinates with averaging
- Use larger minNeighbors

**Import error: haarcascade file not found:**
```python
# Use full path
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
detector = cv2.CascadeClassifier(cascade_path)
```

---

##  Key Concepts Summary

### Haar Cascade Classifier
- Machine learning based object detection
- Trained on thousands of positive/negative images
- Fast enough for real-time detection
- Best for frontal faces
- Multiple cascades available (profile, eye, smile)

### detectMultiScale Parameters
```python
faces = cascade.detectMultiScale(
    image,              # Grayscale input
    scaleFactor=1.1,    # Image pyramid scale (1.05-1.5)
    minNeighbors=5,     # Quality threshold (3-6)
    minSize=(30, 30),   # Min face size in pixels
    maxSize=(300, 300)  # Max face size (optional)
)
```

### Bounding Box Format
```python
for (x, y, w, h) in faces:
    # x, y: top-left corner
    # w: width of face
    # h: height of face
    cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)
```

### Best Practices
- Always convert to grayscale first
- Validate detection results
- Handle empty detection arrays
- Optimize for your specific use case
- Test with various lighting conditions

---

##  Additional Resources

- OpenCV Haar Cascade: https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html
- Face Detection Paper: Viola-Jones Algorithm
- Pre-trained Models: cv2.data.haarcascades
- Alternative: DNN-based detectors (faster, more accurate)

---

##  Next Steps

Setelah selesai minggu 2:

1.  Dapat detect faces dari image dengan reliable
2.  Real-time detection smooth (>15 FPS)
3.  Parameters di-tune dengan baik
4.  Pindah ke folder ../project/
5.  Review face_detector.py module
6.  Run tests: python ../project/test_detector.py
7.  Lanjut ke **Minggu 3: Face Recognition**

---

**Great progress! **

*Face detection adalah fondasi untuk face recognition. Master this first!*
