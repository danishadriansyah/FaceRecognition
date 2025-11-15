# Minggu 2 - Project Module: Face Detector

## 📚 Overview
Folder ini berisi implementasi production-ready module **face_detector.py** untuk face detection menggunakan Haar Cascade Classifier. Module ini adalah upgrade dari minggu-1 dengan tambahan face detection capabilities.

## 📁 File Structure

```
project/
├── README.md (file ini)
├── image_utils.py      # Week 1 module (duplicated)
├── face_detector.py    # NEW: Face detection module
└── test_detector.py    # Unit tests for face detector
```

---

## 🎯 File Descriptions

### face_detector.py
**Purpose:** Production-ready face detection module dengan Haar Cascade

**Class: FaceDetector**

**Methods:**
1. **__init__(cascade_path)** - Initialize dengan Haar Cascade model
2. **detect_faces(image, scaleFactor, minNeighbors, minSize)** - Detect faces
3. **detect_faces_webcam(scaleFactor, minNeighbors)** - Real-time dari webcam
4. **draw_detections(image, faces, color, thickness)** - Draw bounding boxes
5. **get_face_regions(image, faces)** - Extract face ROIs as array
6. **count_faces(image)** - Quick count berapa wajah
7. **validate_detection(faces, min_confidence)** - Filter low-quality detections

**Key Features:**
- ✅ Multiple cascade support (frontal, profile, eye)
- ✅ Parameter tuning interface
- ✅ Validation dan error handling
- ✅ Face ROI extraction untuk recognition
- ✅ Performance optimization built-in

**Cara menggunakan:**
```python
from face_detector import FaceDetector

# Initialize detector
detector = FaceDetector()

# Detect from image
import cv2
image = cv2.imread('photo.jpg')
faces = detector.detect_faces(image)

# Draw results
image_with_boxes = detector.draw_detections(image, faces)
cv2.imshow('Detected', image_with_boxes)

# Get face count
count = detector.count_faces(image)
print(f'Found {count} faces')

# Extract face regions for recognition
face_images = detector.get_face_regions(image, faces)
for i, face in enumerate(face_images):
    cv2.imwrite(f'face_{i}.jpg', face)
```

**Design Principles:**
- **Encapsulation:** All detection logic dalam class
- **Flexibility:** Configurable parameters
- **Reusability:** Easy to use in other modules
- **Performance:** Optimized untuk real-time

---

### image_utils.py
**Purpose:** Week 1 module duplicated untuk progressive build

Sama seperti minggu-1, berisi:
- load_image(), save_image()
- resize_image(), crop_image()
- rotate_image(), flip_image()
- to_grayscale(), apply_blur()
- draw_rectangle(), add_text()

**Why duplicated?**
Setiap minggu standalone, tidak import dari minggu lain (lihat PROGRESSIVE_MODULES.md)

---

### test_detector.py
**Purpose:** Unit tests untuk validate face_detector.py

**Test Cases:**
1. ✅ test_init_detector - Cascade loaded correctly
2. ✅ test_detect_faces_single - One face detection
3. ✅ test_detect_faces_multiple - Multiple faces
4. ✅ test_detect_faces_empty - No faces (empty array)
5. ✅ test_draw_detections - Bounding boxes drawn
6. ✅ test_get_face_regions - ROI extraction
7. ✅ test_count_faces - Count accuracy
8. ✅ test_validate_detection - Filter low quality
9. ✅ test_parameters_tuning - Different parameters
10. ✅ test_webcam_detection - Real-time (mock)

**Cara menjalankan:**
```bash
cd minggu-2-face-detection/project
python test_detector.py
```

**Expected output:**
```
test_init_detector ... OK
test_detect_faces_single ... OK
test_detect_faces_multiple ... OK
test_detect_faces_empty ... OK
test_draw_detections ... OK
test_get_face_regions ... OK
test_count_faces ... OK
test_validate_detection ... OK
test_parameters_tuning ... OK
test_webcam_detection ... OK

----------------------------------------------------------------------
Ran 10 tests in 1.234s

OK
```

---

## 🚀 How to Use This Module

### Step 1: Understand the Code
```bash
code face_detector.py  # or notepad face_detector.py
```

Review:
- Class structure
- Method signatures
- Parameter meanings
- Error handling approach

### Step 2: Run Tests
```bash
python test_detector.py
```

Pastikan semua PASS sebelum pakai module.

### Step 3: Test Manually
Create test script:
```python
# test_manual.py
from face_detector import FaceDetector
import cv2

# Initialize
detector = FaceDetector()

# Test dengan gambar
img = cv2.imread('test_photo.jpg')
faces = detector.detect_faces(img)
print(f'Detected {len(faces)} faces')

# Draw boxes
result = detector.draw_detections(img, faces, color=(0,255,0))
cv2.imshow('Result', result)
cv2.waitKey(0)

# Extract faces
face_regions = detector.get_face_regions(img, faces)
for i, face in enumerate(face_regions):
    cv2.imshow(f'Face {i}', face)
cv2.waitKey(0)
```

### Step 4: Integrate dengan Learning
```python
# Di learning files
import sys
sys.path.append('../project')
from face_detector import FaceDetector

detector = FaceDetector()
# Use methods...
```

---

## 📋 Complete API Reference

### FaceDetector Class

#### __init__(cascade_path=None)
Initialize face detector

**Parameters:**
- cascade_path (str, optional): Path to Haar Cascade XML
  - Default: Uses OpenCV's frontal face cascade
  - Can specify custom cascade for profile/eye detection

**Returns:**
- FaceDetector instance

**Example:**
```python
# Use default frontal face cascade
detector = FaceDetector()

# Use profile face cascade
detector = FaceDetector('haarcascade_profileface.xml')
```

---

