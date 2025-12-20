# Minggu 7 - Project: Complete Desktop GUI Application

## 📚 Overview
Production-ready desktop GUI application untuk Face Recognition Attendance System. Complete dengan registration, live attendance marking, dan reporting.

## 📁 Project Structure

```
project/
├── README.md (file ini)
├── main_app.py (ENTRY POINT - run this!)
├── test_gui.py (comprehensive testing suite)
├── gui/
│   ├── __init__.py
│   ├── main_window.py (Main dashboard)
│   ├── register_window.py (Register new persons)
│   ├── attendance_window.py (Mark attendance)
│   └── reports_window.py (View & export reports)
├── attendance_system.py (from Week 6)
├── recognition_service.py (from Week 5)
├── dataset_manager.py (from Week 4)
├── face_detector.py (from Week 2)
├── image_utils.py (from Week 1)
├── dataset/ (face encodings storage)
│   ├── encodings.pkl
│   ├── persons.json
│   └── person_ID/
│       ├── face_0.jpg
│       ├── face_1.jpg
│       └── ...
├── logs/ (attendance logs)
│   ├── attendance_2024-01-15.csv
│   └── ...
└── output/ (exported reports)
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install opencv-python pillow mediapipe numpy pandas
```

### 2. Run Application
```bash
python main_app.py
```

### 3. Test Application
```bash
python test_gui.py
```

---

## 🎯 Application Components

### 1. Main Dashboard (`gui/main_window.py`)

**Features:**
- Live webcam preview dengan face detection
- Real-time detection boxes (green rectangles)
- Today's attendance summary stats
- Quick navigation buttons
- Status bar dengan FPS counter

**GUI Layout:**
```
┌──────────────────────────────────────────────────────────┐
│  Face Recognition Attendance System v1.0                 │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────┐   📊 Today's Attendance        │
│  │                    │   ─────────────────────         │
│  │  LIVE WEBCAM       │   Total: 15 persons            │
│  │  WITH DETECTION    │   Check-ins: 12                │
│  │                    │   Check-outs: 8                │
│  │  [Green boxes]     │   Current: 4 persons           │
│  │                    │                                │
│  └────────────────────┘   ⏱️ Last Update: 10:30 AM    │
│                                                          │
│  ┌────────────────┬────────────────┬─────────────────┐ │
│  │  📝 Register    │  ✅ Attendance  │  📊 Reports     │ │
│  │  New Person    │  Mark Now      │  View Logs      │ │
│  └────────────────┴────────────────┴─────────────────┘ │
│                                                          │
│  Status: Ready | Camera: 0 | FPS: 30 | Faces: 2        │
└──────────────────────────────────────────────────────────┘
```

**Key Features:**
```python
class MainWindow:
    def __init__(self):
        # Initialize services
        self.face_detector = FaceDetector()
        self.recognition_service = RecognitionService()
        self.attendance_system = AttendanceSystem()
        
        # Start webcam thread
        self.webcam_thread = WebcamThread()
        self.webcam_thread.frame_ready.connect(self.update_frame)
        self.webcam_thread.start()
    
    def update_frame(self, frame):
        """Update webcam display with face detection"""
        # Detect faces
        faces = self.face_detector.detect_faces(frame)
        
        # Draw bounding boxes
        for face in faces:
            x, y, w, h = face['box']
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
        # Update GUI
        self.display_frame(frame)
```

---

### 2. Register Window (`gui/register_window.py`)

**Features:**
- Form input (Name, ID, Department, Email)
- Auto-capture 20 photos dengan countdown
- Progress bar tracking
- Face quality validation
- Auto-save to dataset

