# Minggu 7: Desktop GUI Development

## Tujuan Pembelajaran
- Build desktop interface dengan Tkinter
- GUI design principles
- Event-driven programming
- Multi-window application
- Real-time webcam preview di GUI

## Struktur Folder

```
minggu-7-desktop-gui/
├── README.md
├── learning/          # Tutorial dan latihan
│   ├── 01_tkinter_basics.py
│   ├── 02_layout_management.py
│   ├── 03_webcam_preview.py
│   ├── 04_multi_windows.py
│   └── latihan.py
└── project/           # Module untuk progressive build
    ├── gui/
    │   ├── __init__.py
    │   ├── main_window.py
    │   ├── register_window.py
    │   ├── attendance_window.py
    │   └── reports_window.py
    ├── main_app.py
    ├── test_gui.py
    └── README.md
```

## Learning Goals

### Tutorial Materials (learning/)
1. **01_tkinter_basics.py** - Tkinter fundamentals (window, labels, buttons, entry)
2. **02_layout_management.py** - Grid, pack, place layout managers
3. **03_webcam_preview.py** - Embed webcam feed di Tkinter Canvas
4. **04_multi_windows.py** - Multiple windows & dialog boxes
5. **latihan.py** - Complete desktop app prototype

### Konsep Utama
- Tkinter widgets (Button, Label, Entry, Canvas, Frame)
- Layout managers (grid, pack, place)
- Event handling (button clicks, keyboard events)
- Threading untuk webcam (non-blocking GUI)
- PIL/Pillow untuk display images
- Dialog boxes (messagebox, filedialog)
- Menu bars & toolbars
- Custom themes & styling

## Project Development

### GUI Windows:

#### Main Window (`main_window.py`)
- **Left Panel:** Live webcam preview dengan face detection bounding boxes
- **Right Panel:** Recognition status, person info, attendance count
- **Bottom Panel:** Action buttons (Register Person, View Reports, Settings)
- **Menu Bar:** File, View, Help

#### Register Person Window (`register_window.py`)
- **Top Section:** Person info form (Name, ID, Department, Email)
- **Middle Section:** Webcam preview untuk capture photos
- **Bottom Section:** Capture button, photo count (20/20), Save button
- **Features:** Auto quality validation, progress indicator

#### Attendance Window (`attendance_window.py`)
- **Main Area:** Real-time webcam dengan face recognition
- **Side Panel:** Recognized person info, check-in time
- **Bottom:** Manual check-in button (if recognition fails)
- **Notifications:** Toast messages untuk successful/failed recognition

#### Reports Window (`reports_window.py`)
- **Top:** Date range picker, filter by person/department
- **Middle:** Table dengan attendance records (scrollable)
- **Bottom:** Export buttons (Excel, CSV), Print button
- **Charts:** Attendance statistics (optional - matplotlib)

### Integration
Uses all modules from Week 1-6:
- `recognition_service.py` - Recognition logic
- `attendance_service.py` - Attendance logic
- `models.py` - Database models
- All core modules

## Cara Penggunaan

### Learning (Tutorial)
```bash
cd minggu-7-desktop-gui/learning
python 01_tkinter_basics.py        # Basic widgets & layouts
python 02_layout_management.py     # Grid, pack, place
python 03_webcam_preview.py        # Webcam di GUI
python 04_multi_windows.py         # Multiple windows
python latihan.py                  # Complete app prototype
```

### Project Development
```bash
cd minggu-7-desktop-gui/project

# Run main application
python main_app.py

# Test GUI components
python test_gui.py

# Integrate to root project
# Copy gui/ folder to ../../gui/
# Copy main_app.py to ../../main_app.py
```

## GUI Features

### Main Window Features
```python
# Real-time webcam preview
- OpenCV capture → PIL Image → Tkinter Canvas
- Face detection boxes drawn on preview
- Recognition results displayed in real-time

# Status Display
- Current recognized person
- Confidence score
- Database statistics (total persons, today's attendance)

# Action Buttons
- "Register New Person" → Open register window
- "View Reports" → Open reports window
- "Settings" → Configure camera, threshold, theme
```

### Threading untuk Smooth GUI
```python
# Webcam thread (background)
# - Capture frames continuously
# - Update canvas without freezing GUI

# Recognition thread (background)
# - Process face recognition
# - Update UI via queue
```

## Deliverables

### Learning
- Tkinter GUI development
- Layout management
- Webcam integration di GUI
- Multi-window application
- Event-driven programming

### Project
- Complete desktop application
- Main window dengan webcam preview
- Register person module
- Attendance tracking interface
- Reports window dengan export functionality

## Next Week Preview

**Minggu 8: Final App & Distribution**
- Polish UI/UX (colors, fonts, icons)
- Error handling & validations
- Unit testing dengan pytest
- Create executable dengan PyInstaller
- User manual & documentation

---

**Time Estimate:** 5-6 hours  
**Difficulty:** Medium
