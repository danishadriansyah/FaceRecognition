# Minggu 6 - Project: AttendanceSystem Class

## 📚 Overview
Production-ready `AttendanceSystem` class yang mengintegrasikan database management dengan face recognition untuk complete automated attendance system.

## 📁 Project Files

```
project/
├── README.md (file ini)
├── attendance_system.py (NEW - Main class)
├── recognition_service.py (from Week 5)
├── dataset_manager.py (from Week 4)
├── face_recognizer.py (from Week 3)
├── face_detector.py (from Week 2)
├── image_utils.py (from Week 1)
└── test_attendance.py (Testing file)
```

---

## 🎯 AttendanceSystem Class - Complete API

### Initialization

```python
from attendance_system import AttendanceSystem

# Basic initialization
attendance = AttendanceSystem(
    db_path='attendance.db',
    dataset_path='dataset/'
)

# With configuration
attendance = AttendanceSystem(
    db_path='attendance.db',
    dataset_path='dataset/',
    config={
        'work_hours': {
            'start': '09:00',
            'end': '17:00',
            'grace_minutes': 15
        },
        'recognition': {
            'min_confidence': 0.7,
            'duplicate_prevention_minutes': 5
        },
        'camera': {
            'location': 'Main Entrance',
            'id': 0
        }
    }
)
```

**Initializes:**
- SQLite database connection
- RecognitionService instance
- AttendanceLogic engine
- Configuration settings
- Logging system

---

## 🔧 Core Methods

### 1. add_employee()
**Purpose:** Register new employee in system

```python
# Basic add
attendance.add_employee(
    employee_id='001',
    name='Alice Johnson',
    department='Engineering'
)

# With full details
attendance.add_employee(
    employee_id='001',
    name='Alice Johnson',
    department='Engineering',
    email='alice@company.com',
    phone='+1234567890',
    metadata={
        'shift': 'morning',
        'position': 'Senior Engineer'
    }
)
```

**Parameters:**
- `employee_id` (str): Unique employee identifier
- `name` (str): Full name
- `department` (str): Department name
- `email` (str): Email address (optional)
- `phone` (str): Phone number (optional)
- `metadata` (dict): Additional info (optional)

**Returns:** `bool` - True if successful

**Creates:** Employee record in database

---

### 2. register_employee_face()
**Purpose:** Capture and register employee face

```python
# Interactive capture
attendance.register_employee_face(
    employee_id='001',
    photo_count=30
)

# From existing photos
attendance.register_employee_face(
    employee_id='001',
    from_folder='alice_photos/'
)
```

**Parameters:**
- `employee_id` (str): Employee identifier
- `photo_count` (int): Number of photos to capture (default: 30)
- `from_folder` (str): Load from folder instead of capture (optional)

**Process:**
1. Opens webcam (or loads folder)
2. Guides photo capture
3. Validates quality
4. Generates encodings
5. Updates recognition database
6. Links to employee record

**Returns:** `dict`
```python
{
    'success': True,
    'photos_captured': 28,
    'encodings_generated': 28,
    'quality_score': 0.92
}
```

---

### 3. mark_attendance_auto()
**Purpose:** Automated attendance marking via face recognition

```python
# Start automatic marking
attendance.mark_attendance_auto(
    camera_id=0,
    show_display=True
)

# With custom callback
def on_attendance_marked(employee_info):
    print(f"Welcome {employee_info['name']}!")
    # Send notification, unlock door, etc.

attendance.mark_attendance_auto(
    camera_id=0,
    on_attendance_callback=on_attendance_marked
)
```

**Parameters:**
- `camera_id` (int): Camera index (default: 0)
- `show_display` (bool): Show video feed (default: True)
- `on_attendance_callback` (callable): Callback when attendance marked (optional)
- `save_snapshots` (bool): Save recognized face images (default: False)

**Behavior:**
- Continuous face recognition
- Auto check-in on recognition
- Duplicate prevention (5-minute window)
- Confidence threshold filtering
- Real-time display with status
- Logging all attempts

**Display:**
```
┌─────────────────────────────────────┐
│  [Webcam Feed with Face Boxes]     │
│                                     │
│  ✅ Alice Johnson - 09:15 AM       │
│  ✅ Bob Smith - 09:18 AM           │
│  ⏳ Processing...                  │
│                                     │
│  FPS: 25 | Active: 2 employees     │
└─────────────────────────────────────┘
```

---

### 4. mark_attendance_manual()
**Purpose:** Manual attendance entry