#### detect_faces(image, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
Detect faces dari image

**Parameters:**
- image (numpy.ndarray): Input image (color or grayscale)
- scaleFactor (float): Image pyramid scale (1.05-1.5)
  - Lower = more accurate, slower
  - Higher = faster, less accurate
- minNeighbors (int): Quality threshold (3-8)
  - Lower = more detections, more false positives
  - Higher = fewer false positives
- minSize (tuple): Minimum face size (width, height)

**Returns:**
- list: Array of tuples [(x, y, w, h), ...]
  - x, y: top-left corner
  - w, h: width and height
  - Empty list if no faces detected

**Example:**
```python
faces = detector.detect_faces(image)
# [(120, 80, 150, 150), (300, 100, 140, 140)]

# Aggressive detection
faces = detector.detect_faces(image, scaleFactor=1.05, minNeighbors=3)

# Conservative detection  
faces = detector.detect_faces(image, scaleFactor=1.3, minNeighbors=7)
```

---

#### detect_faces_webcam(scaleFactor=1.2, minNeighbors=5)
Real-time face detection dari webcam

**Parameters:**
- scaleFactor (float): Detection scale
- minNeighbors (int): Quality threshold

**Returns:**
- None (displays window, press 'q' to quit)

**Behavior:**
- Opens webcam window
- Draws green rectangles around faces
- Shows FPS counter
- Press 'q' to exit

**Example:**
```python
# Start real-time detection
detector.detect_faces_webcam()

# With custom parameters
detector.detect_faces_webcam(scaleFactor=1.1, minNeighbors=6)
```

---

#### draw_detections(image, faces, color=(0,255,0), thickness=2)
Draw bounding boxes pada detected faces

**Parameters:**
- image (numpy.ndarray): Input image
- faces (list): Detection results dari detect_faces()
- color (tuple): BGR color for rectangle
- thickness (int): Line thickness

**Returns:**
- numpy.ndarray: Image dengan bounding boxes

**Example:**
```python
faces = detector.detect_faces(image)
result = detector.draw_detections(image, faces, color=(255,0,0), thickness=3)
cv2.imshow('Faces', result)
```

---

#### get_face_regions(image, faces)
Extract face regions sebagai separate images

**Parameters:**
- image (numpy.ndarray): Original image
- faces (list): Detection results

**Returns:**
- list: Array of face images (cropped)

**Example:**
```python
faces = detector.detect_faces(image)
face_images = detector.get_face_regions(image, faces)

# Save each face
for i, face in enumerate(face_images):
    cv2.imwrite(f'face_{i}.jpg', face)
```

---

#### count_faces(image)
Quick count jumlah faces

**Parameters:**
- image (numpy.ndarray): Input image

**Returns:**
- int: Number of detected faces

**Example:**
```python
count = detector.count_faces(image)
print(f'Found {count} people')
```

---

#### validate_detection(faces, min_size=30)
Filter detections based on criteria

**Parameters:**
- faces (list): Raw detection results
- min_size (int): Minimum face dimension

**Returns:**
- list: Filtered detections

**Example:**
```python
faces = detector.detect_faces(image, minNeighbors=3)
# Filter small false positives
valid_faces = detector.validate_detection(faces, min_size=50)
```

---

## 🔍 Testing Checklist

```
[ ] test_init_detector - Cascade loaded
[ ] test_detect_faces_single - Single face OK
[ ] test_detect_faces_multiple - Multiple faces OK
[ ] test_detect_faces_empty - No crash on empty
[ ] test_draw_detections - Boxes drawn correctly
[ ] test_get_face_regions - ROI extracted properly
[ ] test_count_faces - Count matches
[ ] test_validate_detection - Filtering works
[ ] test_parameters_tuning - Parameters effective
[ ] test_webcam_detection - Real-time works
[ ] All 10 tests PASSED
```

---

## 🐛 Troubleshooting

**Error: Cascade not loaded**
```python
# Use full path
import cv2
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
detector = FaceDetector(cascade_path)
```

**No faces detected on clear image**
- Try lower scaleFactor (1.05)
- Try lower minNeighbors (3)
- Ensure face is frontal, not profile
- Check lighting conditions

**Too many false positives**
- Increase minNeighbors (6-8)
- Increase minSize (50, 50)
- Use validate_detection() to filter

**Slow performance**
- Resize image before detection
- Increase scaleFactor (1.3)
- Process fewer frames (skip frames)

---

## 📚 Integration with Main Project

Module ini akan di-copy ke structure utama:

```
ExtraQueensya/
└── core/
    ├── image_utils.py     # From week 1
    └── face_detector.py   # From week 2 ← NEW
```

**Usage in week 3+:**
```python
from core.image_utils import load_image, resize_image
from core.face_detector import FaceDetector

# Week 3 akan add face recognition
# face_detector.py digunakan untuk preprocessing
```

---

## ⏭️ Next Steps

Setelah semua tests passing:

1. ✅ Pahami FaceDetector class dan methods
2. ✅ Test manually dengan berbagai images
3. ✅ Tune parameters untuk use case kamu
4. ✅ Integrate dengan minggu-1 image_utils
5. ✅ Lanjut ke **Minggu 3: Face Recognition**
   - Face detector akan digunakan untuk locate faces
   - Week 3 adds face_recognizer.py untuk identify people

---

## 💡 Best Practices Learned

1. **Class-based Design:** Encapsulate related functions
2. **Default Parameters:** Sensible defaults dengan override option
3. **Validation:** Check inputs dan outputs
4. **Extraction:** Separate detection dari visualization
5. **Testing:** Comprehensive tests untuk reliability

---

**Excellent progress on Week 2! 🎉**

*Face detection adalah prerequisite untuk face recognition. Module ini akan heavily used di week 3-8!*
