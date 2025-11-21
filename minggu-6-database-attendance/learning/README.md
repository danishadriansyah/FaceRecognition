# Minggu 6 - Learning: Database & Attendance System

## 📚 Overview
Folder ini berisi 3 tutorial files untuk build complete attendance system dengan SQLite database, attendance logic, dan report generation.

## 📁 File Structure

```
learning/
├── README.md (file ini)
├── 01_database_setup.py
├── 02_database_design.py
└── 03_attendance_logic.py
```

---

## 🎯 Tutorial Files - Detailed Guide

### 01_database_setup.py
**Tujuan:** Setup SQLite database untuk attendance system

**Apa yang dipelajari:**
- SQLite basics dalam Python
- Database connection management
- Table creation dengan proper schema
- CRUD operations (Create, Read, Update, Delete)
- Data integrity dan constraints
- Database migrations

**Cara menggunakan:**
```bash
cd minggu-6-database-attendance/learning
python 01_database_setup.py
```

**Output yang diharapkan:**
- Creates `attendance.db` file
- Tables created successfully
- Sample data inserted
- Query results displayed

**Database schema:**

**1. employees table:**
```sql
CREATE TABLE employees (
    employee_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    date_joined DATE,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**2. attendance_records table:**
```sql
CREATE TABLE attendance_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id VARCHAR(10) NOT NULL,
    check_in_time TIMESTAMP,
    check_out_time TIMESTAMP,
    date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'present',
    confidence REAL,
    camera_location VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
```

**3. recognition_logs table:**
```sql
CREATE TABLE recognition_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id VARCHAR(10),
    recognition_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confidence REAL,
    camera_location VARCHAR(50),
    image_path VARCHAR(255),
    status VARCHAR(20),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
```

**Python implementation:**

```python
import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path='attendance.db'):
        self.db_path = db_path
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Dict-like access
        return self.connection
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def create_tables(self):
        """Create all necessary tables"""
        cursor = self.connection.cursor()
        
        # Employees table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                employee_id VARCHAR(10) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                department VARCHAR(50),
                email VARCHAR(100),
                phone VARCHAR(20),
                date_joined DATE,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Attendance records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance_records (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id VARCHAR(10) NOT NULL,
                check_in_time TIMESTAMP,
                check_out_time TIMESTAMP,
                date DATE NOT NULL,
                status VARCHAR(20) DEFAULT 'present',
                confidence REAL,
                camera_location VARCHAR(50),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
            )
        ''')
        
        # Recognition logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recognition_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id VARCHAR(10),
                recognition_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                confidence REAL,
                camera_location VARCHAR(50),
                image_path VARCHAR(255),
                status VARCHAR(20),
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
            )
        ''')
        
        self.connection.commit()
        print("✅ All tables created successfully")

# Usage
db = DatabaseManager('attendance.db')
db.connect()
db.create_tables()
db.close()
```

**CRUD operations:**

**Create (Insert):**
```python
def add_employee(employee_id, name, department, email):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO employees (employee_id, name, department, email, date_joined)
        VALUES (?, ?, ?, ?, ?)
    ''', (employee_id, name, department, email, datetime.now().date()))
    connection.commit()
    print(f"✅ Added employee: {name}")
```

**Read (Select):**
```python
def get_employee(employee_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM employees WHERE employee_id = ?', (employee_id,))
    row = cursor.fetchone()
    
    if row:
        return dict(row)  # Convert Row to dict
    return None
```

**Update:**
```python
def update_employee_department(employee_id, new_department):
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE employees 
        SET department = ? 
        WHERE employee_id = ?
    ''', (new_department, employee_id))
    connection.commit()
    print(f"✅ Updated department for {employee_id}")
