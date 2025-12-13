"""
Lesson 2: Reports & Analytics (File-Based)
Generate attendance reports from CSV logs
"""
import os
import sys
import csv
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from collections import defaultdict

def load_attendance_csv(csv_file):
    """Load attendance records from CSV"""
    records = []
    
    if not Path(csv_file).exists():
        return records
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    
    return records

def generate_daily_report(records, target_date):
    """Generate daily attendance report"""
    date_str = target_date.isoformat()
    
    # Filter by date
    daily_records = [r for r in records if r['date'] == date_str]
    
    # Group by person
    persons = defaultdict(list)
    for record in daily_records:
        persons[record['person_name']].append(record)
    
    report = {
        'date': date_str,
        'total_persons': len(persons),
        'total_records': len(daily_records),
        'check_ins': len([r for r in daily_records if r['type'] == 'check_in']),
        'check_outs': len([r for r in daily_records if r['type'] == 'check_out']),
        'persons': []
    }
    
    for person_name, person_records in persons.items():
        check_in = next((r for r in person_records if r['type'] == 'check_in'), None)
        check_out = next((r for r in person_records if r['type'] == 'check_out'), None)
        
        report['persons'].append({
            'name': person_name,
            'check_in': check_in['time'] if check_in else '-',
            'check_out': check_out['time'] if check_out else '-',
            'confidence': float(check_in['confidence']) if check_in else 0.0
        })
    
    return report

def generate_monthly_summary(records, year, month):
    """Generate monthly attendance summary"""
    # Filter by month
    monthly_records = [
        r for r in records 
        if r['date'].startswith(f"{year:04d}-{month:02d}")
    ]
    
    # Count working days
    working_days = len(set(r['date'] for r in monthly_records))
    
    # Group by person
    persons = defaultdict(lambda: {'check_ins': 0, 'check_outs': 0, 'dates': set()})
    
    for record in monthly_records:
        name = record['person_name']
        persons[name]['dates'].add(record['date'])
        
        if record['type'] == 'check_in':
            persons[name]['check_ins'] += 1
        else:
            persons[name]['check_outs'] += 1
    
    report = {
        'year': year,
        'month': month,
        'month_name': datetime(year, month, 1).strftime('%B %Y'),
        'working_days': working_days,
        'total_records': len(monthly_records),
        'persons': []
    }
    
    for name, stats in persons.items():
        attendance_days = len(stats['dates'])
        attendance_rate = (attendance_days / working_days * 100) if working_days > 0 else 0
        
        report['persons'].append({
            'name': name,
            'check_ins': stats['check_ins'],
            'check_outs': stats['check_outs'],
            'attendance_days': attendance_days,
            'attendance_rate': attendance_rate
        })
    
    return report

def generate_person_history(records, person_name, start_date, end_date):
    """Generate attendance history for specific person"""
    # Filter by person and date range
    person_records = [
        r for r in records
        if r['person_name'] == person_name and
        start_date.isoformat() <= r['date'] <= end_date.isoformat()
    ]
    
    # Group by date
    by_date = defaultdict(list)
    for record in person_records:
        by_date[record['date']].append(record)
    
    report = {
        'person_name': person_name,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'total_days': len(by_date),
        'total_records': len(person_records),
        'days': []
    }
    
    for date_str in sorted(by_date.keys()):
        day_records = by_date[date_str]
        check_in = next((r for r in day_records if r['type'] == 'check_in'), None)
        check_out = next((r for r in day_records if r['type'] == 'check_out'), None)
        
        report['days'].append({
            'date': date_str,
            'check_in': check_in['time'] if check_in else '-',
            'check_out': check_out['time'] if check_out else '-',
            'confidence': float(check_in['confidence']) if check_in else 0.0
        })
    
    return report

def print_daily_report(report):
    """Print daily report"""
    print("\n" + "="*80)
    print(f"DAILY ATTENDANCE REPORT - {report['date']}")
    print("="*80)
    
    print(f"\n📊 Summary:")
    print(f"   Total Persons: {report['total_persons']}")
    print(f"   Check-ins: {report['check_ins']}")
    print(f"   Check-outs: {report['check_outs']}")
    print(f"   Total Records: {report['total_records']}")
    
    print(f"\n📋 Attendance List:")
    print("-" * 80)
    print(f"{'Name':<20} {'Check-in':<12} {'Check-out':<12} {'Confidence':<12}")
    print("-" * 80)
    
    for person in report['persons']:
        print(f"{person['name']:<20} {person['check_in']:<12} {person['check_out']:<12} "
              f"{person['confidence']:.2f}")
    
    print("-" * 80)

