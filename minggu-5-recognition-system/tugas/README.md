# 📝 TUGAS MINGGU 5 - Recognition System

## Deskripsi
Buat complete face recognition pipeline dengan optimization dan performance monitoring.

---

## 🎯 Objektif
- Build end-to-end recognition pipeline
- Dataset → Encodings → Recognition
- Performance optimization
- Metrics & monitoring
- Production-ready system

---

## 📋 Tugas: Optimized Recognition Pipeline

Buat program `recognition_pipeline.py` dengan fitur:

### Fitur Wajib

1. **Pipeline Builder**
   - Load dataset dari folder structure
   - Generate encodings untuk semua persons
   - Save encodings (pickle format)
   - Progress tracking

2. **Recognition Service**
   - Fast recognition (<100ms per frame)
   - Batch processing support
   - Confidence thresholds
   - Unknown person handling

3. **Performance Optimization**
   - Frame skip untuk real-time (process every N frames)
   - Face location caching
   - Model selection (HOG vs CNN)
   - Multi-threading support

4. **Metrics & Monitoring**
   - FPS counter (real-time)
   - Recognition accuracy
   - Processing time per face
   - Memory usage
   - Statistics dashboard

---

## 📦 Deliverables

```
tugas/
├── recognition_pipeline.py    # Main pipeline
├── dataset/                   # Source faces
│   ├── person1/
│   ├── person2/
│   └── ...
├── encodings/                 # Generated encodings
│   └── face_encodings.pkl
├── logs/                      # Performance logs
│   └── metrics_20251118.log
├── output/                    # Recognition results
└── README.md
```

---

## 🎯 Example Output

### Pipeline Building:
```
========================================
   RECOGNITION PIPELINE BUILDER
========================================

Step 1: Loading dataset...
Found 5 persons with 87 total photos

Step 2: Generating encodings...
[████████████████████] 100%
✅ person1: 18/18 photos processed
✅ person2: 20/20 photos processed
✅ person3: 15/15 photos processed
✅ person4: 17/17 photos processed
✅ person5: 17/17 photos processed

Step 3: Saving encodings...
✅ Saved to: encodings/face_encodings.pkl

Summary:
--------
Total persons: 5
Total encodings: 87
Success rate: 100%
Build time: 23.4s
Average: 0.27s per encoding
```

### Real-time Recognition:
```
========================================
   REAL-TIME RECOGNITION
========================================

Performance Metrics:
--------------------
FPS: 28.5
Detection time: 15ms
Recognition time: 32ms
Total latency: 47ms

Recognized Faces:
-----------------
✅ Andi (94.2% confidence)
✅ Budi (89.7% confidence)
❌ Unknown Person

Press 's' to save, 'q' to quit
```

### Performance Report:
```
PERFORMANCE REPORT
==================
Date: 2025-11-18 15:30:00
Duration: 5 minutes

FPS Statistics:
---------------
Average FPS: 27.3
Min FPS: 22.1
Max FPS: 31.8

Recognition Stats:
------------------
Total faces: 145
Recognized: 132 (91.0%)
Unknown: 13 (9.0%)

Processing Time:
----------------
Avg per frame: 35ms
Avg per face: 28ms

Memory Usage:
-------------
Peak: 256 MB
Average: 198 MB
```

---

## 💡 Hints & Tips

### Build Pipeline
```python
import face_recognition
import pickle
import os

def build_pipeline(dataset_path):
    encodings = []
    names = []
    
    # Iterate through persons
    for person_name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_name)
        
        # Process each photo
        for photo in os.listdir(person_path):
            img_path = os.path.join(person_path, photo)
            img = face_recognition.load_image_file(img_path)
            
            # Generate encoding
            enc = face_recognition.face_encodings(img)
            
            if len(enc) > 0:
                encodings.append(enc[0])
                names.append(person_name)
    
    # Save
    data = {'encodings': encodings, 'names': names}
    with open('encodings/face_encodings.pkl', 'wb') as f:
        pickle.dump(data, f)
    
    return len(encodings)
```

### Optimized Recognition
```python
import time

class RecognitionService:
    def __init__(self, encoding_path):
        # Load encodings
        with open(encoding_path, 'rb') as f:
            data = pickle.load(f)
        
        self.known_encodings = data['encodings']
        self.known_names = data['names']
        self.frame_skip = 2  # Process every 2nd frame
        self.frame_count = 0
        self.last_recognized = {}
    
    def recognize_optimized(self, frame):
        self.frame_count += 1
        
        # Skip frames for performance
        if self.frame_count % self.frame_skip != 0:
            return self.last_recognized
        
        # Use HOG (faster than CNN)
        face_locations = face_recognition.face_locations(
            frame, 
            model='hog'
        )
        
        face_encodings = face_recognition.face_encodings(
            frame, 
            face_locations
        )
        
        results = []
        for encoding, location in zip(face_encodings, face_locations):
            # Fast comparison
            distances = face_recognition.face_distance(
                self.known_encodings, 
                encoding
            )
            
            best_match = np.argmin(distances)
            
            if distances[best_match] < 0.5:  # Threshold
                name = self.known_names[best_match]
                confidence = (1 - distances[best_match]) * 100
            else:
                name = "Unknown"
                confidence = 0
            
            results.append({
                'name': name,
                'confidence': confidence,
                'location': location
            })
        
        self.last_recognized = results
        return results
```

### FPS Counter
```python
class FPSCounter:
    def __init__(self):
        self.start_time = time.time()
        self.frame_count = 0
    
    def update(self):
        self.frame_count += 1
    
    def get_fps(self):
        elapsed = time.time() - self.start_time
        return self.frame_count / elapsed if elapsed > 0 else 0
```

### Performance Logger
```python
import logging
from datetime import datetime

def setup_logger():
    log_file = f"logs/metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(message)s'
    )
    
    return logging.getLogger()

# Usage
logger = setup_logger()
logger.info(f"FPS: {fps:.1f}, Faces: {face_count}, Latency: {latency:.2f}ms")
```

---

## ✅ Kriteria Penilaian

| Kriteria | Bobot | Poin |
|----------|-------|------|
| Pipeline builder | 20% | 20 |
| Recognition accuracy (>90%) | 25% | 25 |
| Performance (>20 FPS) | 20% | 20 |
| Optimization techniques | 15% | 15 |
| Metrics & monitoring | 15% | 15 |
| Documentation | 5% | 5 |

**Total: 100 points**

---

## 🌟 Fitur Bonus

- [ ] Multi-threading untuk faster processing
- [ ] GPU acceleration (if available)
- [ ] Adaptive frame skip (based on FPS)
- [ ] Face tracking (reduce re-recognition)
- [ ] Live metrics dashboard (matplotlib)
- [ ] Export metrics to CSV
- [ ] Comparison: HOG vs CNN performance
- [ ] Memory profiling

**+10 pts per fitur**

---

## ⏰ Deadline

**5 hari** setelah menyelesaikan Minggu 5

---

## 🎓 Learning Outcomes

- ✅ Complete recognition pipeline
- ✅ Performance optimization
- ✅ Metrics collection
- ✅ Production considerations
- ✅ Scalability techniques

---

## 📚 Resources

- Minggu 5 Lesson 1 & 2
- `face_recognition` optimization docs
- Performance profiling tools

**Good luck! 🚀⚡**