```

**Delete:**
```python
def deactivate_employee(employee_id):
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE employees 
        SET is_active = 0 
        WHERE employee_id = ?
    ''', (employee_id,))
    connection.commit()
    print(f"✅ Deactivated employee: {employee_id}")
```

---

### 02_database_design.py
**Tujuan:** Advanced database design concepts untuk attendance system

**Apa yang dipelajari:**
- Database normalization
- Indexing untuk performance
- Complex queries dengan JOINs
- Aggregate functions dan GROUP BY
- Transactions dan data consistency
- Database views for reporting

**Cara menggunakan:**
```bash
python 02_database_design.py
```

**Output yang diharapkan:**
- Optimized schema created
- Indexes added
- Complex queries executed
- Performance comparison shown

**Indexing for performance:**

```python
def create_indexes(connection):
    """Create indexes for faster queries"""
    cursor = connection.cursor()
    
    # Index on attendance date (frequently queried)
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_attendance_date 
        ON attendance_records(date)
    ''')
    
    # Index on employee_id in attendance
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_attendance_employee 
        ON attendance_records(employee_id)
    ''')
    
    # Composite index for date range queries
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_employee_date 
        ON attendance_records(employee_id, date)
    ''')
    
    # Index on recognition time
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_recognition_time 
        ON recognition_logs(recognition_time)
    ''')
    
    connection.commit()
    print("✅ Indexes created for better performance")
```

**Complex queries:**

**1. Daily attendance report:**
```python
def get_daily_attendance_report(date):
    cursor = connection.cursor()
    
    query = '''
        SELECT 
            e.employee_id,
            e.name,
            e.department,
            a.check_in_time,
            a.check_out_time,
            a.status,
            CASE 
                WHEN a.check_in_time IS NULL THEN 'Absent'
                WHEN TIME(a.check_in_time) > '09:00:00' THEN 'Late'
                ELSE 'On Time'
            END as punctuality
        FROM employees e
        LEFT JOIN attendance_records a 
            ON e.employee_id = a.employee_id 
            AND a.date = ?
        WHERE e.is_active = 1
        ORDER BY e.department, e.name
    '''
    
    cursor.execute(query, (date,))
    return cursor.fetchall()
```

**2. Monthly summary per employee:**
```python
def get_monthly_summary(employee_id, year, month):
    cursor = connection.cursor()
    
    query = '''
        SELECT 
            COUNT(*) as total_days,
            SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present_days,
            SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent_days,
            SUM(CASE WHEN status = 'leave' THEN 1 ELSE 0 END) as leave_days,
            SUM(CASE WHEN TIME(check_in_time) > '09:00:00' THEN 1 ELSE 0 END) as late_count,
            AVG(
                CASE 
                    WHEN check_in_time IS NOT NULL AND check_out_time IS NOT NULL 
                    THEN (julianday(check_out_time) - julianday(check_in_time)) * 24 
                END
            ) as avg_hours_worked
        FROM attendance_records
        WHERE employee_id = ?
          AND strftime('%Y', date) = ?
          AND strftime('%m', date) = ?
    '''
    
    cursor.execute(query, (employee_id, str(year), f'{month:02d}'))
    return dict(cursor.fetchone())
```

**3. Department-wise attendance:**
```python
def get_department_attendance_stats(date):
    query = '''
        SELECT 
            e.department,
            COUNT(DISTINCT e.employee_id) as total_employees,
            COUNT(a.record_id) as present_employees,
            ROUND(
                (COUNT(a.record_id) * 100.0 / COUNT(DISTINCT e.employee_id)), 
                2
            ) as attendance_percentage
        FROM employees e
        LEFT JOIN attendance_records a 
            ON e.employee_id = a.employee_id 
            AND a.date = ?
        WHERE e.is_active = 1
        GROUP BY e.department
        ORDER BY attendance_percentage DESC
    '''
    
    cursor = connection.cursor()
    cursor.execute(query, (date,))
    return cursor.fetchall()
```

**Database views:**

```python
def create_views(connection):
    cursor = connection.cursor()
    
    # View: Today's attendance
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS v_today_attendance AS
        SELECT 
            e.employee_id,
            e.name,
            e.department,
            a.check_in_time,
            a.check_out_time,
            a.status
        FROM employees e
        LEFT JOIN attendance_records a 
            ON e.employee_id = a.employee_id 
            AND a.date = DATE('now')
        WHERE e.is_active = 1
    ''')
    
    # View: Late arrivals this month
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS v_late_arrivals_month AS
        SELECT 
            e.employee_id,
            e.name,
            COUNT(*) as late_count
        FROM employees e
        JOIN attendance_records a ON e.employee_id = a.employee_id
        WHERE TIME(a.check_in_time) > '09:00:00'
          AND strftime('%Y-%m', a.date) = strftime('%Y-%m', 'now')
        GROUP BY e.employee_id, e.name
        ORDER BY late_count DESC
    ''')
    
    connection.commit()
    print("✅ Database views created")
```

**Transactions:**

```python
def transfer_employee_department(employee_id, new_dept, effective_date):
    """Use transaction to ensure data consistency"""
    try:
        cursor = connection.cursor()
        
        # Start transaction (automatic in Python sqlite3)
        
        # Update employee department
        cursor.execute('''
            UPDATE employees 
            SET department = ? 
            WHERE employee_id = ?
        ''', (new_dept, employee_id))
        
        # Log the transfer
        cursor.execute('''
            INSERT INTO employee_history (employee_id, action, old_value, new_value, date)
            VALUES (?, 'department_transfer', 
                    (SELECT department FROM employees WHERE employee_id = ?),
                    ?, ?)
        ''', (employee_id, employee_id, new_dept, effective_date))
        
        # Commit transaction
        connection.commit()
        print(f"✅ Employee {employee_id} transferred to {new_dept}")
        
    except Exception as e:
        # Rollback on error
        connection.rollback()
        print(f"❌ Transfer failed: {e}")
        raise
```

---

### 03_attendance_logic.py
**Tujuan:** Implement business logic untuk attendance marking

**Apa yang dipelajari:**
- Check-in/check-out logic
- Duplicate prevention
- Grace period handling
- Late arrival detection
- Working hours calculation
- Shift management
- Overtime calculation

**Cara menggunakan:**
```bash
python 03_attendance_logic.py
```

**Output yang diharapkan:**
- Attendance marked correctly
- Duplicate check-ins prevented
- Late arrivals flagged
- Working hours calculated
- Reports generated

**Attendance logic implementation:**

```python
from datetime import datetime, time, timedelta

class AttendanceLogic:
    def __init__(self, db_manager):
        self.db = db_manager
        
        # Configuration
        self.work_start_time = time(9, 0)  # 9:00 AM
        self.work_end_time = time(17, 0)   # 5:00 PM
        self.late_grace_minutes = 15
        self.min_work_hours = 8
        self.duplicate_check_minutes = 5  # Prevent duplicate within 5 min
    
    def mark_check_in(self, employee_id, timestamp=None, confidence=0.0, 
                     camera_location='main'):
        """Mark employee check-in"""
        if timestamp is None:
            timestamp = datetime.now()
        
        date_only = timestamp.date()
        
        # Check if already checked in today
        if self._has_checked_in_today(employee_id, date_only):
            # Check if within duplicate prevention window
            last_check_in = self._get_last_check_in(employee_id, date_only)
            time_diff = (timestamp - last_check_in).total_seconds() / 60
            
            if time_diff < self.duplicate_check_minutes:
                return {
                    'success': False,
                    'message': f'Already checked in {time_diff:.0f} minutes ago',
                    'type': 'duplicate'
                }
        
        # Determine if late
        is_late = timestamp.time() > time(
            self.work_start_time.hour,
            self.work_start_time.minute + self.late_grace_minutes
        )
        
        status = 'late' if is_late else 'on_time'
        
        # Insert attendance record
        cursor = self.db.connection.cursor()
        cursor.execute('''
            INSERT INTO attendance_records 
            (employee_id, check_in_time, date, status, confidence, camera_location)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (employee_id, timestamp, date_only, status, confidence, camera_location))
        
        self.db.connection.commit()
        
        return {
            'success': True,
            'message': f'Check-in recorded: {status}',
            'status': status,
            'time': timestamp
        }
    
    def mark_check_out(self, employee_id, timestamp=None):
        """Mark employee check-out"""
        if timestamp is None:
            timestamp = datetime.now()
        
        date_only = timestamp.date()
        
        # Get today's check-in record
        cursor = self.db.connection.cursor()
        cursor.execute('''
            SELECT record_id, check_in_time 
            FROM attendance_records 
            WHERE employee_id = ? AND date = ?
            ORDER BY check_in_time DESC LIMIT 1
        ''', (employee_id, date_only))
        
        record = cursor.fetchone()
        
        if not record:
            return {
                'success': False,
                'message': 'No check-in record found for today'
            }
        
        record_id, check_in_time = record
        check_in_time = datetime.fromisoformat(check_in_time)
        
        # Calculate working hours
        working_hours = (timestamp - check_in_time).total_seconds() / 3600
        
        # Update record
        cursor.execute('''
            UPDATE attendance_records 
            SET check_out_time = ? 
            WHERE record_id = ?
        ''', (timestamp, record_id))
        
        self.db.connection.commit()
        
        return {
            'success': True,
            'message': 'Check-out recorded',
            'working_hours': working_hours,
            'check_in': check_in_time,
            'check_out': timestamp
        }
    
    def _has_checked_in_today(self, employee_id, date):
        """Check if employee has checked in today"""
        cursor = self.db.connection.cursor()
        cursor.execute('''
            SELECT COUNT(*) 
            FROM attendance_records 
            WHERE employee_id = ? AND date = ?
        ''', (employee_id, date))
        
        count = cursor.fetchone()[0]
        return count > 0
    
    def _get_last_check_in(self, employee_id, date):
        """Get last check-in time for employee on date"""
        cursor = self.db.connection.cursor()
        cursor.execute('''
            SELECT check_in_time 
            FROM attendance_records 
            WHERE employee_id = ? AND date = ?
            ORDER BY check_in_time DESC LIMIT 1
        ''', (employee_id, date))
        
        result = cursor.fetchone()
        if result:
            return datetime.fromisoformat(result[0])
        return None
    
    def calculate_overtime(self, employee_id, date):
        """Calculate overtime hours"""
        cursor = self.db.connection.cursor()
        cursor.execute('''
            SELECT check_in_time, check_out_time 
            FROM attendance_records 
            WHERE employee_id = ? AND date = ?
        ''', (employee_id, date))
        
        record = cursor.fetchone()
        if not record or not record[1]:  # No check-out
            return 0
        
        check_in = datetime.fromisoformat(record[0])
        check_out = datetime.fromisoformat(record[1])
        
        total_hours = (check_out - check_in).total_seconds() / 3600
        overtime = max(0, total_hours - self.min_work_hours)
        
        return overtime
    
    def get_attendance_summary(self, employee_id, start_date, end_date):
        """Get attendance summary for date range"""
        cursor = self.db.connection.cursor()
        cursor.execute('''
            SELECT 
                COUNT(*) as total_days,
                SUM(CASE WHEN status IN ('on_time', 'late') THEN 1 ELSE 0 END) as present_days,
                SUM(CASE WHEN status = 'late' THEN 1 ELSE 0 END) as late_days,
                AVG(
                    CASE WHEN check_out_time IS NOT NULL 
                    THEN (julianday(check_out_time) - julianday(check_in_time)) * 24 
                    END
                ) as avg_hours
            FROM attendance_records
            WHERE employee_id = ? 
              AND date BETWEEN ? AND ?
        ''', (employee_id, start_date, end_date))
        
        return dict(cursor.fetchone())