```python
# Manual check-in
attendance.mark_attendance_manual(
    employee_id='001',
    action='check_in'
)

# Manual check-out
attendance.mark_attendance_manual(
    employee_id='001',
    action='check_out'
)

# With timestamp
from datetime import datetime
attendance.mark_attendance_manual(
    employee_id='001',
    action='check_in',
    timestamp=datetime(2025, 11, 14, 9, 15)
)
```

**Parameters:**
- `employee_id` (str): Employee identifier
- `action` (str): 'check_in' or 'check_out'
- `timestamp` (datetime): Custom timestamp (optional, default: now)
- `notes` (str): Additional notes (optional)

**Returns:** `dict`
```python
{
    'success': True,
    'employee_name': 'Alice Johnson',
    'action': 'check_in',
    'time': '2025-11-14 09:15:00',
    'status': 'on_time'  # or 'late'
}
```

---

### 5. get_daily_report()
**Purpose:** Generate daily attendance report

```python
# Today's report
report = attendance.get_daily_report()

# Specific date
from datetime import date
report = attendance.get_daily_report(
    date=date(2025, 11, 14)
)

# Export to CSV
attendance.get_daily_report(
    date=date(2025, 11, 14),
    export_csv=True,
    export_path='reports/daily_2025-11-14.csv'
)
```

**Parameters:**
- `date` (date): Report date (default: today)
- `export_csv` (bool): Export to CSV (default: False)
- `export_path` (str): CSV file path (optional)

**Returns:** `dict`
```python
{
    'date': '2025-11-14',
    'total_employees': 50,
    'present': 45,
    'absent': 5,
    'late': 8,
    'on_time': 37,
    'attendance_rate': 0.90,  # 90%
    'employees': [
        {
            'employee_id': '001',
            'name': 'Alice Johnson',
            'department': 'Engineering',
            'check_in': '09:15:00',
            'check_out': '17:30:00',
            'status': 'on_time',
            'working_hours': 8.25
        },
        # ... more employees
    ]
}
```

---

### 6. get_employee_history()
**Purpose:** Get attendance history for employee

```python
# Month history
history = attendance.get_employee_history(
    employee_id='001',
    year=2025,
    month=11
)

# Date range
from datetime import date
history = attendance.get_employee_history(
    employee_id='001',
    start_date=date(2025, 11, 1),
    end_date=date(2025, 11, 30)
)
```

**Parameters:**
- `employee_id` (str): Employee identifier
- `year` (int): Year (optional)
- `month` (int): Month (optional)
- `start_date` (date): Range start (optional)
- `end_date` (date): Range end (optional)

**Returns:** `dict`
```python
{
    'employee_id': '001',
    'name': 'Alice Johnson',
    'period': '2025-11',
    'total_working_days': 22,
    'present_days': 20,
    'absent_days': 2,
    'late_count': 3,
    'total_hours': 162.5,
    'avg_hours_per_day': 8.1,
    'attendance_rate': 0.909,  # 90.9%
    'details': [
        {
            'date': '2025-11-01',
            'check_in': '09:00:00',
            'check_out': '17:15:00',
            'status': 'on_time',
            'hours': 8.25
        },
        # ... more days
    ]
}
```

---

### 7. get_department_summary()
**Purpose:** Department-wise attendance statistics

```python
# All departments today
summary = attendance.get_department_summary()

# Specific date
summary = attendance.get_department_summary(
    date=date(2025, 11, 14)
)
```

**Returns:** `list[dict]`
```python
[
    {
        'department': 'Engineering',
        'total_employees': 20,
        'present': 18,
        'absent': 2,
        'attendance_rate': 0.90,
        'avg_check_in_time': '09:05:00',
        'late_count': 3
    },
    {
        'department': 'Sales',
        'total_employees': 15,
        'present': 15,
        'absent': 0,
        'attendance_rate': 1.00,
        'avg_check_in_time': '08:55:00',
        'late_count': 0
    }
]
```

---

### 8. generate_monthly_report()
**Purpose:** Comprehensive monthly report

```python
# Generate report
report = attendance.generate_monthly_report(
    year=2025,
    month=11,
    export_pdf=True,
    output_path='reports/monthly_2025-11.pdf'
)
```

**Parameters:**
- `year` (int): Report year
- `month` (int): Report month
- `export_pdf` (bool): Generate PDF (default: False)
- `export_excel` (bool): Generate Excel (default: False)
- `output_path` (str): Output file path (optional)

