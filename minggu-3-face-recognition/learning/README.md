# Minggu 3 - Learning: Face Recognition

## 📚 Overview
Folder ini berisi 3 tutorial files untuk belajar face recognition menggunakan **MediaPipe** library (updated dari face_recognition). Anda akan belajar cara mengenali dan membedakan wajah orang menggunakan face encodings (128-d vectors).

⚠️ **NOTE:** Project sudah migrate dari `face_recognition` ke `MediaPipe` karena:
- ✅ Tidak butuh compile C++ (no dlib!)
- ✅ Super cepat (30+ FPS)
- ✅ Google product (well-maintained)

## 📁 File Structure

```
learning/
├── README.md (file ini)
├── 01_face_encodings.py
├── 02_face_comparison.py
└── 03_recognition_webcam.py
```

---

## 🎯 Tutorial Files - Detailed Guide

### 01_face_encodings.py
**Tujuan:** Memahami face encodings dan bagaimana wajah direpresentasikan sebagai vectors

**Apa yang dipelajari:**
- Generate face encodings (128-dimension vectors)
- Save encodings ke file (.pkl, .npy)
- Load encodings dari file
- Understand encoding properties
- Compare encoding similarity

**Cara menggunakan:**
```bash
cd minggu-3-face-recognition/learning
python 01_face_encodings.py
```

**Output yang diharapkan:**
- Console print: encoding vector (128 numbers)
- Saved encodings file: person_encoding.pkl
- Shape: (128,) float array
- Values: normalized between -1 and 1

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
        
        # Save encoding (from face_recognizer module)
        from minggu-3-face-recognition.project.face_recognizer import FaceRecognizer
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

### 02_face_comparison.py  
**Tujuan:** Membandingkan encodings untuk recognize faces

**Apa yang dipelajari:**
- MediaPipe feature extraction
- Similarity scoring dengan distance calculation
- Set tolerance threshold untuk accuracy
- Handle multiple known faces
- Best match selection

**Cara menggunakan:**
```bash
python 02_face_comparison.py
```

**Output yang diharapkan:**
- Console print: Match results (True/False)
- Distance scores untuk setiap comparison
- Best match name
- Confidence percentages

**Konsep penting:**

**Feature Extraction (MediaPipe):**
```python
from minggu-3-face-recognition.project.face_recognizer import FaceRecognizer
import cv2

# Use FaceRecognizer untuk extract features
recognizer = FaceRecognizer()
img = cv2.imread('face.jpg')
encoding = recognizer.encode_face(img)
print(f"Encoding shape: {encoding.shape}")  # (128,)
```

**Distance Calculation:**
```python
import numpy as np

# Calculate Euclidean distance
distance = np.linalg.norm(encoding1 - encoding2)
print(f"Distance: {distance:.4f}")

# Lower distance = more similar
# If distance <= tolerance (0.6): Match!
```

**Tolerance explained:**
- 0.6: Default, balanced
- 0.5: Stricter, fewer false positives
- 0.7: Looser, more false positives
- Typical range: 0.4 - 0.6

**Best practices:**
```python
# Get best match
distances = face_recognition.face_distance(known_encodings, unknown)
best_match_index = np.argmin(distances)
min_distance = distances[best_match_index]

if min_distance < 0.6:
    name = known_names[best_match_index]
    confidence = (1 - min_distance) * 100
    print(f'Matched: {name} ({confidence:.1f}% confidence)')
else:
    print('Unknown person')
```

---

### 03_recognition_webcam.py
**Tujuan:** Real-time face recognition dari webcam

**Apa yang dipelajari:**
- Load known faces database
- Detect dan recognize faces real-time
- Display names on video feed
- Handle multiple faces simultaneously
- Optimize untuk smooth performance

**Cara menggunakan:**
```bash
python 03_recognition_webcam.py
```

