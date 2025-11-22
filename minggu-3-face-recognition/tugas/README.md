# 📝 TUGAS MINGGU 3 - Face Recognition System (Fill in the Blanks)

## 📖 Deskripsi
Lengkapi sistem face recognition dengan mengisi 8 soal

## 🎯 Objektif
- Build face recognition system dengan MediaPipe
- Database management (register, save, load)
- Recognition dari image & webcam

---

## 📋 SOAL (Total: 8 Soal)

File: `face_recognition_template.py`

**SOAL 1** (Baris 18): Import FaceRecognizer class
**SOAL 2** (Baris 29-30): Load pickle file (mode 'rb', pickle.load)
**SOAL 3** (Baris 47-48): Save pickle file (mode 'wb', pickle.dump)
**SOAL 4** (Baris 60): Buka webcam (cv2.VideoCapture)
**SOAL 5** (Baris 69): Detect tombol SPACE (ord(' '))
**SOAL 6** (Baris 100): Load image (cv2.imread)
**SOAL 7** (Baris 119): Warna merah untuk unknown (255)
**SOAL 8** (Baris 149): Method untuk recognize faces

---

## 🚀 Cara Mengerjakan

```bash
cd minggu-3-face-recognition/tugas
copy face_recognition_template.py face_recognition.py
# Edit face_recognition.py, isi semua blanks
python face_recognition.py
```

---

## 💡 Cheat Sheet

- `FaceRecognizer` - Class dari face_recognizer module
- `pickle.load(f)` / `pickle.dump(data, f)` - Load/save data
- `cv2.VideoCapture(0)` - Buka webcam
- `ord(' ')` - ASCII code untuk SPACE
- `cv2.imread()` - Load image
- `(0, 0, 255)` - Warna merah (BGR)
- `recognize_faces_in_image()` - Method FaceRecognizer

---

## ✅ Penilaian

| Soal | Poin |
|------|------|
| 1-8 | 10 pts each = 80 pts |
| Functionality | 20 pts |
| **TOTAL** | **100 pts** |

---

## 📚 Resources

- `../project/face_recognizer.py` - Module reference
- Minggu 3 Lesson 1 & 2

**Good luck! 🧑‍🤝‍🧑**

---

## 💡 Hints & Tips

### Generate Encoding
```python
import mediapipe as mp
import cv2
import numpy as np

# Initialize MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

# Load image
img = cv2.imread('photo.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Generate encoding
results = face_mesh.process(img_rgb)

if results.multi_face_landmarks:
    landmarks = results.multi_face_landmarks[0]
    # Extract feature vector
    encoding = extract_features(landmarks)  # Helper function
    # Save to database
```

### Recognition
```python
import numpy as np

# Load known encodings
known_encodings = [...]  # From database
known_names = ['Budi', 'Siti', ...]

# Calculate distances using Euclidean distance
distances = []
for known_enc in known_encodings:
    distance = np.linalg.norm(known_enc - unknown_encoding)
    distances.append(distance)

best_match = np.argmin(distances)

if distances[best_match] < 0.6:  # Threshold
    name = known_names[best_match]
    confidence = (1 - distances[best_match]) * 100
else:
    name = "Unknown"
```

### Save Database
```python
import pickle

database = {
    'encodings': known_encodings,
    'names': known_names
}

with open('known_faces/encodings.pkl', 'wb') as f:
    pickle.dump(database, f)
```

### Real-time Recognition
```python
cap = cv2.VideoCapture(0)

# Initialize MediaPipe
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection()

while True:
    ret, frame = cap.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect faces with MediaPipe
    results = face_detection.process(rgb_frame)
    
    if results.detections:
        for detection in results.detections:
            # Extract bounding box
            bbox = detection.location_data.relative_bounding_box
            h, w, _ = frame.shape
            
            left = int(bbox.xmin * w)
            top = int(bbox.ymin * h)
            right = int((bbox.xmin + bbox.width) * w)
            bottom = int((bbox.ymin + bbox.height) * h)
            
            # Get encoding and recognize
            face_crop = frame[top:bottom, left:right]
            encoding = extract_encoding(face_crop)  # Use face_recognizer
            name = recognize_face(encoding)
            
            # Draw box
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top-10), ...)
```

---

## ✅ Kriteria Penilaian

| Kriteria | Bobot | Poin |
|----------|-------|------|
| Register function | 20% | 20 |
| Image recognition | 20% | 20 |
| Webcam recognition | 20% | 20 |
| Database management | 15% | 15 |
| Accuracy (>85%) | 15% | 15 |
| Documentation | 10% | 10 |

**Total: 100 points**

---

## 🌟 Fitur Bonus

- [ ] Multiple encodings per person (improved accuracy)
- [ ] Attendance logging (auto-save recognition)
- [ ] Confidence threshold setting
- [ ] Face image preview in database
- [ ] Export recognition log to CSV
- [ ] GUI interface
- [ ] Email notification for unknown person

**+10 pts per fitur**

---

## ⏰ Deadline

**4 hari** setelah menyelesaikan Minggu 3

---

## 🎓 Learning Outcomes

- ✅ Face encoding generation
- ✅ Face comparison & matching
- ✅ Database management
- ✅ Real-time recognition
- ✅ Confidence thresholds

---

## 📚 Resources

- Minggu 3 Lesson 1 & 2
- MediaPipe Face Mesh documentation
- Known faces samples

**Good luck! 🧑‍🤝‍🧑✨**
