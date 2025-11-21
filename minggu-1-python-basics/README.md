# Minggu 1: Python Basics & Image Processing

## Tujuan Pembelajaran
- Setup development environment
- Memahami Python fundamentals untuk CV
- Mengenal OpenCV library
- Image manipulation & processing
- Build reusable image utilities

## Struktur Folder

```
minggu-1-python-basics/
├── learning/                   # Tutorial & latihan
│   ├── lesson-1/              # Python & OpenCV Basics
│   │   ├── README.md         # Penjelasan materi
│   │   ├── main.py           # Code praktik
│   │   └── output/           # Hasil praktik
│   ├── lesson-2/              # Drawing & Webcam
│   │   ├── README.md
│   │   ├── main.py
│   │   └── output/
│   ├── images/               # Sample images
│   ├── output/               # Shared output
│   └── README.md             # Overview
│
├── project/                   # Project development
│   ├── image_utils.py
│   ├── test_utils.py
│   ├── output/
│   └── test_images/
│
├── tugas/                     # Assignment
│   └── README.md             # Tugas minggu 1
│
└── README.md                  # This file
```

## Materi Learning

### Lesson 1: Python & OpenCV Basics
- Installation & setup
- Reading, displaying, saving images
- Image as numpy arrays
- Basic operations: grayscale, resize, crop, rotate
- Save processed images

**File:** `learning/lesson-1/main.py`

### Lesson 2: Drawing Shapes & Webcam
- Drawing shapes (rectangles, circles, lines)
- Adding text to images
- Color spaces (BGR, RGB)
- Access webcam
- Capture frames & snapshots
- Real-time processing

**File:** `learning/lesson-2/main.py`

## Project Development

### Module: `image_utils.py`
Helper functions untuk image processing yang akan digunakan di minggu-minggu berikutnya.

**Functions to implement:**
- `load_image(path)` - Load dan validate image
- `resize_image(image, width, height)` - Resize dengan aspect ratio
- `preprocess_image(image)` - Standardize image untuk processing
- `convert_to_grayscale(image)` - Convert color space
- `save_image(image, path)` - Save dengan compression
- `validate_image_quality(image)` - Check blur, brightness, etc

### Integration Plan
Module ini akan menjadi foundation untuk:
- Week 2: Face detection preprocessing
- Week 3: Face recognition input handling
- Week 4: Dataset image validation
- Week 8: API image upload handling

## Cara Penggunaan

### Learning (Tutorial)
```bash
cd minggu-1-python-basics/learning

# Lesson 1: OpenCV Basics
cd lesson-1
python main.py

# Lesson 2: Drawing & Webcam
cd ../lesson-2
python main.py
```

### Project Development
```bash
cd minggu-1-python-basics/project

# Develop image utilities
python image_utils.py

# Test functions
python test_utils.py
```

### Tugas (Assignment)
```bash
cd minggu-1-python-basics/tugas

# Baca tugas di README.md
# Kerjakan tugas: Photo Editor Sederhana
```

## Konsep Penting

### Image Representation
```
Image = Matrix of Pixels
- Grayscale: 1 channel (0-255)
- Color (BGR): 3 channels
- Coordinate: (x, y) top-left is (0,0)
```

### OpenCV Coordinate System
```
(0,0) -----> X (width)
  |
  v
  Y (height)
```

## Deliverables

### Learning
- ✅ Lesson 1: Basic image operations
- ✅ Lesson 2: Drawing & webcam handling
- ✅ Understanding of OpenCV fundamentals

### Project
- ✅ `image_utils.py` - Reusable functions
- ✅ `test_utils.py` - Unit tests

### Tugas
- 📝 Photo Editor Sederhana (see tugas/README.md)

## Next Week Preview

**Minggu 2: Face Detection**
- Haar Cascade implementation
- Detection API endpoint
- Integration dengan image utilities

---

**Time Estimate:** 3-4 hours
**Difficulty:** Beginner
