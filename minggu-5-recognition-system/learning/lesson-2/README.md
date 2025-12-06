# Lesson 2: Recognition Service & Real-time Recognition

## Tujuan
- Build RecognitionService class dengan hybrid approach
- Real-time webcam recognition (6-9 FPS)
- Load encodings from database
- Compare faces using distance threshold
- Performance optimization (caching, frame skipping)

## Hybrid Pipeline

```
┌─────────────────────────────────────────────────────┐
│         Real-time Recognition Pipeline              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Webcam Frame (640x480)                            │
│       ↓                                             │
│  MediaPipe Detection (10-15ms)                     │
│       ↓                                             │
│  Face Found? → Crop face region                    │
│       ↓                                             │
│  DeepFace Encoding (100-150ms)                     │
│       ↓                                             │
│  Compare with Database (Euclidean distance)        │
│       ↓                                             │
│  Best Match? → person_id + confidence              │
│       ↓                                             │
│  Draw box + name on frame                          │
│                                                     │
│  Total: 110-165ms per face = 6-9 FPS              │
└─────────────────────────────────────────────────────┘
```

## Files
1. **`recognition_service.py`** - Complete hybrid recognition service
2. **`main.py`** - Real-time webcam demo

## Yang Dipelajari
1. Load face encodings from database
2. Real-time face detection dengan MediaPipe
3. Generate encoding for unknown face dengan DeepFace
4. Compare encodings using Euclidean distance
5. Threshold tuning (balance false positives vs negatives)
6. Performance optimization:
   - Frame skipping (process every Nth frame)
   - Encoding caching (reuse detection results)
   - Batch processing (multiple faces)

## Recognition Algorithm

### Distance Comparison
```python
# Calculate Euclidean distance between two encodings
distance = np.linalg.norm(encoding1 - encoding2)

# Threshold: Lower = more strict
if distance <= threshold:
    # Match found!
    confidence = (1 - distance) * 100  # Convert to percentage
```

### Threshold Values
| Threshold | Behavior | Use Case |
|-----------|----------|----------|
| **0.4** | Very strict | High security (banking, access control) |
| **0.6** (Default) | Balanced | General purpose |
| **0.8** | Lenient | Large database, some false positives OK |

## Prerequisites
```bash
# All dependencies from Week 4-5
pip install opencv-python mediapipe deepface
```

**Database Requirements:**
- XAMPP MySQL running
- Database `face_recognition_db` dengan data
- Table `face_encodings` sudah berisi encodings (dari Lesson 1)
- Check di HeidiSQL: Pastikan ada encodings untuk setiap person

## Langkah
1. **Start XAMPP MySQL** (pastikan running)
2. **Check di HeidiSQL**: Table `face_encodings` harus ada data
3. **Complete Lesson 1 first** jika belum ada encodings
4. **Run recognition service**: `python main.py`
5. **Camera selection**: 
   - Script auto-detect available cameras
   - Info ditampilkan (nama, resolusi, FPS)
   - Camera akan dibuka otomatis untuk recognition
6. **Test with webcam** - Point camera at registered person
7. **Check results** - Name + confidence displayed
8. **Press 'q' to quit**

## Output
```
="*60
LESSON 2: Real-time Recognition Service
="*60

📊 Step 1: Initialize Recognition Service
✅ MediaPipe detector loaded
✅ DeepFace model loaded (Facenet512)

📊 Step 2: Load Encodings from Database
✅ Loaded 40 encodings for 2 persons
   - Alice (EMP0001): 20 encodings
   - Bob (EMP0002): 20 encodings

📊 Step 3: Start Real-time Recognition
Camera resolution: 640x480
Press 'q' to quit

[Webcam opens]
Frame 0010: 1 face detected
   ✅ Alice (87.3% confidence) - 0.138s

Frame 0025: 1 face detected
   ✅ Bob (92.1% confidence) - 0.145s

Frame 0040: 1 face detected
   ❌ Unknown person (confidence < 75%)

Performance Stats:
   Total frames: 120
   Faces detected: 45
   Recognized: 42 (93.3%)
   Unknown: 3 (6.7%)
   Avg FPS: 7.2
```

## Performance Tips

### 1. Frame Skipping
```python
# Process every 3rd frame (3x faster, still smooth)
if frame_count % 3 == 0:
    recognize_faces(frame)
```

### 2. Encoding Cache
```python
# Don't re-generate encoding for same face
cache = {}  # {face_hash: encoding}
if face_hash in cache:
    encoding = cache[face_hash]
```

### 3. Region of Interest (ROI)
```python
# Only process center region (where user likely is)
roi = frame[100:380, 160:480]  # Center region
```

## Code Structure

### RecognitionService Class
```python
class RecognitionService:
    def __init__(self, db_connection_string):
        # Initialize detector, encoder, database
        
    def load_encodings(self):
        # Load from database
        
    def recognize_face(self, image, bbox):
        # Main recognition method
        # Returns: (person_id, name, confidence)
        
    def process_webcam(self):
        # Real-time webcam loop
```

## Why This Matters
- **Production-ready:** 6-9 FPS is real-time for attendance
- **Accurate:** 97%+ recognition rate vs 85% MediaPipe-only
- **Scalable:** Can handle 100+ persons in database
- **Robust:** Handles unknown faces gracefully
- **Tunable:** Adjust threshold based on security needs

## Next: Week 6
Build **Attendance System** dengan automatic check-in/check-out!
