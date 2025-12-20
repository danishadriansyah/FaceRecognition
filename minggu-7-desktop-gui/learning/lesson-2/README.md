# Lesson 2: Complete GUI dengan Backend Integration

## Tujuan
- Integrate face recognition ke GUI
- Add webcam preview real-time
- Connect ke attendance system (Week 6)
- Multi-window management
- Complete desktop application

## Prerequisites
- ✅ Lesson 1 selesai (Tkinter basics)
- ✅ Dataset sudah di-setup (jalankan `setup_week7.py`)
- ✅ Face encodings ready

## Features Integrated

### Backend Modules (Week 1-6)
- **Face Detection:** MediaPipe (Week 2)
- **Face Recognition:** DeepFace Facenet512 (Week 3)
- **Dataset Manager:** Pickle + JSON (Week 4)
- **Recognition Service:** Hybrid pipeline (Week 5)
- **Attendance System:** CSV logging (Week 6)

### GUI Components
1. **Main Window** - Dashboard dengan webcam preview
2. **Register Window** - Form + auto capture 20 photos
3. **Attendance Window** - Real-time recognition
4. **Reports Window** - View & export records

## Webcam Integration

```python
import cv2
from PIL import Image, ImageTk
import threading

def update_webcam():
    while running:
        ret, frame = cap.read()
        # Convert BGR → RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert to PIL
        img = Image.fromarray(frame)
        # Convert to Tkinter
        imgtk = ImageTk.PhotoImage(image=img)
        # Update label
        webcam_label.configure(image=imgtk)
        
# Run in background thread
threading.Thread(target=update_webcam, daemon=True).start()
```

## Face Recognition Integration

```python
# In attendance window
result = recognition_service.recognize_face(frame)

if result['success']:
    name = result['name']
    confidence = result['confidence']
    
    # Auto mark attendance
    attendance_system.record_attendance(
        name=name,
        attendance_type='check_in',
        confidence=confidence,
        photo=frame
    )
```

## Langkah-Langkah

1. **Setup dataset (jika belum):**
   ```bash
   cd ../..
   python setup_week7.py
   # Pilih option 1 atau 2
   ```

2. **Run complete GUI:**
   ```bash
   cd learning/lesson-2
   python main.py
   ```

3. **Test semua fitur:**
   - Main dashboard → lihat webcam preview
   - Register → capture new person
   - Attendance → mark check-in/out
   - Reports → view & export

## Threading untuk Non-Blocking UI

GUI harus responsive, jadi webcam & recognition jalan di background:

```python
# Webcam thread
webcam_thread = threading.Thread(target=update_webcam, daemon=True)
webcam_thread.start()

# Recognition thread (untuk Attendance window)
recognition_thread = threading.Thread(target=process_recognition, daemon=True)
recognition_thread.start()
```

## Multi-Window Management

```python
# From main window
def open_register():
    # Create new top-level window
    register_window = tk.Toplevel(root)
    # Initialize RegisterWindow class
    RegisterWindow(register_window, self)

# Close handler
def on_closing():
    # Stop threads
    webcam_running = False
    # Release camera
    cap.release()
    # Destroy window
    window.destroy()
```

## Key Concepts

- **Threading:** Non-blocking webcam
- **PIL/ImageTk:** Display OpenCV frames
- **Toplevel:** Multiple windows
- **Callbacks:** Pass references antara windows
- **Integration:** Combine backend modules

## What's Next?

- **Lesson 3:** Testing, debugging, deployment
- **Project folder:** Production-ready code

## Troubleshooting

**Webcam tidak muncul:**
```bash
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

**Import errors:**
```bash
pip install opencv-python pillow mediapipe deepface
```

**Slow performance:**
- Close other apps using webcam
- Reduce FPS (change sleep time)
- Use better lighting

