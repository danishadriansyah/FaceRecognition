# 📝 TUGAS MINGGU 7 - Complete Desktop Application

## Deskripsi
Buat production-ready desktop application dengan GUI lengkap yang mengintegrasikan semua fitur minggu 1-6.

---

## 🎯 Objektif
- Complete GUI dengan Tkinter
- Integrate all modules
- User-friendly interface
- Professional look & feel
- Production-ready application

---

## 📋 Tugas: Face Recognition Attendance Desktop App

Buat aplikasi desktop `attendance_app.py` dengan GUI lengkap:

### Fitur Wajib

1. **Main Window**
   - Menu bar (File, Edit, View, Help)
   - Toolbar dengan icon buttons
   - Status bar (database status, FPS, info)
   - Tab navigation:
     - 📸 Registration
     - ✅ Attendance
     - 📊 Reports
     - ⚙️ Settings

2. **Registration Tab**
   - Form: Name input
   - Webcam preview (live)
   - Quality indicators (brightness, blur, size)
   - Progress bar (0/20 photos)
   - Capture button / Auto-capture
   - Person list (registered persons)
   - Delete person button

3. **Attendance Tab**
   - Webcam preview dengan recognition
   - Recognized person display:
     - Name (large font)
     - Confidence percentage
     - Status (Present/Already marked)
   - Today's attendance list
   - Manual attendance button
   - Export today's report

4. **Reports Tab**
   - Date range selector
   - Report type dropdown:
     - Daily report
     - Monthly summary
     - Person detail
   - Preview pane (table view)
   - Export buttons (Excel, CSV, PDF)
   - Statistics dashboard:
     - Total persons
     - Today's attendance
     - This month attendance
     - Charts (optional)

5. **Settings Tab**
   - Database connection
   - Confidence threshold slider
   - Auto-attendance toggle
   - Face detection model (HOG/CNN)
   - Frame skip settings
   - Backup/restore database

---

## 📦 Deliverables

```
tugas/
├── attendance_app.py          # Main GUI application
├── modules/
│   ├── gui/
│   │   ├── main_window.py
│   │   ├── registration_tab.py
│   │   ├── attendance_tab.py
│   │   ├── reports_tab.py
│   │   └── settings_tab.py
│   ├── core/
│   │   ├── face_detector.py
│   │   ├── face_recognizer.py
│   │   ├── dataset_manager.py
│   │   └── attendance_system.py
│   └── utils/
│       ├── image_utils.py
│       └── db_utils.py
├── assets/
│   ├── icons/               # Button icons
│   └── logo.png
├── database/
│   └── attendance.db
├── dataset/
├── reports/
└── README.md
```

---

## 🎯 Example Screenshots

### Main Window:
```
┌─────────────────────────────────────────────────────┐
│ File  Edit  View  Help                              │
├─────────────────────────────────────────────────────┤
│ [📸] [✅] [📊] [⚙️]                                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┬──────────────────────────────┐   │
│  │ Registration │ Attendance │ Reports │ Settings│  │
│  ├──────────────┴──────────────────────────────┤   │
│  │                                               │   │
│  │   [Webcam Preview - 640x480]                 │   │
│  │                                               │   │
│  │   Name: [________________]                   │   │
│  │                                               │   │
│  │   Quality: ████████░░ 80%                    │   │
│  │   Photos: [████████░░░░] 8/20                │   │
│  │                                               │   │
│  │   [Start Capture]  [Delete Person]           │   │
│  │                                               │   │
│  │   Registered Persons:                        │   │
│  │   ┌────────────────────────────────────┐     │   │
│  │   │ Andi           (20 photos)         │     │   │
│  │   │ Budi           (18 photos)         │     │   │
│  │   │ Citra          (20 photos)         │     │   │
│  │   └────────────────────────────────────┘     │   │
│  │                                               │   │
│  └───────────────────────────────────────────────┘   │
│                                                      │
├─────────────────────────────────────────────────────┤
│ 🟢 Database connected │ FPS: 28 │ Ready            │
└─────────────────────────────────────────────────────┘
```

---

## 💡 Hints & Tips

