# Lesson 1: Attendance Logic & Real-time Tracking

## Tujuan
- Build AttendanceSystem class dengan business rules
- Real-time check-in/check-out dengan webcam
- Prevent duplicate check-ins
- Calculate attendance status (On Time, Late, Early Leave)

## Prerequisites
- ✅ **Dataset sudah di-setup:** Jalankan `setup_week6.py` di root folder week 6
- ✅ **Face encodings ready:** Setup script akan auto-copy dari Week 5 atau 4
- ✅ Minimal 2 persons dengan encodings

### Belum Setup?

**Jalankan setup script dulu (WAJIB!):**
```bash
# Dari folder minggu-6-attendance-system
cd ..\..
python setup_week6.py
```

**Pilih option:**
- `[1]` Copy dari Week 5 (recommended) - Langsung siap pakai!
- `[2]` Copy dari Week 4 - Jika Week 5 belum ada
- `[3]` Capture faces baru - Pakai camera helper
- `[4]` Skip - Setup manual nanti

**Verifikasi Setup Berhasil:**
```bash
# Cek dataset ada
Test-Path dataset\encodings.pkl
# Output: True (✅ berhasil)

# Cek berapa encodings
python -c "import pickle; d=pickle.load(open('dataset/encodings.pkl','rb')); print(f'{len(d[\"encodings\"])} encodings loaded')"
# Output: 40 encodings loaded (✅ siap!)
```

## Attendance Logging
```
CSV Format (logs/attendance.csv):
- timestamp (ISO format)
- date (YYYY-MM-DD)
- time (HH:MM:SS)
- person_name
- type (check_in / check_out)
- confidence (0.0-1.0)
- photo_path (relative to logs/)
- location (optional)
- notes
```

## Files
1. **`main.py`** - Real-time webcam attendance demo

## Yang Dipelajari
1. Load face encodings dari pickle file
2. Real-time face recognition dengan webcam
3. Business logic: check_in(), check_out()
4. Duplicate prevention (one check-in per day)
5. Save ke CSV + capture verification photos

## Output Example
```
====================================================================
LESSON 1: Attendance Logic & Real-time Tracking (File-Based)
====================================================================

📊 Step 1: Initialize Attendance System
------------------------------------------------------------
✅ AttendanceSystem initialized (File-based mode)
   Dataset: C:\...\dataset
   Log directory: C:\...\output
   Attendance file: attendance.csv

📊 Step 2: Loaded Data
------------------------------------------------------------
Known persons: 2
Known encodings: 40

📊 Step 3: Today's Statistics
------------------------------------------------------------
Total records today: 0
  No attendance records yet today

📊 Step 4: Real-time Attendance Check-in
------------------------------------------------------------

🎥 Opening webcam for automatic check-in...
📌 How it works:
   1. Face detected → Recognized
   2. Press SPACE to record attendance
   3. Duplicate prevention (one check-in per day)
   4. Photos saved automatically

💡 Press 'q' to quit

Press ENTER to start real-time check-in...

🔍 Detecting cameras...
  ✅ Camera 0: Built-in Webcam / Default Camera

Mode: CHECK_IN
SPACE: Record | Q: Quit

   ✅ Captured: Alice (0.85)
   ✅ Recorded: Alice (0.85)

   ⚠️  Alice already checked in today at 10:05:30

   ✅ Captured: Bob (0.92)
   ✅ Recorded: Bob (0.92)

📊 Step 5: Final Statistics
------------------------------------------------------------
Total records: 2
Check-ins: 2
Check-outs: 0
```

**CSV Output** (`../output/attendance.csv`):
```csv
timestamp,date,time,person_name,type,confidence,photo_path,location,notes
2025-12-12T10:05:30,2025-12-12,10:05:30,Alice,check_in,0.8500,photos/Alice_20251212_100530.jpg,,Auto check-in via face recognition
2025-12-12T10:07:15,2025-12-12,10:07:15,Bob,check_in,0.9200,photos/Bob_20251212_100715.jpg,,Auto check-in via face recognition
```
2. **Camera detection**:
   - Script auto-detect available cameras
   - Pilih camera (0 untuk built-in, 1 untuk USB)
   - Info: nama, resolusi, FPS

