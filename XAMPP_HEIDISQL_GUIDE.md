# 🗄️ XAMPP + HeidiSQL Quick Guide

## Setup Database (First Time Only)

### 1. Install XAMPP
- Download: https://www.apachefriends.org/
- Install dengan default settings
- Lokasi default: `C:\xampp`

### 2. Install HeidiSQL (Usually included with XAMPP)
- Atau download: https://www.heidisql.com/download.php
- Portable version juga bisa

### 3. Start MySQL
1. Buka **XAMPP Control Panel**
2. Click **Start** di baris MySQL
3. Status berubah jadi hijau "Running"

### 4. Create Database
**Option A: HeidiSQL (Recommended)**
1. Buka HeidiSQL
2. Session Manager → Click **New**
   - Network type: `MySQL (TCP/IP)`
   - Hostname: `localhost` atau `127.0.0.1`
   - User: `root`
   - Password: *(kosongkan)*
   - Port: `3306`
3. Click **Open**
4. Di sidebar, right-click → **Create new** → **Database**
5. Database name: `face_recognition_db`
6. Collation: `utf8mb4_general_ci`
7. Click **OK**

**Option B: Terminal (Alternative)**
```bash
# Windows Command Prompt
cd C:\xampp\mysql\bin
mysql -u root

# Di MySQL prompt:
CREATE DATABASE face_recognition_db CHARACTER SET utf8mb4;
exit;
```

## Daily Usage

### Start XAMPP MySQL
1. Buka XAMPP Control Panel
2. Click **Start** di MySQL
3. Pastikan status hijau

### Connect HeidiSQL
1. Buka HeidiSQL
2. Click session yang sudah dibuat
3. Click **Open**

### View Tables & Data
1. Di sidebar, expand `face_recognition_db`
2. Lihat daftar tables:
   - `persons` - Data orang
   - `face_images` - Path foto yang dicapture
   - `face_encodings` - Encoding untuk recognition
   - `attendances` - Log attendance (Week 6)
3. Double-click table untuk lihat isi data
4. Click **Refresh** (F5) setelah run Python script

### Run SQL Queries
1. Click tab **Query** di HeidiSQL
2. Ketik/paste SQL query
3. Click **Run** (F9) atau toolbar button ▶️

**Example Queries:**
```sql
-- Lihat semua persons
SELECT * FROM persons;

-- Count total face images
SELECT COUNT(*) FROM face_images;

-- Attendance hari ini
SELECT p.name, a.check_in, a.status
FROM attendances a
JOIN persons p ON a.person_id = p.id
WHERE DATE(a.check_in) = CURDATE();

-- Monthly attendance summary
SELECT 
  p.name,
  COUNT(*) as days_present,
  SUM(CASE WHEN a.status = 'Late' THEN 1 ELSE 0 END) as late_days
FROM attendances a
JOIN persons p ON a.person_id = p.id
WHERE YEAR(a.check_in) = 2024 AND MONTH(a.check_in) = 11
GROUP BY p.id;
```

### Export Data
1. Right-click table → **Export grid rows**
2. Format: CSV, Excel, HTML, XML, SQL
3. Choose location & filename
4. Click **OK**

## Connection String untuk Python

```python
# Default XAMPP (no password)
connection_string = "mysql+pymysql://root:@localhost:3306/face_recognition_db"

# Jika sudah set password
connection_string = "mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/face_recognition_db"
```

Edit di file:
- Week 4: `minggu-4-dataset-database/learning/lesson-2/database.py` (line 19)
- Week 5: Uses database.py dari Week 4
- Week 6: Uses database.py dari Week 4

## Troubleshooting

### ❌ "Can't connect to MySQL server"
- Pastikan XAMPP MySQL running (status hijau)
- Check port 3306 tidak dipakai aplikasi lain
- Restart XAMPP MySQL

### ❌ "Access denied for user 'root'"
- Password salah di connection string
- XAMPP default: user `root`, password kosong
- Edit connection string sesuaikan password

### ❌ "Unknown database 'face_recognition_db'"
- Database belum dibuat
- Create database dulu di HeidiSQL

### ❌ Port 3306 already in use
- Ada MySQL lain yang running (standalone installation)
- Stop MySQL lain atau change XAMPP port:
  1. Edit `C:\xampp\mysql\bin\my.ini`
  2. Ubah `port=3306` jadi `port=3307`
  3. Update connection string juga

## Tips

### 🎯 Best Practices
1. **Always start XAMPP MySQL** sebelum run Python scripts
2. **Refresh HeidiSQL** (F5) setelah run Python untuk lihat data baru
3. **Backup database** sebelum testing: Tools → Export database as SQL
4. **Use HeidiSQL Query tab** untuk quick data analysis

### 🚀 Shortcuts HeidiSQL
- `F5` - Refresh database
- `F9` - Run query
- `Ctrl+T` - New query tab
- `Ctrl+D` - Describe table structure
- `Ctrl+R` - Run query from cursor

### 📊 Monitor Database Size
```sql
SELECT 
  table_name,
  ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb
FROM information_schema.tables
WHERE table_schema = 'face_recognition_db';
```

## Week-by-Week Database Usage

### Week 4 - Dataset & Database
- **Create:** `persons`, `face_images`, `face_encodings` tables
- **Store:** Captured faces to database
- **View:** HeidiSQL → Check stored images paths

### Week 5 - Hybrid Recognition
- **Read:** Load persons & images from database
- **Write:** Generate & store face encodings (DeepFace)
- **View:** HeidiSQL → Check encoding_data (BLOB)

### Week 6 - Attendance System
- **Create:** `attendances` table
- **Write:** Log check-in/check-out from webcam
- **Query:** Generate reports (daily, monthly, per person)
- **Export:** Excel/CSV reports dari attendance data

### Week 7 - Desktop GUI
- **All operations:** GUI uses same database
- **CRUD:** Manage persons, view attendance via GUI
- **Reports:** Export reports from GUI buttons
