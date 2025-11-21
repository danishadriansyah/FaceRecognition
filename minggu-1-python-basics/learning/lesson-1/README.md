# Lesson 1: Python & OpenCV Basics

## Tujuan
- Install OpenCV
- Load & display images
- Basic image operations
- Save images

## Konsep yang Dipelajari
1. **OpenCV Installation**
   ```bash
   pip install opencv-python
   ```

2. **Load Image**
   ```python
   import cv2
   img = cv2.imread('image.jpg')
   ```

3. **Display Image**
   ```python
   cv2.imshow('Window', img)
   cv2.waitKey(0)
   cv2.destroyAllWindows()
   ```

4. **Basic Operations**
   - Convert to grayscale
   - Resize image
   - Rotate image
   - Crop image

5. **Save Image**
   ```python
   cv2.imwrite('output.jpg', img)
   ```

## Langkah
1. Run: `python main.py`
2. Coba load sample image
3. Experiment dengan operations
4. Save hasil ke output/

## Output
- Grayscale image
- Resized image
- Cropped image
