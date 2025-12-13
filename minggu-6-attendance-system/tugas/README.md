# 📝 TUGAS MINGGU 6 - Database & Attendance System

## Deskripsi
Buat complete attendance system dengan MySQL database, auto-attendance, dan comprehensive reporting.

---

## 🎯 Objektif
- MySQL database integration
- Attendance logic implementation
- Duplicate prevention
- Report generation (Excel/CSV)
- Analytics & statistics

---

## 📋 Tugas: Smart Attendance System

Buat program `attendance_system.py` dengan fitur:

### Fitur Wajib

1. **Database Setup**
   - MySQL database dengan 3 tables:
     - `persons` (id, name, photo_path, created_at)
     - `attendance` (id, person_id, timestamp, confidence)
     - `settings` (key, value)
   - SQLAlchemy ORM models
   - Auto-create tables
   - Sample data seeder

2. **Auto-Attendance**
   - Real-time webcam recognition
   - Auto-mark attendance saat recognize
   - Duplicate prevention (1x per day)
   - Confidence threshold (min 85%)
   - Visual/audio feedback
   - Save screenshot

3. **Manual Attendance**
   - Register person form
   - Mark attendance manually
   - Edit attendance
   - Delete attendance (admin only)

4. **Reports & Analytics**
   - **Daily Report**:
     - Who attended today
     - Attendance time
     - Confidence score
   - **Monthly Summary**:
     - Total attendance per person
     - Attendance percentage
     - Most active days
   - **Export Options**:
     - Excel (formatted)
     - CSV (raw data)
     - PDF report (bonus)

---

## 📦 Deliverables

```
tugas/
├── attendance_system.py       # Main application
├── database/
│   ├── models.py             # SQLAlchemy models
│   ├── db_manager.py         # Database operations
│   └── seed_data.py          # Sample data
├── reports/                  # Generated reports
│   ├── daily_20251118.xlsx
│   ├── monthly_202511.xlsx
│   └── attendance.csv
├── screenshots/              # Attendance screenshots
├── logs/                     # Application logs
└── README.md
```

---

## 🎯 Example Output

### Auto-Attendance:
```
========================================
   SMART ATTENDANCE SYSTEM
========================================

Database: MySQL connected ✅
Total registered: 15 persons
Today's attendance: 8 persons

Mode: Auto-Attendance (Webcam)

[11:23:45] ✅ Andi recognized (92.3%)
           ✅ Attendance marked
           Screenshot saved

[11:24:12] ✅ Budi recognized (88.7%)
           ⚠️  Already marked today

[11:24:45] ❌ Unknown person (67.2%)
           Confidence too low

Press 'r' for report, 'q' to quit
```

### Daily Report:
```
DAILY ATTENDANCE REPORT
========================
Date: November 18, 2025

Total Present: 8/15 (53.3%)

Name          Time      Confidence
---------------------------------
Andi          08:15     92.3%
Budi          08:23     88.7%
Citra         08:45     95.1%
Dedi          09:02     87.9%
Endang        09:15     91.4%
Fajar         09:30     89.2%
Gita          10:12     93.7%
Hendra        10:45     90.8%

Absent: 7 persons
---------------------------------
Indah, Joko, Kiki, Lina, 
Maya, Nanda, Omar

Report saved to: reports/daily_20251118.xlsx
```

---

## 💡 Hints & Tips

### Database Models
```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Person(Base):
    __tablename__ = 'persons'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    photo_path = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    
    attendances = relationship('Attendance', back_populates='person')

class Attendance(Base):
    __tablename__ = 'attendance'
    
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'))
    timestamp = Column(DateTime, default=datetime.now)
    confidence = Column(Float)
    screenshot_path = Column(String(255))
    
    person = relationship('Person', back_populates='attendances')

# Create tables
engine = create_engine('mysql+pymysql://root:password@localhost/attendance_db')
Base.metadata.create_all(engine)
```

