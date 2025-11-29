# Minggu 4 - Project: DatasetManager Class

## 📚 Overview
Production-ready `DatasetManager` class untuk systematic dataset collection, validation, organization, dan management. Complete dengan quality control, metadata handling, dan backup functionality.

## 📁 Project Files

```
project/
├── README.md (file ini)
├── dataset_manager.py (NEW - Main class)
├── face_detector.py (from Week 2)
├── face_recognizer.py (from Week 3 - UPGRADED to Hybrid!)
├── image_utils.py (from Week 1)
└── test_dataset.py (Testing file)
```

---

## 🔧 Tech Stack Upgrade: Hybrid Architecture

### **NEW:** MediaPipe + DeepFace Hybrid System

**Why Hybrid?**

Starting Minggu 4, we upgrade to **hybrid approach** for production-ready performance:

```
Input Image → MediaPipe Detection (10-15ms) → DeepFace Recognition (100ms) → Result
              ⚡ FAST                          🎯 ACCURATE                    97%+
```

**Comparison:**

| Approach | Speed | Accuracy | Real-time | Use Case |
|----------|-------|----------|-----------|----------|
| MediaPipe only (Week 3) | ⚡⚡⚡⚡⚡ | ❌ No ID | ✅ Yes | Learning |
| DeepFace only | ⚡⚡ | ⭐⭐⭐⭐⭐ | ❌ No | - |
| **Hybrid (Week 4-7)** | **⚡⚡⚡⚡** | **⭐⭐⭐⭐⭐** | **✅ Yes** | **Production** |

