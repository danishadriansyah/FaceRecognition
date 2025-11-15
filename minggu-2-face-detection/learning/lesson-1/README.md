# Lesson 1: Face Detection dengan Haar Cascade (Gambar)

## Tujuan Pembelajaran

Di lesson ini kamu akan belajar:
1. Apa itu Haar Cascade dan cara kerjanya
2. Load Haar Cascade classifier dari OpenCV
3. Detect wajah dari gambar
4. Gambar rectangle di wajah yang terdeteksi
5. Save hasil detection

## Konsep: Haar Cascade

**Haar Cascade** adalah algoritma machine learning untuk deteksi objek (dalam hal ini wajah). Cara kerjanya:

1. **Training:** OpenCV sudah train model dengan ribuan gambar wajah dan non-wajah
2. **Cascade:** Menggunakan banyak "classifier" bertingkat untuk cek apakah ada wajah
3. **Haar Features:** Mendeteksi pola gelap-terang di area gambar (mata, hidung, mulut)

**File Haar Cascade yang dipakai:**
- `haarcascade_frontalface_default.xml` - Deteksi wajah dari depan

## Yang Akan Kamu Pelajari

### 1. Load Haar Cascade
```python
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
```

### 2. Detect Faces
```python
faces = face_cascade.detectMultiScale(
    gray,           # Gambar grayscale
    scaleFactor=1.1,    # Seberapa banyak resize
    minNeighbors=5,     # Seberapa strict detection
    minSize=(30, 30)    # Ukuran minimal wajah
)
```

### 3. Draw Rectangle
```python
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

## Parameter Penting

### `scaleFactor`
- Nilai: 1.01 - 1.5
- Default: 1.1
- Semakin kecil = lebih akurat tapi lebih lambat
- Semakin besar = lebih cepat tapi bisa miss detection

### `minNeighbors`
- Nilai: 3 - 10
- Default: 5
- Semakin kecil = detect lebih banyak (tapi banyak false positive)
- Semakin besar = lebih strict (bisa miss wajah kecil)

### `minSize`
- Format: (width, height)
- Default: (30, 30)
- Ignore wajah yang lebih kecil dari ukuran ini

## Struktur Code

```python
# 1. Import libraries
import cv2
import os

# 2. Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, 'images')
output_dir = os.path.join(script_dir, 'output')
os.makedirs(output_dir, exist_ok=True)

# 3. Load Haar Cascade
face_cascade = cv2.CascadeClassifier(...)

# 4. Load image
img = cv2.imread(os.path.join(images_dir, 'sample.jpg'))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 5. Detect faces
faces = face_cascade.detectMultiScale(gray, ...)

# 6. Draw rectangles
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
# 7. Save & show result
cv2.imwrite(os.path.join(output_dir, 'detected.jpg'), img)
cv2.imshow('Detected Faces', img)
cv2.waitKey(0)
```

## Langkah-Langkah Praktik

### Step 1: Siapkan Test Image
1. Cari foto yang ada wajahnya (bisa foto kamu sendiri)
2. Rename jadi `sample.jpg`
3. Taruh di folder `lesson-1/images/`

### Step 2: Jalankan Code
```bash
cd minggu-2-face-detection/learning/lesson-1
python main.py
```

### Step 3: Lihat Hasil
- Window akan muncul dengan rectangle hijau di wajah
- Tekan sembarang key untuk close window
- Check file `output/detected.jpg`

### Step 4: Eksperimen
Coba ubah parameter ini di `main.py`:

**Experiment 1: Ubah scaleFactor**
```python
# Lebih cepat tapi kurang akurat
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, ...)

# Lebih lambat tapi lebih akurat
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, ...)
```

**Experiment 2: Ubah minNeighbors**
```python
# Detect lebih banyak (lebih liberal)
faces = face_cascade.detectMultiScale(gray, minNeighbors=3, ...)

# Detect lebih strict
faces = face_cascade.detectMultiScale(gray, minNeighbors=8, ...)
```

**Experiment 3: Ubah minSize**
```python
# Detect wajah kecil juga
faces = face_cascade.detectMultiScale(gray, minSize=(20, 20), ...)

# Hanya detect wajah besar
faces = face_cascade.detectMultiScale(gray, minSize=(100, 100), ...)
```

## Output yang Diharapkan

Kalau berhasil, kamu akan lihat:
```
Found 1 face(s)
Face 1: Position (120, 85), Size 150x150
✅ Result saved to: lesson-1/output/detected.jpg
```

Dan gambar output akan ada rectangle hijau di wajah.

## Troubleshooting

### ❌ Error: "Image not found"
**Solusi:** 
- Pastikan ada file `sample.jpg` di folder `images/`
- Check path nya benar

### ❌ Detected 0 faces
**Solusi:**
- Pastikan gambar ada wajah yang jelas (frontal)
- Coba kurangi `minNeighbors` jadi 3
- Coba kurangi `minSize` jadi (20, 20)
- Pastikan lighting gambar bagus (tidak terlalu gelap)

### ❌ Detected too many faces (false positives)
**Solusi:**
- Tambahkan `minNeighbors` jadi 7-8
- Tambahkan `minSize` jadi (50, 50)

### ❌ Window tidak muncul
**Solusi:**
- Gunakan `cv2.waitKey(0)` setelah `imshow()`
- Kalau masih gak muncul, comment `imshow()` dan cukup save aja

## Challenge

Setelah berhasil, coba:
1. Detect wajah di foto group (banyak orang)
2. Hitung berapa jumlah wajah yang terdeteksi
3. Tampilkan info di gambar pakai `cv2.putText()`
4. Save hasil dengan nama yang ada timestamp

## Next Lesson

Di **Lesson 2** kamu akan belajar:
- Face detection dari **webcam** (real-time)
- Optimize performance untuk video stream
- Handle multiple faces
- Add FPS counter

---

**Happy Learning! 🚀**
