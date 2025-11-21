# Minggu 5 - Learning: Recognition System Integration

## 📚 Overview
Folder ini berisi 2 tutorial files untuk integrate semua components (detector, recognizer, dataset manager) menjadi complete recognition system dengan performance optimization.

## 📁 File Structure

```
learning/
├── README.md (file ini)
├── 02_system_integration.py
└── 03_performance_optimization.py
```

---

## 🎯 Tutorial Files - Detailed Guide

### 02_system_integration.py
**Tujuan:** Combine semua modules menjadi unified recognition service

**Apa yang dipelajari:**
- Component initialization dan configuration
- Service architecture design
- Recognition pipeline flow
- Error handling strategy
- Logging dan monitoring
- Multiple camera support

**Cara menggunakan:**
```bash
cd minggu-5-recognition-system/learning
python 02_system_integration.py
```

**Output yang diharapkan:**
- Recognition service started
- Webcam feed dengan real-time recognition
- Names displayed dengan confidence
- FPS counter
- Log messages untuk tracking

**System architecture:**
```
┌─────────────────────────────────────┐
│     Recognition Service             │
├─────────────────────────────────────┤
│  ┌──────────┐  ┌─────────────────┐ │
│  │ Detector │  │   Recognizer    │ │
│  └──────────┘  └─────────────────┘ │
│  ┌──────────┐  ┌─────────────────┐ │
│  │ Dataset  │  │  Image Utils    │ │
│  │ Manager  │  │                 │ │
│  └──────────┘  └─────────────────┘ │
└─────────────────────────────────────┘
          │
          ▼
    [Webcam Input] → [Recognition] → [Display/Save]
```

**Code structure:**
```python
from face_detector import FaceDetector
from face_recognizer import FaceRecognizer
from dataset_manager import DatasetManager
import logging

class RecognitionService:
    def __init__(self, dataset_path='dataset/'):
        # Initialize components
        self.detector = FaceDetector()
        self.recognizer = FaceRecognizer()
        self.dataset_manager = DatasetManager(dataset_path)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Load known faces
        self._load_database()
    
    def _load_database(self):
        """Load all known face encodings from dataset"""
        self.logger.info("Loading face database...")
        
        all_people = self.dataset_manager.get_person_info('all')
        for person in all_people:
            encodings_path = f"{person['folder']}/encodings.pkl"
            if os.path.exists(encodings_path):
                self.recognizer.load_encodings(
                    person['person_id'],
                    encodings_path
                )
        
        self.logger.info(f"Loaded {len(all_people)} people")
    
    def recognize_frame(self, frame):
        """
        Main recognition pipeline
        
        Args:
            frame: Input image
            
        Returns:
            results: List of (name, confidence, bbox)
        """
        # Step 1: Detect faces
        faces = self.detector.detect_faces(frame)
        
        results = []
        for face in faces:
            x, y, w, h = face
            
            # Step 2: Extract face ROI
            face_roi = frame[y:y+h, x:x+w]
            
            # Step 3: Recognize
            name, confidence = self.recognizer.recognize_face(face_roi)
            
            # Step 4: Collect results
            results.append({
                'name': name,
                'confidence': confidence,
                'bbox': (x, y, w, h)
            })
            
            self.logger.debug(f"Detected: {name} ({confidence:.2f})")
        
        return results
    
    def start_recognition(self, camera_id=0):
        """Start real-time recognition"""
        self.logger.info(f"Starting recognition on camera {camera_id}")
        
        cap = cv2.VideoCapture(camera_id)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Run recognition
            results = self.recognize_frame(frame)
            
            # Draw results
            for result in results:
                x, y, w, h = result['bbox']
                name = result['name']
                conf = result['confidence']
                
                # Draw box
                color = (0, 255, 0) if name != 'Unknown' else (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                
                # Draw label
                label = f"{name} ({conf:.2f})"
                cv2.putText(frame, label, (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            cv2.imshow('Recognition Service', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        self.logger.info("Recognition stopped")

# Usage
if __name__ == '__main__':
    service = RecognitionService(dataset_path='../project/dataset/')
    service.start_recognition()
```

**Component integration:**

**1. Detector + Recognizer:**
```python
# Detect first, then recognize
faces = detector.detect_faces(frame)
for face in faces:
    x, y, w, h = face
    face_roi = frame[y:y+h, x:x+w]
    name, conf = recognizer.recognize_face(face_roi)
```

**2. Dataset Manager integration:**
```python
# Reload database when dataset updated
def reload_database(self):
    self.recognizer.clear_database()
    self._load_database()
    self.logger.info("Database reloaded")
```