def print_monthly_summary(report):
    """Print monthly summary"""
    print("\n" + "="*80)
    print(f"MONTHLY ATTENDANCE SUMMARY - {report['month_name']}")
    print("="*80)
    
    print(f"\n📊 Summary:")
    print(f"   Working Days: {report['working_days']}")
    print(f"   Total Records: {report['total_records']}")
    
    print(f"\n📋 Per Person:")
    print("-" * 80)
    print(f"{'Name':<20} {'Check-ins':<12} {'Check-outs':<12} {'Days':<10} {'Rate':<10}")
    print("-" * 80)
    
    for person in report['persons']:
        print(f"{person['name']:<20} {person['check_ins']:<12} {person['check_outs']:<12} "
              f"{person['attendance_days']:<10} {person['attendance_rate']:.1f}%")
    
    print("-" * 80)

def print_person_history(report):
    """Print person history"""
    print("\n" + "="*80)
    print(f"ATTENDANCE HISTORY - {report['person_name']}")
    print("="*80)
    
    print(f"\n📊 Period: {report['start_date']} to {report['end_date']}")
    print(f"   Total Days: {report['total_days']}")
    print(f"   Total Records: {report['total_records']}")
    
    print(f"\n📋 Daily Records:")
    print("-" * 80)
    print(f"{'Date':<12} {'Check-in':<12} {'Check-out':<12} {'Confidence':<12}")
    print("-" * 80)
    
    for day in report['days']:
        print(f"{day['date']:<12} {day['check_in']:<12} {day['check_out']:<12} "
              f"{day['confidence']:.2f}")
    
    print("-" * 80)

def main():
    print("="*60)
    print("LESSON 2: Reports & Analytics (File-Based)")
    print("="*60)
    
    # Setup paths
    script_dir = Path(__file__).parent
    
    # Try lesson-1/output first (where lesson-1 saves), then fall back to learning/output
    lesson1_log_dir = script_dir / '..' / 'lesson-1' / 'output'
    shared_log_dir = script_dir / '..' / 'output'
    
    # Determine which log directory to use
    if (lesson1_log_dir / 'attendance.csv').exists():
        log_dir = lesson1_log_dir
        print(f"📁 Using Lesson 1 output: {log_dir}")
    elif (shared_log_dir / 'attendance.csv').exists():
        log_dir = shared_log_dir
        print(f"📁 Using shared output: {log_dir}")
    else:
        log_dir = lesson1_log_dir  # Default to lesson-1
    
    attendance_file = log_dir / 'attendance.csv'
    
    # Step 1: Load attendance data
    print("\n📊 Step 1: Load Attendance Data")
    print("-" * 60)
    
    if not attendance_file.exists():
        print(f"❌ No attendance file found: {attendance_file}")
        print("💡 Run Lesson 1 first to generate attendance records")
        return
    
    records = load_attendance_csv(attendance_file)
    print(f"✅ Loaded {len(records)} attendance records")
    
    if len(records) == 0:
        print("⚠️  No records found. Run Lesson 1 to record attendance.")
        return
    
    # Get date range
    dates = [r['date'] for r in records]
    print(f"   Date range: {min(dates)} to {max(dates)}")
    
    # Step 2: Daily Report
    print("\n📊 Step 2: Daily Report")
    print("-" * 60)
    
    today = date.today()
    daily_report = generate_daily_report(records, today)
    print_daily_report(daily_report)
    
    # Step 3: Monthly Summary
    print("\n📊 Step 3: Monthly Summary")
    print("-" * 60)
    
    monthly_report = generate_monthly_summary(records, today.year, today.month)
    print_monthly_summary(monthly_report)
    
    # Step 4: Person History
    print("\n📊 Step 4: Person History")
    print("-" * 60)
    
    # Get unique persons
    persons = list(set(r['person_name'] for r in records))
    
    if persons:
        person = persons[0]  # First person as example
        start_date = today - timedelta(days=30)
        end_date = today
        
        history_report = generate_person_history(records, person, start_date, end_date)
        print_person_history(history_report)
    
    # Step 5: Export Reports
    print("\n📊 Step 5: Export Reports to JSON")
    print("-" * 60)
    
    reports_dir = log_dir / 'reports'
    reports_dir.mkdir(exist_ok=True)
    
    # Export daily report
    daily_file = reports_dir / f'daily_{today.isoformat()}.json'
    with open(daily_file, 'w', encoding='utf-8') as f:
        json.dump(daily_report, f, indent=2, ensure_ascii=False)
    print(f"✅ Daily report: {daily_file.name}")
    
    # Export monthly report
    monthly_file = reports_dir / f'monthly_{today.year}_{today.month:02d}.json'
    with open(monthly_file, 'w', encoding='utf-8') as f:
        json.dump(monthly_report, f, indent=2, ensure_ascii=False)
    print(f"✅ Monthly report: {monthly_file.name}")
    
    print("\n" + "="*60)
    print("✅ LESSON 2 COMPLETE!")
    print("="*60)
    print("\n💡 Output files:")
    print(f"   - {attendance_file}")
    print(f"   - {reports_dir}/")

if __name__ == "__main__":
    main()
