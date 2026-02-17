"""
Attendance System (File-Based)
Week 6 Project Module - Progressive Web Application

Complete attendance system with file-based storage (CSV/JSON)
"""

import cv2
import numpy as np
import json
import csv
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
from pathlib import Path
import sys
import os

# Import recognition service from same package
try:
    from .recognition_service import RecognitionService
except ImportError:
    # Fallback for direct execution
    from recognition_service import RecognitionService


class AttendanceSystem:
    """
    File-based attendance system with CSV logging
    """
    
    def __init__(self, dataset_path: str = "dataset", log_dir: str = "logs"):
        """
        Initialize attendance system
        
        Args:
            dataset_path: Path to dataset folder
            log_dir: Directory for attendance logs
        """
        self.dataset_path = Path(dataset_path)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Attendance CSV file
        self.attendance_file = self.log_dir / "attendance.csv"
        self._init_attendance_file()
        
        # Photo storage
        self.photo_dir = self.log_dir / "photos"
        self.photo_dir.mkdir(exist_ok=True)
        
        # Initialize recognition service
        self.recognition = RecognitionService(dataset_path=str(dataset_path))
        
        # Today's attendance cache
        self.today_cache = {}
        self._load_today_attendance()
        
        print(f"✅ AttendanceSystem initialized (File-based mode)")
        print(f"   Dataset: {self.dataset_path}")
        print(f"   Log directory: {self.log_dir}")
        print(f"   Attendance file: {self.attendance_file.name}")
    
    def _init_attendance_file(self):
        """Initialize CSV file with headers"""
        if not self.attendance_file.exists():
            with open(self.attendance_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'date', 'time', 'person_name', 
                    'type', 'confidence', 'photo_path', 'location', 'notes'
                ])
            print(f"✅ Created attendance file: {self.attendance_file}")
    
    def _load_today_attendance(self):
        """Load today's attendance into cache"""
        self.today_cache = {}
        today_str = date.today().isoformat()
        
        if not self.attendance_file.exists():
            return
        
        with open(self.attendance_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['date'] == today_str:
                    name = row['person_name']
                    if name not in self.today_cache:
                        self.today_cache[name] = []
                    self.today_cache[name].append(row)
    
    def record_attendance(self, name: str, attendance_type: str, 
                         confidence: float, photo: np.ndarray = None,
                         location: str = None, notes: str = None) -> Dict:
        """
        Record attendance entry
        
        Args:
            name: Person name
            attendance_type: 'check_in' or 'check_out'
            confidence: Recognition confidence
            photo: Photo of person (optional)
            location: Location (optional)
            notes: Additional notes (optional)
            
        Returns:
            Attendance record dict
        """
        now = datetime.now()
        timestamp = now.isoformat()
        date_str = now.date().isoformat()
        time_str = now.time().strftime("%H:%M:%S")
        
        # Save photo if provided
        photo_path = None
        if photo is not None:
            photo_filename = f"{name}_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
            photo_path = self.photo_dir / photo_filename
            cv2.imwrite(str(photo_path), photo)
            photo_path = str(photo_path.relative_to(self.log_dir))
        
        # Create record
        record = {
            'timestamp': timestamp,
            'date': date_str,
            'time': time_str,
            'person_name': name,
            'type': attendance_type,
            'confidence': f"{confidence:.4f}",
            'photo_path': photo_path or '',
            'location': location or '',
            'notes': notes or ''
        }
        
        # Append to CSV
        with open(self.attendance_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=record.keys())
            writer.writerow(record)
        
        # Update cache
        if name not in self.today_cache:
            self.today_cache[name] = []
        self.today_cache[name].append(record)
        
        return record
    
    def check_in(self, name: str, confidence: float, photo: np.ndarray = None) -> Dict:
        """
        Record check-in
        
        Args:
            name: Person name
            confidence: Recognition confidence
            photo: Photo of person
            
        Returns:
            Attendance record, or dict with 'already_checked_in' info
        """
        # Check if already checked in today
        if name in self.today_cache:
            for record in self.today_cache[name]:
                if record['type'] == 'check_in':
                    existing_time = record['time']
                    print(f"⚠️  {name} already checked in today at {existing_time}")
                    return {'already_checked_in': True, 'time': existing_time, 'name': name}
        
        record = self.record_attendance(
            name=name,
            attendance_type='check_in',
            confidence=confidence,
            photo=photo,
            notes=f'Check-in pada pukul {datetime.now().strftime("%H:%M:%S")}'
        )
        
        print(f"✅ Check-in recorded: {name} at {record['time']}")
        return record
    
    def check_out(self, name: str, confidence: float, photo: np.ndarray = None) -> Dict:
        """
        Record check-out
        
        Args:
            name: Person name
            confidence: Recognition confidence
            photo: Photo of person
            
        Returns:
            Attendance record or None if not checked in
        """
        # Check if checked in today
        if name not in self.today_cache:
            print(f"⚠️  {name} has not checked in today")
            return None
        
        # Check if already checked in
        has_checkin = any(r['type'] == 'check_in' for r in self.today_cache[name])
        if not has_checkin:
            print(f"⚠️  {name} has not checked in today")
            return None
        
        # Check if already checked out
        has_checkout = any(r['type'] == 'check_out' for r in self.today_cache[name])
        if has_checkout:
            print(f"⚠️  {name} already checked out today")
            return None
        
        record = self.record_attendance(
            name=name,
            attendance_type='check_out',
            confidence=confidence,
            photo=photo,
            notes='Auto check-out via face recognition'
        )
        
        print(f"✅ Check-out recorded: {name} at {record['time']}")
        return record
    
    def delete_record(self, timestamp: str, person_name: str) -> bool:
        """
        Delete a specific attendance record by timestamp and person name.
        Rewrites the CSV without the deleted record and refreshes cache.
        
        Args:
            timestamp: ISO timestamp of the record to delete
            person_name: Name of the person
            
        Returns:
            True if deleted successfully
        """
        if not self.attendance_file.exists():
            return False
        
        # Read all records
        all_records = []
        deleted = False
        
        with open(self.attendance_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row['timestamp'] == timestamp and row['person_name'] == person_name:
                    deleted = True
                    continue  # Skip this record (delete it)
                all_records.append(row)
        
        if not deleted:
            return False
        
        # Rewrite CSV without deleted record
        with open(self.attendance_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_records)
        
        # Refresh today's cache
        self._load_today_attendance()
        
        print(f"🗑️ Deleted record: {person_name} at {timestamp}")
        return True
    
    def process_camera_attendance(self, camera_id: int = 0, mode: str = 'check_in'):
        """
        Process attendance from camera
        
        Args:
            camera_id: Camera device ID
            mode: 'check_in' or 'check_out'
        """
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open camera {camera_id}")
        
        print(f"\n📹 Attendance System - {mode.upper()} Mode")
        print(f"   Press SPACE to capture attendance")
        print(f"   Press 'q' to quit\n")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detect faces in real-time
            results = self.recognition.recognize_faces(frame)
            
            # Draw results
            display_frame = self.recognition.draw_results(frame, results)
            
            # Show instructions
            cv2.putText(display_frame, f"Mode: {mode.upper()}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(display_frame, "SPACE: Record | Q: Quit", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Attendance System', display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' '):  # Space to record
                if len(results) == 1:
                    result = results[0]
                    name = result['name']
                    confidence = result['confidence']
                    
                    if name != 'Unknown':
                        # Extract face photo
                        x, y, w, h = result['bbox']
                        face_photo = frame[y:y+h, x:x+w]
                        
                        # Record attendance
                        if mode == 'check_in':
                            record = self.check_in(name, confidence, face_photo)
                        else:
                            record = self.check_out(name, confidence, face_photo)
                        
                        if record:
                            print(f"   ✅ Recorded: {name} ({confidence:.2f})")
                    else:
                        print(f"   ⚠️  Unknown person detected")
                
                elif len(results) == 0:
                    print(f"   ⚠️  No face detected")
                else:
                    print(f"   ⚠️  Multiple faces detected ({len(results)})")
            
            elif key == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def get_records(self, date_filter: str = None) -> List[Dict]:
        """
        Get attendance records with optional date filter
        
        Args:
            date_filter: Date string in YYYY-MM-DD format, or None for all records
            
        Returns:
            List of attendance records
        """
        records = []
        
        if not self.attendance_file.exists():
            return records
        
        try:
            with open(self.attendance_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if date_filter is None or row.get('date') == date_filter:
                        records.append(row)
        except Exception as e:
            print(f"Error reading records: {e}")
        
        return records
    
    def get_today_attendance(self) -> List[Dict]:
        """Get today's attendance records"""
        records = []
        for person_records in self.today_cache.values():
            records.extend(person_records)
        
        # Sort by timestamp
        records.sort(key=lambda x: x['timestamp'])
        return records
    
    def get_attendance_by_date(self, target_date: date) -> List[Dict]:
        """
        Get attendance records for specific date
        
        Args:
            target_date: Date to query
            
        Returns:
            List of attendance records
        """
        date_str = target_date.isoformat()
        records = []
        
        with open(self.attendance_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['date'] == date_str:
                    records.append(row)
        
        return records
    
    def get_person_attendance_summary(self, person_name: str, 
                                     start_date: date = None, 
                                     end_date: date = None) -> Dict:
        """
        Get attendance summary for a person
        
        Args:
            person_name: Person name
            start_date: Start date (default: 30 days ago)
            end_date: End date (default: today)
            
        Returns:
            Summary dict with statistics
        """
        if start_date is None:
            start_date = date.today() - timedelta(days=30)
        if end_date is None:
            end_date = date.today()
        
        records = []
        
        with open(self.attendance_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row_date = date.fromisoformat(row['date'])
                if (row['person_name'] == person_name and 
                    start_date <= row_date <= end_date):
                    records.append(row)
        
        # Count check-ins and check-outs
        check_ins = [r for r in records if r['type'] == 'check_in']
        check_outs = [r for r in records if r['type'] == 'check_out']
        
        return {
            'person_name': person_name,
            'period': f"{start_date} to {end_date}",
            'total_check_ins': len(check_ins),
            'total_check_outs': len(check_outs),
            'total_records': len(records),
            'records': records
        }
    
    def export_report(self, start_date: date, end_date: date, 
                     output_file: str = None) -> str:
        """
        Export attendance report to JSON
        
        Args:
            start_date: Start date
            end_date: End date
            output_file: Output file path (optional)
            
        Returns:
            Path to exported file
        """
        if output_file is None:
            output_file = self.log_dir / f"report_{start_date}_{end_date}.json"
        else:
            output_file = Path(output_file)
        
        records = []
        
        with open(self.attendance_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row_date = date.fromisoformat(row['date'])
                if start_date <= row_date <= end_date:
                    records.append(row)
        
        # Group by person
        persons = {}
        for record in records:
            name = record['person_name']
            if name not in persons:
                persons[name] = {'check_ins': 0, 'check_outs': 0, 'records': []}
            
            if record['type'] == 'check_in':
                persons[name]['check_ins'] += 1
            else:
                persons[name]['check_outs'] += 1
            
            persons[name]['records'].append(record)
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'summary': {
                'total_persons': len(persons),
                'total_records': len(records),
                'total_check_ins': sum(p['check_ins'] for p in persons.values()),
                'total_check_outs': sum(p['check_outs'] for p in persons.values())
            },
            'persons': persons
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Report exported to: {output_file}")
        return str(output_file)


# Example usage
if __name__ == "__main__":
    print("Attendance System Module - Week 6 Project (File-Based)")
    print("="*60)
    
    # Initialize
    system = AttendanceSystem(dataset_path="dataset", log_dir="logs")
    
    print("\n💡 Available methods:")
    print("   system.process_camera_attendance(camera_id=0, mode='check_in')")
    print("   system.process_camera_attendance(camera_id=0, mode='check_out')")
    print("   records = system.get_today_attendance()")
    print("   summary = system.get_person_attendance_summary('Alice')")
    print("   system.export_report(start_date, end_date)")
