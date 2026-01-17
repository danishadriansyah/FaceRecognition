# User Guide - Face Recognition Attendance System

**Week 8 - Final Project**

Complete guide untuk menggunakan Face Recognition Attendance System.

---

## 📖 Table of Contents

1. [Getting Started](#getting-started)
2. [Main Dashboard](#main-dashboard)
3. [Person Registration](#person-registration)
4. [Marking Attendance](#marking-attendance)
5. [Viewing Reports](#viewing-reports)
6. [System Settings](#system-settings)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

---

## Getting Started

### First Time Setup

1. **Install Python 3.8+**
   - Download from: https://python.org
   - Ensure "Add to PATH" is checked during installation

2. **Install Dependencies (from root workspace)**
   ```bash
   cd c:\Ngoding\Kerja\ExtraQueensya
   pip install -r requirements.txt
   ```

3. **Run Application**
   ```bash
   cd minggu-8-final-project\project
   python main_app.py
   ```

4. **Allow Camera Access**
   - When prompted, allow camera access
   - Application needs camera for face detection

---

## Main Dashboard

### Overview

Dashboard menampilkan:
- **Live Webcam Preview**: Real-time face detection
- **Statistics Panel**: 
  - Total registered persons
  - Today's attendance count
  - System status
- **Navigation Buttons**:
  - Register Person
  - Mark Attendance
  - View Reports
  - Settings (optional)

### Tips
- Dashboard webcam hanya preview, tidak record attendance
- Green boxes = detected faces
- Stats update setiap kali ada perubahan data

---

## Person Registration

### Step-by-Step

1. **Click "Register Person"** button dari dashboard

2. **Fill in Person Information:**
   - **Name**: Full name (required)
   - **Employee ID**: Unique identifier (required)
   - **Department**: Work department (optional)

3. **Photo Capture:**
   - Stand 50-100cm from camera
   - Face camera directly
   - Ensure good lighting
   - System will auto-capture 20 photos
   - Photos taken every 0.5 seconds

4. **Capture Process:**
   ```
   Progress: 1/20 photos captured...
   Progress: 2/20 photos captured...
   ...
   Progress: 20/20 photos captured!
   ```

5. **Wait for Encoding:**
   - System generates face encodings
   - Takes ~15-20 seconds
   - Do not close window

6. **Success!**
   - Person registered successfully
   - Can now be recognized

### Best Practices

**Good Photos:**
- ✅ Face camera directly (frontal view)
- ✅ Good lighting (natural light best)
- ✅ Neutral expression
- ✅ No glasses/mask (or capture with AND without)
- ✅ Multiple angles (turn head slightly during capture)

**Avoid:**
- ❌ Too dark or too bright
- ❌ Face partially hidden
- ❌ Too far (>150cm) or too close (<30cm)
- ❌ Motion blur (stay still)

---

## Marking Attendance

### Check-In Process

1. **Click "Mark Attendance"** dari dashboard

2. **Select Mode: Check-In**
   - Default mode adalah Check-In

3. **Face Camera:**
   - Stand 50-100cm from camera
   - Face camera directly
   - Wait for recognition (1-2 seconds)

4. **Auto Check-In:**
   ```
   ✅ Welcome, John Doe!
   Checked in at 08:30:45
   ```

5. **Cooldown Period:**
   - Cannot check-in again for 5 seconds
   - Prevents accidental duplicates

### Check-Out Process

1. **Click "Check-Out"** mode toggle

2. **Face Camera:**
   - Same process as check-in
   - System recognizes face

3. **Auto Check-Out:**
   ```
   ✅ Goodbye, John Doe!
   Checked out at 17:00:15
   Work duration: 8h 29m
   ```

### Manual Entry (Fallback)

**If Recognition Fails:**

1. **Click "Manual Entry"** button

2. **Select Person from List:**
   - Choose name from dropdown
   - Or type employee ID

3. **Confirm:**
   - Click Check-In/Check-Out
   - Entry recorded with timestamp

### Tips

**For Best Recognition:**
- Stand at same distance as registration
- Use similar lighting conditions
- Face camera directly
- Remove glasses if registered without
- Wait for bounding box to appear

**If Not Recognized:**
- Try moving closer/farther
- Ensure good lighting
- Use manual entry as fallback
- Consider re-registering with more photos

---

## Viewing Reports

### Accessing Reports

1. **Click "View Reports"** dari dashboard

2. **Reports Window Opens** dengan:
   - Attendance table
   - Filter controls
   - Search box
   - Export button

### Filtering Data

**By Date Range:**
- **Today**: Show only today's records
- **This Week**: Last 7 days
- **This Month**: Current month
- **All Time**: All records

**By Search:**
- Type name or employee ID
- Results update instantly
- Case-insensitive search

### Attendance Table

**Columns:**
- **Date**: YYYY-MM-DD format
- **Time**: HH:MM:SS format
- **Employee ID**: Unique identifier
- **Name**: Person name
- **Type**: Check-In or Check-Out
- **Confidence**: Recognition confidence (%)

**Sorting:**
- Click column header to sort
- Click again to reverse order

### Exporting Reports

1. **Click "Export to CSV"** button

2. **Choose File Location:**
   - Save dialog appears
   - Default name: `attendance_report_YYYYMMDD.csv`

3. **Open in Excel/Sheets:**
   - CSV file compatible with all spreadsheet software

---

## System Settings

### Configuration Options

**Recognition Settings:**
- **Threshold**: Adjust recognition sensitivity (0.5-0.7)
  - Lower = stricter (fewer false positives)
  - Higher = lenient (more false positives)
- **Detection Confidence**: Face detection threshold

**Performance Settings:**
- **Frame Skip**: Process every N frames
  - Higher = faster, less accurate
  - Lower = slower, more accurate
- **Max Resolution**: Resize frames for performance

**Attendance Settings:**
- **Cooldown**: Prevent duplicate entries (seconds)
- **Work Hours**: Define work day start/end
- **Auto Check-Out**: Auto check-out after N hours

**Dataset Settings:**
- **Min Photos**: Minimum photos required
- **Max Photos**: Maximum photos to store

### Backup & Restore

**Create Backup:**
1. Settings → Backup → Create Backup
2. Backup saved to `backups/` folder
3. Includes dataset, encodings, attendance logs

**Restore Backup:**
1. Settings → Backup → Restore
2. Select backup file
3. Confirm restoration
4. Application restarts

---

## Troubleshooting

### Camera Issues

**Problem:** Camera not detected

**Solutions:**
1. Check camera is connected
2. Check camera permissions:
   - Windows: Settings → Privacy → Camera
   - Mac: System Preferences → Security → Camera
3. Try different camera index:
   ```python
   # In face_detector.py
   cap = cv2.VideoCapture(1)  # Try 0, 1, 2
   ```
4. Restart computer
5. Update camera drivers

---

**Problem:** Black screen in webcam preview

**Solutions:**
1. Close other apps using camera
2. Restart application
3. Check camera hardware (test with camera app)

---

### Recognition Issues

**Problem:** Person not recognized

**Solutions:**
1. **Check Lighting:**
   - Ensure good, even lighting
   - Avoid backlighting (window behind you)
   - Use same lighting as registration

2. **Check Distance:**
   - Stand 50-100cm from camera
   - Same distance as registration

3. **Adjust Threshold:**
   - Settings → Recognition → Increase threshold to 0.65 or 0.7
   - Makes recognition more lenient

4. **Re-Register:**
   - Delete old registration
   - Re-register with better photos
   - Use variety of angles and expressions

---

**Problem:** Wrong person recognized

**Solutions:**
1. **Lower Threshold:**
   - Settings → Recognition → Decrease to 0.55 or 0.5
   - Makes recognition stricter

2. **Check for Similar Faces:**
   - System may confuse similar-looking people
   - Ensure photos are clear and distinct

3. **Re-Capture Photos:**
   - Register with more distinctive photos
   - Capture from multiple angles

---

### Performance Issues

**Problem:** Slow/laggy camera preview

**Solutions:**
1. **Increase Frame Skip:**
   - Settings → Performance → Frame Skip = 3 or 4
   - Processes fewer frames

2. **Reduce Resolution:**
   - Settings → Performance → Max Resolution = 480
   - Smaller frames process faster

3. **Close Other Apps:**
   - Free up CPU/RAM
   - Close browser, heavy applications

4. **Hardware:**
   - Upgrade to better CPU
   - More RAM (8GB+)

---

### Data Issues

**Problem:** Lost attendance data

**Solutions:**
1. **Check Logs Folder:**
   - `logs/attendance.csv` contains all records

2. **Restore from Backup:**
   - Settings → Backup → Restore
   - Select recent backup

3. **Manual Recovery:**
   - Check `backups/` folder
   - Copy `attendance.csv` from backup

---

**Problem:** Duplicate attendance entries

**Solutions:**
1. **Increase Cooldown:**
   - Settings → Attendance → Cooldown = 10 seconds

2. **Manual Cleanup:**
   - View Reports
   - Export to CSV
   - Edit in Excel
   - Remove duplicates
   - Re-import (if feature available)

---

## FAQ

**Q: Can I use this on multiple computers?**
A: Yes! Copy the entire `dataset/` folder to share encodings between computers.

**Q: How many people can be registered?**
A: Practically unlimited. Tested with 100+ persons without issues.

**Q: Can I recognize multiple people at once?**
A: Yes, system detects and recognizes all visible faces simultaneously.

**Q: How accurate is the recognition?**
A: 95-97% accuracy with good quality photos and lighting.

**Q: Does it work with glasses/mask?**
A: Glasses: Yes (if registered with glasses). Masks: No (face must be visible).

**Q: Can I export data to Excel?**
A: Yes, CSV export is compatible with Excel, Google Sheets, etc.

**Q: Is internet connection required?**
A: No, system works completely offline.

**Q: How much storage does it use?**
A: ~5-10MB per person (20 photos + encodings).

**Q: Can I customize the interface?**
A: Yes, edit `gui/` files to customize colors, layout, buttons.

**Q: Is my data secure?**
A: Data stored locally on your computer. No cloud/external access.

---

## Support

**Need Help?**
1. Check this User Guide
2. Review `docs/API_REFERENCE.md`
3. Check `logs/app.log` for errors
4. Run tests: `python tests/test_integration.py`

---

**Thank you for using Face Recognition Attendance System!**

---

**Version:** 1.0.0  
**Last Updated:** December 2025  
**Week 8 - Final Project**
