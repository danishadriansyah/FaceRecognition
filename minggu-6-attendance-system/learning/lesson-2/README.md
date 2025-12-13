# Lesson 2: Reports & Analytics

## Tujuan
- Generate attendance reports (daily, monthly, per person)
- Calculate attendance statistics & analytics
- Export reports to Excel/CSV
- Visualize attendance trends

## Prerequisites
- ✅ **Setup Script:** Sudah run `setup_week6.py` (buat folder output)
- ✅ **Lesson 1 Selesai:** Attendance CSV data ada di `../output/attendance.csv`
- ✅ Minimal 2-3 attendance records untuk generate reports

### Belum Ada Data Attendance?

**Option 1: Run Lesson 1 dulu**
```bash
# Masuk ke lesson 1
cd ..\lesson-1

# Run attendance system (record 2-3 faces)
python main.py
```

**Option 2: Verifikasi data ada**
```bash
# Cek CSV exists
Test-Path ..\output\attendance.csv
# Output: True (✅ data ada)

# Lihat isi CSV
type ..\output\attendance.csv | Select-Object -First 5

# Count records
python -c "import csv; rows=list(csv.DictReader(open('../output/attendance.csv'))); print(f'{len(rows)} records')"
```

## Report Types

### 1. Daily Report (from CSV)
```
====================================================================
DAILY ATTENDANCE REPORT - 2025-12-12
====================================================================

📊 Summary:
   Total Persons: 2
   Check-ins: 2
   Check-outs: 0
   Total Records: 2

📋 Attendance List:
------------------------------------------------------------
Name                 Check-in     Check-out    Confidence
------------------------------------------------------------
Alice                10:05:30     -            0.85
Bob                  10:07:15     -            0.92
------------------------------------------------------------
```

### 2. Monthly Summary (aggregated from CSV)
```
====================================================================
MONTHLY ATTENDANCE SUMMARY - December 2025
====================================================================

📊 Summary:
   Working Days: 12
   Total Records: 45

📋 Per Person:
------------------------------------------------------------
Name                 Check-ins    Check-outs   Days         Rate
------------------------------------------------------------
Alice                10           8            10           83.3%
Bob                  8            8            8            66.7%
------------------------------------------------------------
```

### 3. Person History (filtered from CSV)
```
====================================================================
ATTENDANCE HISTORY - Alice
====================================================================

📊 Period: 2025-12-01 to 2025-12-12
   Total Days: 10
   Total Records: 18

📋 Daily Records:
------------------------------------------------------------
Date         Check-in     Check-out    Confidence
------------------------------------------------------------
2025-12-01   08:05:00     17:02:00     0.87
2025-12-02   08:12:00     17:05:00     0.91
2025-12-03   -            -            0.00
------------------------------------------------------------
```

## Files
1. **`main.py`** - Report generation dari CSV

## Yang Dipelajari
1. CSV file parsing dengan Python
2. Data aggregation dan grouping
3. Calculate attendance statistics (rates, totals)
4. Export to JSON reports
5. Date range filtering dan person filtering

## Cara Menjalankan

### Run Reports Generator

```bash
# Masuk ke folder lesson 2
cd minggu-6-attendance-system\learning\lesson-2

# Run main.py
python main.py
```

**Program akan:**
1. **Script starts** - Load attendance CSV
   - Reads `../output/attendance.csv`
   - Shows total records loaded
   - Date range of records

2. **Generate Daily Report**:
   - Today's attendance summary
   - List all check-ins/check-outs for today
   - Person names, times, confidence scores

3. **Generate Monthly Summary**:
   - Current month statistics
   - Per-person attendance counts
   - Attendance rates calculated

4. **Generate Person History**:
   - Shows first person as example
   - Last 30 days attendance records
   - Check-in/out pairs

5. **Export to JSON**:
   - Creates `../output/reports/` folder
   - Exports daily report: `daily_YYYY-MM-DD.json`
   - Exports monthly report: `monthly_YYYY_MM.json`

### Output Files
```
minggu-6-attendance-system/learning/output/
├── attendance.csv              ← From Lesson 1
├── photos/                     ← From Lesson 1
└── reports/                    ← NEW from Lesson 2
    ├── daily_2025-12-12.json
    └── monthly_2025_12.json
```

## Troubleshooting

**Error: "No attendance file found"**
```bash
# Run Lesson 1 first
cd ../lesson-1
python main.py
# Record at least 2-3 attendances
```

**Empty reports**
- Ensure Lesson 1 generated attendance records
- Check CSV file: `type ..\output\attendance.csv`

**JSON export fails**
- Check disk space
- Ensure write permissions to `../output/reports/`

## JSON Report Format

**Daily Report** (`daily_2025-12-12.json`):
```json
{
  "date": "2025-12-12",
  "total_persons": 2,
  "total_records": 2,
  "check_ins": 2,
  "check_outs": 0,
  "persons": [
    {
      "name": "Alice",
      "check_in": "10:05:30",
      "check_out": "-",
      "confidence": 0.85
    }
  ]
}
```

**Monthly Report** (`monthly_2025_12.json`):
```json
{
  "year": 2025,
  "month": 12,
  "month_name": "December 2025",
  "working_days": 12,
  "total_records": 45,
  "persons": [
    {
      "name": "Alice",
      "check_ins": 10,
      "check_outs": 8,
      "attendance_days": 10,
      "attendance_rate": 83.3
    }
  ]
}
```

## Why This Matters
- **HR Analytics:** Track employee attendance patterns using CSV data
- **Data Analysis:** Use pandas for aggregation and statistics
- **JSON Reports:** Lightweight, portable format for APIs and dashboards
- **No Database Needed:** File-based reports that can be shared easily

## Next Steps
- **Week 7:** Build Desktop GUI untuk attendance visualization
- **Integration:** Connect JSON reports to dashboard or charts
- **Advanced:** Add filters by department, date range, or attendance rate
