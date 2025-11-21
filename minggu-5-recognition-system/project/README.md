# Minggu 5 - Project: RecognitionService Class

## 📚 Overview
Production-ready `RecognitionService` class yang mengintegrasikan detector, recognizer, dan dataset manager menjadi complete face recognition system dengan performance optimization built-in.

## 📁 Project Files

```
project/
├── README.md (file ini)
├── recognition_service.py (NEW - Main service class)
├── face_detector.py (from Week 2)
├── face_recognizer.py (from Week 3)
├── dataset_manager.py (from Week 4)
├── image_utils.py (from Week 1)
└── test_recognition.py (Testing file)
```

---

## 🎯 RecognitionService Class - Complete API

### Initialization

```python
from recognition_service import RecognitionService

# Basic initialization
service = RecognitionService(dataset_path='dataset/')

# Advanced configuration
service = RecognitionService(
    dataset_path='dataset/',
    config={
        'detector': {
            'scale_factor': 1.1,
            'min_neighbors': 5
        },
        'recognizer': {
            'tolerance': 0.6,
            'model': 'small'
        },
        'performance': {
            'process_every_n_frames': 3,
            'scale_factor': 0.5,
            'enable_caching': True,
            'cache_duration': 2.0
        }
    }
)
```

**Parameters:**
- `dataset_path` (str): Path to face dataset (default: 'dataset/')
- `config` (dict): Configuration dictionary (optional)

**Initializes:**
- FaceDetector instance
- FaceRecognizer instance
- DatasetManager instance
- Performance monitoring
- Result caching
- Logging system

---

## 🔧 Core Methods

### 1. load_database()
**Purpose:** Load known faces from dataset

```python
# Load all known faces
service.load_database()

# Reload after dataset updates
service.load_database(force_reload=True)

# Load from specific path
service.load_database(dataset_path='custom_dataset/')
```

**Parameters:**
- `force_reload` (bool): Force reload even if already loaded (default: False)
- `dataset_path` (str): Override dataset path (optional)

**Returns:** `dict`
```python
{
    'total_people': 5,
    'total_encodings': 120,
    'load_time': 1.23  # seconds
}
```

**Process:**
1. Scans dataset folder
2. Loads encodings for each person
3. Builds recognition database
4. Logs loading statistics

---

### 2. recognize_frame()
**Purpose:** Recognize all faces in single frame

```python
# Basic recognition
results = service.recognize_frame(frame)

# With options
results = service.recognize_frame(
    frame,
    return_encodings=True,
    min_confidence=0.5
)
```

**Parameters:**
- `frame` (numpy.ndarray): Input image
- `return_encodings` (bool): Include face encodings in results (default: False)
- `min_confidence` (float): Minimum confidence threshold (default: 0.0)

**Returns:** `list[dict]`
```python
[
    {
        'name': 'Alice',
        'confidence': 0.85,
        'bbox': (100, 50, 150, 200),  # (x, y, w, h)
        'face_id': 'face_001',  # Tracking ID
        'encoding': array([...])  # If return_encodings=True
    },
    {
        'name': 'Unknown',
        'confidence': 0.45,
        'bbox': (300, 100, 150, 200),
        'face_id': 'face_002'
    }
]
```

**Pipeline:**
1. Detect faces in frame
2. Extract face ROIs
3. Generate encodings
4. Match against database
5. Apply confidence threshold
6. Return results with tracking IDs

---

### 3. start_webcam_recognition()
**Purpose:** Start real-time webcam recognition

```python
# Basic usage
service.start_webcam_recognition()

# With camera selection
service.start_webcam_recognition(camera_id=1)

# With callback
def on_face_detected(results):
    for result in results:
        print(f"Detected: {result['name']}")

service.start_webcam_recognition(
    camera_id=0,
    on_detection=on_face_detected,
    show_fps=True
)
```

**Parameters:**
- `camera_id` (int): Camera index (default: 0)
- `on_detection` (callable): Callback function for detections (optional)
- `show_fps` (bool): Display FPS counter (default: True)
- `save_video` (bool): Save output video (default: False)
- `output_path` (str): Video save path (default: 'output.avi')

**Controls:**
- Press 'q' to quit
- Press 's' to save current frame
- Press 'p' to pause/resume
- Press 'r' to reload database