**Returns:** `dict` with comprehensive monthly statistics

**PDF Report includes:**
- Summary statistics
- Daily attendance chart
- Employee-wise breakdown
- Department comparison
- Late arrivals list
- Perfect attendance list
- Absenteeism analysis

---

### 9. update_employee()
**Purpose:** Update employee information

```python
# Update department
attendance.update_employee(
    employee_id='001',
    department='Research & Development'
)

# Multiple fields
attendance.update_employee(
    employee_id='001',
    department='R&D',
    email='alice.new@company.com',
    phone='+9876543210'
)
```

**Parameters:**
- `employee_id` (str): Employee identifier
- `**kwargs`: Fields to update

**Returns:** `bool` - True if successful

---

### 10. deactivate_employee()
**Purpose:** Mark employee as inactive (resigned/terminated)

```python
# Deactivate
attendance.deactivate_employee(
    employee_id='001',
    reason='Resigned',
    effective_date=date(2025, 11, 30)
)
```

**Parameters:**
- `employee_id` (str): Employee identifier
- `reason` (str): Deactivation reason (optional)
- `effective_date` (date): Effective date (optional, default: today)

**Effect:**
- Marks employee as inactive
- Stops attendance marking
- Preserves historical data
- Logs deactivation

---

## 📖 Complete Usage Examples

### Example 1: Complete Employee Onboarding

```python
from attendance_system import AttendanceSystem

attendance = AttendanceSystem()

# Step 1: Add employee to database
attendance.add_employee(
    employee_id='001',
    name='Alice Johnson',
    department='Engineering',
    email='alice@company.com'
)

# Step 2: Register face
print("Please look at camera for face registration...")
result = attendance.register_employee_face(
    employee_id='001',
    photo_count=30
)

if result['success']:
    print(f"✅ Face registered! Quality: {result['quality_score']:.2f}")
    print(f"   Photos: {result['photos_captured']}")
    print(f"   Encodings: {result['encodings_generated']}")
else:
    print("❌ Face registration failed!")

print("\n✅ Employee onboarding complete!")
```

---

### Example 2: Daily Attendance Operations

```python
import time
from datetime import datetime, date

attendance = AttendanceSystem()

# Start automated attendance marking
print("Starting attendance system...")
print("Press Ctrl+C to stop\n")

# Custom callback for attendance events
def on_attendance(employee_info):
    name = employee_info['name']
    time = employee_info['check_in_time']
    status = employee_info['status']
    
    print(f"\n✅ Attendance marked:")
    print(f"   Name: {name}")
    print(f"   Time: {time}")
    print(f"   Status: {status}")
    
    # Could trigger:
    # - Email notification
    # - Slack message
    # - Door unlock
    # - Update dashboard

try:
    attendance.mark_attendance_auto(
        camera_id=0,
        show_display=True,
        on_attendance_callback=on_attendance,
        save_snapshots=True  # Save recognized faces
    )
except KeyboardInterrupt:
    print("\n\nGenerating daily report...")
    
    # Generate and display report
    report = attendance.get_daily_report(
        export_csv=True,
        export_path=f'reports/daily_{date.today()}.csv'
    )
    
    print(f"\n📊 Daily Report - {report['date']}")
    print(f"   Total Employees: {report['total_employees']}")
    print(f"   Present: {report['present']}")
    print(f"   Absent: {report['absent']}")
    print(f"   Late: {report['late']}")
    print(f"   Attendance Rate: {report['attendance_rate']*100:.1f}%")
    print(f"\n✅ Report saved to reports/daily_{date.today()}.csv")
```

---

### Example 3: Monthly Reporting

```python
from datetime import date

attendance = AttendanceSystem()

# Generate comprehensive monthly report
print("Generating monthly report...")

report = attendance.generate_monthly_report(
    year=2025,
    month=11,
    export_pdf=True,
    export_excel=True,
    output_path='reports/november_2025'
)

print("\n📊 Monthly Report - November 2025")
print(f"   Total Employees: {report['total_employees']}")
print(f"   Avg Attendance Rate: {report['avg_attendance_rate']*100:.1f}%")
print(f"   Total Working Days: {report['working_days']}")
print(f"   Perfect Attendance: {len(report['perfect_attendance'])} employees")
print(f"   High Absenteeism: {len(report['high_absenteeism'])} employees")

print("\n📄 Department Summary:")
for dept in report['department_summary']:
    print(f"   {dept['department']}: {dept['attendance_rate']*100:.1f}%")

print("\n✅ Reports saved:")
print("   - reports/november_2025.pdf")
print("   - reports/november_2025.xlsx")
```

