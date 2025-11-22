# Lesson 1: Face Recognition dari Static Image

## Tujuan
1️⃣ Load face database dari `known_faces/` folder  
2️⃣ Extract 1404-d face encodings menggunakan MediaPipe FaceMesh  
3️⃣ Recognize faces dalam test image menggunakan cosine similarity  
4️⃣ Visualize hasil dengan bounding boxes dan confidence scores  

## Konsep Face Encoding

**Face Encoding** = Vector 1404 angka yang represent wajah seseorang
- **468 landmarks** (mata, hidung, mulut, etc.) × **3 coordinates** (x, y, z)
- Setiap wajah punya encoding 3D yang unik
- Compare 2 encodings menggunakan **cosine similarity**
- Distance < 0.5 → wajah sama (high confidence)
- Distance > 0.6 → wajah beda (low confidence)

## Setup Known Faces Database

Buat struktur folder `known_faces/` seperti ini:
```
known_faces/
├── alice/
│   ├── alice1.jpg
│   └── alice2.jpg
└── bob/
    ├── bob1.jpg
    └── bob2.jpg
```

**Persyaratan:**
- Folder per person (nama folder = person name)
- Minimal 2-3 foto per person
- Foto berkualitas (face jelas terlihat)
- Format: JPG, PNG, atau JPEG

## Yang Dipelajari

### 1. Initialize Face Recognizer
```python
from face_recognizer import FaceRecognizer

# Buat recognizer dengan tolerance 0.5 (0.3-0.7 range)
recognizer = FaceRecognizer(tolerance=0.5)
```

### 2. Load Known Faces
```python
for person_name in os.listdir('known_faces'):
    for filename in os.listdir(f'known_faces/{person_name}'):
        img = cv2.imread(f'known_faces/{person_name}/{filename}')
        encoding = recognizer.encode_face(img)  # 1404-d vector
        recognizer.add_known_face(encoding, person_name)
```

### 3. Recognize Face dari Test Image
```python
test_img = cv2.imread('images/test.jpg')
results = recognizer.recognize_faces_in_image(test_img)

for result in results:
    name = result['name']              # Name or "Unknown"
    confidence = result['confidence']  # 0-1 (1 = 100% match)
    x, y, w, h = result['bbox']        # Bounding box
```

## Langkah Praktik

**Setup:**
1. Buat folder `known_faces/alice/` dan `known_faces/bob/`
2. Copy 2-3 foto masing-masing ke folder
3. Buat folder `images/` dan copy test image ke `test.jpg`

**Run Program:**
```bash
python main.py
```

**Expected Output:**
```
1️⃣  Initializing MediaPipe Face Recognizer...
   ✅ FaceRecognizer ready (tolerance: 0.5)
   📊 Using 1404-dimensional FaceMesh landmarks as encoding

2️⃣  Loading known faces...
   ✅ alice: 2 face(s) loaded
   ✅ bob: 2 face(s) loaded
   📊 Total: 4 face(s) dari 2 person(s)

3️⃣  Testing recognition...
   🔍 Found 2 face(s) in test image
   Face #1: alice (confidence: 92.5%) ✅ MATCHED
   Face #2: bob (confidence: 88.0%) ✅ MATCHED
```

**Output:**
- Visual result di `output/recognized.jpg` (bounding boxes + names)
- Statistics di console

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `known_faces` folder tidak ada | Buat folder sesuai struktur di atas |
| No face detected | Pastikan foto jelas, wajah frontal, cahaya cukup |
| Low confidence score | Coba tambah tolerance ke 0.6, atau gunakan foto lebih baik |
| Unknown faces terus | Pastikan sudah load known_faces dengan benar |

## Challenge

✨ Coba upgrade program:
1. **Multiple test images** - Process `images/` folder
2. **Show statistics** - Hitung matched vs unknown
3. **Batch recognition** - Process 10+ faces sekaligus
4. **Save database** - Persist encoding ke pickle file

## Key Takeaways

✅ MediaPipe FaceMesh menghasilkan 1404-d encoding (10x lebih detail)  
✅ Cosine similarity lebih akurat untuk normalized vectors  
✅ Tolerance 0.5 = balanced (0.3 strict, 0.7 loose)  
✅ Unknown faces = distance > tolerance  

## Next: Lesson 2 - Real-time Recognition dari Webcam