**3. Configuration management:**
```python
class RecognitionService:
    def __init__(self, config_path='config.json'):
        # Load config
        with open(config_path) as f:
            self.config = json.load(f)
        
        # Initialize with config
        self.detector = FaceDetector(
            scale_factor=self.config['detector']['scale_factor']
        )
        self.recognizer = FaceRecognizer(
            tolerance=self.config['recognizer']['tolerance']
        )
```

**Error handling:**
```python
def recognize_frame(self, frame):
    try:
        faces = self.detector.detect_faces(frame)
        # ... recognition logic
    except Exception as e:
        self.logger.error(f"Recognition error: {e}")
        return []
```

**Performance tracking:**
```python
import time

def recognize_frame(self, frame):
    start_time = time.time()
    
    # ... recognition
    
    elapsed = time.time() - start_time
    self.logger.debug(f"Frame processed in {elapsed:.3f}s")
    
    return results
```

---

### 03_performance_optimization.py
**Tujuan:** Optimize recognition system untuk real-time performance

**Apa yang dipelajari:**
- Performance bottleneck identification
- Frame processing optimization
- Multi-threading untuk camera feed
- Recognition caching strategies
- Memory management
- FPS optimization techniques

**Cara menggunakan:**
```bash
python 03_performance_optimization.py
```

**Output yang diharapkan:**
- Before optimization: ~5-10 FPS
- After optimization: 20-30 FPS
- Reduced CPU usage
- Smooth real-time recognition

**Performance metrics:**
```python
import time
from collections import deque

class PerformanceMonitor:
    def __init__(self, window_size=30):
        self.frame_times = deque(maxlen=window_size)
    
    def start_frame(self):
        self.frame_start = time.time()
    
    def end_frame(self):
        elapsed = time.time() - self.frame_start
        self.frame_times.append(elapsed)
    
    def get_fps(self):
        if len(self.frame_times) == 0:
            return 0
        avg_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_time if avg_time > 0 else 0
    
    def get_stats(self):
        return {
            'fps': self.get_fps(),
            'avg_frame_time': sum(self.frame_times) / len(self.frame_times),
            'min_frame_time': min(self.frame_times),
            'max_frame_time': max(self.frame_times)
        }
```

**Optimization techniques:**

**1. Frame skipping:**
```python
# Process every Nth frame only
frame_count = 0
process_every_n_frames = 3

while True:
    ret, frame = cap.read()
    frame_count += 1
    
    if frame_count % process_every_n_frames == 0:
        # Run expensive recognition
        results = service.recognize_frame(frame)
    
    # Always draw last results
    draw_results(frame, results)
```

**2. Resolution downscaling:**
```python
# Process smaller frame, display original
def recognize_frame_optimized(self, frame):
    # Downscale for processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    
    # Detect on small frame
    faces = self.detector.detect_faces(small_frame)
    
    # Scale coordinates back up
    results = []
    for face in faces:
        x, y, w, h = face
        # Scale back to original
        x, y, w, h = x*2, y*2, w*2, h*2
        
        # Extract from original frame for recognition
        face_roi = frame[y:y+h, x:x+w]
        name, conf = self.recognizer.recognize_face(face_roi)
        results.append({'name': name, 'confidence': conf, 'bbox': (x,y,w,h)})
    
    return results
```

**3. Result caching:**
```python
from collections import defaultdict
import time

class RecognitionCache:
    def __init__(self, cache_duration=1.0):
        self.cache = defaultdict(lambda: {'name': None, 'time': 0})
        self.cache_duration = cache_duration
    
    def get(self, face_encoding):
        # Simple location-based cache key
        cache_key = hash(face_encoding.tobytes())
        
        cached = self.cache[cache_key]
        if time.time() - cached['time'] < self.cache_duration:
            return cached['name']
        return None
    
    def set(self, face_encoding, name):
        cache_key = hash(face_encoding.tobytes())
        self.cache[cache_key] = {
            'name': name,
            'time': time.time()
        }

# Usage in recognition
def recognize_with_cache(self, face_roi):
    encoding = self.recognizer.encode_face(face_roi)
    
    # Check cache first
    cached_name = self.cache.get(encoding)
    if cached_name:
        return cached_name, 1.0  # High confidence from cache
    
    # Not in cache, do full recognition
    name, conf = self.recognizer.recognize_face(face_roi)
    
    # Store in cache
    self.cache.set(encoding, name)
    
    return name, conf
```

**4. Multi-threading:**
```python
from threading import Thread
from queue import Queue

class ThreadedCamera:
    def __init__(self, camera_id=0):
        self.cap = cv2.VideoCapture(camera_id)
        self.queue = Queue(maxsize=1)
        self.stopped = False
        
        # Start thread
        Thread(target=self._reader, daemon=True).start()
    
    def _reader(self):
        while not self.stopped:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Keep only latest frame
            if not self.queue.empty():
                try:
                    self.queue.get_nowait()
                except:
                    pass
            
            self.queue.put(frame)
    
    def read(self):
        return self.queue.get()
    
    def stop(self):
        self.stopped = True
        self.cap.release()

# Usage
camera = ThreadedCamera(0)
while True:
    frame = camera.read()  # Always latest frame
    results = service.recognize_frame(frame)
    # ... display
```

