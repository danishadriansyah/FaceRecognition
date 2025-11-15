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
├── learning/          # Tutorial & latihan
│   ├── 01_hello_opencv.py
│   ├── 02_image_operations.py
│   ├── 03_drawing_shapes.py
│   ├── 04_webcam_basics.py
│   └── latihan.py
│
└── project/           # Project development
    ├── image_utils.py
    └── test_utils.py
```

## Materi Learning

### 1. Python & OpenCV Basics
- Installation & setup
- Reading, displaying, saving images
- Image as numpy arrays
- Color spaces (BGR, RGB, Grayscale)

### 2. Image Operations
- Resize, crop, rotate, flip
- Color conversion
- Drawing shapes and text
- Image quality checks

### 3. Webcam Handling
- Access webcam
- Capture frames
- Real-time processing
- Frame rate optimization

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

## Cara Penggunaan

### Learning (Tutorial)
```bash
cd minggu-1-python-basics/learning

# Jalankan tutorial secara berurutan
python 01_hello_opencv.py
python 02_image_operations.py
python 03_drawing_shapes.py
python 04_webcam_basics.py

# Kerjakan latihan
python latihan.py
```

### Project Development
```bash
cd minggu-1-python-basics/project

# Develop image utilities
python image_utils.py

# Test functions
python test_utils.py

# Integrate to main project
# Copy image_utils.py to ../../core/
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
- Completed tutorial exercises
- Understanding of image processing basics
- Ability to work with OpenCV

### Project
- `image_utils.py` - Reusable image processing functions
- `test_utils.py` - Unit tests for utilities
- Documentation of functions

## Next Week Preview

**Minggu 2: Face Detection**
- Haar Cascade implementation
- Detection API endpoint
- Integration dengan image utilities

---

**Time Estimate:** 3-4 hours
**Difficulty:** Beginner
