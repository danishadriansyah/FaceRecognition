"""
Lesson 2: Reports & Analytics
Generate attendance reports, export to Excel/CSV
"""
import os
import sys
from datetime import date

# Add Lesson 1 module
lesson1_path = os.path.join(os.path.dirname(__file__), '..', 'lesson-1')
sys.path.insert(0, lesson1_path)

from attendance_system import AttendanceSystem
from report_generator import ReportGenerator

def print_daily_report(report_data):
    """Print daily report to console"""
    print("\n" + "="*80)
    print(f"DAILY ATTENDANCE REPORT - {report_data['date']}")
    print("="*80)
    
    print(f"\n📊 Summary:")
    print(f"   Total Persons: {report_data['total_persons']}")
    print(f"   Present: {report_data['present']}")
    print(f"   Absent: {report_data['absent']}")
    print(f"   On Time: {report_data['on_time']}")
    print(f"   Late: {report_data['late']}")
    print(f"   Attendance Rate: {report_data['attendance_rate']:.1f}%")
    
    print(f"\n📋 Attendance List:")
    print("-" * 80)
    print(f"{'Name':<20} {'Employee ID':<12} {'Check-in':<10} {'Status':<20} {'Confidence':<12}")
    print("-" * 80)
    
    for record in report_data['records']:
        print(f"{record['name']:<20} {record['employee_id']:<12} {record['check_in']:<10} "
              f"{record['status']:<20} {record['confidence']:<12}")
    
    print("-" * 80)

def print_monthly_summary(summary_data):
    """Print monthly summary to console"""
    print("\n" + "="*80)
    print(f"MONTHLY ATTENDANCE SUMMARY - {summary_data['month_name']}")
    print("="*80)
    
    print(f"\n📊 Overview:")
    print(f"   Working Days: {summary_data['working_days']}")
    print(f"   Total Persons: {summary_data['total_persons']}")
    print(f"   Average Attendance: {summary_data['average_attendance']:.1f}%")
    
    print(f"\n📋 Per Person:")
    print("-" * 80)
    print(f"{'Name':<20} {'Present':<10} {'Late':<10} {'Absent':<10} {'Rate':<10}")
    print("-" * 80)
    
    for stats in summary_data['person_stats'].values():
        print(f"{stats['name']:<20} {stats['present']:<10} {stats['late']:<10} "
              f"{stats['absent']:<10} {stats['attendance_rate']:.1f}%")
    
    print("-" * 80)

def print_person_history(history_data):
    """Print person history to console"""
    person = history_data['person']
    period = history_data['period']
    stats = history_data['stats']
    
    print("\n" + "="*80)
    print(f"ATTENDANCE HISTORY - {person['name']} ({person['employee_id']})")
    print("="*80)
    
    print(f"\n📊 Period: {period['start']} to {period['end']} ({period['days']} days)")
    print(f"   Department: {person['department']}")
    print(f"   Present: {stats['present']} days")
    print(f"   Late: {stats['late']} days")
    print(f"   On Time: {stats['on_time']} days")
    print(f"   Attendance Rate: {stats['attendance_rate']:.1f}%")
    
    print(f"\n📋 Records:")
    print("-" * 80)
    print(f"{'Date':<12} {'Check-in':<12} {'Check-out':<12} {'Status':<20} {'Confidence':<12}")
    print("-" * 80)
    
    for record in history_data['records']:
        print(f"{record['date']:<12} {record['check_in']:<12} {record['check_out']:<12} "
              f"{record['status']:<20} {record['confidence']:<12}")
    
    print("-" * 80)

