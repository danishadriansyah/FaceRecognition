# Minggu 7 - Project: Complete Application (Desktop + API)

## 📚 Overview
Production-ready complete application combining desktop GUI dan RESTful API. Includes admin panel, employee portal, dan monitoring dashboard.

## 📁 Project Files

```
project/
├── README.md (file ini)
├── app.py (NEW - Main Flask application with API)
├── gui_admin.py (NEW - Admin desktop GUI)
├── gui_employee.py (NEW - Employee self-service GUI)
├── attendance_system.py (from Week 6)
├── recognition_service.py (from Week 5)
├── dataset_manager.py (from Week 4)
├── face_recognizer.py (from Week 3)
├── face_detector.py (from Week 2)
├── image_utils.py (from Week 1)
├── config.json (Configuration file)
└── requirements.txt (Dependencies)
```

---

## 🎯 Application Components

### 1. Flask API Server (`app.py`)

Complete RESTful API dengan authentication. Lihat minggu-7/learning untuk endpoint details.

**Features:**
- Employee CRUD operations
- Attendance marking (check-in/out)
- Report generation (daily/monthly)
- Department statistics
- JWT authentication
- Role-based access control

**Run:**
```bash
python app.py
```

**Access:** http://localhost:5000

---

### 2. Admin Desktop GUI (`gui_admin.py`)

Comprehensive admin panel untuk manage complete system.

**Features:**
- Employee management (add/edit/deactivate)
- Face enrollment
- Real-time attendance monitoring
- Report generation dan export
- Database management
- System configuration
- Attendance override
- User management

**Run:**
```bash
python gui_admin.py
```

**GUI Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  ATTENDANCE SYSTEM - ADMIN PANEL                        │
├─────────────────────────────────────────────────────────┤
│ File  Employees  Attendance  Reports  Settings  Help   │
├──────────────┬──────────────────────────────────────────┤
│              │                                          │
│  Dashboard   │  📊 Today's Summary                     │
│  Employees   │  Total Employees: 50                    │
│  Attendance  │  Present: 45 (90%)                      │
│  Face Enroll │  Late: 8                                │
│  Reports     │  Absent: 5                              │
│  Database    │                                          │
│  Settings    │  ┌────────────────────────────────────┐│
│  Users       │  │  Recent Attendance                 ││
│              │  │  09:00 - Alice Johnson   ✅        ││
│              │  │  09:05 - Bob Smith       ✅        ││
│              │  │  09:12 - Charlie Lee     ⚠️ Late   ││
│              │  └────────────────────────────────────┘│
│              │                                          │
│              │  [Start Camera] [Export Report] [Help] │
└──────────────┴──────────────────────────────────────────┘
```

**Implementation (simplified):**

```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from attendance_system import AttendanceSystem
import threading
from datetime import date

class AdminGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Attendance System - Admin Panel")
        self.root.geometry("1200x700")
        
        # Initialize system
        self.attendance = AttendanceSystem()
        
        # Create GUI
        self.create_menu()
        self.create_layout()
        self.load_dashboard()
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Export Database", command=self.export_db)
        file_menu.add_command(label="Backup Database", command=self.backup_db)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Employees menu
        emp_menu = tk.Menu(menubar, tearoff=0)
        emp_menu.add_command(label="Add Employee", command=self.add_employee_dialog)
        emp_menu.add_command(label="View All", command=self.view_employees)
        emp_menu.add_command(label="Enroll Face", command=self.enroll_face_dialog)
        menubar.add_cascade(label="Employees", menu=emp_menu)
        
        # Reports menu
        report_menu = tk.Menu(menubar, tearoff=0)
        report_menu.add_command(label="Daily Report", command=self.daily_report)
        report_menu.add_command(label="Monthly Report", command=self.monthly_report)
        report_menu.add_command(label="Department Summary", command=self.dept_summary)
        menubar.add_cascade(label="Reports", menu=report_menu)
        
        self.root.config(menu=menubar)
    
    def create_layout(self):
        """Create main layout"""
        # Sidebar
        sidebar = tk.Frame(self.root, width=200, bg='#2c3e50', relief='raised', bd=2)
        sidebar.pack(side='left', fill='y')
        
        # Sidebar buttons
        buttons = [
            ("📊 Dashboard", self.load_dashboard),
            ("👥 Employees", self.view_employees),
            ("📋 Attendance", self.view_attendance),
            ("📸 Face Enroll", self.enroll_face_dialog),
            ("📊 Reports", self.show_reports),
            ("💾 Database", self.manage_database),
            ("⚙️ Settings", self.show_settings),
            ("👤 Users", self.manage_users)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                sidebar, text=text, command=command,
                bg='#34495e', fg='white', relief='flat',
                font=('Arial', 11), anchor='w', padx=20
            )
            btn.pack(fill='x', pady=2)
        
        # Main content area
        self.content = tk.Frame(self.root, bg='white')
        self.content.pack(side='right', fill='both', expand=True)
    
    def load_dashboard(self):
        """Load dashboard view"""
        # Clear content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Title
        title = tk.Label(
            self.content, text="📊 Dashboard",
            font=('Arial', 20, 'bold'), bg='white'
        )
        title.pack(pady=20)
        
        # Get today's data
        report = self.attendance.get_daily_report()
        
        # Summary cards
        cards_frame = tk.Frame(self.content, bg='white')
        cards_frame.pack(pady=20)
        
        self.create_card(cards_frame, "Total Employees", 
                        report['total_employees'], "#3498db", 0, 0)
        self.create_card(cards_frame, "Present Today", 
                        report['present'], "#2ecc71", 0, 1)
        self.create_card(cards_frame, "Absent", 
                        report['absent'], "#e74c3c", 0, 2)
        self.create_card(cards_frame, "Late Arrivals", 
                        report['late'], "#f39c12", 0, 3)
        
        # Recent attendance table
        tk.Label(
            self.content, text="Recent Attendance",
            font=('Arial', 14, 'bold'), bg='white'
        ).pack(pady=(20, 10))
        
        # Create table
        table_frame = tk.Frame(self.content)
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('Time', 'Employee ID', 'Name', 'Department', 'Status')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Populate data
        for emp in report['employees'][:20]:  # Show last 20
            status = "✅ On Time" if emp['status'] == 'on_time' else "⚠️ Late"
            tree.insert('', 'end', values=(
                emp['check_in'],
                emp['employee_id'],
                emp['name'],
                emp['department'],
                status
            ))
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Action buttons
        btn_frame = tk.Frame(self.content, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame, text="🎥 Start Camera Attendance",
            command=self.start_camera_attendance, bg='#27ae60',
            fg='white', font=('Arial', 12), padx=20, pady=10
        ).pack(side='left', padx=10)
        
        tk.Button(
            btn_frame, text="📄 Export Today's Report",
            command=self.export_today, bg='#2980b9',
            fg='white', font=('Arial', 12), padx=20, pady=10
        ).pack(side='left', padx=10)
    
    def create_card(self, parent, title, value, color, row, col):
        """Create summary card"""
        card = tk.Frame(parent, bg=color, width=200, height=100)
        card.grid(row=row, column=col, padx=10, pady=10)
        card.grid_propagate(False)
        
        tk.Label(
            card, text=str(value), font=('Arial', 32, 'bold'),
            bg=color, fg='white'
        ).pack(expand=True)
        
        tk.Label(
            card, text=title, font=('Arial', 12),
            bg=color, fg='white'
        ).pack()
    
    def add_employee_dialog(self):
        """Dialog to add new employee"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Employee")
        dialog.geometry("400x300")
        
        # Fields
        fields = [
            ("Employee ID:", "employee_id"),
            ("Full Name:", "name"),
            ("Department:", "department"),
            ("Email:", "email"),
            ("Phone:", "phone")
        ]
        
        entries = {}
        
        for i, (label, field) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, sticky='e', padx=10, pady=5)
            entry = tk.Entry(dialog, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field] = entry
        
        def submit():
            # Get values
            data = {field: entry.get() for field, entry in entries.items()}
            
            # Validate
            if not data['employee_id'] or not data['name']:
                messagebox.showerror("Error", "Employee ID and Name required")
                return
            
            # Add to system
            success = self.attendance.add_employee(**data)
            
            if success:
                messagebox.showinfo("Success", f"Employee {data['name']} added")
                dialog.destroy()
                self.load_dashboard()
            else:
                messagebox.showerror("Error", "Failed to add employee")
        
        tk.Button(
            dialog, text="Add Employee", command=submit,
            bg='#27ae60', fg='white', font=('Arial', 12), padx=20, pady=5
        ).grid(row=len(fields), column=0, columnspan=2, pady=20)
    
    def start_camera_attendance(self):
        """Start automated camera attendance"""
        def run_camera():
            try:
                self.attendance.mark_attendance_auto(
                    camera_id=0,
                    show_display=True
                )
            except Exception as e:
                messagebox.showerror("Error", f"Camera error: {e}")
        
        # Run in thread to not block GUI
        thread = threading.Thread(target=run_camera, daemon=True)
        thread.start()
        
        messagebox.showinfo(
            "Camera Started",
            "Automated attendance marking started.\nPress 'q' in camera window to stop."
        )
    
    def export_today(self):
        """Export today's report"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"attendance_{date.today()}.csv"
        )
        
        if filename:
            self.attendance.get_daily_report(
                export_csv=True,
                export_path=filename
            )
            messagebox.showinfo("Success", f"Report exported to {filename}")
    
    def run(self):
        """Start GUI"""
        self.root.mainloop()