**GUI Layout:**
```
┌──────────────────────────────────────────────────────────┐
│  Register New Person                            [X]      │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Personal Information                                   │
│  ────────────────────                                   │
│  Full Name:     [____________________________]          │
│  Employee ID:   [____________________________]          │
│  Department:    [▼ IT Department            ]          │
│  Email:         [____________________________]          │
│                                                          │
│  Photo Capture                                          │
│  ─────────────                                          │
│  ┌────────────────────┐                                │
│  │                    │  Status: Ready                 │
│  │  WEBCAM PREVIEW    │  Photos captured: 0/20        │
│  │                    │                                │
│  │  [Face detection]  │  Instructions:                │
│  │                    │  - Look at camera             │
│  │                    │  - Turn head slightly         │
│  └────────────────────┘  - Keep good lighting         │
│                                                          │
│  Progress: [████████████░░░░░░░░] 60%                  │
│                                                          │
│  [Start Capture]  [Cancel]  [Save]                     │
└──────────────────────────────────────────────────────────┘
```

**Workflow:**
1. User mengisi form (name, ID, dept, email)
2. Click "Start Capture"
3. System auto-capture 20 photos (1 photo per 0.5 detik)
4. Each photo validated untuk face quality
5. Progress bar updates real-time
6. Auto-save encodings ke dataset/
7. Success notification

**Implementation:**
```python
def auto_capture_photos(self):
    """Auto-capture 20 photos with countdown"""
    count = 0
    total = 20
    
    while count < total:
        # Get frame
        ret, frame = self.cap.read()
        
        # Detect face
        faces = self.face_detector.detect_faces(frame)
        
        if faces:
            # Save photo
            filename = f"dataset/{person_id}/face_{count}.jpg"
            cv2.imwrite(filename, frame)
            
            # Update progress
            count += 1
            progress = (count / total) * 100
            self.progress_bar.set_value(progress)
            
        time.sleep(0.5)
    
    # Generate encodings
    self.dataset_manager.generate_encodings(person_id)
    messagebox.showinfo("Success", "Person registered!")
```

---

### 3. Attendance Window (`gui/attendance_window.py`)

**Features:**
- Live face recognition
- Auto check-in/check-out
- Manual entry fallback
- Today's records display
- Cooldown timer (prevent duplicates)

**GUI Layout:**
```
┌──────────────────────────────────────────────────────────┐
│  Mark Attendance                                [X]      │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────┐   Recognition Status           │
│  │                    │   ─────────────────             │
│  │  LIVE WEBCAM       │   Last Recognized:              │
│  │  WITH RECOGNITION  │   👤 Alice Johnson             │
│  │                    │   ID: EMP001                   │
│  │  [Name labels]     │   Time: 09:15:30               │
│  │                    │   Action: ✅ Check-in          │
│  └────────────────────┘                                 │
│                                                          │
│  Manual Entry (if face not recognized)                  │
│  ──────────────────────────────────                     │
│  Employee ID: [______________]  [Check-in] [Check-out] │
│                                                          │
│  Today's Attendance                                     │
│  ───────────────────                                    │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Time     │ Name           │ ID      │ Action    │  │
│  │──────────┼────────────────┼─────────┼───────────│  │
│  │ 09:00:15 │ Alice Johnson  │ EMP001  │ Check-in  │  │
│  │ 09:05:30 │ Bob Smith      │ EMP002  │ Check-in  │  │
│  │ 09:12:45 │ Charlie Lee    │ EMP003  │ Check-in  │  │
│  │ 12:30:20 │ Alice Johnson  │ EMP001  │ Check-out │  │
│  └──────────┴────────────────┴─────────┴───────────┘  │
│                                                          │
│  [Refresh]  [Export Today]  [Close]                    │
└──────────────────────────────────────────────────────────┘
```

**Recognition Workflow:**
1. Webcam terus detect faces
2. Recognize each face (match dengan dataset)
3. Display name label di atas face
4. Auto check-in jika recognized (cooldown 5 detik)
5. Log to CSV file (logs/attendance_YYYY-MM-DD.csv)
6. Update today's table real-time

