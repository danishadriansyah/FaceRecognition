# Minggu 3 - Learning: Face Recognition

## 📚 Overview
Folder ini berisi 3 tutorial files untuk belajar face recognition menggunakan face_recognition library. Anda akan belajar cara mengenali dan membedakan wajah orang menggunakan face encodings (128-d vectors).

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
- face_recognition.face_encodings() - Generate 128-d vector
- Encoding adalah unique "fingerprint" untuk setiap wajah
- Encodings dapat disimpan dan di-load kembali
- Same person = similar encodings
- Different person = different encodings

**Code example:**
```python
import face_recognition
import pickle

# Load image
image = face_recognition.load_image_file('person.jpg')

# Generate encoding
encodings = face_recognition.face_encodings(image)
if len(encodings) > 0:
    encoding = encodings[0]  # First face
    print(f'Encoding shape: {encoding.shape}')  # (128,)
    
    # Save encoding
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
- face_recognition.compare_faces() untuk matching
- face_recognition.face_distance() untuk similarity score
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

**compare_faces():**
```python
known_encodings = [encoding1, encoding2, encoding3]
unknown_encoding = encoding_test

matches = face_recognition.compare_faces(
    known_encodings, 
    unknown_encoding,
    tolerance=0.6  # Lower = stricter
)
# Returns: [True, False, False]
```

**face_distance():**
```python
distances = face_recognition.face_distance(
    known_encodings,
    unknown_encoding
)
# Returns: [0.42, 0.68, 0.71]
# Lower distance = more similar
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

**1. Setup known faces:**
```python
import face_recognition
import pickle

# Load known encodings
with open('known_faces.pkl', 'rb') as f:
    known_data = pickle.load(f)
    known_encodings = known_data['encodings']
    known_names = known_data['names']
```

**2. Process each frame:**
```python
import cv2

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    
    # Detect faces
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    
    # Recognize each face
    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, encoding)
        name = "Unknown"
        
        if True in matches:
            distances = face_recognition.face_distance(known_encodings, encoding)
            best_match_index = np.argmin(distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]
        
        # Draw box and name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    
    cv2.imshow('Face Recognition', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

**Performance optimization:**
```python
# Process every Nth frame
frame_count = 0
process_this_frame = True

while True:
    ret, frame = cap.read()
    
    # Only process every other frame
    if process_this_frame:
        # Resize for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # Detect and recognize
        face_locations = face_recognition.face_locations(small_frame)
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

**face_recognition.face_encodings() returns empty list:**
- Face tidak terdeteksi di image
- Coba dengan gambar yang lebih jelas
- Pastikan wajah cukup besar di foto

**Wrong person recognized:**
- Lower tolerance (try 0.5)
- Use better quality enrollment photos
- Add more photos per person
- Check for similar-looking people

**Slow performance on webcam:**
- Resize frame to smaller size (0.25 scale)
- Use model='hog' instead of 'cnn'
- Process every 2-3 frames only
- Reduce number of known faces

**Import error: No module named 'face_recognition':**
```bash
pip install face-recognition
pip install dlib  # Required dependency
```

**dlib installation fails:**
- Windows: Use pre-built wheel (see minggu-1 README)
- Mac: `brew install cmake`
- Linux: `sudo apt-get install cmake`

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

- face_recognition library: https://github.com/ageitgey/face_recognition
- How it works: dlib's face recognition model
- Theory: FaceNet paper (128-d embeddings)
- Alternative: OpenCV DNN face recognition

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