**Benefits:**
- ✅ 2x faster than pure DeepFace
- ✅ 97%+ accuracy (vs MediaPipe's basic matching)
- ✅ Real-time capable (6-9 FPS)
- ✅ Industry-standard embeddings

**Models Available:**
- **Facenet512** (default) - Best balance
- ArcFace - Maximum accuracy
- SFace - Mobile/embedded

*See `HYBRID_ARCHITECTURE.md` for details*

---

## 🎯 DatasetManager Class - Complete API

### Initialization

```python
from dataset_manager import DatasetManager

# Initialize with dataset path
manager = DatasetManager(dataset_path='dataset/')

# Custom configuration
manager = DatasetManager(
    dataset_path='my_dataset/',
    min_photos_per_person=20,
    quality_threshold=0.8,
    auto_backup=True
)
```

**Parameters:**
- `dataset_path` (str): Root folder untuk dataset (default: 'dataset/')
- `min_photos_per_person` (int): Minimum photos required (default: 20)
- `quality_threshold` (float): Quality score 0-1 (default: 0.8)
- `auto_backup` (bool): Auto backup sebelum changes (default: True)

---

## 🔧 Core Methods

### 1. add_person()
**Purpose:** Create new person entry dalam dataset

```python
# Basic usage
manager.add_person(
    name='Alice',
    employee_id='001',
    department='Engineering'
)

# With additional metadata
manager.add_person(
    name='Bob',
    employee_id='002',
    department='Sales',
    metadata={
        'email': 'bob@company.com',
        'shift': 'morning'
    }
)
```

**Returns:** `str` - Path to person folder

**Creates:**
```
dataset/person_001_alice/
├── metadata.json
└── photos/ (empty)
```

---

### 2. capture_person_photos()
**Purpose:** Interactive photo capture dari webcam

```python
# Capture with default settings (30 photos)
manager.capture_person_photos(
    person_id='001',
    target_count=30
)

# Custom capture
manager.capture_person_photos(
    person_id='001',
    target_count=50,
    show_guide=True,
    capture_interval=10  # frames between captures
)
```

**Parameters:**
- `person_id` (str): Person identifier
- `target_count` (int): Total photos to capture (default: 30)
- `show_guide` (bool): Show angle guide (default: True)
- `capture_interval` (int): Frames between auto-capture (default: 10)

**Process:**
1. Opens webcam
2. Shows angle guide (frontal, left, right)
3. Validates quality real-time
4. Auto-captures when quality good
5. Saves to person folder
6. Shows progress

**Quality checks:**
- Single face detected
- Face size ≥ 100x100
- Not blurry (variance > 100)
- Good brightness (50-200)

---

### 3. validate_photos()
**Purpose:** Quality validation untuk captured photos

```python
# Validate single person
results = manager.validate_photos('001')
print(f"Good: {results['good']}, Bad: {results['rejected']}")

# Validate entire dataset
all_results = manager.validate_photos('all')
```

**Returns:** `dict`
```python
{
    'person_id': '001',
    'total': 30,
    'good': 24,
    'rejected': 6,
    'pass_rate': 0.8,
    'rejection_reasons': {
        'blurry': 3,
        'dark': 2,
        'multiple_faces': 1
    }
}
```

**Actions:**
- Moves rejected photos to `rejected/` folder
- Updates metadata dengan validation info
- Generates quality report

---

### 4. generate_encodings()
**Purpose:** Generate face encodings using DeepFace Facenet512

```python
# Generate for single person
count = manager.generate_encodings('001')
print(f"Generated {count} encodings")

# Generate for all people
manager.generate_encodings('all')

# With custom DeepFace model
manager.generate_encodings('001', model='ArcFace')  # Maximum accuracy
manager.generate_encodings('001', model='SFace')    # Faster
```

**Parameters:**
- `person_id` (str): Person ID or 'all'
- `model` (str): DeepFace model - 'Facenet512' (default), 'ArcFace', 'SFace'

**Returns:** `int` - Number of encodings generated

**Creates:**
- `encodings.pkl` file in person folder (512-d embeddings)
- Updates metadata with encoding info

**Performance:**
- Facenet512: ~100-150ms per face (high accuracy)
- SFace: ~50-80ms per face (faster)
- GPU acceleration supported

---

### 5. get_person_info()
**Purpose:** Retrieve person metadata

```python
# Get single person info
info = manager.get_person_info('001')
print(info['name'], info['photo_count'])

# Get all people
all_people = manager.get_person_info('all')
for person in all_people:
    print(f"{person['name']}: {person['photo_count']} photos")
```

**Returns:** `dict` or `list[dict]`
```python
{
    'person_id': '001',
    'name': 'Alice',
    'department': 'Engineering',
    'photo_count': 24,
    'encoding_count': 24,
    'capture_date': '2025-11-14T10:30:00',
    'last_updated': '2025-11-14T11:00:00',
    'quality_score': 0.92
}
```

---

### 6. update_person_metadata()
**Purpose:** Update person information

```python
# Update single field
manager.update_person_metadata('001', department='R&D')

# Update multiple fields
manager.update_person_metadata(
    '001',
    department='Research',
    shift='evening',
    custom_field='custom_value'
)
```

**Parameters:**
- `person_id` (str): Person identifier
- `**kwargs`: Key-value pairs to update

**Updates:** `metadata.json` file with new info

---

### 7. backup_dataset()
**Purpose:** Create timestamped dataset backup

```python
# Full backup
backup_path = manager.backup_dataset()
print(f"Backup saved to: {backup_path}")

# Backup with custom name
backup_path = manager.backup_dataset(
    backup_name='before_cleanup'
)

# Backup to specific location
backup_path = manager.backup_dataset(
    backup_dir='E:/backups/'
)
```

**Returns:** `str` - Path to backup folder

**Creates:**
```
backups/
└── dataset_backup_20251114_103000/
    └── [complete dataset copy]
```

---

### 8. cleanup_dataset()
**Purpose:** Remove low-quality data, duplicates

```python
# Auto cleanup
removed = manager.cleanup_dataset()
print(f"Removed {removed} items")

# Cleanup with options
removed = manager.cleanup_dataset(
    remove_rejected=True,
    remove_duplicates=True,
    min_photos=15  # Remove people with <15 photos
)
```

**Parameters:**
- `remove_rejected` (bool): Delete rejected photos (default: True)
- `remove_duplicates` (bool): Remove duplicate encodings (default: True)
- `min_photos` (int): Minimum photos to keep person (default: 10)

**Returns:** `int` - Number of items removed

---

### 9. get_dataset_statistics()
**Purpose:** Comprehensive dataset statistics

```python
stats = manager.get_dataset_statistics()
print(stats)
```

**Returns:** `dict`
```python
{
    'total_people': 5,
    'total_photos': 120,
    'total_encodings': 115,
    'avg_photos_per_person': 24.0,
    'avg_quality_score': 0.88,
    'people_needing_more_photos': ['003'],  # <20 photos
    'people_without_encodings': [],
    'dataset_size_mb': 45.2,
    'last_backup': '2025-11-14T09:00:00'
}
```

---

### 10. export_for_training()
**Purpose:** Export dataset dalam format siap training

```python
# Export all
manager.export_for_training(
    output_path='training_data/',
    format='standard'
)

# Export dengan split
manager.export_for_training(
    output_path='training_data/',
    format='train_val_split',
    split_ratio=0.8  # 80% train, 20% validation
)
```

**Formats:**
- `'standard'`: All data in single folder
- `'train_val_split'`: Separate train/ and val/ folders
- `'encodings_only'`: Just encodings file

**Creates:**
```
training_data/
├── train/
│   ├── person_001/
│   └── person_002/
├── val/
│   ├── person_001/
│   └── person_002/
└── encodings.pkl
```

---

## 📖 Complete Usage Examples

### Example 1: Onboarding New Employee

```python
from dataset_manager import DatasetManager

manager = DatasetManager()

# 1. Create person entry
manager.add_person(
    name='Alice Johnson',
    employee_id='001',
    department='Engineering',
    metadata={'email': 'alice@company.com'}
)

# 2. Capture photos
print("Please look at camera...")
manager.capture_person_photos(
    person_id='001',
    target_count=30
)

# 3. Validate quality
results = manager.validate_photos('001')
if results['pass_rate'] >= 0.8:
    print("✅ Quality passed!")
else:
    print("⚠️ Need more good photos")
    # Recapture if needed

# 4. Generate encodings
count = manager.generate_encodings('001')
print(f"Generated {count} encodings")

# 5. Backup
manager.backup_dataset()
print("Employee onboarded successfully!")
```

---

### Example 2: Dataset Maintenance

```python
manager = DatasetManager()

# 1. Get current stats
stats = manager.get_dataset_statistics()
print(f"Total people: {stats['total_people']}")
print(f"Average quality: {stats['avg_quality_score']:.2f}")

# 2. Identify issues
if stats['people_needing_more_photos']:
    print("People needing more photos:")
    for person_id in stats['people_needing_more_photos']:
        info = manager.get_person_info(person_id)
        print(f"  - {info['name']}: {info['photo_count']} photos")

# 3. Recapture for people with low photo count
for person_id in stats['people_needing_more_photos']:
    response = input(f"Recapture for {person_id}? (y/n): ")
    if response.lower() == 'y':
        manager.capture_person_photos(person_id, target_count=25)

# 4. Cleanup
manager.cleanup_dataset(
    remove_rejected=True,
    remove_duplicates=True
)

# 5. Regenerate all encodings
manager.generate_encodings('all')

# 6. Final backup
manager.backup_dataset(backup_name='after_maintenance')
```

---

### Example 3: Batch Processing

```python
import pandas as pd

manager = DatasetManager()

# Load employee list from CSV
employees = pd.read_csv('employees.csv')

for _, emp in employees.iterrows():
    # Add person
    manager.add_person(
        name=emp['name'],
        employee_id=emp['id'],
        department=emp['department']
    )
    
    print(f"\nProcessing: {emp['name']}")
    print("Please prepare for photo capture...")
    input("Press Enter when ready...")
    
    # Capture
    manager.capture_person_photos(
        person_id=emp['id'],
        target_count=30
    )
    
    # Validate
    results = manager.validate_photos(emp['id'])
    print(f"Quality: {results['pass_rate']:.0%}")
    
    # Generate encodings
    manager.generate_encodings(emp['id'])

# Export for training
manager.export_for_training(
    output_path='ready_for_training/',
    format='train_val_split'
)

print("\n✅ Batch processing complete!")
print(manager.get_dataset_statistics())
```

---

## 🧪 Testing

Run test file:
```bash
cd minggu-4-dataset-database/project
python test_dataset.py
```

**Tests include:**
- Person creation
- Photo capture simulation
- Quality validation
- Encoding generation
- Metadata updates
- Backup creation
- Cleanup functionality
- Export functions

**Expected output:**
```
Test 1: Add Person................... PASS
Test 2: Capture Photos............... PASS
Test 3: Validate Quality............. PASS
Test 4: Generate Encodings........... PASS
Test 5: Update Metadata.............. PASS
Test 6: Backup Dataset............... PASS
Test 7: Cleanup...................... PASS
Test 8: Export....................... PASS

All tests passed! ✅
```

---

## 🔗 Integration with Other Modules

```python
from dataset_manager import DatasetManager
from face_detector import FaceDetector
from face_recognizer import FaceRecognizer

# Initialize with hybrid approach
manager = DatasetManager()
recognizer = FaceRecognizer(model_name='Facenet512')  # Hybrid system

# Build recognition database from managed dataset
dataset_path = 'dataset/'
recognizer.load_known_faces_from_dataset(dataset_path)

# Test recognition with hybrid approach
test_image = cv2.imread('test.jpg')

# Step 1: Fast detection with MediaPipe
faces = recognizer.detect_faces(test_image)

# Step 2: Accurate recognition with DeepFace
for (x, y, w, h) in faces:
    name, confidence = recognizer.recognize_face(test_image, (x, y, w, h))
    print(f"Recognized: {name} ({confidence:.2%})")
```

---

## ⚙️ Configuration Options

Create `dataset_config.json`:
```json
{
  "dataset_path": "dataset/",
  "min_photos_per_person": 20,
  "quality_threshold": 0.8,
  "auto_backup": true,
  "backup_dir": "backups/",
  "max_backups": 10,
  "quality_checks": {
    "blur_threshold": 100,
    "brightness_min": 50,
    "brightness_max": 200,
    "min_face_size": 100
  },
  "capture_settings": {
    "target_count": 30,
    "capture_interval": 10,
    "show_guide": true,
    "resolution": [640, 480]
  }
}
```

Load config:
```python
import json

with open('dataset_config.json') as f:
    config = json.load(f)

manager = DatasetManager(**config)
```

---

## 🐛 Troubleshooting

**Webcam not opening:**
```python
# Check available cameras
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i} available")
        cap.release()
```

**Quality validation too strict:**
- Adjust thresholds in config
- Review rejected photos manually
- Recalibrate for your lighting conditions

**Encodings generation slow:**
- Use Facenet512 (default) for best balance
- Use SFace for speed (less accurate)
- GPU acceleration: Install tensorflow-gpu
- Process in batches for large datasets

**Storage space issues:**
- Compress images (JPEG quality 85-90)
- Delete rejected photos
- Archive old backups

---

## ✅ Best Practices

1. **Regular Backups:** Backup sebelum major changes
2. **Quality First:** Don't compromise on photo quality
3. **Consistent Capture:** Same lighting, camera, procedure
4. **Metadata Complete:** Always fill all metadata fields
5. **Periodic Validation:** Re-validate dataset monthly
6. **Version Control:** Keep backups dated
7. **Documentation:** Document any special cases

---

## 📊 Performance Metrics

- Photo capture: ~30 photos in 2-3 minutes
- Quality validation: ~100 photos/second
- **Encoding generation (Facenet512):** ~100-150ms per face (CPU)
- **Encoding generation (SFace):** ~50-80ms per face (CPU)
- Backup creation: Depends on size, typically <1 minute

**Hybrid Approach Benefits:**
- Detection: 10-15ms (MediaPipe)
- Recognition: 100-150ms (DeepFace)
- Total: ~110-165ms per face (6-9 FPS capable)

---

## ⏭️ Next Steps

After mastering DatasetManager:

1. ✅ Complete dataset with 5+ people
2. ✅ Quality score >0.8 for all
3. ✅ All encodings generated
4. ✅ Proceed to **Minggu 5: Build Recognition System**

---

**Good data management = Reliable system! 📊**

*This class is foundation for production-grade face recognition.*