**Output yang diharapkan:**
- Live webcam dengan face boxes
- Names displayed above each face
- Confidence scores shown
- "Unknown" untuk faces tidak dikenali
- Smooth performance (>10 FPS)

**Implementation steps:**

**1. Setup known faces with MediaPipe:**
```python
from minggu-3-face-recognition.project.face_recognizer import FaceRecognizer
import pickle

# Initialize recognizer
recognizer = FaceRecognizer()

# Load known faces (dapat dari database atau file)
recognizer.load_database('known_faces.pkl')
print(f"Loaded {recognizer.get_statistics()['total_faces']} known faces")
```

**2. Process each frame (using FaceRecognizer):**
```python
import cv2

cap = cv2.VideoCapture(0)
recognizer = FaceRecognizer()
recognizer.load_database('known_faces.pkl')

while True:
    ret, frame = cap.read()
    
    # Recognize all faces in frame
    results = recognizer.recognize_faces_in_image(frame)
    
    # Draw results
    for result in results:
        x, y, w, h = result['bbox']
        name = result['name']
        confidence = result['confidence']
        
        # Draw box and name
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        label = f"{name} ({confidence:.1%})"
        cv2.putText(frame, label, (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    
    cv2.imshow('Face Recognition', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

**Performance optimization:**
```python
# FaceRecognizer sudah optimized, tapi bisa dipercepat lebih lanjut:
import cv2

cap = cv2.VideoCapture(0)
frame_count = 0
results_cache = []

while True:
    ret, frame = cap.read()
    
    # Process every Nth frame
    if frame_count % 2 == 0:
        # Resize untuk faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        results_cache = recognizer.recognize_faces_in_image(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)
        # ... recognition logic ...
    
    process_this_frame = not process_this_frame
    # ... display ...
```

**Tips for smooth performance:**
- Resize frame to 1/4 size (0.25 scale)
- Process every 2nd or 3rd frame
- Cache recognition results briefly
- Use faster detection model: model='hog' (default is 'cnn')

---

## 🎓 Cara Belajar yang Efektif

### Step 1: Understand Encodings
```bash
python 01_face_encodings.py
```
Eksperimen dengan berbagai photos, lihat encoding values

### Step 2: Compare Faces
```bash
python 02_face_comparison.py
```
Test dengan same person vs different person

### Step 3: Build Database
Create folder `known_faces/` dengan photos:
```
known_faces/
├── alice_1.jpg
├── bob_1.jpg
└── charlie_1.jpg
```

### Step 4: Real-time Recognition
```bash
python 03_recognition_webcam.py
```
Test dengan wajah known dan unknown

---

## ✅ Checklist Progress

```
[ ] 01_face_encodings.py - Encodings generated successfully
[ ] 02_face_comparison.py - Comparisons working correctly
[ ] 03_recognition_webcam.py - Real-time recognition smooth
[ ] Built database dengan 3+ known faces
[ ] Recognition accuracy >85%
[ ] Performance >10 FPS
[ ] Understand tolerance tuning
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
- Resize frame to smaller size (0.25 scale)
- Process every 2-3 frames only
- Reduce number of known faces
- MediaPipe sudah fast, tapi resize frame membantu CPU

**Import error: No module named 'mediapipe':**
```bash
pip install mediapipe opencv-python
```

**Other issues:**
- Make sure you ran: `pip install -r requirements.txt`
- Verify MediaPipe installed: `python -c "import mediapipe; print('OK')"`

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

Setelah selesai minggu 3:

1. ✅ Can generate face encodings reliably
2. ✅ Recognition accuracy >85%
3. ✅ Real-time working smoothly
4. ✅ Pindah ke ../project/
5. ✅ Review face_recognizer.py module
6. ✅ Run tests: python ../project/test_recognizer.py
7. ✅ Lanjut ke **Minggu 4: Dataset Collection**

---

**Awesome work! 🚀**

*Face recognition adalah core AI capability. Master ini untuk build attendance system!*
