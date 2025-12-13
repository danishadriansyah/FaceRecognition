"""
Setup Week 6: Attendance System
Auto-setup untuk Week 6 dengan sample dataset
"""
import os
import sys
from pathlib import Path

# Import camera capture library
sys.path.insert(0, str(Path(__file__).parent.parent))
from camera_capture_lib import capture_faces_interactive

def setup_week6():
    """Setup Week 6 learning structure"""
    print("="*60)
    print("SETUP WEEK 6: Attendance System")
    print("="*60)
    
    base_path = Path(__file__).parent
    
    # Setup Lesson 1
    print("\n📁 Setting up Lesson 1...")
    lesson1_path = base_path / "learning" / "lesson-1"
    lesson1_dataset = lesson1_path / "dataset"
    lesson1_output = lesson1_path / "output"
    lesson1_photos = lesson1_output / "photos"
    
    lesson1_dataset.mkdir(parents=True, exist_ok=True)
    lesson1_output.mkdir(parents=True, exist_ok=True)
    lesson1_photos.mkdir(parents=True, exist_ok=True)
    
    print(f"   ✅ {lesson1_dataset}")
    print(f"   ✅ {lesson1_output}")
    print(f"   ✅ {lesson1_photos}")
    
    # Create setup instructions
    instructions = lesson1_dataset / "SETUP_INSTRUCTIONS.txt"
    instructions.write_text(
        "Week 6 Lesson 1 - Attendance System Setup\n"
        "==========================================\n\n"
        "This lesson needs:\n"
        "1. Person images in dataset folder\n"
        "2. Face encodings (encodings.pkl)\n\n"
        "Quick Setup Options:\n"
        "====================\n\n"
        "OPTION A - Copy from Week 5 (Recommended):\n"
        "  Copy-Item ..\\..\\..\\minggu-5-recognition-system\\learning\\lesson-1\\dataset\\* dataset\\ -Recurse -Force\n"
        "  Copy-Item ..\\..\\..\\minggu-5-recognition-system\\learning\\lesson-1\\output\\* dataset\\ -Force\n\n"
        "OPTION B - Copy from Week 4 + Generate Encodings:\n"
        "  Copy-Item ..\\..\\..\\minggu-4-dataset-database\\project\\dataset\\* dataset\\ -Recurse -Force\n"
        "  python -c \"from main import generate_encodings_from_dataset; generate_encodings_from_dataset('dataset', 'dataset')\"\n\n"
        "OPTION C - Use Camera Helper:\n"
        "  cd c:\\Ngoding\\Kerja\\ExtraQueensya\n"
        "  python camera_helper.py\n"
        "  Move-Item captured_faces\\* minggu-6-attendance-system\\learning\\lesson-1\\dataset\\ -Force\n"
        "  cd minggu-6-attendance-system\\learning\\lesson-1\n"
        "  python -c \"from main import generate_encodings_from_dataset; generate_encodings_from_dataset('dataset', 'dataset')\"\n\n"
        "Verify Setup:\n"
        "  Test-Path dataset\\encodings.pkl\n\n"
        "Run Lesson:\n"
        "  python main.py\n",
        encoding='utf-8'
    )
    print(f"   📄 {instructions}")
    
    # Setup Lesson 2
    print("\n📁 Setting up Lesson 2...")
    lesson2_path = base_path / "learning" / "lesson-2"
    lesson2_output = lesson2_path / "output"
    lesson2_reports = lesson2_output / "reports"
    
    lesson2_output.mkdir(parents=True, exist_ok=True)
    lesson2_reports.mkdir(parents=True, exist_ok=True)
    
    print(f"   ✅ {lesson2_output}")
    print(f"   ✅ {lesson2_reports}")
    
    # Create Lesson 2 instructions
    lesson2_instructions = lesson2_path / "SETUP_INSTRUCTIONS.txt"
    lesson2_instructions.write_text(
        "Week 6 Lesson 2 - Reports & Analytics Setup\n"
        "============================================\n\n"
        "This lesson generates reports from Lesson 1 attendance data.\n\n"
        "Prerequisites:\n"
        "1. Complete Lesson 1 first (generate attendance.csv)\n"
        "2. Have at least 2-3 attendance records\n\n"
        "Check Lesson 1 output:\n"
        "  Test-Path ..\\lesson-1\\output\\attendance.csv\n\n"
        "If no attendance data, run Lesson 1 first:\n"
        "  cd ..\\lesson-1\n"
        "  python main.py\n"
        "  # Do some check-ins/check-outs\n"
        "  # Press 'q' to quit\n\n"
        "Then run this lesson:\n"
        "  cd ..\\lesson-2\n"
        "  python main.py\n\n"
        "Reports will be saved to:\n"
        "  output/reports/daily_YYYY-MM-DD.json\n"
        "  output/reports/monthly_YYYY_MM.json\n",
        encoding='utf-8'
    )
    print(f"   📄 {lesson2_instructions}")
    
    # Setup project
    print("\n📁 Setting up Project...")
    project_path = base_path / "project"
    project_dataset = project_path / "dataset"
    project_logs = project_path / "logs"
    project_reports = project_path / "reports"
    
    project_dataset.mkdir(parents=True, exist_ok=True)
    project_logs.mkdir(parents=True, exist_ok=True)
    project_reports.mkdir(parents=True, exist_ok=True)
    
    print(f"   ✅ {project_dataset}")
    print(f"   ✅ {project_logs}")
    print(f"   ✅ {project_reports}")
    
    print("\n" + "="*60)
    print("✅ WEEK 6 SETUP COMPLETE!")
    print("="*60)
    
    # Interactive dataset population
    print("\n📋 Populate Dataset for Lesson 1:")
    print("="*60)
    print("1. Copy dari Week 5 (Recommended - with encodings)")
    print("2. Copy dari Week 4 (need generate encodings)")
    print("3. Capture faces dengan camera")
    print("4. Generate encodings dari dataset yang ada")
    print("5. Skip (populate manual nanti)")
    
    choice = input("\nPilih opsi (1/2/3/4/5): ").strip()
    
    if choice == "1":
        week5_dataset = Path(__file__).parent.parent / "minggu-5-recognition-system" / "learning" / "lesson-1" / "dataset"
        week5_output = Path(__file__).parent.parent / "minggu-5-recognition-system" / "learning" / "lesson-1" / "output"
        
        if week5_dataset.exists():
            print("\n📂 Copying dari Week 5...")
            import shutil
            try:
                for item in week5_dataset.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        dest = lesson1_dataset / item.name
                        if dest.exists():
                            shutil.rmtree(dest)
                        shutil.copytree(item, dest)
                        print(f"   ✅ Copied: {item.name}")
                
                # Copy encodings from output
                if week5_output.exists():
                    encodings = week5_output / "encodings.pkl"
                    metadata = week5_output / "metadata.json"
                    
                    if encodings.exists():
                        shutil.copy(encodings, lesson1_dataset)
                        print(f"   ✅ Copied: encodings.pkl")
                    
                    if metadata.exists():
                        shutil.copy(metadata, lesson1_dataset)
                        print(f"   ✅ Copied: metadata.json")
                
                print("\n✅ Dataset + encodings copied from Week 5!")
            except Exception as e:
                print(f"\n❌ Error: {e}")
        else:
            print("\n⚠️  Week 5 dataset tidak ditemukan. Gunakan opsi lain.")
    
    elif choice == "2":
        week4_dataset = Path(__file__).parent.parent / "minggu-4-dataset-database" / "project" / "dataset"
        if week4_dataset.exists():
            print("\n📂 Copying dari Week 4...")
            import shutil
            try:
                for item in week4_dataset.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        dest = lesson1_dataset / item.name
                        if dest.exists():
                            shutil.rmtree(dest)
                        shutil.copytree(item, dest)
                        print(f"   ✅ Copied: {item.name}")
                
                encodings = week4_dataset / "encodings.pkl"
                if encodings.exists():
                    shutil.copy(encodings, lesson1_dataset)
                    print(f"   ✅ Copied: encodings.pkl")
                
                print("\n✅ Dataset copied from Week 4!")
                
                # Ask if want to generate encodings
                gen = input("\n🔄 Generate encodings sekarang? (y/n): ").strip().lower()
                if gen == 'y':
                    print("\n🔄 Generating encodings...")
                    lesson1_path = base_path / "learning" / "lesson-1"
                    sys.path.insert(0, str(lesson1_path))
                    try:
                        from main import generate_encodings_from_dataset
                        success = generate_encodings_from_dataset(
                            str(lesson1_dataset),
                            str(lesson1_dataset),
                            model_name='Facenet512'
                        )
                        if success:
                            print("\n✅ Encodings generated successfully!")
                        else:
                            print("\n⚠️  No encodings generated. Check dataset.")
                    except Exception as e:
                        print(f"❌ Error generating encodings: {e}")
                        print("\n   Try manual dengan:")
                        print("   cd minggu-6-attendance-system\\learning\\lesson-1")
                        print("   python -c \"from main import generate_encodings_from_dataset; generate_encodings_from_dataset('dataset', 'dataset')\"")
                else:
                    print("\n⚠️  Generate encodings jika belum ada:")
                    print("   cd minggu-6-attendance-system\\learning\\lesson-1")
                    print("   python -c \"from main import generate_encodings_from_dataset; generate_encodings_from_dataset('dataset', 'dataset')\"")
            except Exception as e:
                print(f"\n❌ Error: {e}")
        else:
            print("\n⚠️  Week 4 dataset tidak ditemukan.")
    
    elif choice == "3":
        print("\n🎥 Starting face capture...")
        print("=" * 60)
        
        # Capture faces directly into lesson1 dataset
        results = capture_faces_interactive(lesson1_dataset, target_count=20)
        
        print("\n" + "=" * 60)
        print("✅ CAPTURE COMPLETED!")
        print("=" * 60)
        print(f"Total captured: {results['total_captured']}")
        print(f"Total rejected: {results['total_rejected']}")
        
        if results['persons']:
            print("\nPer person:")
            for person, stats in results['persons'].items():
                print(f"  {person}: {stats['captured']} captured")
        
        if results['total_captured'] > 0:
            # Ask if want to generate encodings
            gen = input("\n🔄 Generate encodings sekarang? (y/n): ").strip().lower()
            if gen == 'y':
                print("\n🔄 Generating encodings...")
                lesson1_path = base_path / "learning" / "lesson-1"
                sys.path.insert(0, str(lesson1_path))
                try:
                    from main import generate_encodings_from_dataset
                    success = generate_encodings_from_dataset(
                        str(lesson1_dataset),
                        str(lesson1_dataset),
                        model_name='Facenet512'
                    )
                    if success:
                        print("\n✅ Encodings generated successfully!")
                    else:
                        print("\n⚠️  No encodings generated. Check dataset.")
                except Exception as e:
                    print(f"❌ Error generating encodings: {e}")
                    print("\n   Try manual dengan:")
                    print("   cd minggu-6-attendance-system\\learning\\lesson-1")
                    print("   python -c \"from main import generate_encodings_from_dataset; generate_encodings_from_dataset('dataset', 'dataset')\"")
            else:
                print("\n✅ Next: Generate encodings")
                print("   cd minggu-6-attendance-system\\learning\\lesson-1")
                print("   python -c \"from main import generate_encodings_from_dataset; generate_encodings_from_dataset('dataset', 'dataset')\"")
        else:
            print("\n⚠️ No faces captured. Try again or add images manually.")
    
    elif choice == "4":
        print("\n🔍 Checking dataset...")
        
        # Check if dataset has person folders
        person_folders = [d for d in lesson1_dataset.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        if not person_folders:
            print("\n⚠️  Dataset kosong! Tidak ada folder person.")
            print("   Gunakan opsi 1, 2, atau 3 untuk populate dataset dulu.")
        else:
            print(f"\n📊 Found {len(person_folders)} person(s) in dataset:")
            total_images = 0
            for folder in person_folders:
                images = list(folder.glob("*.jpg")) + list(folder.glob("*.png"))
                total_images += len(images)
                print(f"   - {folder.name}: {len(images)} images")
            
            if total_images == 0:
                print("\n⚠️  No images found in person folders!")
                print("   Add images manually atau gunakan opsi capture.")
            else:
                print(f"\n✅ Total: {total_images} images ready")
                gen = input("\n🔄 Generate encodings sekarang? (y/n): ").strip().lower()
                
                if gen == 'y':
                    print("\n🔄 Generating encodings from existing dataset...")
                    lesson1_path = base_path / "learning" / "lesson-1"
                    sys.path.insert(0, str(lesson1_path))
                    try:
                        from main import generate_encodings_from_dataset
                        success = generate_encodings_from_dataset(
                            str(lesson1_dataset),
                            str(lesson1_dataset),
                            model_name='Facenet512'
                        )
                        if success:
                            print(f"\n   📁 Saved to: {lesson1_dataset / 'encodings.pkl'}")
                        else:
                            print("\n⚠️  No encodings generated. Check dataset.")
                    except Exception as e:
                        print(f"\n❌ Error generating encodings: {e}")
                        print("\n   Try manual dengan:")
                        print("   cd minggu-6-attendance-system\\learning\\lesson-1")
                        print("   python -c \"from main import generate_encodings_from_dataset; generate_encodings_from_dataset('dataset', 'dataset')\"")
                else:
                    print("\n💡 Generate encodings nanti dengan:")
                    print("   cd minggu-6-attendance-system\\learning\\lesson-1")
                    print("   python -c \"from main import generate_encodings_from_dataset; generate_encodings_from_dataset('dataset', 'dataset')\"")
    
    print("\n📋 Next Steps:")
    print("   1. Run attendance:")
    print("      cd minggu-6-attendance-system\\learning\\lesson-1")
    print("      python main.py")
    print("\n   2. Generate reports:")
    print("      cd minggu-6-attendance-system\\learning\\lesson-2")
    print("      python main.py")

if __name__ == '__main__':
    setup_week6()
