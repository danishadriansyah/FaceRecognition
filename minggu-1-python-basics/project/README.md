# Minggu 1 - Project Module

##  Overview
Folder ini berisi implementasi production-ready module **image_utils.py** yang merupakan hasil dari konsep-konsep yang dipelajari di folder learning/. Module ini akan digunakan sebagai fondasi untuk minggu-minggu selanjutnya.

##  File Structure

```
project/
 README.md (file ini)
 image_utils.py     # Main module (production code)
 test_utils.py      # Unit tests
```

---

##  File Descriptions

### image_utils.py
**Purpose:** Production-ready utility module untuk image processing operations

**Apa yang ada di dalam:**
1. **load_image(path)** - Load image dari file dengan error handling
2. **save_image(image, path)** - Save image ke file  
3. **resize_image(image, width, height)** - Resize ke ukuran spesifik
4. **crop_image(image, x, y, width, height)** - Crop ROI dari image
5. **rotate_image(image, angle)** - Rotate dengan sudut tertentu
6. **flip_image(image, flip_code)** - Flip horizontal/vertical
7. **to_grayscale(image)** - Convert ke grayscale
8. **apply_blur(image, kernel_size)** - Apply Gaussian blur
9. **draw_rectangle(image, x, y, width, height, color, thickness)** - Draw box
10. **add_text(image, text, x, y, color, font_scale)** - Add text overlay

**Key Features:**
-  Error handling untuk semua operations
-  Input validation (check None, check dimensions)
-  Consistent return values
-  Clean and readable code
-  Well documented dengan docstrings

**Cara menggunakan:**
```python
from image_utils import load_image, resize_image, save_image

# Load image
img = load_image('photo.jpg')

# Resize to 640x480
resized = resize_image(img, 640, 480)

# Save result
save_image(resized, 'output.jpg')
```

**Design Principles:**
- **Single Responsibility:** Setiap fungsi hanya melakukan 1 task
- **Error Handling:** Return None jika operation gagal
- **Immutable:** Tidak memodifikasi input image (gunakan .copy())
- **Type Hints:** Parameter types jelas (untuk IDE autocomplete)

---

### test_utils.py
**Purpose:** Unit tests untuk validate semua fungsi di image_utils.py

**Apa yang di-test:**
1.  load_image() - Test valid path, invalid path, None
2.  save_image() - Test berhasil save, path invalid
3.  resize_image() - Test berbagai ukuran, edge cases
4.  crop_image() - Test valid crop, out of bounds
5.  rotate_image() - Test berbagai sudut (90, 180, 45)
6.  flip_image() - Test horizontal, vertical, both
7.  to_grayscale() - Test conversion, check channels
8.  apply_blur() - Test berbagai kernel sizes
9.  draw_rectangle() - Test drawing, check pixels changed
10.  add_text() - Test text overlay

**Cara menjalankan:**
```bash
cd minggu-1-python-basics/project

# Run all tests
python test_utils.py

# Expected output:
# .........
# ----------------------------------------------------------------------
# Ran 10 tests in 0.523s
# OK
```

**Expected Results:**
```
test_load_image_valid ... OK
test_load_image_invalid ... OK
test_resize_image ... OK
test_crop_image ... OK
test_rotate_image ... OK
test_flip_image ... OK
test_to_grayscale ... OK
test_apply_blur ... OK
test_draw_rectangle ... OK
test_add_text ... OK

----------------------------------------------------------------------
Ran 10 tests in 0.XXXs

OK
```

**Jika test FAILED:**
1. Baca error message dengan teliti
2. Check fungsi yang fail di image_utils.py
3. Verify input/output di test case
4. Fix bug di image_utils.py
5. Run test lagi sampai semua PASS

---

##  How to Use This Module

### Step 1: Understand the Code
Buka image_utils.py dan baca setiap fungsi:
```bash
# Windows
notepad image_utils.py

# Mac/Linux
nano image_utils.py
# atau gunakan VS Code
code image_utils.py
```

### Step 2: Run Tests
Pastikan semua tests passing:
```bash
python test_utils.py
```

### Step 3: Test Manually
Create simple script untuk test manual:
```python
# test_manual.py
from image_utils import *

# Test load
img = load_image('test.jpg')
print(f'Image shape: {img.shape}')

# Test resize
resized = resize_image(img, 320, 240)
print(f'Resized shape: {resized.shape}')

# Test grayscale
gray = to_grayscale(img)
print(f'Grayscale channels: {len(gray.shape)}')

# Test blur
blurred = apply_blur(img, 15)
save_image(blurred, 'blurred_output.jpg')
print('Blur saved!')
```

### Step 4: Integrate to Learning
Gunakan module ini di learning/ exercises:
```python
# Di learning/latihan.py
import sys
sys.path.append('../project')
from image_utils import resize_image, apply_blur

# Sekarang bisa pakai functions
frame = resize_image(frame, 640, 480)
frame = apply_blur(frame, 5)
```

---

##  Module API Reference

### Image I/O Functions

#### load_image(path: str)
Load image dari file

**Parameters:**
- path (str): Path ke image file

**Returns:**
- numpy.ndarray: Image array jika sukses
- None: Jika file tidak ditemukan atau error

**Example:**
```python
img = load_image('photo.jpg')
if img is not None:
    print('Image loaded successfully')
```

---

#### save_image(image, path: str)
Save image ke file

