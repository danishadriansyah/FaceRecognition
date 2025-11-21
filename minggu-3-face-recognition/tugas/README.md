# 📝 TUGAS MINGGU 3 - Face Recognition

## Deskripsi
Buat sistem face recognition yang bisa mengenali orang dari database wajah yang sudah terdaftar.

---

## 🎯 Objektif
- Build face recognition system
- Create known faces database
- Recognition dari gambar & webcam
- Handle unknown persons

---

## 📋 Tugas: Face Recognition System

Buat program `face_recognizer.py` dengan fitur:

### Fitur Wajib
1. **Register Mode**
   - Input nama orang
   - Capture/upload foto
   - Generate face encoding
   - Save to database

2. **Recognition Mode**
   - Load image → recognize person
   - Show name + confidence
   - Handle "Unknown" person
   - Bounding box dengan label

3. **Webcam Recognition**
   - Real-time recognition
   - Display name di atas wajah
   - Confidence percentage
   - Color coding (green=known, red=unknown)

4. **Database Management**
   - List all registered persons
   - View person details
   - Delete person
   - Database statistics

---

## 📦 Deliverables

```
tugas/
├── face_recognizer.py      # Main program
├── known_faces/            # Database
│   ├── person1_*.jpg
│   ├── person2_*.jpg
│   └── encodings.pkl      # Saved encodings
├── test_images/            # Test images
├── output/                 # Recognition results
└── README.md              # Documentation
```

---

## 🎯 Example Output

### Console:
```
========================================
   FACE RECOGNITION SYSTEM
========================================

Database: 5 persons registered

Main Menu:
1. Register New Person
2. Recognize from Image
3. Recognize from Webcam
4. Manage Database
5. Exit

Pilih: 2

Enter image path: test_images/group.jpg

Processing...
✅ Recognized 3 faces:
   - Budi (87.3% confidence)
   - Siti (92.1% confidence)
   - Unknown Person

Saved to: output/recognized_group.jpg
```

### Database Structure:
```
known_faces/
├── budi_001.jpg
├── budi_002.jpg
├── budi_003.jpg
├── siti_001.jpg
├── siti_002.jpg
└── encodings.pkl
```

---

## 💡 Hints & Tips

### Generate Encoding
```python
import face_recognition

img = face_recognition.load_image_file('photo.jpg')
encodings = face_recognition.face_encodings(img)

if len(encodings) > 0:
    encoding = encodings[0]  # First face
    # Save to database
```

### Recognition
```python
# Load known encodings
known_encodings = [...]  # From database
known_names = ['Budi', 'Siti', ...]

# Compare
distances = face_recognition.face_distance(known_encodings, unknown_encoding)
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

while True:
    ret, frame = cap.read()
    
    # Detect faces
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    
    # Recognize each face
    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
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
- `face_recognition` library docs
- Known faces samples

**Good luck! 🧑‍🤝‍🧑✨**
