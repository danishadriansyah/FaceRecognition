# Minggu 3 - Project Module: Face Recognizer

## 📚 Overview
Folder ini berisi implementasi production-ready module **face_recognizer.py** untuk face recognition menggunakan **MediaPipe** library (updated dari face_recognition). Module ini combines face detection (week 2) dengan face recognition untuk identify people.

⚠️ **MIGRATION UPDATE (MediaPipe):**
Seluruh project sudah di-migrate dari `face_recognition` (yang butuh dlib) ke **MediaPipe** karena:
- ✅ **Tidak butuh compile dlib** - Just pip install!
- ✅ **Super cepat** - 30+ FPS real-time processing
- ✅ **Google product** - Well-maintained, frequently updated
- ✅ **Works everywhere** - Windows, Mac, Linux instantly

**What changed in code:**
- `face_recognition.face_encodings()` → `MediaPipe FaceMesh + feature extraction`
- `face_recognition.face_locations()` → `MediaPipe FaceDetection`
- `face_recognition.face_distance()` → `numpy Euclidean distance`
- API sekarang di `FaceRecognizer` class (sudah handle semua internally)

**Dari user perspective:**
- Install: `pip install -r requirements.txt` (tidak perlu C++ tools!)
- Usage: Sama seperti sebelumnya, via `FaceRecognizer` class
- Performance: **Lebih cepat** (30+ FPS vs 15-20 FPS sebelumnya)
- All week 3-7 modules updated automatically

## 📁 File Structure

```
project/
├── README.md (file ini)
├── image_utils.py         # Week 1 module (duplicated)
├── face_detector.py       # Week 2 module (duplicated)
├── face_recognizer.py     # NEW: Face recognition module
├── test_recognizer.py     # Unit tests
├── test_images/           # Sample images untuk testing
└── output/                # Test results output
```

### 📝 Penjelasan Setiap File

| File | Fungsi | Cara Run |
|------|--------|----------|
| **image_utils.py** | Helper functions (resize, convert, save) | ❌ Tidak dirun langsung (library) |
| **face_detector.py** | Detect faces di image | ❌ Tidak dirun langsung (library) |
| **face_recognizer.py** | **MAIN MODULE** - Face recognition | ❌ Tidak dirun langsung (library) |
| **test_recognizer.py** | Test semua fungsi face_recognizer | ✅ **RUN INI!** → `python test_recognizer.py` |

### 📂 Penjelasan Folder