def main():
    print("="*60)
    print("LESSON 2: Reports & Analytics")
    print("="*60)
    
    # XAMPP Default: root user, no password
    connection_string = "mysql+pymysql://root:@localhost:3306/face_recognition_db"
    
    # Step 1: Initialize
    print("\n📊 Step 1: Initialize Report Generator")
    print("-" * 60)
    
    try:
        attendance_system = AttendanceSystem(connection_string)
        report_generator = ReportGenerator(attendance_system)
        print("✅ Report generator initialized")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. XAMPP MySQL running")
        print("   2. Week 4 & Week 6 Lesson 1 completed")
        print("   3. Check HeidiSQL: attendances table should have data")
        print("   4. Install: pip install pandas openpyxl")
        return
    
    # Create reports directory
    reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Interactive menu
    while True:
        print("\n" + "="*60)
        print("ATTENDANCE REPORTS MENU")
        print("="*60)
        print("1. Daily Report (Today)")
        print("2. Daily Report (Specific Date)")
        print("3. Monthly Summary (This Month)")
        print("4. Monthly Summary (Specific Month)")
        print("5. Person History")
        print("6. Export Daily Report to Excel")
        print("7. Export Monthly Summary to Excel")
        print("8. Export to CSV")
        print("9. Exit")
        print("="*60)
        
        choice = input("\nSelect option (1-9): ").strip()
        
        if choice == '1':
            # Daily report - today
            report = report_generator.daily_report()
            print_daily_report(report)
            
        elif choice == '2':
            # Daily report - specific date
            date_str = input("Enter date (YYYY-MM-DD): ").strip()
            try:
                from datetime import datetime
                report_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                report = report_generator.daily_report(report_date)
                print_daily_report(report)
            except ValueError:
                print("❌ Invalid date format")
            
        elif choice == '3':
            # Monthly summary - this month
            summary = report_generator.monthly_summary()
            print_monthly_summary(summary)
            
        elif choice == '4':
            # Monthly summary - specific month
            try:
                year = int(input("Enter year (e.g., 2024): ").strip())
                month = int(input("Enter month (1-12): ").strip())
                summary = report_generator.monthly_summary(year, month)
                print_monthly_summary(summary)
            except ValueError:
                print("❌ Invalid input")
            
        elif choice == '5':
            # Person history
            print("\n📋 Available Persons:")
            session = attendance_system.db.get_session()
            from models import Person
            persons = session.query(Person).all()
            
            for idx, person in enumerate(persons, 1):
                print(f"   {idx}. {person.name} ({person.employee_id})")
            
            try:
                person_idx = int(input("\nSelect person number: ").strip()) - 1
                if 0 <= person_idx < len(persons):
                    person_id = persons[person_idx].id
                    days = int(input("Number of days (e.g., 30): ").strip() or "30")
                    history = report_generator.person_history(person_id, days)
                    print_person_history(history)
                else:
                    print("❌ Invalid selection")
            except ValueError:
                print("❌ Invalid input")
            
        elif choice == '6':
            # Export daily to Excel
            report = report_generator.daily_report()
            filename = os.path.join(reports_dir, f"daily_{report['date']}.xlsx")
            report_generator.export_to_excel(report, filename)
            
        elif choice == '7':
            # Export monthly to Excel
            summary = report_generator.monthly_summary()
            filename = os.path.join(reports_dir, f"monthly_{summary['year']}_{summary['month']:02d}.xlsx")
            report_generator.export_to_excel(summary, filename)
            
        elif choice == '8':
            # Export to CSV
            print("\n1. Daily Report")
            print("2. Monthly Summary")
            export_choice = input("Select report type: ").strip()
            
            if export_choice == '1':
                report = report_generator.daily_report()
                filename = os.path.join(reports_dir, f"daily_{report['date']}.csv")
                report_generator.export_to_csv(report, filename)
            elif export_choice == '2':
                summary = report_generator.monthly_summary()
                filename = os.path.join(reports_dir, f"monthly_{summary['year']}_{summary['month']:02d}.csv")
                report_generator.export_to_csv(summary, filename)
            
        elif choice == '9':
            # Exit
            print("\n👋 Exiting report generator...")
            break
        
        else:
            print("❌ Invalid option")
    
    # Summary
    print("\n" + "="*60)
    print("✅ REPORT SESSION COMPLETE!")
    print("="*60)
    print(f"Reports saved to: {reports_dir}")
    
    print("\n💡 Next Steps:")
    print("   - Week 7: Build Desktop GUI")
    print("   - Integrate reports into GUI")
    print("   - Add charts and visualizations")
    
    attendance_system.close()

if __name__ == '__main__':
    main()
