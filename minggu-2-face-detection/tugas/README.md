# 📝 TUGAS MINGGU 2 - Multi-Face Detector (Fill in the Blanks)

## 📖 Deskripsi
Lengkapi program face detector dengan mengisi 10 soal (bagian kosong)

## 🎯 Objektif
- Implement Haar Cascade face detection
- Handle multiple faces dalam satu image
- Real-time detection dari webcam
- Batch processing & reporting

---

## 📋 SOAL - Isi Bagian yang Kosong!

File template: `face_detector_template.py`

### ✏️ Daftar Soal (Total: 10 Soal)

**SOAL 1** (Baris 13): Load Haar Cascade classifier
```python
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + '_______________________________________'
)
```
💡 Hint: Nama file XML untuk frontal face detection

**SOAL 2** (Baris 25): Convert ke grayscale
```python
gray = cv2.cvtColor(image, _________________)
```
💡 Hint: Constant untuk BGR to GRAY

**SOAL 3** (Baris 30): Detect faces
```python
faces = face_cascade._____________________(gray, _____, _____)
```
💡 Hint: Method untuk detectMultiScale, scaleFactor 1.1, minNeighbors 5

**SOAL 4** (Baris 41): Draw rectangle
```python
cv2.rectangle(image, (x, y), (_____, _____), (0, 255, 0), 2)
```
💡 Hint: Bottom-right corner = (x+w, y+h)

**SOAL 5**: Sudah ada di code (putText)

**SOAL 6** (Baris 58): Load image
```python
img = _________(f'input_images/{filename}')
```
💡 Hint: Fungsi untuk baca image

**SOAL 7** (Baris 74): Save hasil detection
```python
_________(output_path, result)
```
💡 Hint: Fungsi untuk save image

**SOAL 8** (Baris 91): Buka webcam
```python
cap = _________(0)
```
💡 Hint: Class untuk video capture

**SOAL 9** (Baris 114): Detect tombol 's' untuk screenshot
```python
if key == ord('_'):
```
💡 Hint: Karakter untuk save screenshot

**SOAL 10** (Baris 174): Open file untuk write
```python
with _______('output/report.txt', '_') as f:
```
💡 Hint: Fungsi built-in untuk file I/O, mode 'w' untuk write

---

---

## 📦 Struktur File

```
tugas/
├── face_detector_template.py    # Template dengan blanks (JANGAN EDIT)
├── face_detector.py              # ISI JAWABAN KAMU DI SINI
├── input_images/                 # Taruh test images (min 5)
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── ...
├── output/                       # Hasil detection
└── README.md
```

---

## 🚀 Cara Mengerjakan

### Step 1: Copy Template
```bash
cd minggu-2-face-detection/tugas
copy face_detector_template.py face_detector.py
```

### Step 2: Isi 10 Soal
Buka `face_detector.py` dan isi semua blanks

### Step 3: Test Program
```bash
python face_detector.py
```

### Step 4: Test Semua Mode
- Mode 1: Test dengan single image
- Mode 2: Test webcam real-time
- Mode 3: Test batch processing

---

## 💡 Cheat Sheet

| Fungsi/Constant | Kegunaan |
|-----------------|----------|
| `haarcascade_frontalface_default.xml` | Cascade classifier file |
| `cv2.COLOR_BGR2GRAY` | Convert BGR to grayscale |
| `detectMultiScale(gray, 1.1, 5)` | Detect faces |
| `cv2.imread()` | Load image |
| `cv2.imwrite()` | Save image |
| `cv2.VideoCapture(0)` | Buka webcam |
| `ord('s')` | ASCII code untuk karakter 's' |
| `open(file, 'w')` | Buka file untuk write |

---

## ✅ Checklist Pengerjaan

```
[ ] SOAL 1: haarcascade_frontalface_default.xml
[ ] SOAL 2: cv2.COLOR_BGR2GRAY
[ ] SOAL 3: detectMultiScale, 1.1, 5
[ ] SOAL 4: x+w, y+h
[ ] SOAL 6: cv2.imread
[ ] SOAL 7: cv2.imwrite
[ ] SOAL 8: cv2.VideoCapture
[ ] SOAL 9: 's'
[ ] SOAL 10: open, 'w'
[ ] Mode 1 (Image) working
[ ] Mode 2 (Webcam) working
[ ] Mode 3 (Batch) working
[ ] Report generated correctly
```

---

## ✅ Kriteria Penilaian

| No | Soal | Poin |
|----|------|------|
| 1 | Haar Cascade path | 10 pts |
| 2 | COLOR_BGR2GRAY | 10 pts |
| 3 | detectMultiScale (3 params) | 15 pts |
| 4 | Rectangle coords | 10 pts |
| 6 | cv2.imread | 10 pts |
| 7 | cv2.imwrite | 10 pts |
| 8 | VideoCapture | 10 pts |
| 9 | ord('s') | 10 pts |
| 10 | open + mode | 10 pts |
| **Fungsionalitas** | Semua mode working | +15 pts |
| **TOTAL** | | **110 pts** |

---

## 🎓 Learning Outcomes

- ✅ Face detection dengan Haar Cascade
- ✅ Multi-face handling
- ✅ Real-time webcam processing
- ✅ Batch processing workflow
- ✅ Report generation

---

## 📚 Resources

- Minggu 2 Lesson 1 & 2 (`learning/lesson-1/main.py`, `learning/lesson-2/main.py`)
- [Haar Cascade Documentation](https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html)

**Good luck! 👤🔍**