**Implementation:**
```python
def recognize_and_mark(self):
    """Continuous recognition and auto-marking"""
    while self.running:
        ret, frame = self.cap.read()
        
        # Detect faces
        faces = self.face_detector.detect_faces(frame)
        
        for face in faces:
            # Get face region
            face_img = frame[y:y+h, x:x+w]
            
            # Recognize
            result = self.recognition_service.recognize_face(face_img)
            
            if result['person_name'] != 'Unknown':
                person_id = result['person_id']
                
                # Check cooldown (prevent duplicate)
                if self.can_mark_attendance(person_id):
                    # Auto check-in
                    self.attendance_system.mark_checkin(person_id)
                    
                    # Update UI
                    self.add_to_table(result)
                    
                    # Set cooldown
                    self.last_marked[person_id] = time.time()
        
        time.sleep(0.1)
```

---

### 4. Reports Window (`gui/reports_window.py`)

**Features:**
- Date range filtering (Today/Week/Month/All)
- Search by name or ID
- Export to CSV
- Summary statistics

**GUI Layout:**
```
┌──────────────────────────────────────────────────────────┐
│  Attendance Reports                             [X]      │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Filters                                                │
│  ───────                                                │
│  Date Range: [▼ This Month  ]  From: [📅]  To: [📅]   │
│  Search:     [______________]  [🔍 Search]             │
│                                                          │
│  Summary                                                │
│  ───────                                                │
│  Total Records: 150   |   Unique Persons: 15           │
│  Check-ins: 80        |   Check-outs: 70               │
│                                                          │
│  Records                                                │
│  ───────                                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Date       │ Time  │ Name     │ ID    │ Action  │  │
│  │────────────┼───────┼──────────┼───────┼─────────│  │
│  │ 2024-01-15 │ 09:00 │ Alice J. │ EMP001│ In      │  │
│  │ 2024-01-15 │ 09:05 │ Bob S.   │ EMP002│ In      │  │
│  │ 2024-01-15 │ 12:30 │ Alice J. │ EMP001│ Out     │  │
│  │ 2024-01-15 │ 13:00 │ Charlie  │ EMP003│ In      │  │
│  │ ...        │ ...   │ ...      │ ...   │ ...     │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  [Export CSV]  [Print]  [Close]                        │
└──────────────────────────────────────────────────────────┘
```

**Features:**
```python
def filter_records(self, date_range='month'):
    """Filter attendance records"""
    # Load all logs
    records = self.attendance_system.get_records()
    
    # Filter by date
    if date_range == 'today':
        records = [r for r in records if r['date'] == date.today()]
    elif date_range == 'week':
        week_start = date.today() - timedelta(days=7)
        records = [r for r in records if r['date'] >= week_start]
    elif date_range == 'month':
        month_start = date.today().replace(day=1)
        records = [r for r in records if r['date'] >= month_start]
    
    # Update table
    self.display_records(records)
    
    # Update summary
    self.update_summary(records)

def export_csv(self):
    """Export records to CSV"""
    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")]
    )
    
    if filename:
        df = pd.DataFrame(self.records)
        df.to_csv(filename, index=False)
        messagebox.showinfo("Success", f"Exported to {filename}")
```

---

## 🔧 Dependencies

**Core Libraries:**
```txt
opencv-python==4.8.0.76
Pillow==10.0.0
mediapipe==0.10.0
numpy==1.24.3
pandas==2.0.3
```

**Standard Library:**
```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from datetime import date, datetime, timedelta
import json
import csv
import os
```

---

## 📝 File Formats

### Dataset Structure
```
dataset/
├── encodings.pkl (pickled face encodings)
├── persons.json (person metadata)
└── PERSON_ID/
    ├── face_0.jpg
    ├── face_1.jpg
    └── ...
```

### Persons Metadata (persons.json)
```json
[
  {
    "id": "EMP001",
    "name": "Alice Johnson",
    "department": "IT",
    "email": "alice@company.com",
    "registered_date": "2024-01-15",
    "num_photos": 20
  }
]
```

### Attendance Logs (logs/attendance_2024-01-15.csv)
```csv
timestamp,person_id,person_name,action
2024-01-15 09:00:15,EMP001,Alice Johnson,check-in
2024-01-15 09:05:30,EMP002,Bob Smith,check-in
2024-01-15 12:30:20,EMP001,Alice Johnson,check-out
```

---

## 🎯 Application Flow