### Main Window Structure
```python
import tkinter as tk
from tkinter import ttk

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1000x700")
        
        # Menu bar
        self.create_menu()
        
        # Toolbar
        self.create_toolbar()
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Tabs
        self.registration_frame = ttk.Frame(self.notebook)
        self.attendance_frame = ttk.Frame(self.notebook)
        self.reports_frame = ttk.Frame(self.notebook)
        self.settings_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.registration_frame, text='📸 Registration')
        self.notebook.add(self.attendance_frame, text='✅ Attendance')
        self.notebook.add(self.reports_frame, text='📊 Reports')
        self.notebook.add(self.settings_frame, text='⚙️ Settings')
        
        # Status bar
        self.create_status_bar()
        
        # Build tabs
        self.build_registration_tab()
        self.build_attendance_tab()
        self.build_reports_tab()
        self.build_settings_tab()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Person", command=self.new_person)
        file_menu.add_command(label="Export Report", command=self.export_report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
    
    def create_status_bar(self):
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side='bottom', fill='x')
        
        self.status_label = ttk.Label(status_frame, text="Ready", relief='sunken')
        self.status_label.pack(side='left', fill='x', expand=True)
        
        self.fps_label = ttk.Label(status_frame, text="FPS: 0", relief='sunken')
        self.fps_label.pack(side='right')
```

### Webcam Preview in Tkinter
```python
import cv2
from PIL import Image, ImageTk

class WebcamPreview:
    def __init__(self, parent, width=640, height=480):
        self.parent = parent
        self.width = width
        self.height = height
        
        # Canvas for video
        self.canvas = tk.Canvas(parent, width=width, height=height)
        self.canvas.pack()
        
        # Webcam
        self.cap = cv2.VideoCapture(0)
        
        # Start update loop
        self.update()
    
    def update(self):
        ret, frame = self.cap.read()
        
        if ret:
            # Resize
            frame = cv2.resize(frame, (self.width, self.height))
            
            # Convert BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PhotoImage
            img = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=img)
            
            # Update canvas
            self.canvas.create_image(0, 0, image=photo, anchor='nw')
            self.canvas.image = photo  # Keep reference
        
        # Schedule next update (30 FPS = 33ms)
        self.parent.after(33, self.update)
    
    def close(self):
        self.cap.release()
```

### Progress Bar
```python
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(
    frame,
    variable=progress_var,
    maximum=20,
    mode='determinate'
)
progress_bar.pack()

# Update
progress_var.set(8)  # 8/20 photos
```

### Listbox with Data
```python
# Create Listbox
person_listbox = tk.Listbox(frame, height=10)
person_listbox.pack()

# Populate
persons = get_all_persons()  # From database
for person in persons:
    person_listbox.insert('end', f"{person.name} ({person.photo_count} photos)")

# Handle selection
def on_select(event):
    selection = person_listbox.curselection()
    if selection:
        index = selection[0]
        person_name = person_listbox.get(index).split(' ')[0]
        # Do something with selected person

person_listbox.bind('<<ListboxSelect>>', on_select)
```

### Table View (Treeview)
```python
# Create Treeview
columns = ('Name', 'Time', 'Confidence')
tree = ttk.Treeview(frame, columns=columns, show='headings')

# Define headings
tree.heading('Name', text='Name')
tree.heading('Time', text='Time')
tree.heading('Confidence', text='Confidence')

tree.pack()

# Populate
attendances = get_today_attendance()
for att in attendances:
    tree.insert('', 'end', values=(att.name, att.time, f"{att.confidence:.1f}%"))
```

---

## ✅ Kriteria Penilaian

| Kriteria | Bobot | Poin |
|----------|-------|------|
| GUI design & layout | 15% | 15 |
| Registration tab functional | 20% | 20 |
| Attendance tab functional | 20% | 20 |
| Reports tab functional | 20% | 20 |
| Settings tab functional | 10% | 10 |
| Integration with backend | 10% | 10 |
| Documentation & README | 5% | 5 |

**Total: 100 points**

---

## 🌟 Fitur Bonus

- [ ] Custom theme/styling (ttk themes)
- [ ] Icon buttons with images
- [ ] Splash screen saat startup
- [ ] Keyboard shortcuts
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Charts & graphs (matplotlib)
- [ ] Print report functionality
- [ ] Drag & drop image upload
- [ ] System tray icon
- [ ] Auto-update checker

**+5-15 pts per fitur**

---

## ⏰ Deadline

**7 hari** setelah menyelesaikan Minggu 7

---

## 🎓 Learning Outcomes

- ✅ Complete GUI development
- ✅ Multi-tab interface
- ✅ Webcam integration in GUI
- ✅ Module integration
- ✅ Production-ready app design

---

## 📚 Resources

- Minggu 7 Lesson 1, 2, & 3
- Tkinter documentation
- PIL/Pillow for image display
- ttk themes

**Good luck! 🖥️✨**
