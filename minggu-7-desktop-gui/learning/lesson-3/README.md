# Lesson 3: Testing, Debugging & Deployment

## Tujuan
- Test semua komponen sistem
- Debug & fix issues yang ditemukan
- Performance testing (FPS, memory)
- Prepare untuk deployment
- Package sebagai executable (optional)

## Testing Checklist

### 1. Import & Dependencies
```bash
python -c "import tkinter; print('Tkinter OK')"
python -c "import cv2; print('OpenCV OK')"
python -c "import PIL; print('Pillow OK')"
python -c "import mediapipe; print('MediaPipe OK')"
```

### 2. File Structure
- ✅ Dataset folder exists
- ✅ Encodings.pkl exists
- ✅ Logs folder created
- ✅ All modules can be imported

### 3. Webcam Testing
```bash
# Test webcam detection
python main.py
# Check: Apakah semua cameras terdeteksi?
# Check: Info camera lengkap (nama, resolusi, FPS)?
```

### 4. GUI Components
- ✅ Main window opens
- ✅ Webcam preview working
- ✅ Register window opens
- ✅ Attendance window opens
- ✅ Reports window opens
- ✅ All buttons functional

### 5. Face Recognition
- ✅ Face detection working (green boxes)
- ✅ Recognition accuracy >90%
- ✅ Performance: 5-10 FPS minimum
- ✅ No lag/freeze

### 6. Database Operations
- ✅ Register person → saved to dataset
- ✅ Attendance recorded to CSV
- ✅ Reports loaded correctly
- ✅ Export CSV working

## Debugging Tips

### Webcam Issues
```python
# List all cameras
import cv2
for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i}: Found")
        cap.release()
```

### Memory Leaks
```python
# Check memory usage
import psutil
import os

process = psutil.Process(os.getpid())
print(f"Memory: {process.memory_info().rss / 1024**2:.2f} MB")
```

### Performance Profiling
```python
import time

start = time.time()
# Your code here
elapsed = time.time() - start
print(f"Elapsed: {elapsed:.3f}s")
```

## Performance Targets

| Component | Target | Actual |
|-----------|--------|--------|
| Face Detection | 30+ FPS | ??? |
| Recognition | 5-10 FPS | ??? |
| GUI Response | <100ms | ??? |
| Startup Time | <5s | ??? |
| Memory Usage | <500MB | ??? |

## Deployment (Optional)

### Option 1: PyInstaller
```bash
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed main_app.py

# Output: dist/main_app.exe
```

### Option 2: cx_Freeze
```bash
pip install cx_Freeze

# Create setup.py
python setup.py build

# Output: build/exe.win-amd64-3.x/
```

### Option 3: Distribution ZIP
```bash
# Package everything
1. Copy semua files ke folder baru
2. Include requirements.txt
3. Include README dengan instructions
4. Zip folder
```

## Common Issues & Solutions

**Issue:** Webcam lag/freeze
**Solution:** Reduce FPS, close other apps

**Issue:** Recognition inaccurate
**Solution:** Re-capture photos dengan better lighting

**Issue:** Import errors
**Solution:** `pip install -r requirements.txt`

**Issue:** Dataset kosong
**Solution:** Run `setup_week7.py` lagi

**Issue:** GUI tidak responsive
**Solution:** Check threading, pastikan daemon=True

## Final Checklist

Before considering project complete:

- [ ] All imports working
- [ ] Dataset populated dengan minimal 2-3 persons
- [ ] Webcam detection & selection working
- [ ] All GUI windows functional
- [ ] Face recognition accuracy >85%
- [ ] Performance acceptable (5+ FPS)
- [ ] No crashes or major bugs
- [ ] CSV logging working
- [ ] Reports generation working
- [ ] Export functionality working

## Langkah

1. **Run test suite:**
   ```bash
   python main.py
   ```

2. **Test each component:**
   - Camera detection
   - Face detection
   - Recognition accuracy
   - GUI responsiveness

3. **Fix any issues found**

4. **Verify system ready untuk production**

## 🎉 Congratulations!

Kamu sudah menyelesaikan **7 minggu pembelajaran**!

✅ Python basics & image processing
✅ Face detection dengan MediaPipe
✅ Face recognition dengan DeepFace
✅ Dataset management
✅ Hybrid recognition system
✅ Attendance system backend
✅ **Desktop GUI application!**

## Next Step: Build Your Own!

Sekarang waktunya build **attendance system sendiri** dari scratch menggunakan semua ilmu yang sudah dipelajari!

**Final Project Goals:**
- Design your own GUI
- Choose your own features
- Optimize performance
- Add custom functionality
- Deploy to users!

Good luck! 🚀

