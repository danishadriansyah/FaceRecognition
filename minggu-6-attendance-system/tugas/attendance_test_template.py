"""
📝 TUGAS MINGGU 6 - Attendance System (Fill in the Blanks)
Total: 6 soal - Database & attendance management
"""

import sys
sys.path.append('../project')

# SOAL 1: Import AttendanceSystem
from attendance_system import _____________

attendance = AttendanceSystem(db_path='attendance.db')

def check_in():
    """Check-in attendance"""
    name = input("Nama: ")
    
    # SOAL 2: Record check-in
    # Hint: attendance.check_in(name)
    success = attendance._________(name)
    
    if success:
        print(f"✅ {name} checked in")


def check_out():
    """Check-out attendance"""
    name = input("Nama: ")
    
    # SOAL 3: Record check-out
    success = attendance._________(name)
    
    if success:
        print(f"✅ {name} checked out")


def view_today():
    """View today's attendance"""
    # SOAL 4: Get today's records
    # Hint: attendance.get_today_records()
    records = attendance._____________()
    
    print(f"\n📋 Today's Attendance ({len(records)} records)")
    for r in records:
        print(f"  {r['name']}: {r['check_in']} - {r['check_out']}")


def generate_report():
    """Generate monthly report"""
    month = input("Month (1-12): ")
    year = input("Year (e.g. 2025): ")
    
    # SOAL 5: Generate report
    # Hint: attendance.generate_report(month, year)
    report = attendance._____________(int(month), int(year))
    
    # SOAL 6: Export to Excel
    # Hint: attendance.export_to_excel(report, filename)
    attendance._____________(report, f'reports/report_{year}_{month}.xlsx')
    
    print("✅ Report generated")


if __name__ == "__main__":
    print("1. Check In\n2. Check Out\n3. Today\n4. Report")
    choice = input("Pilih: ")
    
    if choice == '1':
        check_in()
    elif choice == '2':
        check_out()
    elif choice == '3':
        view_today()
    elif choice == '4':
        generate_report()
