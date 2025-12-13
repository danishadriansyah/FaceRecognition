"""
Report Generator: Generate attendance reports and analytics
Daily, monthly, and person-specific attendance reports
"""
import os
import sys
from datetime import datetime, date, timedelta
from collections import defaultdict

# Add Week 6 Lesson 1 module
lesson1_path = os.path.join(os.path.dirname(__file__), '..', 'lesson-1')
sys.path.insert(0, lesson1_path)

from attendance_system import AttendanceSystem, Attendance, Person  # type: ignore

# Try to import pandas for Excel export
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class ReportGenerator:
    """Generate attendance reports and analytics"""
    
    def __init__(self, attendance_system):
        """
        Initialize report generator
        
        Args:
            attendance_system: AttendanceSystem instance
        """
        self.system = attendance_system
        self.session = attendance_system.db.get_session()
    
    def daily_report(self, report_date=None):
        """
        Generate daily attendance report
        
        Args:
            report_date: date object (default: today)
            
        Returns:
            dict with report data
        """
        if report_date is None:
            report_date = date.today()
        
        # Get all attendances for the date
        attendances = self.session.query(Attendance).filter_by(date=report_date).all()
        
        # Get all persons
        all_persons = self.session.query(Person).all()
        
        # Create attendance map
        attendance_map = {att.person_id: att for att in attendances}
        
        report_data = {
            'date': report_date,
            'total_persons': len(all_persons),
            'present': len(attendances),
            'absent': len(all_persons) - len(attendances),
            'records': []
        }
        
        # Process each person
        for person in all_persons:
            if person.id in attendance_map:
                att = attendance_map[person.id]
                record = {
                    'name': person.name,
                    'employee_id': person.employee_id,
                    'check_in': att.check_in.strftime('%H:%M:%S') if att.check_in else '-',
                    'check_out': att.check_out.strftime('%H:%M:%S') if att.check_out else '-',
                    'status': att.status,
                    'confidence': f"{att.confidence:.1f}%",
                    'present': True
                }
            else:
                record = {
                    'name': person.name,
                    'employee_id': person.employee_id,
                    'check_in': '-',
                    'check_out': '-',
                    'status': 'Absent',
                    'confidence': '-',
                    'present': False
                }
            
            report_data['records'].append(record)
        
        # Count statuses
        on_time = sum(1 for r in report_data['records'] if 'On Time' in r['status'])
        late = sum(1 for r in report_data['records'] if 'Late' in r['status'])
        
        report_data['on_time'] = on_time
        report_data['late'] = late
        report_data['attendance_rate'] = (report_data['present'] / report_data['total_persons'] * 100) if report_data['total_persons'] > 0 else 0
        
        return report_data
    
    def monthly_summary(self, year=None, month=None):
        """
        Generate monthly attendance summary
        
        Args:
            year: Year (default: current year)
            month: Month 1-12 (default: current month)
            
        Returns:
            dict with summary data
        """
        if year is None or month is None:
            today = date.today()
            year = year or today.year
            month = month or today.month
        
        # Get date range
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        # Get all attendances in month
        attendances = self.session.query(Attendance).filter(
            Attendance.date >= start_date,
            Attendance.date <= end_date
        ).all()
        
        # Get all persons
        all_persons = self.session.query(Person).all()
        
        # Calculate working days (excluding weekends)
        working_days = 0
        current = start_date
        while current <= end_date:
            if current.weekday() < 5:  # Monday = 0, Friday = 4
                working_days += 1
            current += timedelta(days=1)
        
        # Group by person
        person_stats = {}
        for person in all_persons:
            person_attendances = [att for att in attendances if att.person_id == person.id]
            
            present_days = len(person_attendances)
            late_count = sum(1 for att in person_attendances if 'Late' in att.status)
            on_time_count = sum(1 for att in person_attendances if att.status == 'On Time')
            absent_days = working_days - present_days
            
            person_stats[person.id] = {
                'name': person.name,
                'employee_id': person.employee_id,
                'present': present_days,
                'late': late_count,
                'on_time': on_time_count,
                'absent': absent_days,
                'attendance_rate': (present_days / working_days * 100) if working_days > 0 else 0
            }
        
        summary = {
            'year': year,
            'month': month,
            'month_name': start_date.strftime('%B %Y'),
            'working_days': working_days,
            'total_persons': len(all_persons),
            'person_stats': person_stats,
            'average_attendance': sum(s['attendance_rate'] for s in person_stats.values()) / len(person_stats) if person_stats else 0
        }
        
        return summary
    
    def person_history(self, person_id, days=30):
        """
        Generate attendance history for specific person
        
        Args:
            person_id: Person ID
            days: Number of days to include
            
        Returns:
            dict with person history
        """
        person = self.session.query(Person).filter_by(id=person_id).first()
        
        if not person:
            return None
        
        # Get date range
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        # Get attendances
        attendances = self.session.query(Attendance).filter(
            Attendance.person_id == person_id,
            Attendance.date >= start_date,
            Attendance.date <= end_date
        ).order_by(Attendance.date.desc()).all()
        
        records = []
        for att in attendances:
            records.append({
                'date': att.date.strftime('%Y-%m-%d'),
                'check_in': att.check_in.strftime('%H:%M:%S') if att.check_in else '-',
                'check_out': att.check_out.strftime('%H:%M:%S') if att.check_out else '-',
                'status': att.status,
                'confidence': f"{att.confidence:.1f}%"
            })
        
        # Calculate stats
        present_days = len(attendances)
        late_days = sum(1 for att in attendances if 'Late' in att.status)
        on_time_days = sum(1 for att in attendances if att.status == 'On Time')
        
        history = {
            'person': {
                'name': person.name,
                'employee_id': person.employee_id,
                'department': person.department
            },
            'period': {
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d'),
                'days': days
            },
            'records': records,
            'stats': {
                'present': present_days,
                'late': late_days,
                'on_time': on_time_days,
                'attendance_rate': (present_days / days * 100) if days > 0 else 0
            }
        }
        
        return history
    
    def export_to_csv(self, report_data, filename):
        """Export report to CSV"""
        if not PANDAS_AVAILABLE:
            print("⚠️  pandas not installed. Install: pip install pandas")
            return False
        
        try:
            if 'records' in report_data:
                # Daily report
                df = pd.DataFrame(report_data['records'])
            elif 'person_stats' in report_data:
                # Monthly summary
                df = pd.DataFrame(report_data['person_stats'].values())
            else:
                # Person history
                df = pd.DataFrame(report_data['records'])
            
            df.to_csv(filename, index=False)
            print(f"✅ Exported to: {filename}")
            return True
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
    
    def export_to_excel(self, report_data, filename):
        """Export report to Excel"""
        if not PANDAS_AVAILABLE:
            print("⚠️  pandas not installed. Install: pip install pandas openpyxl")
            return False
        
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                if 'records' in report_data:
                    # Daily report
                    df = pd.DataFrame(report_data['records'])
                    df.to_excel(writer, sheet_name='Daily Report', index=False)
                    
                    # Summary sheet
                    summary_data = {
                        'Metric': ['Total Persons', 'Present', 'Absent', 'On Time', 'Late', 'Attendance Rate'],
                        'Value': [
                            report_data['total_persons'],
                            report_data['present'],
                            report_data['absent'],
                            report_data['on_time'],
                            report_data['late'],
                            f"{report_data['attendance_rate']:.1f}%"
                        ]
                    }
                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)
                    
                elif 'person_stats' in report_data:
                    # Monthly summary
                    df = pd.DataFrame(report_data['person_stats'].values())
                    df.to_excel(writer, sheet_name='Monthly Summary', index=False)
                else:
                    # Person history
                    df = pd.DataFrame(report_data['records'])
                    df.to_excel(writer, sheet_name='History', index=False)
            
            print(f"✅ Exported to: {filename}")
            return True
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False


def test_report_generator():
    """Test report generator"""
    print("="*60)
    print("TEST: Report Generator")
    print("="*60)
    
    # XAMPP Default: root user, no password
    connection_string = "mysql+pymysql://root:@localhost:3306/face_recognition_db"
    
    try:
        system = AttendanceSystem(connection_string)
        generator = ReportGenerator(system)
        
        # Daily report
        print("\n📊 Daily Report:")
        daily = generator.daily_report()
        print(f"   Date: {daily['date']}")
        print(f"   Present: {daily['present']}/{daily['total_persons']}")
        print(f"   Attendance rate: {daily['attendance_rate']:.1f}%")
        
        # Monthly summary
        print("\n📊 Monthly Summary:")
        monthly = generator.monthly_summary()
        print(f"   Month: {monthly['month_name']}")
        print(f"   Working days: {monthly['working_days']}")
        print(f"   Average attendance: {monthly['average_attendance']:.1f}%")
        
        system.close()
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")


if __name__ == '__main__':
    test_report_generator()