| Folder | Fungsi | Isi |
|--------|--------|-----|
| **test_images/** | Sample photos untuk testing | Foto-foto test (Alice, Bob, group, dll) |
| **output/** | Hasil testing & recognition | Gambar hasil annotated, logs, dll |

### 🚀 Cara Menjalankan Project

**Yang harus dijalankan cuma 1 file: `test_recognizer.py`**

```bash
cd minggu-3-face-recognition/project
python test_recognizer.py
```

**Output yang diharapkan:**
```
test_encode_face ... OK
test_add_known_face ... OK
test_recognize_face_match ... OK
test_recognize_face_unknown ... OK
test_save_load_database ... OK
test_recognize_multiple_faces ... OK

----------------------------------------------------------------------
Ran 6 tests in 2.3s

OK ✅
```

**File lainnya (image_utils.py, face_detector.py, face_recognizer.py):**
- **Tidak dirun langsung!** ❌
- Mereka adalah **library/module** yang di-import oleh test_recognizer.py
- Seperti perpustakaan - dipanggil kalau butuh, bukan dijalankan sendiri

### 🎯 Workflow Lengkap

```
1. Setup test images:
   test_images/alice.jpg     ← Taruh foto Alice
   test_images/bob.jpg       ← Taruh foto Bob
   test_images/test.jpg      ← Foto yang mau dikenali

2. Run tests:
   python test_recognizer.py

3. Check results:
   output/recognized_*.jpg   ← Hasil recognition dengan nama
   output/test_log.txt       ← Log hasil testing
```

### 🔄 Progressive Duplication Explained

**Kenapa ada `image_utils.py` dan `face_detector.py` di sini?**

Ini adalah **progressive duplication** - setiap minggu punya **semua dependencies** yang dibutuhkan agar:
- ✅ Setiap minggu **standalone** (bisa dijalankan sendiri)
- ✅ Tidak perlu import dari folder lain
- ✅ Mudah dipahami dependency-nya apa saja
- ✅ Lebih mudah untuk debugging dan testing

**PENTING:** File .py yang 3 itu (image_utils, face_detector, face_recognizer) **BUKAN untuk dirun langsung!** Mereka adalah **library/module** yang dipanggil oleh `test_recognizer.py`.

**Analogi:**
- `image_utils.py`, `face_detector.py`, `face_recognizer.py` = Seperti **buku di perpustakaan** (tidak dibaca langsung)
- `test_recognizer.py` = Seperti **siswa yang baca buku** (yang dijalankan)

**Struktur progressive:**
```
minggu-1/project/
  └── image_utils.py                    ← Week 1 module

minggu-2/project/
  ├── image_utils.py                    ← Copy dari week 1
  └── face_detector.py                  ← NEW week 2

minggu-3/project/                        ← KITA DI SINI
  ├── image_utils.py                    ← Copy dari week 1
  ├── face_detector.py                  ← Copy dari week 2
  ├── face_recognizer.py                ← NEW week 3
  └── test_recognizer.py                ← RUN INI! ✅

minggu-4/project/
  ├── image_utils.py                    ← Copy dari week 1
  ├── face_detector.py                  ← Copy dari week 2
  ├── face_recognizer.py                ← Copy dari week 3
  ├── dataset_manager.py                ← NEW week 4
  └── test_dataset.py                   ← RUN yang ini ✅
```

**Benefit:**
- Student bisa mulai dari minggu mana aja tanpa bingung
- Setiap minggu punya dokumentasi lengkap
- Testing lebih mudah (semua file dalam 1 folder)

---

## 🎯 File Descriptions

### Perbedaan `learning/` vs `project/`

| Aspek | learning/ | project/ |
|-------|-----------|----------|
| **Tujuan** | Tutorial & latihan | Production-ready modules |
| **File** | lesson-1, lesson-2 | Python modules (.py) |
| **Gaya code** | Tutorial-style, banyak comment | Clean, reusable functions |
| **Testing** | Manual run & check output | Automated unit tests |
| **Usage** | Belajar konsep step-by-step | Dipakai di minggu selanjutnya |

**Workflow:**
1. **learning/** → Pahami konsep (lesson-1, lesson-2)
2. **project/** → Pakai module production-ready (`face_recognizer.py`)
3. **test_recognizer.py** → Verify module works correctly

---

### face_recognizer.py
**Purpose:** Production-ready face recognition dengan encoding-based matching

**Class: FaceRecognizer**

**Methods:**
1. **__init__()** - Initialize recognizer
2. **encode_face(image)** - Generate 128-d encoding dari image
3. **encode_faces_batch(images)** - Batch encoding multiple images
4. **add_known_face(name, encoding)** - Add person to database
5. **load_known_faces(file_path)** - Load database dari file
6. **save_known_faces(file_path)** - Save database ke file
7. **recognize_face(encoding, tolerance)** - Identify person dari encoding
8. **recognize_faces_image(image, tolerance)** - Recognize all faces in image
9. **get_face_distance(encoding1, encoding2)** - Calculate similarity
10. **clear_database()** - Reset known faces database

**Key Features:**
- ✅ 128-dimension face encoding generation
- ✅ Database management (add, save, load)
- ✅ Multiple recognition strategies
- ✅ Confidence scoring
- ✅ Batch processing support
- ✅ Tolerance tuning interface

**Cara menggunakan:**
```python
from face_recognizer import FaceRecognizer
import cv2

# Initialize
recognizer = FaceRecognizer()

# Add known faces
img1 = cv2.imread('alice.jpg')
encoding1 = recognizer.encode_face(img1)
recognizer.add_known_face('Alice', encoding1)

img2 = cv2.imread('bob.jpg')
encoding2 = recognizer.encode_face(img2)
recognizer.add_known_face('Bob', encoding2)

# Save database
recognizer.save_known_faces('known_faces.pkl')

# Later: Load database
recognizer.load_known_faces('known_faces.pkl')

# Recognize unknown face
unknown_img = cv2.imread('test.jpg')
results = recognizer.recognize_faces_image(unknown_img)

for result in results:
    print(f"Found: {result['name']} ({result['confidence']:.1f}%)")
    location = result['location']  # (top, right, bottom, left)
```

**Design Principles:**
- **Persistence:** Save/load database functionality
- **Scalability:** Handle 100+ known faces efficiently
- **Accuracy:** Configurable tolerance for precision
- **Flexibility:** Multiple recognition modes

---

### test_recognizer.py
**Purpose:** Comprehensive tests untuk face_recognizer.py

**Test Cases:**
1. ✅ test_encode_face - Encoding generation
2. ✅ test_encode_faces_batch - Multiple encodings
3. ✅ test_add_known_face - Database addition
4. ✅ test_recognize_face_match - Correct recognition
5. ✅ test_recognize_face_unknown - Unknown handling
6. ✅ test_face_distance - Similarity calculation
7. ✅ test_save_load_database - Persistence
8. ✅ test_recognize_multiple - Multiple faces
9. ✅ test_tolerance_tuning - Different tolerances
10. ✅ test_confidence_scoring - Score accuracy

**Cara menjalankan:**
```bash
cd minggu-3-face-recognition/project
python test_recognizer.py
```

**Expected output:**
```
test_encode_face ... OK
test_encode_faces_batch ... OK
test_add_known_face ... OK
test_recognize_face_match ... OK
test_recognize_face_unknown ... OK
test_face_distance ... OK
test_save_load_database ... OK
test_recognize_multiple ... OK
test_tolerance_tuning ... OK
test_confidence_scoring ... OK

----------------------------------------------------------------------
Ran 10 tests in 2.456s

OK
```

---

## 📋 Complete API Reference

### FaceRecognizer Class

#### encode_face(image)
Generate face encoding dari single image

**Parameters:**
- image (numpy.ndarray): Input image containing a face

**Returns:**
- numpy.ndarray: 128-d encoding vector
- None: If no face detected

**Example:**
```python
img = cv2.imread('person.jpg')
encoding = recognizer.encode_face(img)
if encoding is not None:
    print(f'Encoding shape: {encoding.shape}')  # (128,)
```

---

#### add_known_face(name, encoding)
Add person to known faces database

**Parameters:**
- name (str): Person's name/ID
- encoding (numpy.ndarray): Face encoding

**Returns:**
- bool: True if added successfully

**Example:**
```python
recognizer.add_known_face('Alice', alice_encoding)
recognizer.add_known_face('Bob', bob_encoding)
```

---

#### save_known_faces(file_path)
Save database to pickle file

**Parameters:**
- file_path (str): Output file path (.pkl)

**Returns:**
- bool: True if saved successfully

**Example:**
```python
recognizer.save_known_faces('database.pkl')
```

---

#### load_known_faces(file_path)
Load database from pickle file

**Parameters:**
- file_path (str): Database file path

**Returns:**
- bool: True if loaded successfully

**Example:**
```python
if recognizer.load_known_faces('database.pkl'):
    print(f'Loaded {len(recognizer.known_names)} people')
```

---

#### recognize_face(encoding, tolerance=0.6)
Identify person from encoding

**Parameters:**
- encoding (numpy.ndarray): Face encoding to identify
- tolerance (float): Match threshold (0.4-0.7)

**Returns:**
- dict: Recognition result
  - name (str): Person name or 'Unknown'
  - confidence (float): Match confidence (0-100)
  - distance (float): Best match distance

**Example:**
```python
result = recognizer.recognize_face(unknown_encoding, tolerance=0.6)
print(f"{result['name']}: {result['confidence']:.1f}%")
```

---

#### recognize_faces_image(image, tolerance=0.6)
Recognize all faces in image

**Parameters:**
- image (numpy.ndarray): Input image
- tolerance (float): Match threshold

**Returns:**
- list: Array of recognition results
  - Each result contains: name, confidence, location, encoding

**Example:**
```python
results = recognizer.recognize_faces_image(group_photo)
for person in results:
    name = person['name']
    conf = person['confidence']
    top, right, bottom, left = person['location']
    print(f'{name} at ({left},{top}) - {conf:.1f}%')
```

---

#### get_face_distance(encoding1, encoding2)
Calculate similarity between two encodings

**Parameters:**
- encoding1, encoding2 (numpy.ndarray): Face encodings

**Returns:**
- float: Distance (0.0 = identical, higher = more different)

**Example:**
```python
distance = recognizer.get_face_distance(enc1, enc2)
if distance < 0.6:
    print('Same person')
else:
    print('Different person')
```

---

## 🔍 Usage Examples

### Example 1: Build Face Database
```python
from face_recognizer import FaceRecognizer
import cv2
import os

recognizer = FaceRecognizer()

# Load known faces from folder
known_faces_dir = 'known_faces/'
for filename in os.listdir(known_faces_dir):
    if filename.endswith('.jpg'):
        # Get name from filename
        name = filename.replace('.jpg', '')
        
        # Load and encode
        img = cv2.imread(os.path.join(known_faces_dir, filename))
        encoding = recognizer.encode_face(img)
        
        if encoding is not None:
            recognizer.add_known_face(name, encoding)
            print(f'Added {name}')

# Save database
recognizer.save_known_faces('faces_db.pkl')
print(f'Database saved with {len(recognizer.known_names)} people')
```

---

### Example 2: Recognize from Webcam
```python
from face_recognizer import FaceRecognizer
import cv2

# Load database
recognizer = FaceRecognizer()
recognizer.load_known_faces('faces_db.pkl')

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Recognize faces
    results = recognizer.recognize_faces_image(frame, tolerance=0.6)
    
    # Draw results
    for person in results:
        top, right, bottom, left = person['location']
        name = person['name']
        conf = person['confidence']
        
        # Draw box
        color = (0, 255, 0) if name != 'Unknown' else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        
        # Draw name and confidence
        label = f"{name} ({conf:.1f}%)"
        cv2.putText(frame, label, (left, top-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    cv2.imshow('Face Recognition', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

### Example 3: Batch Recognition
```python
import cv2
import glob

recognizer = FaceRecognizer()
recognizer.load_known_faces('faces_db.pkl')

# Process all images in folder
test_images = glob.glob('test_photos/*.jpg')

for img_path in test_images:
    print(f'\nProcessing: {img_path}')
    img = cv2.imread(img_path)
    
    results = recognizer.recognize_faces_image(img)
    
    if len(results) == 0:
        print('  No faces detected')
    else:
        for i, person in enumerate(results):
            print(f"  Face {i+1}: {person['name']} "
                  f"({person['confidence']:.1f}%)")
```

---

## 🔍 Testing Checklist

```
[ ] test_encode_face - Encoding works
[ ] test_encode_faces_batch - Batch processing OK
[ ] test_add_known_face - Database addition works
[ ] test_recognize_face_match - Correct matches
[ ] test_recognize_face_unknown - Unknown detection
[ ] test_face_distance - Distance calculation accurate
[ ] test_save_load_database - Persistence works
[ ] test_recognize_multiple - Multiple faces handled
[ ] test_tolerance_tuning - Tolerance effects correct
[ ] test_confidence_scoring - Scores make sense
[ ] All 10 tests PASSED
```

---

## 🐛 Troubleshooting

**No face detected in image:**
- Check image quality and lighting
- Ensure face is frontal and clear
- Try different image
- Verify image loaded correctly (not None)

**Recognition accuracy low:**
- Use high-quality enrollment photos
- Add multiple photos per person (different angles)
- Tune tolerance (try 0.5 for stricter)
- Ensure good lighting in test images

**Wrong person recognized:**
- Lower tolerance (0.4-0.5)
- Check for similar-looking people in database
- Add more distinct photos per person
- Verify database not corrupted

**Slow performance:**
- Resize images before encoding
- Use batch processing for multiple images
- Cache encodings instead of regenerating
- Consider using GPU acceleration (MediaPipe support)

**Database file corrupted:**
```python
# Rebuild database
recognizer.clear_database()
# Re-add all known faces
# Save again
```

---

## 📚 Integration with Main Project

```
ExtraQueensya/
└── core/
    ├── image_utils.py        # Week 1
    ├── face_detector.py      # Week 2
    └── face_recognizer.py    # Week 3 ← NEW
```

**Usage in week 4+:**
```python
from core.face_detector import FaceDetector
from core.face_recognizer import FaceRecognizer

# Detect faces
detector = FaceDetector()
faces = detector.detect_faces(image)

# Recognize faces
recognizer = FaceRecognizer()
recognizer.load_known_faces('db.pkl')
results = recognizer.recognize_faces_image(image)
```

---

## ⏭️ Next Steps

Setelah week 3 complete:

1. ✅ Face recognition working accurately (>85%)
2. ✅ Database management understood
3. ✅ All tests passing
4. ✅ Lanjut ke **Minggu 4: Dataset Collection**
   - Systematic face data collection
   - Quality validation
   - Dataset management tools

---

## 💡 Best Practices Learned

1. **Database Management:** Save/load for persistence
2. **Confidence Scoring:** Always show confidence with results
3. **Tolerance Tuning:** Balance accuracy vs false negatives
4. **Batch Processing:** Efficient for multiple images
5. **Error Handling:** Always check for None returns

---

**Outstanding work on Week 3! 🎉**

*Face recognition is the core AI of the attendance system. You now have all building blocks for weeks 4-8!*
