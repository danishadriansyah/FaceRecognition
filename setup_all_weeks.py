"""
Setup All Weeks - Complete Project Setup
Run this script to setup all weeks at once
"""
import os
import sys
from pathlib import Path

# Import individual setup scripts
import setup_week4
import setup_week5
import setup_week6
import setup_week7

def main():
    """Setup all weeks in sequence"""
    print("\n" + "="*70)
    print(" "*15 + "FACE RECOGNITION PROJECT SETUP")
    print(" "*15 + "Setup All Weeks (4-7)")
    print("="*70)
    
    print("\nThis will create the complete folder structure for:")
    print("  - Week 4: Dataset Management")
    print("  - Week 5: Recognition System")
    print("  - Week 6: Attendance System")
    print("  - Week 7: Desktop GUI")
    
    response = input("\nProceed with setup? (y/n): ")
    if response.lower() != 'y':
        print("Setup cancelled.")
        return
    
    print("\n" + "="*70)
    
    # Setup each week
    try:
        print("\n🚀 Starting Week 4 setup...")
        setup_week4.setup_week4()
        
        print("\n\n🚀 Starting Week 5 setup...")
        setup_week5.setup_week5()
        
        print("\n\n🚀 Starting Week 6 setup...")
        setup_week6.setup_week6()
        
        print("\n\n🚀 Starting Week 7 setup...")
        setup_week7.setup_week7()
        
        print("\n\n" + "="*70)
        print("✅ ALL WEEKS SETUP COMPLETE!")
        print("="*70)
        
        print("\n📋 Quick Start Guide:")
        print("="*70)
        
        print("\n1️⃣  WEEK 4 - Capture & Store Dataset:")
        print("     cd minggu-4-dataset-database/project")
        print("     python camera_helper.py  # Capture faces")
        print("     python dataset_manager.py  # Manage dataset")
        
        print("\n2️⃣  WEEK 5 - Face Recognition:")
        print("     cd minggu-5-recognition-system/learning/lesson-1")
        print("     # Copy dataset from Week 4 or use camera_helper.py")
        print("     python main.py  # Generate encodings")
        print("     cd ../lesson-2")
        print("     python main.py  # Real-time recognition")
        
        print("\n3️⃣  WEEK 6 - Attendance System:")
        print("     cd minggu-6-attendance-system/learning/lesson-1")
        print("     # Copy dataset+encodings from Week 5")
        print("     python main.py  # Attendance tracking")
        print("     cd ../lesson-2")
        print("     python main.py  # Generate reports")
        
        print("\n4️⃣  WEEK 7 - Desktop GUI:")
        print("     cd minggu-7-desktop-gui/project")
        print("     # Copy dataset from any previous week")
        print("     python app.py  # Launch GUI application")
        
        print("\n" + "="*70)
        print("📚 Documentation:")
        print("="*70)
        print("  - INDEPENDENT_WEEKS_GUIDE.md - Complete independence guide")
        print("  - Each dataset folder has SETUP_INSTRUCTIONS.txt")
        print("  - Each lesson folder has README.md with details")
        
        print("\n💡 Tips:")
        print("  - Each week is independent (no cross-dependencies)")
        print("  - Use camera_helper.py at root for capturing faces")
        print("  - Copy datasets between weeks as needed")
        print("  - All data is file-based (no database required)")
        
        print("\n🎯 Ready to start? Begin with Week 4!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
