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

3. **Webcam Access with Camera Selection**
   ```python
   # Auto-detect available cameras
   available_cameras = detect_available_cameras()
   camera_id = select_camera(available_cameras)
   
   # Open selected camera
   cap = cv2.VideoCapture(camera_id)
   ret, frame = cap.read()
   cap.release()
   ```
   
   Features:
   - Auto-detect semua camera yang tersedia
   - Tampilkan info: nama, resolusi, FPS, backend
   - User pilih camera yang mau dipakai
   - Support multiple cameras (built-in + USB)

4. **Keyboard Controls**
   - 'q': Quit
   - 's': Save snapshot
   - 'ESC': Exit

## Langkah
1. Run: `python main.py`
2. Script akan detect available cameras
3. Pilih camera yang mau dipakai (jika ada multiple)
4. Webcam akan terbuka
5. Tekan 's' untuk snapshot
6. Tekan 'q' untuk quit

## Output
- Image dengan shapes
- Webcam snapshots