## Cara Menjalankan

### 1️⃣ Setup Dataset (Jika Belum)

**Jalankan setup script di root folder Week 6:**
```bash
# Dari folder lesson-1, naik ke root Week 6
cd ..\..

# Run setup script
python setup_week6.py
# Pilih [1] untuk copy dari Week 5 (termudah!)
```

### 2️⃣ Jalankan Attendance System

```bash
# Masuk ke folder lesson 1
cd learning\lesson-1

# Run main.py
python main.py
```

**Itu aja!** Setup script sudah handle semua copy dataset otomatis.

**Program flow:**
1. Initialize attendance system
2. Load encodings dari dataset
3. Show business rules (working hours, late threshold, etc)
4. Pilih camera (default 0)
5. Webcam terbuka
6. Face detection & recognition real-time
7. Press 'c' untuk check-in, 'o' untuk check-out, 'q' untuk quit

**Check hasil:**
```bash
# Lihat CSV
type output\attendance.csv

# Check photos
Get-ChildItem output\photos\
```

## Troubleshooting

**Error: "No encodings file found"**
```bash
# Run setup script
cd ../..
python setup_week6.py
# Pilih [1] Copy dari Week 5 (termudah!)
```

**Error: "No cameras detected"**
```bash
# Test camera manual
python -c "import cv2; cap=cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera FAIL')"

# Close aplikasi lain yang pakai camera (Zoom, Teams, dll)
```

**Warning: "Unknown person detected"**
- Person belum diregister di dataset
- Run setup_week6.py lagi, pilih [3] untuk capture faces baru

**Already checked in**
- Normal behavior - cegah duplicate
- Untuk check-out, ganti mode ke 'check_out'

## File Output Structure
```
minggu-6-attendance-system/learning/
├── lesson-1/
│   ├── main.py
│   └── README.md (you are here)
└── output/                    ← Created automatically
    ├── attendance.csv         ← All attendance records
    └── photos/                ← Verification photos
        ├── Alice_20251212_100530.jpg
        └── Bob_20251212_100715.jpg
```

## Why This Matters
- **Automated:** No manual attendance input
- **Accurate:** 97%+ recognition from Week 5  
- **Portable:** CSV files, easy to process
- **Audit trail:** Photos + confidence scores stored
- **Simple:** No database setup needed!

## Next: Lesson 2
Generate **reports & analytics** dari CSV attendance data!
   - ✅ Only one check-in per person per day
   - ✅ Photo automatically saved to `../output/photos/`
   - ⚠️ Unknown person = skip
   - ⚠️ Already checked in = warning message

5. **Check results**:
   ```bash
   # View CSV log
   type ..\output\attendance.csv
   
   # Or open in Excel/Notepad
   start ..\output\attendance.csv
   
   # Check photos
   explorer ..\output\photos\
   ```

## Output
```
📊 Starting Attendance System
✅ Database connected
✅ Recognition service loaded (2 persons)

🎥 Real-time Check-in (Press 'q' to quit)

Frame 0010:
   ✅ Alice recognized (89% confidence)
   ✅ Check-in recorded: 08:05 (On Time)

Frame 0025:
   ⚠️  Alice already checked in today

Frame 0040:
   ✅ Bob recognized (92% confidence)
   ⚠️  Late check-in: 08:25 (Late - 10 mins)
```

## Why This Matters
- **Automated:** No manual attendance input
- **Accurate:** 97%+ recognition from Week 5
- **Business rules:** Enforces company policy
- **Audit trail:** Confidence scores stored

## Next: Lesson 2
Generate **reports & analytics** dari attendance data!
