# 📝 TUGAS MINGGU 4 - Dataset Collection

## Deskripsi
Buat sistem untuk mengumpulkan dan mengelola dataset wajah dengan quality control otomatis.

---

## 🎯 Objektif
- Face capture dengan validasi kualitas
- Dataset organization
- Quality metrics
- Data augmentation
- Backup & restore

---

## 📋 Tugas: Smart Dataset Manager

Buat program `dataset_manager.py` dengan fitur:

### Fitur Wajib
1. **Smart Capture**
   - Auto-detect face position
   - Quality validation:
     - ✅ Brightness check (tidak terlalu gelap/terang)
     - ✅ Blur detection
     - ✅ Face size validation
     - ✅ Face angle check
   - Visual feedback (box hijau=good, merah=bad)
   - Auto-capture saat quality ok
   - Capture 20 photos per person

2. **Quality Control**
   - Real-time quality score (0-100)
   - Reject low quality images
   - Save to `rejected/` folder
   - Quality report per session

3. **Dataset Organization**
   - Structure: `dataset/{person_name}/*.jpg`
   - Auto-rename files (person_001.jpg, ...)
   - Metadata file (JSON/CSV)
   - Face count per person

4. **Management Features**
   - List all persons
   - View person's photos
   - Delete person
   - Reorganize dataset
   - Create backup (ZIP)

---

## 📦 Deliverables

```
tugas/
├── dataset_manager.py      # Main program
├── dataset/                # Collected faces
│   ├── person1/
│   │   ├── person1_001.jpg
│   │   ├── person1_002.jpg
│   │   └── ...
│   ├── person2/
│   └── metadata.json
├── rejected/               # Low quality images
├── backups/                # ZIP backups
│   └── dataset_20251118.zip
└── README.md
```

---

## 🎯 Example Output

### Console:
```
========================================
   SMART DATASET MANAGER
========================================

Main Menu:
1. Capture New Person
2. View Dataset
3. Delete Person
4. Create Backup
5. Quality Report
6. Exit

Pilih: 1

Enter person name: Andi

Starting smart capture...
Target: 20 photos

Status:
[████████░░░░░░░░░░] 8/20
Quality Score: 87/100 ✅
✅ Brightness: OK
✅ Blur: OK
✅ Size: OK
⚠️  Angle: Slightly off

Press SPACE to force capture, Q to quit
Auto-capturing in 3... 2... 1... ✓

Capture complete!
Accepted: 18 photos
Rejected: 5 photos (too dark: 3, blurry: 2)

Dataset updated: dataset/andi/
```

### metadata.json:
```json
{
  "persons": [
    {
      "name": "Andi",
      "photo_count": 18,
      "created": "2025-11-18 10:30:00",
      "quality_avg": 85.3,
      "rejected": 5
    }
  ],
  "total_persons": 1,
  "total_photos": 18
}
```

---

## 💡 Hints & Tips

### Brightness Check
```python
import cv2
import numpy as np

gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
brightness = np.mean(gray)

if 40 < brightness < 200:
    brightness_ok = True
```

### Blur Detection
```python
# Laplacian variance method
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

if laplacian_var > 100:  # Not blurry
    blur_ok = True
```

### Face Size Check
```python
face_area = w * h
frame_area = frame.shape[0] * frame.shape[1]

face_ratio = face_area / frame_area

if 0.05 < face_ratio < 0.4:  # 5-40% of frame
    size_ok = True
```

### Quality Score
```python
def calculate_quality(face, brightness, blur_score, size_ratio):
    score = 0
    
    # Brightness (30 points)
    if 40 < brightness < 200:
        score += 30
    
    # Blur (40 points)
    if blur_score > 100:
        score += 40
    elif blur_score > 50:
        score += 20
    
    # Size (30 points)
    if 0.1 < size_ratio < 0.3:
        score += 30
    elif 0.05 < size_ratio < 0.4:
        score += 15
    
    return score
```

### Auto-capture
```python
if quality_score >= 80 and auto_mode:
    # Wait countdown
    for i in range(3, 0, -1):
        cv2.putText(frame, str(i), ...)
        cv2.imshow('Capture', frame)
        cv2.waitKey(1000)
    
    # Capture
    filename = f'dataset/{name}/{name}_{count:03d}.jpg'
    cv2.imwrite(filename, face)
    count += 1
```

### Create Backup
```python
import zipfile
from datetime import datetime

backup_name = f"backups/dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"

with zipfile.ZipFile(backup_name, 'w') as zipf:
    for folder, subfolders, files in os.walk('dataset/'):
        for file in files:
            filepath = os.path.join(folder, file)
            zipf.write(filepath)
```

---

## ✅ Kriteria Penilaian

| Kriteria | Bobot | Poin |
|----------|-------|------|
| Smart capture dengan quality check | 30% | 30 |
| Quality validation (4 checks) | 20% | 20 |
| Dataset organization | 15% | 15 |
| Management features | 20% | 20 |
| Backup/restore | 10% | 10 |
| Documentation | 5% | 5 |

**Total: 100 points**

---

## 🌟 Fitur Bonus

- [ ] Face alignment (rotate to center)
- [ ] Data augmentation (flip, rotate)
- [ ] Duplicate detection
- [ ] Face cropping (consistent size)
- [ ] Progress visualization
- [ ] Export statistics to PDF
- [ ] Restore from backup
- [ ] Multi-person batch capture

**+5-10 pts per fitur**

---

## ⏰ Deadline

**4 hari** setelah menyelesaikan Minggu 4

---

## 🎓 Learning Outcomes

- ✅ Quality validation techniques
- ✅ Dataset organization
- ✅ Metadata management
- ✅ File operations & backup
- ✅ User experience design

---

## 📚 Resources

- Minggu 4 Lesson 1 & 2
- OpenCV image quality metrics
- Dataset best practices

**Good luck! 📸✨**
