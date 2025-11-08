# Week 1 - Learning Materials

## Tutorial Files

### 01_hello_opencv.py
Introduction to OpenCV basics:
- Loading and displaying images
- Image information (shape, dtype, pixel values)
- Keyboard controls
- Saving images

**Run:** `python 01_hello_opencv.py`

### 02_image_operations.py
Image transformation operations:
- Resize (specific size, scale factor, interpolation)
- Crop (array slicing, ROI selection)
- Rotate (90°, 180°, custom angles)
- Flip (horizontal, vertical)
- Color space conversion (BGR, RGB, Grayscale, HSV)

**Run:** `python 02_image_operations.py`

### 03_drawing_shapes.py
Drawing on images:
- Lines (different types and thicknesses)
- Rectangles (filled and outlined)
- Circles (concentric patterns)
- Text (fonts, sizes, with background)
- Complete example combining all shapes

**Run:** `python 03_drawing_shapes.py`

### 04_webcam_basics.py
Real-time webcam access:
- Opening camera and reading frames
- FPS calculation and display
- Real-time effects (grayscale, blur, edge detection, negative)
- Mirror mode
- Snapshot capture

**Run:** `python 04_webcam_basics.py`

### latihan.py
Practice exercise - Photo Editor:
- Combines all week 1 concepts
- Interactive keyboard controls
- Multiple image operations
- Save edited results

**Run:** `python latihan.py`

## Learning Path

Work through files in order:
1. Start with `01_hello_opencv.py` to understand basics
2. Move to `02_image_operations.py` for transformations
3. Learn drawing with `03_drawing_shapes.py`
4. Try real-time with `04_webcam_basics.py`
5. Complete the exercise in `latihan.py`

## Key Concepts

### Image Representation
- Images are NumPy arrays
- Shape: (height, width, channels)
- Color format: BGR (not RGB)
- Data type: uint8 (0-255)

### Coordinates
- Origin (0,0) is top-left
- X-axis: left to right (width)
- Y-axis: top to bottom (height)

### Best Practices
- Always check if image loaded successfully
- Use `.copy()` to avoid modifying original
- Call `cv2.destroyAllWindows()` after display
- Release camera with `cap.release()`

## Tips

1. Run each file multiple times to understand behavior
2. Try modifying parameters (sizes, colors, effects)
3. Read the code comments carefully
4. Complete the practice challenges in each file
5. Ask questions if something is unclear

## Resources

- OpenCV Documentation: https://docs.opencv.org/
- NumPy Documentation: https://numpy.org/doc/
- Python Image Processing: https://opencv-python-tutroals.readthedocs.io/