### Complete User Journey

**1. Register New Person:**
```
Open App → Main Window → Click "Register"
→ Fill form (name, ID, dept, email)
→ Click "Start Capture"
→ Auto-capture 20 photos (with progress bar)
→ System generates encodings
→ Success! Person registered
```

**2. Mark Attendance:**
```
Open App → Main Window → Click "Attendance"
→ Webcam starts recognition
→ Person stands in front of camera
→ System recognizes face (display name label)
→ Auto check-in (or check-out if already in)
→ Record saved to CSV
→ Updated in today's table
```

**3. View Reports:**
```
Open App → Main Window → Click "Reports"
→ Select date range (today/week/month/all)
→ View records in table
→ Search by name or ID
→ Click "Export CSV" → Save file
→ Open CSV in Excel or Google Sheets
```

---

## 🐛 Testing

### Comprehensive Test Suite (`test_gui.py`)

**6 Test Categories:**
1. ✅ Package Imports - verify all dependencies
2. ✅ Project Structure - check folders & files
3. ✅ Webcam Detection - auto-detect cameras
4. ✅ Face Detection - module functionality
5. ✅ Dataset Validation - encodings & persons
6. ✅ GUI Components - interactive window test

**Run Tests:**
```bash
python test_gui.py
```

**Example Output:**
```
===== DESKTOP GUI APPLICATION TEST SUITE =====

Test 1/6: Package Imports
✅ All packages imported successfully

Test 2/6: Project Structure
✅ All required folders present
✅ All required files present

Test 3/6: Webcam Detection
✅ Camera 0: 1280x720 @ 30 FPS

Test 4/6: Face Detection
✅ MediaPipe initialized
✅ detect_faces() works

Test 5/6: Dataset Validation
✅ encodings.pkl exists (15 persons)
✅ persons.json exists
⚠️  Some persons missing photos

Test 6/6: GUI Components
✅ Main window created
✅ All buttons functional
[Interactive GUI test window opens]

===== TEST SUMMARY =====
✅ Passed: 5/6
⚠️  Warnings: 1/6
❌ Failed: 0/6

Verdict: READY FOR PRODUCTION ✅
```

---

## 🚀 Deployment

### Production Checklist

Before deploying:

- [ ] All tests passed (run `test_gui.py`)
- [ ] Webcam working (camera permissions granted)
- [ ] Dataset folder present
- [ ] At least 1 person registered
- [ ] Attendance logs folder created
- [ ] Good lighting conditions

### Performance Optimization

**Face Detection Speed:**
```python
# Reduce frame size for faster processing
frame = cv2.resize(frame, (640, 480))

# Lower FPS for slower computers
time.sleep(0.05)  # 20 FPS instead of 30

# Use GPU acceleration (if available)
detector = FaceDetector(use_gpu=True)
```

**Memory Optimization:**
```python
# Limit encodings in memory
max_encodings = 100

# Clear old frames
del frame
gc.collect()

# Release webcam when not in use
cap.release()
```

---

## 🐛 Troubleshooting

### Issue 1: Webcam tidak muncul
**Symptoms:** Black screen di webcam preview

**Solutions:**
```bash
# Test webcam
python -c "import cv2; print('OK' if cv2.VideoCapture(0).isOpened() else 'FAIL')"

# Check camera permissions
# Windows: Settings → Privacy → Camera → Allow desktop apps

# Try different camera index
cap = cv2.VideoCapture(1)  # atau 2, 3, etc
```

### Issue 2: Face tidak ke-detect
**Symptoms:** No green boxes muncul

**Solutions:**
- Improve lighting (use lamp, open curtains)
- Face webcam directly (front view)
- Adjust distance (50-80cm optimal)
- Check face not blocked (hair, mask, glasses)

**Debug:**
```python
# Print detection info
faces = detector.detect_faces(frame)
print(f"Detected {len(faces)} faces")
for face in faces:
    print(f"Confidence: {face['confidence']}")
```

### Issue 3: Recognition salah
**Symptoms:** System recognize wrong person