**Display:**
- Green boxes: Known faces
- Red boxes: Unknown faces
- Name + confidence above box
- FPS counter (top-left)
- Status bar (bottom)

---

### 4. recognize_image()
**Purpose:** Recognize faces in static image

```python
# From file
results = service.recognize_image('photo.jpg')

# From numpy array
import cv2
img = cv2.imread('photo.jpg')
results = service.recognize_image(img)

# Save annotated image
results = service.recognize_image(
    'photo.jpg',
    save_annotated=True,
    output_path='result.jpg'
)
```

**Parameters:**
- `image` (str or numpy.ndarray): Input image path or array
- `save_annotated` (bool): Save image with boxes/labels (default: False)
- `output_path` (str): Save path for annotated image (optional)

**Returns:** Same as `recognize_frame()`

**Creates:** Annotated image file (if save_annotated=True)

---

### 5. recognize_video()
**Purpose:** Process entire video file

```python
# Basic processing
results = service.recognize_video('input_video.mp4')

# With output video
results = service.recognize_video(
    'input_video.mp4',
    output_video='output_video.avi',
    show_progress=True
)

# Process every Nth frame for speed
results = service.recognize_video(
    'input_video.mp4',
    process_every_n_frames=5
)
```

**Parameters:**
- `video_path` (str): Input video file path
- `output_video` (str): Output video path (optional)
- `show_progress` (bool): Show progress bar (default: True)
- `process_every_n_frames` (int): Frame skip for speed (default: 1)

**Returns:** `dict`
```python
{
    'total_frames': 1000,
    'processed_frames': 1000,
    'total_faces_detected': 150,
    'unique_people': ['Alice', 'Bob', 'Unknown'],
    'processing_time': 45.2,  # seconds
    'avg_fps': 22.1
}
```

**Progress output:**
```
Processing video: input_video.mp4
Frame 500/1000 (50%) | FPS: 22.1 | Faces: 75
```

---

### 6. get_performance_stats()
**Purpose:** Get performance metrics

```python
stats = service.get_performance_stats()
print(stats)
```

**Returns:** `dict`
```python
{
    'current_fps': 28.5,
    'avg_fps': 27.2,
    'min_fps': 22.0,
    'max_fps': 30.0,
    'avg_frame_time': 0.035,  # seconds
    'total_frames_processed': 5420,
    'total_faces_detected': 892,
    'cache_hit_rate': 0.65,  # 65% cache hits
    'uptime': 300.5  # seconds
}
```

---

### 7. set_recognition_parameters()
**Purpose:** Update recognition settings on-the-fly

```python
# Adjust tolerance (lower = stricter)
service.set_recognition_parameters(tolerance=0.5)

# Multiple parameters
service.set_recognition_parameters(
    tolerance=0.6,
    scale_factor=1.05,
    min_neighbors=4,
    process_every_n_frames=2
)
```

**Parameters:**
- `tolerance` (float): Face matching threshold (0.0-1.0)
- `scale_factor` (float): Detector scale factor
- `min_neighbors` (int): Detector min neighbors
- `process_every_n_frames` (int): Frame skip count
- `cache_duration` (float): Cache lifetime (seconds)

**Effect:** Immediate - applies to next recognition call

---

### 8. add_person_interactive()
**Purpose:** Add new person via webcam capture

```python
# Interactive add
service.add_person_interactive(
    name='Charlie',
    employee_id='003',
    photo_count=30
)
```

**Parameters:**
- `name` (str): Person name
- `employee_id` (str): Unique ID
- `photo_count` (int): Photos to capture (default: 30)
- `department` (str): Department (optional)

**Process:**
1. Shows webcam feed
2. Guides user through angles
3. Validates photo quality
4. Saves to dataset
5. Generates encodings
6. Reloads database
7. Returns success status

**Returns:** `bool` - True if successful

---

### 9. benchmark_performance()
**Purpose:** Run performance benchmark

```python
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

### With Attendance System (Preview Week 6)

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
4. ✅ Proceed to **Minggu 6: Database & Attendance System**

---

**Integration is where magic happens! 🎯**

*A well-integrated system is greater than sum of its parts.*