if __name__ == '__main__':
    app = AdminGUI()
    app.run()
```

---

### 3. Employee Self-Service GUI (`gui_employee.py`)

Simple interface untuk employees check attendance dan view history.

**Features:**
- View today's status (checked in/out)
- Monthly attendance summary
- Personal statistics
- Request leave (placeholder)

**Run:**
```bash
python gui_employee.py
```

**GUI Layout:**
```
┌─────────────────────────────────────────┐
│  Employee Portal - Alice Johnson        │
├─────────────────────────────────────────┤
│                                         │
│  📅 Today: November 14, 2025           │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │  ✅ Checked In: 09:15 AM       │  │
│  │  ⏳ Not Checked Out Yet         │  │
│  └─────────────────────────────────┘  │
│                                         │
│  📊 November Summary                   │
│                                         │
│  Present Days:   20 / 22               │
│  Attendance:     90.9%                 │
│  Late Count:     3                     │
│  Total Hours:    162.5                 │
│  Avg Hours/Day:  8.1                   │
│                                         │
│  [View Full History] [Request Leave]   │
└─────────────────────────────────────────┘
```

**Implementation:**

```python
import tkinter as tk
from tkinter import messagebox
from attendance_system import AttendanceSystem
from datetime import date, datetime

class EmployeeGUI:
    def __init__(self, employee_id):
        self.employee_id = employee_id
        self.attendance = AttendanceSystem()
        
        # Get employee info
        self.employee = self.attendance.get_employee_info(employee_id)
        
        if not self.employee:
            messagebox.showerror("Error", "Employee not found")
            return
        
        self.root = tk.Tk()
        self.root.title(f"Employee Portal - {self.employee['name']}")
        self.root.geometry("500x600")
        
        self.create_ui()
    
    def create_ui(self):
        """Create employee UI"""
        # Header
        header = tk.Frame(self.root, bg='#3498db', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header, text=f"Welcome, {self.employee['name']}!",
            font=('Arial', 18, 'bold'), bg='#3498db', fg='white'
        ).pack(pady=25)
        
        # Content
        content = tk.Frame(self.root, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Today's status
        tk.Label(
            content, text=f"📅 {date.today().strftime('%B %d, %Y')}",
            font=('Arial', 12), bg='white'
        ).pack(pady=(0, 20))
        
        status_frame = tk.Frame(content, bg='#ecf0f1', relief='ridge', bd=2)
        status_frame.pack(fill='x', pady=10)
        
        today_status = self.attendance.get_employee_today_status(self.employee_id)
        
        if today_status['checked_in']:
            check_in_text = f"✅ Checked In: {today_status['check_in_time']}"
        else:
            check_in_text = "❌ Not Checked In Yet"
        
        tk.Label(
            status_frame, text=check_in_text,
            font=('Arial', 14), bg='#ecf0f1', fg='#27ae60' if today_status['checked_in'] else '#e74c3c'
        ).pack(pady=10)
        
        if today_status['checked_in'] and today_status['checked_out']:
            tk.Label(
                status_frame, text=f"✅ Checked Out: {today_status['check_out_time']}",
                font=('Arial', 14), bg='#ecf0f1', fg='#27ae60'
            ).pack(pady=10)
            
            tk.Label(
                status_frame, text=f"Hours Worked: {today_status['hours_worked']:.2f}",
                font=('Arial', 12, 'bold'), bg='#ecf0f1'
            ).pack(pady=10)
        elif today_status['checked_in']:
            tk.Label(
                status_frame, text="⏳ Not Checked Out Yet",
                font=('Arial', 14), bg='#ecf0f1', fg='#f39c12'
            ).pack(pady=10)
        
        # Monthly summary
        tk.Label(
            content, text="📊 This Month Summary",
            font=('Arial', 14, 'bold'), bg='white'
        ).pack(pady=(20, 10))
        
        history = self.attendance.get_employee_history(
            employee_id=self.employee_id,
            year=date.today().year,
            month=date.today().month
        )
        
        stats = [
            ("Present Days", f"{history['present_days']} / {history['total_working_days']}"),
            ("Attendance Rate", f"{history['attendance_rate']*100:.1f}%"),
            ("Late Count", str(history['late_count'])),
            ("Total Hours", f"{history['total_hours']:.1f}"),
            ("Avg Hours/Day", f"{history['avg_hours_per_day']:.1f}")
        ]
        
        for label, value in stats:
            row = tk.Frame(content, bg='white')
            row.pack(fill='x', pady=5)
            
            tk.Label(
                row, text=label + ":", font=('Arial', 11),
                bg='white', anchor='w'
            ).pack(side='left')
            
            tk.Label(
                row, text=value, font=('Arial', 11, 'bold'),
                bg='white', anchor='e'
            ).pack(side='right')
        
        # Buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(pady=30)
        
        tk.Button(
            btn_frame, text="View Full History",
            command=self.view_history, bg='#3498db',
            fg='white', font=('Arial', 11), padx=15, pady=8
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame, text="Refresh",
            command=self.create_ui, bg='#95a5a6',
            fg='white', font=('Arial', 11), padx=15, pady=8
        ).pack(side='left', padx=5)
    
    def view_history(self):
        """Show full attendance history"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Attendance History")
        history_window.geometry("600x400")
        
        # Get history
        history = self.attendance.get_employee_history(
            employee_id=self.employee_id,
            year=date.today().year,
            month=date.today().month
        )
        
        # Create table
        from tkinter import ttk
        
        columns = ('Date', 'Check In', 'Check Out', 'Hours', 'Status')
        tree = ttk.Treeview(history_window, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
        
        for detail in history['details']:
            tree.insert('', 'end', values=(
                detail['date'],
                detail['check_in'] or '-',
                detail['check_out'] or '-',
                f"{detail['hours']:.2f}" if detail['hours'] else '-',
                detail['status']
            ))
        
        tree.pack(fill='both', expand=True)
    
    def run(self):
        """Start GUI"""
        self.root.mainloop()

if __name__ == '__main__':
    # Login dialog to get employee ID
    login_root = tk.Tk()
    login_root.withdraw()
    
    employee_id = tk.simpledialog.askstring("Login", "Enter Employee ID:")
    
    if employee_id:
        app = EmployeeGUI(employee_id)
        app.run()
```

---

## 🔧 Complete Setup

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**requirements.txt:**
```
opencv-python
face-recognition
numpy
Pillow
Flask
flask-cors
flask-jwt-extended
werkzeug
pandas
openpyxl
reportlab
```

---

### Configuration

**config.json:**
```json
{
  "database": {
    "path": "attendance.db"
  },
  "dataset": {
    "path": "dataset/"
  },
  "api": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false,
    "jwt_secret": "change-this-in-production"
  },
  "camera": {
    "default_id": 0,
    "resolution": [640, 480]
  },
  "work_hours": {
    "start": "09:00",
    "end": "17:00",
    "grace_minutes": 15
  }
}
```

---

## 🚀 Running the Complete System

### Option 1: Desktop Only

```bash
# Run admin GUI
python gui_admin.py

# Or employee portal
python gui_employee.py
```

### Option 2: API + Desktop

**Terminal 1 - API Server:**
```bash
python app.py
```

**Terminal 2 - Admin GUI:**
```bash
python gui_admin.py
```

### Option 3: Production Mode

```bash
# Use production server
pip install gunicorn

# Run API
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Run GUI on client machines
python gui_admin.py
```

---

## 📖 User Guide

### Admin Tasks

**1. Add New Employee:**
- Employees → Add Employee
- Fill details
- Click "Add Employee"

**2. Enroll Face:**
- Face Enroll → Select employee
- Click "Start Capture"
- Follow on-screen instructions
- System captures 30 photos
- Encodings generated automatically

**3. View Reports:**
- Reports → Daily/Monthly
- Select date/month
- Click "Generate"
- Export to CSV/PDF

### Employee Tasks

**1. Check Status:**
- Login with employee ID
- View today's check-in/out
- See monthly summary

**2. View History:**
- Click "View Full History"
- Browse past attendance
- Check hours worked

---

## ✅ Testing Checklist

```
[ ] API server starts without errors
[ ] Admin GUI opens successfully
[ ] Employee GUI opens successfully
[ ] Can add new employee
[ ] Face enrollment works
[ ] Camera attendance functional
[ ] Reports generate correctly
[ ] Database updates properly
[ ] Authentication working
[ ] All endpoints responsive
```

---

## 🐛 Troubleshooting

**GUI won't start:**
- Install tkinter: `sudo apt-get install python3-tk` (Linux)
- Check Python version (3.7+)

**API connection failed:**
- Check if server running
- Verify port 5000 available
- Check firewall settings

**Camera not working:**
- Test camera index (0, 1, 2)
- Check camera permissions
- Close other apps using camera

**Database locked:**
- Close all connections
- Check file permissions
- Restart application

---

## ⏭️ Next Steps

Complete! Lanjut ke **Minggu 8: Final Testing & Deployment**

---

**Complete system ready! 🎉**

*From concept to production!*
