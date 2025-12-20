# Minggu 5 - Project: RecognitionService Class (File-Based Mode)

## 📚 Overview
Production-ready `RecognitionService` class dengan **file-based storage** (pickle + JSON). Mengintegrasikan semua modules dari Week 1-4 untuk membuat complete face recognition system tanpa database.

**🔥 Key Features:**
- ✅ File-based storage (Pickle for encodings, JSON for metadata)
- ✅ Auto-load encodings from pickle file
- ✅ Real-time face recognition
- ✅ Statistics tracking
- ✅ Modular design (compatible dengan Week 2-3 modules)
- ✅ No database setup required!

## 📁 Project Files

```
project/
├── README.md (file ini)
├── recognition_service.py ✨ (File-based service)
├── test_recognition.py (7 comprehensive tests)
├── dataset/ (dataset folder with encodings)
│   ├── encodings.pkl (face encodings)
│   ├── metadata.json (person info)
│   └── person_name/ (person folders)
└── image_utils.py (from Week 1)
```

**Note:** 
- `face_detector.py` dan `face_recognizer.py` di-import dari Week 2-3 project
- `dataset_manager.py` dapat digunakan untuk generate encodings (from Week 4)
## ⚠️ Prerequisites

**WAJIB diselesaikan sebelum menggunakan project ini:**

1. ✅ **Week 4 Complete** - Dataset with generated encodings
2. ✅ **Encodings File** - encodings.pkl must exist in dataset folder
3. ✅ **Dependencies Installed** - See requirements below

### Check Prerequisites:
```bash
# 1. Check dataset structure
ls dataset/
# Should see: encodings.pkl, metadata.json, person_name/

# 2. Check encodings file
python -c "import pickle; data=pickle.load(open('dataset/encodings.pkl','rb')); print(f'Loaded {len(data[\"encodings\"])} encodings')"

# 3. Check dependencies
pip list | findstr "opencv-python deepface mediapipe"
```

---

## 🎯 RecognitionService Class - Complete API

### Initialization

```python
from recognition_service import RecognitionService

# Basic initialization (uses default dataset path)
service = RecognitionService()

# Custom dataset path and tolerance
service = RecognitionService(
    dataset_path="dataset",
    tolerance=0.6
)
```

**Parameters:**
- `dataset_path` (str): Path to dataset folder (default: "dataset")
  - Must contain: encodings.pkl
- `tolerance` (float): Recognition distance threshold (default: 0.6)
  - Lower = stricter matching
  - Higher = more lenient matching

**What happens during initialization:**
1. ✅ Auto-initialize FaceDetector (Week 2 - MediaPipe)
2. ✅ Auto-initialize FaceRecognizer (Week 3 - DeepFace Facenet512)
3. ✅ Load known encodings from `encodings.pkl`
4. ✅ Initialize statistics tracking

### 1. reload_encodings()
**Purpose:** Reload face encodings from pickle file (useful after adding new persons)

```python
# Reload encodings after updating dataset
service.reload_encodings()
```

**Returns:** `bool` - True if successful

**Use case:** After adding new persons to dataset folder

---

### 2. process_image()
**Purpose:** Process single image untuk face recognition

```python
import cv2

# Load image
image = cv2.imread('test_image.jpg')

# Process
result = service.process_image(image, return_faces=True)

print(f"Found {result['count']} people")
for person in result['people']:
    print(f"  - {person['name']} (confidence: {person['confidence']:.2f})")
```

**Parameters:**
- `image` (np.ndarray): Input image (BGR format)
- `return_faces` (bool): Include cropped face images in result (default: True)

**Returns:** `dict`
```python
{
    "people": [
        {
            "face_idx": 0,
            "person_id": 1,
            "name": "Alice",
            "confidence": 0.87,
            "position": {"x": 100, "y": 50, "w": 150, "h": 150}
        }
    ],
    "count": 1,
    "timestamp": "2024-01-15T10:30:00",
    "faces": [face_image_array]  # if return_faces=True
}
```

**Pipeline:**
1. FaceDetector finds faces in image
2. Crop face regions
3. FaceRecognizer generates encodings
4. Compare with known encodings from database
5. Find best match using Euclidean distance
6. Return results with confidence scores

