# 📝 TUGAS MINGGU 2 - Face Detection

## Deskripsi
Buat aplikasi face detection yang bisa mendeteksi wajah dari gambar dan webcam, dengan statistik dan reporting.

---

## 🎯 Objektif
- Implement face detection dengan Haar Cascade
- Handle multiple faces
- Optimization techniques
- Generate detection reports

---

## 📋 Tugas: Multi-Face Detector

Buat program `face_detector_app.py` dengan fitur:

### Fitur Wajib
1. **Image Mode**
   - Upload gambar
   - Detect semua wajah
   - Draw rectangles dengan confidence
   - Show jumlah wajah terdeteksi

2. **Webcam Mode**
   - Real-time detection
   - FPS counter
   - Face count display
   - Save screenshot (tekan 's')

3. **Batch Mode**
   - Process multiple images dari folder
   - Generate report: berapa wajah per gambar
   - Save all results

4. **Statistics**
   - Total images processed
   - Total faces detected
   - Average faces per image
   - Processing time

---

## 📦 Deliverables

```
tugas/
├── face_detector_app.py    # Main program
├── input_images/           # Test images (min 5 gambar)
├── output/                 # Detection results
│   ├── detected_*.jpg     # Images with rectangles
│   └── report.txt         # Statistics report
└── README.md              # Documentation
```

---

## 🎯 Example Output

### Console:
```
========================================
   MULTI-FACE DETECTOR
========================================

Mode:
1. Image Mode (single)
2. Webcam Mode (real-time)
3. Batch Mode (multiple)
4. Exit

Pilih: 3

Processing batch...
✅ image1.jpg - 3 faces detected (0.12s)
✅ image2.jpg - 1 face detected (0.08s)
✅ image3.jpg - 5 faces detected (0.15s)

Report saved to: output/report.txt
```

### report.txt:
```
FACE DETECTION REPORT
=====================
Date: 2025-11-18
Mode: Batch Processing

Results:
--------
image1.jpg: 3 faces
image2.jpg: 1 face
image3.jpg: 5 faces

Statistics:
-----------
Total images: 3
Total faces: 9
Average: 3.0 faces/image
Total time: 0.35s
```

---

## 💡 Hints & Tips

### Face Detection
```python
import cv2

cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = cascade.detectMultiScale(gray, 1.1, 5)

print(f"Found {len(faces)} faces")
```

### Draw with Count
```python
for i, (x, y, w, h) in enumerate(faces, 1):
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(img, f'Face {i}', (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
```

### Batch Processing
```python
import os
from datetime import datetime

results = []

for filename in os.listdir('input_images/'):
    img = cv2.imread(f'input_images/{filename}')
    # Detect faces
    # Save results
    results.append({
        'filename': filename,
        'faces': len(faces),
        'time': processing_time
    })
```

---

## ✅ Kriteria Penilaian

| Kriteria | Bobot | Poin |
|----------|-------|------|
| Image mode working | 20% | 20 |
| Webcam mode working | 20% | 20 |
| Batch mode working | 20% | 20 |
| Statistics & report | 20% | 20 |
| Code quality | 10% | 10 |
| Documentation | 10% | 10 |

**Total: 100 points**

---

## 🌟 Fitur Bonus

- [ ] Eye detection (Haar Cascade eyes)
- [ ] Save video recording
- [ ] Confidence score per face
- [ ] Filter: minimum face size
- [ ] Export report to CSV
- [ ] GUI dengan Tkinter
- [ ] Face blur untuk privacy

**+10 pts per fitur bonus**

---

## ⏰ Deadline

**3 hari** setelah menyelesaikan Minggu 2

---

## 🎓 Learning Outcomes

- ✅ Face detection implementation
- ✅ Multi-face handling
- ✅ Batch processing
- ✅ Performance metrics
- ✅ Report generation

---

## 📚 Resources

- Minggu 2 Lesson 1 & 2
- `haarcascade_frontalface_default.xml`
- OpenCV Cascade Classifier docs

**Good luck! 👤🔍**
