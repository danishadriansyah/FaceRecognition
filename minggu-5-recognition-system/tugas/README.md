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
import mediapipe as mp
import pickle
import os
import cv2
import numpy as np

# Initialize MediaPipe
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh

def build_pipeline(dataset_path):
    encodings = []
    names = []
    
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)
    
    # Iterate through persons
    for person_name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_name)
        
        # Process each photo
        for photo in os.listdir(person_path):
            img_path = os.path.join(person_path, photo)
            img = cv2.imread(img_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Generate encoding using MediaPipe
            results = face_mesh.process(img_rgb)
            
            if results.multi_face_landmarks:
                # Extract landmarks as encoding
                landmarks = results.multi_face_landmarks[0]
                feature_vector = []
                for landmark in landmarks.landmark:
                    feature_vector.extend([landmark.x, landmark.y, landmark.z])
                
                encodings.append(np.array(feature_vector))
                names.append(person_name)
    
    face_mesh.close()
    
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
        
        # Use MediaPipe for detection
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detection_results = self.face_detection.process(rgb_frame)
        
        results = []
        if detection_results.detections:
            for detection in detection_results.detections:
                # Extract face region
                bbox = detection.location_data.relative_bounding_box
                h, w, _ = frame.shape
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                w_box = int(bbox.width * w)
                h_box = int(bbox.height * h)
                
                face_crop = frame[y:y+h_box, x:x+w_box]
                
                # Get encoding using face_recognizer
                encoding = self.recognizer.encode_face(face_crop)
                
                if encoding is not None:
                    # Fast comparison using numpy
                    distances = []
                    for known_enc in self.known_encodings:
                        dist = np.linalg.norm(known_enc - encoding)
                        distances.append(dist)
                    
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
                        'location': (y, x+w_box, y+h_box, x)
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
- MediaPipe optimization best practices
- Performance profiling tools

**Good luck! 🚀⚡**