---

### 3. process_webcam_frame()
**Purpose:** Process single webcam frame dengan visualization

```python
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Process frame with visualization
    annotated_frame, results = service.process_webcam_frame(
        frame, 
        draw_boxes=True,
        draw_labels=True
    )
    
    cv2.imshow('Recognition', annotated_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

**Parameters:**
- `frame` (np.ndarray): Input webcam frame
- `draw_boxes` (bool): Draw bounding boxes (default: True)
- `draw_labels` (bool): Draw name + confidence labels (default: True)

**Returns:** `tuple`
```python
(annotated_frame, results)

# annotated_frame: Frame dengan boxes dan labels
# results: List of recognized people (same format as process_image)
```

**Visual Output:**
- Green boxes: Known people
- Red boxes: Unknown people
- Labels: Name + confidence percentage

---

### 4. get_statistics()
**Purpose:** Get recognition statistics

```python
stats = service.get_statistics()

print(f"Total processed: {stats['total_processed']}")
print(f"Recognition rate: {stats['recognition_rate']:.1%}")
```

**Returns:** `dict`
```python
{
    "total_processed": 150,
    "total_recognized": 120,
    "total_unknown": 30,
    "recognition_rate": 0.8,  # 80%
    "avg_processing_time": 0.145  # seconds per frame
}
```

---

### 5. reset_statistics()
**Purpose:** Reset all statistics counters

```python
service.reset_statistics()
```

**Effect:** Resets all counters to 0

---

### 7. get_timestamp()
**Purpose:** Get current timestamp in ISO format

```python
timestamp = service.get_timestamp()
# Returns: "2024-01-15T10:30:00"
```

**Returns:** `str` - ISO format timestamp

---

## 🗄️ Database Integration

### Schema Usage

RecognitionService uses these data files from Week 4:

**File Structure:**
```
dataset/
├── encodings.pkl          # Pickle file with face encodings
│   - encodings: List[ndarray]  # 512-d vectors
│   - names: List[str]          # Person names
│   - person_ids: List[str]     # Person IDs
│
├── metadata.json          # Person metadata
│   {
│     "persons": [
│       {
│         "id": "PERSON001",
│         "name": "John Doe",
│         "department": "IT",
│         "registered_date": "2024-01-15"
│       }
│     ]
│   }
│
└── person_id/             # Person photo folders
    ├── face_0.jpg
    ├── face_1.jpg
    └── ...
```

### File Operations

**On Initialization:**
1. Load encodings from `encodings.pkl` file
2. Load person metadata from `metadata.json`
3. Store encodings in memory for fast matching

**During Recognition:**
1. Generate encoding for detected face
2. Compare with in-memory encodings (Euclidean distance)
3. Find best match below threshold
4. Return person_id, name, confidence

**Storage:**
- Encodings stored in `dataset/encodings.pkl` (pickle format)
- Metadata stored in `dataset/metadata.json`
- Fast loading on startup (no database connection needed)

---

## 🔗 Integration dengan Learning

### Learning → Project Flow

**Learning Lesson 1:**
- Generate encodings for all persons
- Store to `encodings.pkl` file
- **Output:** Pickle file dengan encodings siap pakai

**Learning Lesson 2:**
- Build RecognitionService for real-time
- Load encodings from pickle file
- **Output:** Working real-time recognition

**Project (This):**
- Production-ready RecognitionService class
- Same file-based backend as Learning
- **Output:** Reusable module untuk Week 6-7

### Code Reuse

```python
# Learning Lesson 2 approach (simple demo)
from recognition_service import RecognitionService
service = RecognitionService(db_connection_string=...)
service.run_webcam()

# Project approach (production-ready, auto-initialized)
from recognition_service import RecognitionService

service = RecognitionService()
# FaceDetector & FaceRecognizer are auto-initialized!

