# Lesson 2: Real-Time Face Recognition dari Webcam

## Tujuan
1️⃣ Load face database yang sama dari Lesson 1  
2️⃣ Capture live video dari webcam  
3️⃣ Recognize faces secara real-time dengan frame caching  
4️⃣ Display live statistics (FPS, face count, confidence)  
5️⃣ Capture snapshots dari live stream  

## Perbedaan Lesson 1 vs 2

| Aspek | Lesson 1 | Lesson 2 |
|-------|----------|----------|
| **Input** | Static image (1 frame) | Video stream (~30 fps) |
| **Speed Requirement** | Slow OK (seconds) | Fast (real-time) |
| **Optimization** | None needed | Frame caching required |
| **Output** | Single result image | Live video + snapshots |
| **Faces** | Few | Multiple simultaneous |

## Performa & Optimization

### Frame Caching Strategy
- Process **every 3rd frame** untuk detection
- Cache hasil untuk 2 frame berikutnya
- Hasil: **30+ FPS** dengan akurasi tinggi

### Why Frame Caching?
```
Without caching:    With caching:
 0ms: detect         0ms: detect
 30ms: detect        30ms: (from cache)
 60ms: detect        60ms: (from cache)
 90ms: detect        90ms: detect
```

**Hasil:** 3x lebih cepat dengan minimal accuracy loss

## Setup

**Persyaratan:**
1. Sudah selesai Lesson 1 (punya `known_faces/` folder)
2. Webcam tersedia dan working
3. Good lighting (penting untuk face detection)

**Permission (Windows):**
- Buka Settings → Privacy → Camera
- Aktifkan camera untuk Python/terminal

## Langkah Praktik

**Run Program:**
```bash
python main.py
```

**Expected Output:**
```
1️⃣  Initializing recognizer...
   ✅ FaceRecognizer ready

2️⃣  Loading known faces...
   ✅ alice: 2 face(s)
   ✅ bob: 2 face(s)
   📊 Total loaded: 4 faces

3️⃣  Opening webcam...
   ✅ Webcam ready

🎮 LIVE RECOGNITION
FPS: 32.5 | Faces: 2 | Frame: 156
```

**Live Window:**
- Bounding boxes (green = matched, red = unknown)
- Nama + confidence score
- FPS counter di top-left
- Face count counter
- Frame counter
- Control tips di bottom

## Keyboard Controls

| Key | Action |
|-----|--------|
| **SPACE** | Capture screenshot to `output/` |
| **ESC** atau **Q** | Exit program |

## Understanding Output

### Live Statistics
- **FPS:** Frame per second (target 30+)
- **Faces:** Total faces detected in frame
- **Frame:** Total frames processed

### Bounding Boxes
- **Green box** = Known person (matched)
- **Red box** = Unknown person
- Label format: `NAME CONFIDENCE%`

### Snapshots
Ketika tekan SPACE:
```
📸 Captured: capture_1732273890.jpg
   - Faces: 2 (Matched: 1, Unknown: 1)
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Webcam tidak terbuka | Check permission, restart program, try different camera app |
| Low FPS (<20) | Reduce tolerance, skip more frames (change cache_interval) |
| No faces detected | Improve lighting, move closer, clear webcam lens |
| Wrong recognition | Retrain with better photos, adjust tolerance to 0.5-0.6 |

## Advanced Tips

**1. Adjust Tolerance:**
```python
recognizer = FaceRecognizer(tolerance=0.4)  # Stricter
# vs
recognizer = FaceRecognizer(tolerance=0.6)  # Looser
```

**2. Change Detection Frequency:**
```python
cache_interval = 3   # Current (detect every 3 frames)
cache_interval = 5   # Faster (detect every 5 frames, ~50 fps)
cache_interval = 1   # Accurate (detect every frame, ~15 fps)
```

**3. Adjust Resolution:**
```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)   # Faster
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # Current (balanced)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Slower but more accurate
```

## Performance Metrics

**Expected Performance:**
- **FPS:** 30-40 fps (dengan frame caching)
- **Latency:** ~100ms (3 frames)
- **CPU:** 30-50% (single core)
- **Memory:** ~200-300 MB

**Device Tested On:**
- Windows 11
- Intel i5/i7
- 8GB+ RAM
- USB webcam 1080p

## Challenge

✨ Upgrade program:
1. **Save video** - Record recognized stream ke MP4
2. **Statistics** - Track recognized person per session
3. **Alert system** - Beep ketika unknown person detected
4. **Multi-angle** - Use multiple webcams simultaneously
5. **Motion detection** - Only process when motion detected

## Key Takeaways

✅ Frame caching = key untuk real-time performance  
✅ 30+ FPS = user experience smooth  
✅ Tolerance tuning = balance accuracy vs false positives  
✅ Good lighting = crucial untuk face detection  
✅ Cache interval tuning = performance vs accuracy trade-off  

## Next: Lesson 3 (Advanced) - Multi-person Tracking & Analytics
