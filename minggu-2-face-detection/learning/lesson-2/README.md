# Lesson 2: Face Detection Real-Time dari Webcam

## Tujuan Pembelajaran

Di lesson ini kamu akan belajar:
1. Akses webcam untuk video stream
2. Face detection real-time (setiap frame)
3. Optimize performance untuk video
4. Handle multiple faces
5. Display FPS (Frames Per Second)
6. Capture dan save detected faces

## Perbedaan Image vs Video Detection

| Aspek | Image (Lesson 1) | Video/Webcam (Lesson 2) |
|-------|------------------|-------------------------|
| Input | 1 gambar | Stream frames continuous |
| Speed | Gak penting | Harus cepat (30+ FPS) |
| Processing | Full quality | Bisa resize untuk speed |
| Output | 1 file | Real-time display |

## Konsep Video Processing

### 1. Camera Detection & Selection
```python
# Detect available cameras
available_cameras = detect_available_cameras()
for cam in available_cameras:
    print(f"Camera {cam['id']}: {cam['name']}")
    print(f"  Resolution: {cam['resolution']}")
    print(f"  FPS: {cam['fps']}")

# User select camera
camera_id = select_camera(available_cameras)

# Open selected camera
cap = cv2.VideoCapture(camera_id)
```

### 2. Read Frame Loop
```python
while True:
    ret, frame = cap.read()  # Baca 1 frame
    if not ret:
        break
    
    # Process frame...
    
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
```

### 3. Frame Rate
- Webcam biasanya 30 FPS (30 frames per second)
- Detection harus < 33ms per frame untuk maintain 30 FPS
- Kalau lambat → video lag/choppy

## Optimization Techniques

### 1. Resize Frame
```python
# Resize ke 640x480 untuk speed
small = cv2.resize(frame, (640, 480))
faces = face_cascade.detectMultiScale(small, ...)
```

### 2. Skip Frames
```python
frame_count = 0
if frame_count % 3 == 0:  # Detect setiap 3 frame
    faces = face_cascade.detectMultiScale(...)
frame_count += 1
```

### 3. Adjust Parameters
```python
# Faster parameters (less accurate)
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.3,    # Lebih besar = lebih cepat
    minNeighbors=3,     # Lebih kecil = lebih cepat
    minSize=(50, 50)    # Lebih besar = lebih cepat
)
```

## Display FPS (Frames Per Second)

```python
import time

fps = 0
prev_time = time.time()

while True:
    ret, frame = cap.read()
    
    # Calculate FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    
    # Display FPS
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), ...)
```

## Struktur Code

```python
# 1. Setup
import cv2
import time
import os

# 2. Load Haar Cascade
face_cascade = cv2.CascadeClassifier(...)

# 3. Open webcam
cap = cv2.VideoCapture(0)

# 4. Setup FPS counter
prev_time = time.time()

# 5. Main loop
while True:
    # Read frame
    ret, frame = cap.read()
    
    # Detect faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, ...)
    
    # Draw rectangles
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Calculate & display FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(frame, f'FPS: {int(fps)}', ...)
    
    # Show frame
    cv2.imshow('Face Detection', frame)
    
    # Exit on ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 6. Cleanup
cap.release()
cv2.destroyAllWindows()
```

## Langkah-Langkah Praktik

### Step 1: Check Webcam
Pastikan webcam kamu nyala dan gak dipake aplikasi lain (Zoom, Skype, etc).

### Step 2: Jalankan Code
```bash
cd minggu-2-face-detection/learning/lesson-2
python main.py
```

### Step 3: Lihat Hasil
- Window webcam akan muncul
- Rectangle hijau akan muncul di wajah kamu
- FPS counter di pojok kiri atas
- Face count di pojok kanan atas

### Step 4: Test Features

**Keyboard Controls:**
- `ESC` - Exit program
- `SPACE` - Capture dan save snapshot
- `C` - Toggle face count display
- `F` - Toggle FPS display

### Step 5: Check Performance

**Good Performance:**
- FPS: 25-30 (smooth video)
- Detection responsive

**Poor Performance (FPS < 15):**
- Coba resize frame lebih kecil
- Skip frames (detect setiap 3 frame)
- Increase `scaleFactor` ke 1.3
- Increase `minSize` ke (60, 60)

## Fitur Tambahan

### 1. Save Snapshot
```python
if key == 32:  # SPACE key
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    filename = f'snapshot_{timestamp}.jpg'
    cv2.imwrite(os.path.join(output_dir, filename), frame)
    print(f"Snapshot saved: {filename}")
```

### 2. Display Face Count
```python
face_count = len(faces)
cv2.putText(
    frame,
    f'Faces: {face_count}',
    (frame.shape[1] - 150, 30),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (0, 255, 0),
    2
)
```

### 3. Color Detection Box
```python
# Hijau untuk 1 wajah, kuning untuk banyak
color = (0, 255, 0) if len(faces) == 1 else (0, 255, 255)
for (x, y, w, h) in faces:
    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
```

## Output yang Diharapkan

Console output:
```
Webcam opened successfully
Resolution: 640x480
FPS: 28.5
Faces detected: 1

Press:
  ESC - Exit
  SPACE - Save snapshot
  C - Toggle face count
  F - Toggle FPS
```

Window akan show:
- Live webcam feed
- Green rectangles di wajah
- FPS counter
- Face count

## Troubleshooting

### ❌ Error: "Cannot open webcam"
**Solusi:**
- Pastikan webcam terhubung
- Close aplikasi lain yang pakai webcam
- Try different camera index: `cv2.VideoCapture(1)` atau `(2)`
- Windows: Check Camera Privacy Settings

### ❌ FPS sangat rendah (< 10)
**Solusi:**
```python
# Option 1: Resize frame
frame = cv2.resize(frame, (320, 240))

# Option 2: Skip frames
if frame_count % 3 == 0:
    faces = face_cascade.detectMultiScale(...)

# Option 3: Adjust parameters
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.3,
    minNeighbors=3,
    minSize=(60, 60)
)
```

### ❌ Detection tidak akurat (banyak false positive)
**Solusi:**
- Increase `minNeighbors` jadi 5-7
- Increase `minSize` jadi (50, 50)
- Pastikan lighting bagus

### ❌ Window freeze/lag
**Solusi:**
- Pastikan ada `cv2.waitKey(1)` di loop
- Jangan process yang berat di dalam loop
- Reduce resolution

## Challenge

Setelah berhasil, coba:
1. Tambahkan counter berapa kali wajah terdeteksi
2. Record video dengan detected faces
3. Detect mata juga (haarcascade_eye.xml)
4. Save foto setiap 5 detik otomatis
5. Tampilkan "Smile!" kalau terdeteksi 1 wajah

## Perbandingan Lesson 1 vs Lesson 2

| Feature | Lesson 1 (Image) | Lesson 2 (Webcam) |
|---------|------------------|-------------------|
| Input | Static image | Live video stream |
| Speed | Slow OK | Must be fast (30 FPS) |
| Output | 1 saved image | Real-time display |
| Complexity | Simple | Medium |
| Use Case | Batch processing | Live monitoring |

## Next Steps

Setelah menguasai Lesson 1 & 2, kamu siap untuk:
- **Minggu 3:** Face Recognition (recognize siapa orangnya)
- **Minggu 4:** Dataset Collection (collect training data)
- **Minggu 5:** Build complete recognition system

---

**Happy Learning! 🚀**

**Tips:** Lighting yang bagus = detection lebih akurat!