# Process images immediately
result = service.process_image(image)
```

---

## 📊 Performance Characteristics

### Speed Benchmarks

**Single Face Recognition:**
- Detection (Week 2 detector): ~10-20ms
- Encoding generation (Week 3): ~100-150ms
- Database matching: ~1-2ms
- **Total: ~110-170ms per face**

**Multi-Face Recognition:**
- Detection: ~10-20ms (finds all faces)
- Per face encoding: ~100-150ms each
- **Total: ~110ms + (150ms × num_faces)**

**Real-time Performance:**
- Single person: 6-9 FPS ✅
- Two people: 3-4 FPS
- Three+ people: <3 FPS (consider frame skipping)

### Memory Usage

**Baseline:**
- RecognitionService: ~50MB
- Per person (1 encoding): ~2KB
- 100 persons: ~50MB + 200KB = ~50.2MB

**With modules loaded:**
- FaceDetector: +10MB
- FaceRecognizer: +30MB
- **Total for 100 persons: ~90MB**

---

## 🧪 Testing

### Running Tests

```bash
cd minggu-5-recognition-system/project
python test_recognition.py
```

### Test Suite (7 tests)

```python
# test_recognition.py includes:

1. test_service_initialization()
   ✅ Encodings file loaded
   ✅ Person metadata loaded
   ✅ FaceDetector auto-loaded (MediaPipe)
   ✅ FaceRecognizer auto-loaded (DeepFace)

2. test_find_best_match()
   ✅ Encoding matching logic
   ✅ Distance calculation
   ✅ Confidence scoring

3. test_process_image()
   ✅ Image processing pipeline
   ✅ Result format correct

4. test_webcam_frame_processing()
   ✅ Frame annotation
   ✅ Visualization working

5. test_statistics()
   ✅ Stats tracking
   ✅ Recognition rate calculation

6. test_database_integration()
   ✅ Database connectivity
   ✅ Data retrieval

7. test_reset_statistics()
   ✅ Counter reset working
```

**Expected output:**
```
============================================================
WEEK 5 - RECOGNITION SERVICE TESTS (Database Mode)
============================================================

Test 1: Service Initialization (Database Mode)
--------------------------------------------------
✅ RecognitionService initialized with database
   - Storage: File-based (encodings.pkl)
   - Tolerance: 0.6
   - Known encodings: 0

Test 2: Detector & Recognizer Setup
--------------------------------------------------
✅ Detection and recognition modules set up
   - FaceDetector mock: Ready
   - FaceRecognizer mock: Ready

...

============================================================
ALL TESTS COMPLETED
============================================================
```

---

## 💡 Usage Examples

### Example 1: Basic Image Recognition

```python
from recognition_service import RecognitionService
import cv2

# Initialize (detector & recognizer auto-loaded)
service = RecognitionService()

# Process image
image = cv2.imread('group_photo.jpg')
result = service.process_image(image)

# Display results
print(f"Found {result['count']} people:")
for person in result['people']:
    if person['person_id']:
        print(f"  ✅ {person['name']} ({person['confidence']:.0%})")
    else:
        print(f"  ❓ Unknown person")
```

### Example 2: Real-time Webcam Recognition

```python
from recognition_service import RecognitionService
import cv2

# Initialize (detector & recognizer auto-loaded)
service = RecognitionService()

# Open webcam
cap = cv2.VideoCapture(0)

print("Press 'q' to quit, 's' for statistics")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Process frame
    annotated, results = service.process_webcam_frame(frame)
    
    # Display
    cv2.imshow('Recognition', annotated)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        stats = service.get_statistics()
        print(f"\nStats: {stats['total_recognized']}/{stats['total_processed']} recognized")

cap.release()
cv2.destroyAllWindows()

# Final stats
stats = service.get_statistics()
print(f"\nFinal recognition rate: {stats['recognition_rate']:.1%}")
```

### Example 3: Custom Threshold Testing

```python
from recognition_service import RecognitionService
from face_detector import FaceDetector
from face_recognizer import FaceRecognizer
import cv2

# Test different thresholds
thresholds = [0.4, 0.6, 0.8]
image = cv2.imread('test.jpg')

for threshold in thresholds:
    service = RecognitionService(tolerance=threshold)
    
    result = service.process_image(image)
    
    print(f"\nThreshold {threshold}:")
    for person in result['people']:
        print(f"  {person['name']} ({person['confidence']:.2f})")
