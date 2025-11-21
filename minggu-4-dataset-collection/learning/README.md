# Minggu 4 - Learning: Dataset Collection & Management

## 📚 Overview
Folder ini berisi 3 tutorial files untuk belajar systematic face data collection, quality validation, dan dataset management. Ini adalah fase krusial untuk build reliable face recognition system.

## 📁 File Structure

```
learning/
├── README.md (file ini)
├── 01_capture_faces.py
├── 02_quality_control.py
└── 03_dataset_management.py
```

---

## 🎯 Tutorial Files - Detailed Guide

### 01_capture_faces.py
**Tujuan:** Systematic face capture dari webcam dengan quality checks

**Apa yang dipelajari:**
- Capture multiple photos per person (20-30 photos)
- Guide user untuk different angles (frontal, left, right)
- Real-time quality feedback (lighting, blur, size)
- Auto-save dengan organized naming
- Progress tracking

**Cara menggunakan:**
```bash
cd minggu-4-dataset-collection/learning
python 01_capture_faces.py
```

**Output yang diharapkan:**
- Webcam window dengan capture guide
- Instructions untuk angle changes
- Quality indicator (good/bad)
- Auto-save to person_name/photo_001.jpg
- Progress: "15/30 photos captured"

**Capture workflow:**
1. Enter person name
2. Position face (frontal)
3. Capture 10 frontal photos
4. Turn head left, capture 5
5. Turn head right, capture 5
6. Various expressions, capture 10
7. Review captured photos

**Quality checks implemented:**
- Face size minimum 100x100 pixels
- Brightness level check (not too dark)
- Blur detection (sharpness threshold)
- Face centered in frame
- Only one face detected

**Code concept:**
```python
import cv2
from face_detector import FaceDetector

detector = FaceDetector()
cap = cv2.VideoCapture(0)
person_name = input("Enter person name: ")
photo_count = 0
target_count = 30

while photo_count < target_count:
    ret, frame = cap.read()
    faces = detector.detect_faces(frame)
    
    # Quality checks
    if len(faces) == 1:  # Single face only
        x, y, w, h = faces[0]
        
        # Size check
        if w >= 100 and h >= 100:
            # Blur check
            face_roi = frame[y:y+h, x:x+w]
            blur_score = cv2.Laplacian(face_roi, cv2.CV_64F).var()
            
            if blur_score > 100:  # Not too blurry
                # Auto capture every 10 frames
                if frame_count % 10 == 0:
                    filename = f'{person_name}/photo_{photo_count:03d}.jpg'
                    cv2.imwrite(filename, frame)
                    photo_count += 1
```

**Tips:**
- Good lighting is critical
- Vary expressions (smile, neutral, serious)
- Different angles help recognition
- Capture over 2-3 sessions for variety

---

### 02_quality_control.py
**Tujuan:** Validate dan filter captured dataset

**Apa yang dipelajari:**
- Image quality metrics (blur, brightness, contrast)
- Face detection validation
- Duplicate detection
- Auto-filtering low-quality images
- Quality report generation

**Cara menggunakan:**
```bash
python 02_quality_control.py
```

**Output yang diharapkan:**
- Quality scan of dataset folder
- Report: X good, Y rejected
- Move bad photos to rejected/
- Summary statistics
- Recommendations for re-capture

**Quality metrics:**

**1. Blur Detection:**
```python
def is_blurry(image, threshold=100):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    return variance < threshold
```

**2. Brightness Check:**
```python
def check_brightness(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mean_brightness = np.mean(hsv[:,:,2])
    # Good range: 50-200
    return 50 <= mean_brightness <= 200
```

**3. Face Detection:**
```python
def has_single_face(image):
    faces = detector.detect_faces(image)
    return len(faces) == 1
```

**4. Face Size:**
```python
def is_face_large_enough(face, min_size=100):
    x, y, w, h = face
    return w >= min_size and h >= min_size
```

**Validation process:**
```python
import os
import shutil

good_count = 0
rejected_count = 0

for filename in os.listdir('person_name/'):
    img = cv2.imread(f'person_name/{filename}')
    
    # Run all checks
    if (not is_blurry(img) and 
        check_brightness(img) and
        has_single_face(img)):
        good_count += 1
    else:
        # Move to rejected folder
        shutil.move(f'person_name/{filename}', 
                   f'rejected/{filename}')
        rejected_count += 1

print(f'Good: {good_count}, Rejected: {rejected_count}')
```

**Quality report output:**
```
=== Quality Report ===
Total images: 30
Passed: 24 (80%)
Failed: 6 (20%)

Failure reasons:
- Blurry: 3
- Too dark: 2
- Multiple faces: 1

Recommendation: Recapture 6 more photos
```

---

### 03_dataset_management.py
**Tujuan:** Organize, backup, dan manage complete dataset

**Apa yang dipelajari:**
- Dataset folder structure best practices
- Metadata generation (person info, capture date)
- Backup dan versioning
- Dataset splitting (train/validation)
- Export untuk different purposes