**5. Face tracking (avoid re-recognition):**
```python
class FaceTracker:
    def __init__(self, max_disappeared=30):
        self.next_id = 0
        self.objects = {}  # id -> (centroid, name)
        self.disappeared = {}  # id -> frame count
        self.max_disappeared = max_disappeared
    
    def register(self, centroid, name):
        self.objects[self.next_id] = (centroid, name)
        self.disappeared[self.next_id] = 0
        self.next_id += 1
    
    def deregister(self, object_id):
        del self.objects[object_id]
        del self.disappeared[object_id]
    
    def update(self, bboxes, names):
        # Match bboxes to existing tracked objects
        # Only recognize new/unmatched faces
        # Details: implement centroid tracking algorithm
        pass
```

**Complete optimized system:**
```python
class OptimizedRecognitionService(RecognitionService):
    def __init__(self, dataset_path='dataset/'):
        super().__init__(dataset_path)
        
        # Optimization components
        self.perf_monitor = PerformanceMonitor()
        self.cache = RecognitionCache(cache_duration=2.0)
        self.face_tracker = FaceTracker()
        
        # Settings
        self.process_every_n_frames = 3
        self.scale_factor = 0.5
    
    def start_recognition(self, camera_id=0):
        camera = ThreadedCamera(camera_id)
        frame_count = 0
        last_results = []
        
        while True:
            self.perf_monitor.start_frame()
            
            # Get latest frame
            frame = camera.read()
            frame_count += 1
            
            # Process every Nth frame
            if frame_count % self.process_every_n_frames == 0:
                last_results = self.recognize_frame_optimized(frame)
            
            # Always draw (even if not processed)
            display_frame = frame.copy()
            for result in last_results:
                self._draw_result(display_frame, result)
            
            # Show FPS
            fps = self.perf_monitor.get_fps()
            cv2.putText(display_frame, f"FPS: {fps:.1f}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow('Optimized Recognition', display_frame)
            
            self.perf_monitor.end_frame()
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        camera.stop()
        cv2.destroyAllWindows()
```

**Benchmark results:**
```python
# Before optimization
- FPS: 8
- Frame time: 125ms
- CPU usage: 80%

# After optimization
- FPS: 28
- Frame time: 36ms
- CPU usage: 45%

Improvements:
- 3.5x faster FPS
- 55% lower frame time
- 44% less CPU usage
```

---

## 🎓 Best Practices

### System Design
- **Modular:** Keep components independent
- **Configurable:** Use config files, not hardcoded values
- **Logged:** Log important events and errors
- **Testable:** Each component testable separately

### Performance
- **Profile first:** Measure before optimizing
- **Optimize bottlenecks:** Focus on slowest parts
- **Balance quality/speed:** Trade accuracy for speed if needed
- **Monitor in production:** Track FPS and errors

### Integration
- **Error handling:** Graceful degradation
- **Resource cleanup:** Properly release cameras, close files
- **Version compatibility:** Check component versions
- **Documentation:** Document integration points

---

## ✅ Checklist Progress

```
[ ] 02_system_integration.py - Integrated all components successfully
[ ] 03_performance_optimization.py - Achieved 20+ FPS
[ ] Recognition service tested with multiple people
[ ] Error handling tested (camera disconnect, no faces, etc.)
[ ] Performance benchmarks recorded
[ ] Configuration file created
```

---

## 🐛 Common Issues & Solutions

**Low FPS (<10):**
- Enable frame skipping
- Downscale resolution
- Use smaller recognition model
- Implement caching

**Memory leak:**
- Release unused resources
- Clear caches periodically
- Limit queue sizes
- Use context managers

**Recognition lag:**
- Multi-threading for camera
- Async recognition processing
- Reduce recognition frequency
- Optimize encoding computation

**Component conflicts:**
- Check version compatibility
- Review initialization order
- Verify configuration values
- Check file paths

---

## 📖 Additional Resources

- Threading in Python: concurrent.futures, threading
- Performance profiling: cProfile, line_profiler
- OpenCV optimization: CUDA, OpenCL support
- Design patterns: Factory, Singleton, Observer

---

## ⏭️ Next Steps

Setelah minggu 5:

1. ✅ Recognition service running smoothly
2. ✅ 20+ FPS achieved
3. ✅ All components integrated
4. ✅ Lanjut ke **Minggu 6: Database & Attendance**

---

**Fast + Accurate = Great UX! ⚡**

*Performance optimization makes or breaks real-time systems!*