```

---

## 🐛 Troubleshooting

### Common Issues

**❌ "Cannot load encodings.pkl"**
```
Solution:
1. Check if dataset/encodings.pkl file exists
2. Complete Week 5 Learning Lesson 1 to generate encodings
3. Verify pickle file is not corrupted
4. Check file permissions
```

**❌ "No encodings found"**
```
Solution:
1. Complete Week 5 Learning Lesson 1 first
2. Check encodings.pkl file size (should not be 0 bytes)
3. Verify dataset folder has person folders with photos
4. Regenerate encodings if needed
```

**❌ "FaceDetector/FaceRecognizer not initialized"**
```
Solution:
Check error message during initialization:
⚠️  FaceDetector initialization warning: ...
⚠️  FaceRecognizer initialization warning: ...

Install missing dependencies:
pip install mediapipe==0.10.8
pip install deepface==0.0.89 tensorflow==2.15.0
```

**❌ "All faces showing as 'Unknown'"**
```
Solution:
1. Check if encodings loaded: len(service.known_encodings)
2. Try lower threshold: RecognitionService(tolerance=0.8)
3. Regenerate encodings (Learning Lesson 1)
4. Check face image quality from Week 4
```

---

## 📚 Next Steps

### Week 6 Integration

RecognitionService akan digunakan di Week 6 untuk:

```python
# Week 6: Attendance System
from recognition_service import RecognitionService
from attendance_logger import AttendanceLogger

service = RecognitionService()
logger = AttendanceLogger(connection_string=...)

# Real-time attendance
while True:
    frame = get_webcam_frame()
    annotated, results = service.process_webcam_frame(frame)
    
    for person in results:
        if person['person_id']:
            logger.log_attendance(
                person_id=person['person_id'],
                timestamp=service.get_timestamp(),
                confidence=person['confidence']
            )
```

### Week 7 Integration

Desktop GUI application akan menggunakan RecognitionService sebagai backend.

---

## ✅ Checklist Completion

Before using in production:

- [ ] Week 4 complete (dataset with encodings.pkl)
- [ ] Learning Lesson 1 complete (encodings generated)
- [ ] encodings.pkl file exists in dataset folder
- [ ] All dependencies installed (opencv-python, deepface, mediapipe)
- [ ] Test suite passing (7/7 tests)
- [ ] MediaPipe & DeepFace installed
- [ ] Real-time recognition tested
- [ ] Threshold tuned for your use case

---

**Production-ready RecognitionService with database integration!** 🚀
# Quick benchmark
report = service.benchmark_performance()

# Detailed benchmark
report = service.benchmark_performance(
    duration=60,  # seconds
    camera_id=0,
    save_report=True,
    report_path='benchmark_report.json'
)
```

**Parameters:**
- `duration` (int): Benchmark duration in seconds (default: 30)
- `camera_id` (int): Camera to use (default: 0)
- `save_report` (bool): Save report to file (default: False)
- `report_path` (str): Report file path (optional)

**Returns:** `dict`
```python
{
    'duration': 60,
    'total_frames': 1680,
    'avg_fps': 28.0,
    'total_faces': 245,
    'avg_faces_per_frame': 0.15,
    'recognition_accuracy': 0.94,
    'avg_frame_time': 0.036,
    'cpu_usage_avg': 42.5,  # percent
    'memory_usage_mb': 320.5,
    'optimizations_enabled': ['caching', 'threading', 'frame_skipping']
}
```

---

### 10. export_recognition_log()
**Purpose:** Export recognition history

```python
# Export all logs
service.export_recognition_log('recognition_log.csv')

# Export with filters
service.export_recognition_log(
    output_path='recognition_log.csv',
    person_filter='Alice',  # Only Alice
    date_from='2025-11-01',
    date_to='2025-11-30'
)
```

**Parameters:**
- `output_path` (str): CSV file path
- `person_filter` (str): Filter by person name (optional)
- `date_from` (str): Start date YYYY-MM-DD (optional)
- `date_to` (str): End date YYYY-MM-DD (optional)