**Cara menggunakan:**
```bash
python 03_dataset_management.py
```

**Output yang diharapkan:**
- Organized dataset structure
- metadata.json per person
- Backup created
- Train/val split
- Dataset statistics

**Recommended folder structure:**
```
dataset/
├── person_001_alice/
│   ├── metadata.json
│   ├── frontal_01.jpg
│   ├── frontal_02.jpg
│   ├── left_01.jpg
│   ├── right_01.jpg
│   └── encodings.pkl
├── person_002_bob/
│   ├── metadata.json
│   ├── frontal_01.jpg
│   └── ...
└── dataset_info.json
```

**Metadata structure:**
```json
{
  "person_id": "001",
  "name": "Alice",
  "department": "Engineering",
  "photo_count": 24,
  "capture_date": "2025-11-14",
  "encoding_generated": true,
  "quality_score": 0.92
}
```

**Dataset management functions:**

**1. Add Person:**
```python
def add_person(name, employee_id, department):
    person_folder = f'dataset/person_{employee_id}_{name}/'
    os.makedirs(person_folder, exist_ok=True)
    
    metadata = {
        'person_id': employee_id,
        'name': name,
        'department': department,
        'photo_count': 0,
        'capture_date': datetime.now().isoformat()
    }
    
    with open(f'{person_folder}/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
```

**2. Generate Encodings:**
```python
def generate_encodings_for_person(person_folder):
    recognizer = FaceRecognizer()
    encodings = []
    
    for img_file in os.listdir(person_folder):
        if img_file.endswith('.jpg'):
            img = cv2.imread(f'{person_folder}/{img_file}')
            encoding = recognizer.encode_face(img)
            if encoding is not None:
                encodings.append(encoding)
    
    # Save encodings
    with open(f'{person_folder}/encodings.pkl', 'wb') as f:
        pickle.dump(encodings, f)
    
    return len(encodings)
```

**3. Dataset Statistics:**
```python
def get_dataset_stats(dataset_path):
    total_people = 0
    total_photos = 0
    
    for person_folder in os.listdir(dataset_path):
        if os.path.isdir(f'{dataset_path}/{person_folder}'):
            total_people += 1
            photos = len([f for f in os.listdir(f'{dataset_path}/{person_folder}') 
                         if f.endswith('.jpg')])
            total_photos += photos
    
    return {
        'total_people': total_people,
        'total_photos': total_photos,
        'avg_photos_per_person': total_photos / total_people if total_people > 0 else 0
    }
```

**4. Backup Dataset:**
```python
import shutil
from datetime import datetime

def backup_dataset(dataset_path):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f'backups/dataset_backup_{timestamp}'
    shutil.copytree(dataset_path, backup_path)
    print(f'Backup created: {backup_path}')
```

---

## 🎓 Best Practices

### Data Collection
- **Quantity:** 20-30 photos per person minimum
- **Variety:** Different angles, expressions, lighting
- **Quality:** Sharp, well-lit, single face
- **Consistency:** Same camera/settings if possible

### Organization
- **Naming:** person_ID_name format
- **Metadata:** Always include capture info
- **Backups:** Regular backups before changes
- **Versioning:** Date-stamped backups

### Quality Control
- **Automated:** Use scripts to validate
- **Manual Review:** Spot-check samples
- **Reject Criteria:** Too blurry, dark, or multiple faces
- **Re-capture:** Don't hesitate to recapture bad data

---

## ✅ Checklist Progress

```
[ ] 01_capture_faces.py - Captured 3+ people, 20+ photos each
[ ] 02_quality_control.py - Validated quality, >80% pass rate
[ ] 03_dataset_management.py - Organized structure, metadata generated
[ ] Dataset backup created
[ ] Encodings generated for all people
[ ] Dataset statistics reviewed
```

---

## 🐛 Common Issues & Solutions

**Webcam capture laggy:**
- Reduce frame resolution
- Increase capture interval
- Close other apps using camera

**Quality check too strict:**
- Adjust blur threshold (lower = more lenient)
- Adjust brightness range
- Review rejected photos manually

**Storage space issues:**
- Compress images (JPEG quality 90)
- Delete duplicates
- Archive old datasets

**Inconsistent dataset:**
- Recapture with same lighting
- Use same camera throughout
- Standardize capture procedure

---

## 📖 Additional Resources

- Dataset best practices: Computer Vision guidelines
- Face quality metrics: ISO/IEC 19794-5 standard
- Python file management: shutil, os modules

---

## ⏭️ Next Steps

Setelah minggu 4:

1. ✅ Dataset dengan 5+ people, 20+ photos each
2. ✅ Quality validated (>80% good)
3. ✅ Encodings generated
4. ✅ Lanjut ke **Minggu 5: Recognition System**

---

**Great dataset = Great recognition! 📸**

*Quality data is foundation of good AI. Take time to do this right!*
