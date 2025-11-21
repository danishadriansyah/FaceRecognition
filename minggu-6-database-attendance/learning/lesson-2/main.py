"""Lesson 2: Reports & Analytics"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os
from datetime import datetime

def main():
    print("="*60)
    print("LESSON 2: Reports & Analytics")
    print("="*60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(script_dir, 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Connect to database
    db_path = os.path.join(script_dir, '..', 'lesson-1', 'attendance_demo.db')
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    
    # Generate daily report
    print("\n1. Generating daily report...")
    query = """
        SELECT 
            p.name,
            a.check_in_time,
            a.date
        FROM attendance a
        JOIN persons p ON a.person_id = p.id
        WHERE a.date = date('now')
        ORDER BY a.check_in_time
    """
    
    df = pd.read_sql(query, engine)
    
    if len(df) > 0:
        today = datetime.now().strftime('%Y-%m-%d')
        csv_path = os.path.join(reports_dir, f'daily_report_{today}.csv')
        df.to_csv(csv_path, index=False)
        print(f"   ✅ Daily report saved: {csv_path}")
        print(f"   Total attendance: {len(df)} persons")
        
        # Try Excel export
        try:
            excel_path = os.path.join(reports_dir, f'daily_report_{today}.xlsx')
            df.to_excel(excel_path, index=False, engine='openpyxl')
            print(f"   ✅ Excel report saved: {excel_path}")
        except:
            print("   ℹ️ Excel export skipped (install openpyxl if needed)")
    else:
        print("   ⚠️ No attendance records today")
    
    # Monthly summary
    print("\n2. Generating monthly summary...")
    query = """
        SELECT 
            p.name,
            COUNT(*) as days_present,
            MIN(a.check_in_time) as first_checkin,
            MAX(a.check_in_time) as last_checkin
        FROM attendance a
        JOIN persons p ON a.person_id = p.id
        GROUP BY p.name
    """
    
    df_summary = pd.read_sql(query, engine)
    
    if len(df_summary) > 0:
        summary_path = os.path.join(reports_dir, 'monthly_summary.csv')
        df_summary.to_csv(summary_path, index=False)
        print(f"   ✅ Monthly summary saved: {summary_path}")
        
        print("\n   Summary:")
        for _, row in df_summary.iterrows():
            print(f"   - {row['name']}: {row['days_present']} days")
    
    print("\n✅ REPORTS GENERATED!")
    print(f"📁 Check: {reports_dir}")

if __name__ == '__main__':
    main()