**Solutions:**
- Register dengan lebih banyak photos (30-50)
- Re-register dengan better lighting
- Remove old encodings: `rm dataset/encodings.pkl`
- Re-generate: `python -c "from dataset_manager import DatasetManager; DatasetManager().generate_all_encodings()"`

### Issue 4: GUI freezing
**Symptoms:** Window not responding

**Solutions:**
- Ensure webcam runs di thread (daemon=True)
- Don't do heavy processing di main thread
- Use queue untuk thread communication
- Release webcam properly on exit

**Fix:**
```python
# Correct threading
def webcam_loop():
    while running:
        # process frame
        pass

thread = threading.Thread(target=webcam_loop, daemon=True)
thread.start()
```

### Issue 5: Attendance duplicate
**Symptoms:** Same person logged multiple times

**Solutions:**
- Increase cooldown timer (5 → 10 seconds)
- Check last_marked dictionary not cleared
- Verify timestamp comparison logic

**Fix:**
```python
COOLDOWN = 10  # seconds

def can_mark_attendance(self, person_id):
    if person_id in self.last_marked:
        elapsed = time.time() - self.last_marked[person_id]
        return elapsed > COOLDOWN
    return True
```

---

## 📚 Code Architecture

### Module Dependencies
```
main_app.py
    │
    ├── gui/main_window.py
    │   ├── recognition_service.py
    │   │   ├── face_recognizer.py
    │   │   └── face_detector.py
    │   └── attendance_system.py
    │
    ├── gui/register_window.py
    │   ├── dataset_manager.py
    │   │   └── face_recognizer.py
    │   └── face_detector.py
    │
    ├── gui/attendance_window.py
    │   ├── recognition_service.py
    │   └── attendance_system.py
    │
    └── gui/reports_window.py
        └── attendance_system.py
```

### Design Patterns Used

**1. Singleton Pattern** (Services)
```python
class RecognitionService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

**2. Observer Pattern** (Webcam threads)
```python
class WebcamThread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.observers = []
    
    def add_observer(self, callback):
        self.observers.append(callback)
    
    def notify(self, frame):
        for callback in self.observers:
            callback(frame)
```

**3. Factory Pattern** (Window creation)
```python
class WindowFactory:
    @staticmethod
    def create(window_type, parent):
        if window_type == 'register':
            return RegisterWindow(parent)
        elif window_type == 'attendance':
            return AttendanceWindow(parent)
        elif window_type == 'reports':
            return ReportsWindow(parent)
```

---

## 🎓 Learning Resources

**Tkinter Documentation:**
- Official: https://docs.python.org/3/library/tkinter.html
- Tutorial: https://realpython.com/python-gui-tkinter/

**OpenCV Python:**
- Official: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
- Face Detection: https://docs.opencv.org/4.x/d2/d99/tutorial_js_face_detection.html

**Threading in GUI:**
- Best Practices: https://docs.python.org/3/library/threading.html
- Tkinter Threading: https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop

---

## ✅ Success Criteria

Application considered successful if:

1. ✅ Main window opens without errors
2. ✅ Webcam preview working (30 FPS)
3. ✅ Face detection boxes visible
4. ✅ Can register new person (20 photos)
5. ✅ Can mark attendance (check-in/out)
6. ✅ Recognition accuracy > 90%
7. ✅ Can view today's records
8. ✅ Can export CSV reports
9. ✅ No crashes after 1 hour continuous use
10. ✅ Response time < 2 seconds for all actions

---

## 🎉 Congratulations!

You've completed the Desktop GUI Application!

**What you've learned:**
- ✅ Tkinter GUI development
- ✅ Webcam integration dengan OpenCV
- ✅ Threading untuk non-blocking UI
- ✅ Face detection & recognition
- ✅ Dataset management
- ✅ Attendance logging & reporting
- ✅ Production deployment

**Next steps:**
- Add more features (notifications, backup, etc)
- Improve UI/UX design
- Add error logging
- Create installer (PyInstaller)
- Share dengan teman!

**Need help?** Read [learning/README.md](../learning/README.md) for tutorials!
