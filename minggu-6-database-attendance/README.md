# Minggu 6: Database & Attendance System

## Tujuan Pembelajaran
- Setup database MySQL
- Database models dan relationships
- Attendance record management
- CRUD operations
- Query dan reporting

## Struktur Folder

```
minggu-6-database-attendance/
├── README.md
├── learning/          # Tutorial dan latihan
│   ├── 01_database_setup.py
│   ├── 02_models_sqlalchemy.py
│   ├── 03_crud_operations.py
│   ├── 04_attendance_records.py
│   └── latihan.py
└── project/           # Module untuk progressive build
    ├── database.py
    ├── models.py
    ├── attendance_service.py
    ├── test_database.py
    └── README.md
```

## Learning Goals

### Tutorial Materials (learning/)
1. **01_database_setup.py** - MySQL & SQLAlchemy setup
2. **02_models_sqlalchemy.py** - Define database models
3. **03_crud_operations.py** - Create, Read, Update, Delete
4. **04_attendance_records.py** - Attendance management
5. **latihan.py** - Complete attendance system

### Konsep Utama
- MySQL connection & configuration
- SQLAlchemy ORM
- Database models (Person, Attendance)
- Relationships (One-to-Many)
- Migrations dengan Alembic
- Query optimization
- Transactions & connection pooling

## Project Development

### Modules:

#### `models.py`
Database models:
- `Person` - User information
- `Attendance` - Attendance records
- `FaceEncoding` - Store face encodings

#### `database.py`
Database utilities:
- MySQL connection string
- Database connection
- Session management
- Migration helpers
- Connection pooling

#### `attendance_service.py`
Attendance business logic:
- `AttendanceService` class
- `record_attendance()` - Record check-in/check-out
- `get_attendance_today()` - Today's records
- `get_person_attendance()` - Person's attendance history
- `generate_report()` - Attendance reports
- `check_duplicate()` - Prevent duplicate entries

### Integration
Uses Week 5 `recognition_service.py` for identification.  
Module ini akan digunakan oleh:
- Week 7-8: Desktop GUI untuk display dan user interaction

## Cara Penggunaan

### Learning (Tutorial)
```bash
cd minggu-6-database-attendance/learning
python 01_database_setup.py
python 02_models_sqlalchemy.py
python 03_crud_operations.py
python 04_attendance_records.py
python latihan.py
```

### Project Development
```bash
cd minggu-6-database-attendance/project
python test_database.py

# Integrate to main project
# Copy to ../../models/ and ../../services/
```

## Database Schema

```sql
Person
- id (PK)
- name
- employee_id
- department
- created_at

Attendance
- id (PK)
- person_id (FK)
- timestamp
- type (check_in/check_out)
- photo_path
- confidence

FaceEncoding
- id (PK)
- person_id (FK)
- encoding_data
- created_at
```

## Deliverables

### Learning
- Database setup dan configuration
- CRUD operations
- Attendance management

### Project
- `models.py` - Database models
- `database.py` - DB utilities
- `attendance_service.py` - Business logic
- `test_database.py` - Database tests
- Migration scripts

## Next Week Preview

**Minggu 7: Desktop GUI Development**
- Tkinter GUI development
- Multi-window application
- Webcam integration
- User interface design

---

**Time Estimate:** 6-7 hours  
**Difficulty:** Advanced
