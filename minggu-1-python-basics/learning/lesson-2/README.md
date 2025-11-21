# Lesson 2: Drawing Shapes & Webcam Basics

## Tujuan
- Draw shapes on images
- Add text to images
- Access webcam
- Capture frames
- Basic video processing

## Konsep yang Dipelajari
1. **Drawing Shapes**
   - Rectangle: `cv2.rectangle()`
   - Circle: `cv2.circle()`
   - Line: `cv2.line()`
   - Text: `cv2.putText()`

2. **Colors in OpenCV**
   - Format: BGR (Blue, Green, Red)
   - White: (255, 255, 255)
   - Black: (0, 0, 0)
   - Red: (0, 0, 255)
   - Green: (0, 255, 0)
   - Blue: (255, 0, 0)

3. **Webcam Access**
   ```python
   cap = cv2.VideoCapture(0)  # 0 = default webcam
   ret, frame = cap.read()
   cap.release()
   ```

4. **Keyboard Controls**
   - 'q': Quit
   - 's': Save snapshot
   - 'ESC': Exit

## Langkah
1. Run: `python main.py`
2. Webcam akan terbuka
3. Tekan 's' untuk snapshot
4. Tekan 'q' untuk quit

## Output
- Image dengan shapes
- Webcam snapshots