---

### Example 4: Employee Self-Service

```python
attendance = AttendanceSystem()

# Employee portal functionality
def employee_portal(employee_id):
    """Simple employee self-service portal"""
    
    # Get employee info
    employee = attendance.get_employee_info(employee_id)
    print(f"\n👤 Welcome, {employee['name']}!")
    
    # Today's status
    today_status = attendance.get_employee_today_status(employee_id)
    if today_status['checked_in']:
        print(f"✅ Checked in at {today_status['check_in_time']}")
        if today_status['checked_out']:
            print(f"✅ Checked out at {today_status['check_out_time']}")
            print(f"   Hours worked: {today_status['hours_worked']:.2f}")
        else:
            print("⏳ Not checked out yet")
    else:
        print("❌ Not checked in today")
    
    # Monthly summary
    history = attendance.get_employee_history(
        employee_id=employee_id,
        year=2025,
        month=11
    )
    
    print(f"\n📊 Your November Summary:")
    print(f"   Present Days: {history['present_days']}/{history['total_working_days']}")
    print(f"   Attendance Rate: {history['attendance_rate']*100:.1f}%")
    print(f"   Late Count: {history['late_count']}")
    print(f"   Total Hours: {history['total_hours']:.1f}")
    print(f"   Avg Hours/Day: {history['avg_hours_per_day']:.1f}")

# Usage
employee_portal('001')
```

---

## 🧪 Testing

Run comprehensive tests:
```bash
cd minggu-6-database-attendance/project
python test_attendance.py
```

**Tests include:**
- Employee registration
- Face enrollment
- Check-in/check-out
- Duplicate prevention
- Late detection
- Report generation
- Database queries
- Error handling

**Expected output:**
```
Test 1: Add Employee.................. PASS
Test 2: Register Face................. PASS
Test 3: Mark Attendance............... PASS
Test 4: Duplicate Prevention.......... PASS
Test 5: Late Detection................ PASS
Test 6: Daily Report.................. PASS
Test 7: Monthly Report................ PASS
Test 8: Department Summary............ PASS
Test 9: Employee History.............. PASS
Test 10: Deactivate Employee.......... PASS

All tests passed! ✅
```

---

## ⚙️ Configuration File

Create `attendance_config.json`:
```json
{
  "database": {
    "path": "attendance.db",
    "backup_enabled": true,
    "backup_interval_hours": 24
  },
  "work_hours": {
    "start": "09:00",
    "end": "17:00",
    "grace_minutes": 15,
    "min_work_hours": 8
  },
  "recognition": {
    "min_confidence": 0.7,
    "duplicate_prevention_minutes": 5,
    "save_snapshots": true,
    "snapshot_path": "snapshots/"
  },
  "camera": {
    "default_id": 0,
    "location": "Main Entrance",
    "resolution": [640, 480],
    "fps": 30
  },
  "reports": {
    "output_dir": "reports/",
    "auto_export_daily": true,
    "auto_export_monthly": true,
    "formats": ["csv", "pdf", "excel"]
  },
  "notifications": {
    "enabled": true,
    "late_arrival_alert": true,
    "absent_alert": true,
    "email_notifications": false
  }
}
```

---

## 🐛 Troubleshooting

**Recognition not working:**
- Check camera connection
- Verify faces registered
- Lower confidence threshold
- Improve lighting

**Duplicate attendance:**
- Verify duplicate prevention setting
- Check time window configuration
- Review logs for timing issues

**Database errors:**
- Check file permissions
- Verify schema migrations
- Backup and restore if corrupted

**Report generation slow:**
- Add database indexes
- Limit date ranges
- Use caching for frequent queries

---

## 📊 Performance Metrics

**Attendance marking:**
- Recognition time: <1 second
- Database insert: <100ms
- Total check-in time: ~1-2 seconds

**Report generation:**
- Daily report (50 employees): <1 second
- Monthly report: <5 seconds
- Export to PDF: <10 seconds

---

## ⏭️ Next Steps

After mastering AttendanceSystem:

1. ✅ Complete employee database
2. ✅ Face recognition working
3. ✅ Daily operations smooth
4. ✅ Proceed to **Minggu 7: Desktop GUI Application**

---

**Automation saves time! ⏰**

*Let technology handle attendance, humans focus on work!*