**CSV format:**
```csv
timestamp,name,confidence,source,location
2025-11-14 10:30:15,Alice,0.85,webcam,office_cam_1
2025-11-14 10:30:18,Bob,0.92,webcam,office_cam_1
2025-11-14 10:30:22,Unknown,0.45,webcam,office_cam_1
```

---

## 📖 Complete Usage Examples

### Example 1: Real-Time Recognition with Callback

```python
from recognition_service import RecognitionService
import datetime

service = RecognitionService(dataset_path='dataset/')
service.load_database()

# Custom callback for recognized faces
def handle_recognition(results):
    for result in results:
        if result['name'] != 'Unknown' and result['confidence'] > 0.7:
            timestamp = datetime.datetime.now()
            print(f"[{timestamp}] Recognized: {result['name']} "
                  f"(Confidence: {result['confidence']:.2f})")
            
            # Could trigger other actions:
            # - Log to database
            # - Send notification
            # - Update attendance
            # - Unlock door

# Start with callback
service.start_webcam_recognition(
    camera_id=0,
    on_detection=handle_recognition,
    show_fps=True
)
```

---

### Example 2: Batch Video Processing

```python
import os

service = RecognitionService()
service.load_database()

# Process all videos in folder
video_folder = 'security_footage/'
output_folder = 'processed_footage/'

for video_file in os.listdir(video_folder):
    if video_file.endswith('.mp4'):
        print(f"\nProcessing: {video_file}")
        
        input_path = os.path.join(video_folder, video_file)
        output_path = os.path.join(output_folder, f"processed_{video_file}")
        
        results = service.recognize_video(
            input_path,
            output_video=output_path,
            process_every_n_frames=5,  # Speed up
            show_progress=True
        )
        
        # Summary
        print(f"Total faces detected: {results['total_faces_detected']}")
        print(f"Unique people: {', '.join(results['unique_people'])}")
        print(f"Processing time: {results['processing_time']:.1f}s")
        print(f"Average FPS: {results['avg_fps']:.1f}")

print("\n✅ All videos processed!")
```

---

### Example 3: Performance Monitoring Dashboard

```python
import time
from recognition_service import RecognitionService

service = RecognitionService()
service.load_database()

def print_dashboard():
    stats = service.get_performance_stats()
    
    print("\n" + "="*50)
    print("RECOGNITION SERVICE DASHBOARD")
    print("="*50)
    print(f"FPS: {stats['current_fps']:.1f} "
          f"(avg: {stats['avg_fps']:.1f}, "
          f"min: {stats['min_fps']:.1f}, "
          f"max: {stats['max_fps']:.1f})")
    print(f"Frame Time: {stats['avg_frame_time']*1000:.1f}ms")
    print(f"Frames Processed: {stats['total_frames_processed']}")
    print(f"Faces Detected: {stats['total_faces_detected']}")
    print(f"Cache Hit Rate: {stats['cache_hit_rate']*100:.1f}%")
    print(f"Uptime: {stats['uptime']:.1f}s")
    print("="*50 + "\n")

# Start recognition in separate thread
import threading
recognition_thread = threading.Thread(
    target=service.start_webcam_recognition,
    daemon=True
)
recognition_thread.start()

# Print dashboard every 5 seconds
try:
    while True:
        time.sleep(5)
        print_dashboard()
except KeyboardInterrupt:
    print("\nShutting down...")
```

---

### Example 4: Multi-Camera Setup

```python
from recognition_service import RecognitionService
import threading

# Create separate service for each camera
cameras = [
    {'id': 0, 'location': 'Main Entrance'},
    {'id': 1, 'location': 'Back Door'},
    {'id': 2, 'location': 'Office Floor'}
]

services = []
threads = []

for cam in cameras:
    # Create service instance
    service = RecognitionService(dataset_path='dataset/')
    service.load_database()
    services.append(service)
    
    # Detection callback
    def make_callback(location):
        def callback(results):
            for result in results:
                if result['name'] != 'Unknown':
                    print(f"[{location}] Detected: {result['name']}")
        return callback
    
    # Start in thread
    thread = threading.Thread(
        target=service.start_webcam_recognition,
        kwargs={
            'camera_id': cam['id'],
            'on_detection': make_callback(cam['location'])
        },
        daemon=True
    )
    thread.start()
    threads.append(thread)

print("All cameras running. Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping all cameras...")
```