### Duplicate Prevention
```python
from datetime import date

def can_mark_attendance(person_id, session):
    today = date.today()
    
    existing = session.query(Attendance).filter(
        Attendance.person_id == person_id,
        func.date(Attendance.timestamp) == today
    ).first()
    
    return existing is None

# Usage
if can_mark_attendance(person_id, session):
    attendance = Attendance(
        person_id=person_id,
        confidence=confidence,
        screenshot_path=screenshot_path
    )
    session.add(attendance)
    session.commit()
    print("✅ Attendance marked")
else:
    print("⚠️  Already marked today")
```

### Daily Report
```python
import pandas as pd
from datetime import date

def generate_daily_report(session, report_date=None):
    if report_date is None:
        report_date = date.today()
    
    # Query attendance
    attendances = session.query(Attendance, Person).join(Person).filter(
        func.date(Attendance.timestamp) == report_date
    ).all()
    
    # Create dataframe
    data = []
    for att, person in attendances:
        data.append({
            'Name': person.name,
            'Time': att.timestamp.strftime('%H:%M'),
            'Confidence': f"{att.confidence:.1f}%"
        })
    
    df = pd.DataFrame(data)
    
    # Export to Excel
    filename = f"reports/daily_{report_date.strftime('%Y%m%d')}.xlsx"
    df.to_excel(filename, index=False)
    
    return filename
```

### Monthly Summary
```python
def generate_monthly_report(session, year, month):
    attendances = session.query(
        Person.name,
        func.count(Attendance.id).label('total'),
        func.avg(Attendance.confidence).label('avg_confidence')
    ).join(Attendance).filter(
        extract('year', Attendance.timestamp) == year,
        extract('month', Attendance.timestamp) == month
    ).group_by(Person.id).all()
    
    data = []
    for name, total, avg_conf in attendances:
        data.append({
            'Name': name,
            'Total Days': total,
            'Avg Confidence': f"{avg_conf:.1f}%",
            'Attendance %': f"{(total/22)*100:.1f}%"  # Assuming 22 working days
        })
    
    df = pd.DataFrame(data)
    filename = f"reports/monthly_{year}{month:02d}.xlsx"
    
    # Write with formatting
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Summary', index=False)
    
    return filename
```

### Visual Feedback
```python
def mark_attendance_with_feedback(person_name, confidence):
    print(f"\n{'='*50}")
    print(f"  ✅ ATTENDANCE MARKED")
    print(f"{'='*50}")
    print(f"  Name: {person_name}")
    print(f"  Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"  Confidence: {confidence:.1f}%")
    print(f"{'='*50}\n")
    
    # Optional: Play sound
    # import winsound
    # winsound.Beep(1000, 200)  # Frequency, Duration
```

---

## ✅ Kriteria Penilaian

| Kriteria | Bobot | Poin |
|----------|-------|------|
| Database setup & models | 15% | 15 |
| Auto-attendance working | 25% | 25 |
| Duplicate prevention | 15% | 15 |
| Daily report (Excel) | 15% | 15 |
| Monthly report (Excel) | 15% | 15 |
| Manual attendance CRUD | 10% | 10 |
| Documentation | 5% | 5 |

**Total: 100 points**

---

## 🌟 Fitur Bonus

- [ ] PDF report generation
- [ ] Email daily report automatically
- [ ] SMS notification for attendance
- [ ] Late arrival tracking (>09:00)
- [ ] Leave management
- [ ] Export to Google Sheets
- [ ] Attendance trends (graphs)
- [ ] Multi-shift support
- [ ] Backup database daily
- [ ] Admin dashboard (web-based)

**+10 pts per fitur**

---

## ⏰ Deadline

**5 hari** setelah menyelesaikan Minggu 6

---

## 🎓 Learning Outcomes

- ✅ MySQL database integration
- ✅ SQLAlchemy ORM
- ✅ Business logic implementation
- ✅ Report generation
- ✅ Data export (Excel/CSV)

---

## 📚 Resources

- Minggu 6 Lesson 1 & 2
- SQLAlchemy documentation
- Pandas & openpyxl docs
- MySQL tutorials

**Good luck! 📊✅**
