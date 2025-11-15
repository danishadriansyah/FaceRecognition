# Lesson 1: Face Encoding & Recognition (Gambar)

## Tujuan
- Understand konsep face encoding (128-d vector)
- Generate face encodings dari gambar
- Compare encodings untuk recognize wajah
- Build simple face recognition system

## Konsep Face Encoding

**Face Encoding** = Vector 128 angka yang represent wajah seseorang
- Setiap wajah punya encoding unik
- Compare 2 encodings → tahu sama/beda orang
- Distance < 0.6 → wajah sama
- Distance > 0.6 → wajah beda

## Setup Known Faces

Buat folder per person di `known_faces/`:
```
known_faces/
├── alice/
│   ├── photo1.jpg
│   └── photo2.jpg
└── bob/
    ├── photo1.jpg
    └── photo2.jpg
```

## Yang Dipelajari

### 1. Load Known Faces
```python
known_encodings = []
known_names = []

for person_name in os.listdir('known_faces'):
    for filename in os.listdir(f'known_faces/{person_name}'):
        img = face_recognition.load_image_file(...)
        encoding = face_recognition.face_encodings(img)[0]
        known_encodings.append(encoding)
        known_names.append(person_name)
```

### 2. Recognize Face
```python
# Load test image
test_img = face_recognition.load_image_file('test.jpg')
test_encoding = face_recognition.face_encodings(test_img)[0]

# Compare
matches = face_recognition.compare_faces(known_encodings, test_encoding)
distances = face_recognition.face_distance(known_encodings, test_encoding)

# Get best match
best_match_index = np.argmin(distances)
if matches[best_match_index]:
    name = known_names[best_match_index]
```

## Langkah Praktik

1. Buat folder `known_faces/alice/` dan `known_faces/bob/`
2. Taruh 2-3 foto masing-masing
3. Taruh test image di `images/test.jpg`
4. Run: `python main.py`
5. Check output di `output/`

## Challenge
- Recognize dari group photo (multiple faces)
- Show confidence score
- Handle unknown faces

## Next: Lesson 2 - Real-time recognition dari webcam