---

## 🧪 Testing

Run comprehensive tests:
```bash
cd minggu-5-recognition-system/project
python test_recognition.py
```

**Tests include:**
- Database loading
- Single frame recognition
- Webcam feed processing
- Image recognition
- Video processing
- Performance benchmarking
- Parameter adjustment
- Callback functionality
- Multi-threading
- Error handling

**Expected output:**
```
Test 1: Load Database................. PASS (1.2s)
Test 2: Recognize Frame............... PASS
Test 3: Webcam Recognition............ PASS
Test 4: Image Recognition............. PASS
Test 5: Video Processing.............. PASS (25.3s)
Test 6: Performance Benchmark......... PASS (30.1s)
Test 7: Parameter Updates............. PASS
Test 8: Add Person Interactive........ SKIP (manual)
Test 9: Export Log.................... PASS
Test 10: Multi-threading.............. PASS

9/10 tests passed ✅
Total time: 58.7s
```

---

## 🔗 Integration Examples

### With Attendance System (Preview Minggu 6)

```python
from recognition_service import RecognitionService
from attendance_system import AttendanceSystem

recognition = RecognitionService()
recognition.load_database()

attendance = AttendanceSystem(db_path='attendance.db')

def on_recognition(results):
    for result in results:
        if result['name'] != 'Unknown' and result['confidence'] > 0.7:
            # Mark attendance
            success = attendance.mark_attendance(
                employee_id=result['name'],
                timestamp=datetime.datetime.now()
            )
            if success:
                print(f"✅ Attendance marked for {result['name']}")

recognition.start_webcam_recognition(on_detection=on_recognition)
```

---

## ⚙️ Configuration File

Create `recognition_config.json`:
```json
{
  "dataset_path": "dataset/",
  "detector": {
    "scale_factor": 1.1,
    "min_neighbors": 5,
    "min_size": [30, 30]
  },
  "recognizer": {
    "tolerance": 0.6,
    "model": "small"
  },
  "performance": {
    "process_every_n_frames": 3,
    "scale_factor": 0.5,
    "enable_caching": true,
    "cache_duration": 2.0,
    "enable_threading": true
  },
  "display": {
    "show_fps": true,
    "show_confidence": true,
    "box_color_known": [0, 255, 0],
    "box_color_unknown": [0, 0, 255],
    "font_scale": 0.6
  },
  "logging": {
    "enabled": true,
    "level": "INFO",
    "log_file": "recognition.log"
  }
}
```

Load config:
```python
import json

with open('recognition_config.json') as f:
    config = json.load(f)

service = RecognitionService(
    dataset_path=config['dataset_path'],
    config=config
)
```

---

## 🐛 Troubleshooting

**Low FPS:**
- Increase `process_every_n_frames`
- Enable frame scaling
- Enable caching
- Use threading
- Check CPU usage

**Recognition inaccurate:**
- Lower tolerance (stricter)
- Improve dataset quality
- Add more photos per person
- Better lighting conditions

**Memory usage high:**
- Clear cache periodically
- Limit frame buffer size
- Process smaller frames
- Reduce encoding storage

**Webcam lag:**
- Use ThreadedCamera
- Lower resolution
- Reduce detector parameters
- Skip more frames

---

## 📊 Performance Targets

**Minimum acceptable:**
- FPS: 15+
- Recognition accuracy: 85%+
- Frame time: <70ms
- CPU usage: <60%

**Good performance:**
- FPS: 20-25
- Recognition accuracy: 90%+
- Frame time: 40-50ms
- CPU usage: 40-50%

**Excellent performance:**
- FPS: 28-30
- Recognition accuracy: 95%+
- Frame time: <35ms
- CPU usage: <40%

---

## ⏭️ Next Steps

After mastering RecognitionService:

1. ✅ Real-time recognition working smoothly
2. ✅ 20+ FPS achieved
3. ✅ Recognition accuracy >90%
4. ✅ Proceed to **Minggu 6: Attendance System**

---

**Integration is where magic happens! 🎯**

*A well-integrated system is greater than sum of its parts.*