**Parameters:**
- image (numpy.ndarray): Image to save
- path (str): Output file path

**Returns:**
- bool: True jika sukses, False jika gagal

**Example:**
```python
success = save_image(img, 'output.jpg')
if success:
    print('Image saved')
```

---

### Transformation Functions

#### resize_image(image, width: int, height: int)
Resize image ke ukuran baru

**Parameters:**
- image: Input image
- width (int): Target width
- height (int): Target height

**Returns:**
- numpy.ndarray: Resized image

**Example:**
```python
resized = resize_image(img, 640, 480)
```

---

#### crop_image(image, x: int, y: int, width: int, height: int)
Crop region dari image

**Parameters:**
- image: Input image
- x (int): Top-left X coordinate
- y (int): Top-left Y coordinate
- width (int): Crop width
- height (int): Crop height

**Returns:**
- numpy.ndarray: Cropped image

**Example:**
```python
# Crop 200x200 region starting at (100, 100)
cropped = crop_image(img, 100, 100, 200, 200)
```

---

#### rotate_image(image, angle: float)
Rotate image dengan sudut tertentu

**Parameters:**
- image: Input image
- angle (float): Rotation angle in degrees

**Returns:**
- numpy.ndarray: Rotated image

**Example:**
```python
rotated = rotate_image(img, 45)  # Rotate 45 degrees
```

---

#### flip_image(image, flip_code: int)
Flip image

**Parameters:**
- image: Input image
- flip_code (int): 
  - 0 = vertical flip
  - 1 = horizontal flip
  - -1 = both

**Returns:**
- numpy.ndarray: Flipped image

**Example:**
```python
h_flip = flip_image(img, 1)  # Horizontal flip
```

---

### Color & Filter Functions

#### to_grayscale(image)
Convert to grayscale

**Parameters:**
- image: Input color image

**Returns:**
- numpy.ndarray: Grayscale image

**Example:**
```python
gray = to_grayscale(img)
```

---

#### apply_blur(image, kernel_size: int)
Apply Gaussian blur

**Parameters:**
- image: Input image
- kernel_size (int): Blur kernel size (must be odd)

**Returns:**
- numpy.ndarray: Blurred image

**Example:**
```python
blurred = apply_blur(img, 15)  # Strong blur
```

---

### Drawing Functions

#### draw_rectangle(image, x, y, width, height, color, thickness)
Draw rectangle pada image

**Parameters:**
- image: Input image
- x, y (int): Top-left corner
- width, height (int): Rectangle dimensions
- color (tuple): BGR color (B, G, R)
- thickness (int): Line thickness (-1 = filled)

**Returns:**
- numpy.ndarray: Image with rectangle

**Example:**
```python
# Draw green rectangle
img = draw_rectangle(img, 100, 100, 200, 150, (0, 255, 0), 2)
```

---

#### add_text(image, text, x, y, color, font_scale)
Add text overlay

**Parameters:**
- image: Input image
- text (str): Text to display
- x, y (int): Text position
- color (tuple): BGR color
- font_scale (float): Text size

**Returns:**
- numpy.ndarray: Image with text

**Example:**
```python
img = add_text(img, 'Hello', 50, 50, (255, 255, 255), 1.0)
```

---

##  Testing Checklist

Pastikan semua tests PASS sebelum lanjut ke minggu 2:

```
[ ] test_load_image_valid - PASS
[ ] test_load_image_invalid - PASS
[ ] test_resize_image - PASS
[ ] test_crop_image - PASS
[ ] test_rotate_image - PASS
[ ] test_flip_image - PASS
[ ] test_to_grayscale - PASS
[ ] test_apply_blur - PASS
[ ] test_draw_rectangle - PASS
[ ] test_add_text - PASS
[ ] All 10 tests passed - OK
```

---

##  Troubleshooting

**ImportError: cannot import name 'load_image'**
- Check apakah image_utils.py ada di folder yang sama
- Check apakah function name benar (case-sensitive)

**Test failed: AssertionError**
- Baca error message untuk tau test mana yang fail
- Check expected vs actual output
- Debug function di image_utils.py

**AttributeError: 'NoneType' object has no attribute 'shape'**
- Image loading failed (return None)
- Check file path benar
- Validate input sebelum process

---

##  Integration with Main Project

Module ini akan di-copy ke main project structure:

```
ExtraQueensya/
 core/
     image_utils.py   Copy from minggu-1/project/
```

**Cara integrate:**
```bash
# Copy module ke main project
cp minggu-1-python-basics/project/image_utils.py core/

# Import di module lain
from core.image_utils import load_image, resize_image
```

---

##  Next Steps

Setelah semua tests passing:

1.  Pahami setiap fungsi di image_utils.py
2.  Semua tests harus PASS
3.  Coba gunakan functions di manual test
4.  Lanjut ke **Minggu 2: Face Detection**
   - Module ini akan digunakan untuk preprocessing
   - Week 2 akan menambah face_detector.py

---

##  Good Practices Learned

1. **Error Handling:** Always validate inputs, handle edge cases
2. **Testing:** Write tests untuk semua functions
3. **Documentation:** Clear docstrings dan comments
4. **Modularity:** Small functions, single responsibility
5. **Reusability:** Build once, use everywhere

---

**Great job completing Week 1! **

*Module ini adalah fondasi untuk 7 minggu ke depan. Pastikan kamu paham betul!*
