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

**`known_faces/`** = Database orang yang **SUDAH DIKENAL** (untuk training/enrollment)

Buat folder per person di `known_faces/`:
```
known_faces/
├── alice/
│   ├── photo1.jpg      ← Foto Alice untuk dikenali nanti
│   └── photo2.jpg
└── bob/
    ├── photo1.jpg      ← Foto Bob untuk dikenali nanti
    └── photo2.jpg
```

**`images/`** = Test images yang **MAU DIKENALI** (bisa known atau unknown person)

Taruh test image di `images/`:
```
images/
├── test1.jpg           ← Foto seseorang (mungkin Alice, Bob, atau orang lain)
├── test2.jpg           ← Foto untuk dicek "ini siapa ya?"
└── group.jpg           ← Bisa multiple faces
```

**Cara kerjanya:**
1. Program **baca known_faces/** → Build database encoding (Alice, Bob)
2. Program **baca images/test.jpg** → "Ini foto siapa ya?"
3. Program **bandingkan** → "Oh ini Alice!" atau "Unknown person"

## Yang Dipelajari

### 1. Load Known Faces
```python
known_encodings = []
known_names = []

# Use face_recognizer module
from face_recognizer import FaceRecognizer
recognizer = FaceRecognizer()

for person_name in os.listdir('known_faces'):
    for filename in os.listdir(f'known_faces/{person_name}'):
        img = cv2.imread(...)  # Load with OpenCV
        encoding = recognizer.encode_face(img)
        if encoding is not None:
            known_encodings.append(encoding)
            known_names.append(person_name)
```

### 2. Recognize Face
```python
import numpy as np

# Load test image
test_img = cv2.imread('test.jpg')
test_encoding = recognizer.encode_face(test_img)

# Compare using distance calculation
distances = [np.linalg.norm(known_enc - test_encoding) for known_enc in known_encodings]

# Get best match
best_match_index = np.argmin(distances)
if distances[best_match_index] < 0.6:  # threshold
    name = known_names[best_match_index]
```

## Langkah Praktik

1. **Setup known faces (database):**
   - Buat folder `known_faces/alice/` dan `known_faces/bob/`
   - Taruh 2-3 foto **Alice** di folder alice/
   - Taruh 2-3 foto **Bob** di folder bob/

2. **Setup test images (yang mau dikenali):**
   - Taruh foto test di `images/test1.jpg` 
   - Bisa foto Alice (harusnya detect "Alice")
   - Bisa foto Bob (harusnya detect "Bob")
   - Bisa foto orang lain (harusnya detect "Unknown")

3. **Run program:**
   ```bash
   python main.py
   ```

4. **Check output:**
   - Lihat hasil recognition di console
   - Check output images di folder `output/`

**Contoh flow:**
```
known_faces/alice/photo1.jpg  →  Build encoding Alice
known_faces/bob/photo1.jpg    →  Build encoding Bob
images/test1.jpg              →  Load image → Compare → "Ini Alice!" ✅
```

## Challenge
- Recognize dari group photo (multiple faces)
- Show confidence score
- Handle unknown faces

## Next: Lesson 2 - Real-time recognition dari webcam