```

**Usage example:**
```python
# Initialize
db = DatabaseManager('attendance.db')
db.connect()
logic = AttendanceLogic(db)

# Check-in
result = logic.mark_check_in('001', confidence=0.95, camera_location='main_entrance')
if result['success']:
    print(f"✅ {result['message']}")
else:
    print(f"❌ {result['message']}")

# Check-out
result = logic.mark_check_out('001')
if result['success']:
    print(f"✅ Worked {result['working_hours']:.2f} hours")

# Calculate overtime
overtime = logic.calculate_overtime('001', datetime.now().date())
print(f"Overtime: {overtime:.2f} hours")
```

---

## 🎓 Best Practices

### Database Design
- **Normalization:** Avoid data redundancy
- **Indexes:** Add on frequently queried columns
- **Foreign Keys:** Maintain referential integrity
- **Constraints:** Use NOT NULL, UNIQUE where appropriate

### Performance
- **Connection Pooling:** Reuse connections
- **Batch Operations:** Insert multiple rows at once
- **Query Optimization:** Use EXPLAIN to analyze
- **Pagination:** Limit large result sets

### Data Integrity
- **Transactions:** Use for related operations
- **Validation:** Check data before insert
- **Backup:** Regular database backups
- **Logging:** Log all important operations

---

## ✅ Checklist Progress

```
[ ] 01_database_setup.py - Database created, tables working
[ ] 02_database_design.py - Indexes added, complex queries tested
[ ] 03_attendance_logic.py - Check-in/out working, duplicates prevented
[ ] Sample employees added
[ ] Sample attendance records created
[ ] Reports generated successfully
```

---

## 🐛 Common Issues & Solutions

**Database locked error:**
- Close all connections properly
- Use `connection.commit()` after writes
- Don't share connections between threads

**Foreign key violations:**
- Ensure referenced records exist
- Check employee_id exists before attendance
- Enable foreign keys: `PRAGMA foreign_keys = ON`

**Slow queries:**
- Add indexes on filtered columns
- Use EXPLAIN QUERY PLAN
- Limit result sets
- Optimize JOIN conditions

**Date/time issues:**
- Store as ISO format strings
- Use datetime.fromisoformat() to parse
- Handle timezone if needed
- Consistent date formatting

---

## 📖 Additional Resources

- SQLite documentation: https://sqlite.org/docs.html
- Python sqlite3: https://docs.python.org/3/library/sqlite3.html
- Database normalization: Study 1NF, 2NF, 3NF
- SQL optimization techniques

---

## ⏭️ Next Steps

Setelah minggu 6:

1. ✅ Database operational
2. ✅ Attendance logic working
3. ✅ Reports generated
4. ✅ Lanjut ke **Minggu 7: Desktop GUI with Tkinter**

---

**Data is the foundation! 💾**

*Good database design = Scalable system!*
