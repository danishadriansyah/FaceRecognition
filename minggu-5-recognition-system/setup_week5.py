"""
Setup Week 5: Recognition System
Auto-setup untuk Week 5 dengan sample dataset
"""
import os
import sys
import shutil
from pathlib import Path

# Import camera capture library
sys.path.insert(0, str(Path(__file__).parent.parent))
from camera_capture_lib import capture_faces_interactive

def setup_week5():
    """Setup Week 5 learning structure with sample data"""
    print("="*60)
    print("SETUP WEEK 5: Recognition System")
    print("="*60)
    
    base_path = Path(__file__).parent
    
    # Setup Lesson 1
    print("\n📁 Setting up Lesson 1...")
    lesson1_path = base_path / "learning" / "lesson-1"
    lesson1_dataset = lesson1_path / "dataset"
    lesson1_output = lesson1_path / "output"
    
    lesson1_dataset.mkdir(parents=True, exist_ok=True)
    lesson1_output.mkdir(parents=True, exist_ok=True)
    
    print(f"   ✅ {lesson1_dataset}")
    print(f"   ✅ {lesson1_output}")
    
    # Create sample persons in Lesson 1
    sample_persons = ["Person1", "Person2", "Person3"]
    for person in sample_persons:
        person_folder = lesson1_dataset / person
        person_folder.mkdir(exist_ok=True)
        
        # Create placeholder
        placeholder = person_folder / "README.txt"
        placeholder.write_text(
            f"Add {person}'s images here:\n"
            f"- 3-5 images per person\n"
            f"- JPG or PNG format\n"
            f"- Clear face, good lighting\n\n"
            f"To populate:\n"
            f"1. Use camera_helper.py at root\n"
            f"2. Copy from Week 4\n"
            f"3. Add images manually\n",
            encoding='utf-8'
        )
        print(f"   👤 {person_folder}")
    
    # Setup Lesson 2
    print("\n📁 Setting up Lesson 2...")
    lesson2_path = base_path / "learning" / "lesson-2"
    lesson2_dataset = lesson2_path / "dataset"
    
    lesson2_dataset.mkdir(parents=True, exist_ok=True)
    print(f"   ✅ {lesson2_dataset}")
    
    # Create instructions file in Lesson 2
    instructions = lesson2_dataset / "SETUP_INSTRUCTIONS.txt"
    instructions.write_text(
        "Lesson 2 Dataset Setup:\n"
        "=======================\n\n"
        "Before running Lesson 2, copy encodings from Lesson 1:\n\n"
        "PowerShell:\n"
        "  Copy-Item ..\\lesson-1\\output\\* . -Force\n\n"
        "Or copy entire dataset:\n"
        "  Copy-Item ..\\lesson-1\\dataset\\* . -Recurse -Force\n\n"
        "Then run:\n"
        "  python main.py\n",
        encoding='utf-8'
    )
    
    # Setup project dataset
    print("\n📁 Setting up Project...")
    project_dataset = base_path / "project" / "dataset"
    project_dataset.mkdir(parents=True, exist_ok=True)
    print(f"   ✅ {project_dataset}")
    
    print("\n" + "="*60)
    print("✅ WEEK 5 SETUP COMPLETE!")
    print("="*60)
    
    # Interactive dataset population
    print("\n📋 Populate Dataset for Lesson 1:")
    print("="*60)
    print("1. Capture faces dengan camera (Recommended)")
    print("2. Copy dataset dari Week 4")
    print("3. Skip (populate manual nanti)")
    
    choice = input("\nPilih opsi (1/2/3): ").strip()
    
    if choice == "1":
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
            print("\n✅ Next: Generate encodings")
            print("   cd minggu-5-recognition-system\\learning\\lesson-1")
            print("   python -c \"import sys; sys.path.insert(0, '../../project'); from dataset_manager import DatasetManager; dm = DatasetManager('dataset'); dm.generate_encodings()\"")
        else:
            print("\n⚠️ No faces captured. Try again or add images manually.")
                                print(f"   ✅ Moved: {person_folder.name}")
                        
                        print("\n✅ Faces captured and moved to dataset!")
                        print("\n⚠️  Next: Generate encodings")
                        print("   cd minggu-5-recognition-system\\learning\\lesson-1")
                        print("   python -c \"import sys; sys.path.insert(0, '../../project'); from dataset_manager import DatasetManager; dm = DatasetManager('dataset'); dm.generate_encodings()\"")
                    else:
                        print("\n⚠️  No captured_faces folder found. User might have skipped capture.")
                else:
                    print("\n⚠️  Camera helper exited. Check if faces were captured.")
                    
            except Exception as e:
                print(f"\n❌ Error running camera helper: {e}")
    
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
                
                # Copy encodings if exists
                encodings = week4_dataset / "encodings.pkl"
                if encodings.exists():
                    shutil.copy(encodings, lesson1_dataset)
                    print(f"   ✅ Copied: encodings.pkl")
                
                metadata = week4_dataset / "metadata.json"
                if metadata.exists():
                    shutil.copy(metadata, lesson1_dataset)
                    print(f"   ✅ Copied: metadata.json")
                
                print("\n✅ Dataset copied from Week 4!")
            except Exception as e:
                print(f"\n❌ Error copying: {e}")
        else:
            print("\n⚠️  Week 4 dataset tidak ditemukan.")
            print("   Setup Week 4 dulu atau gunakan opsi 1 (camera)")
    
    print("\n📋 Next Steps:")
    print("   1. Generate encodings:")
    print("      cd minggu-5-recognition-system\\learning\\lesson-1")
    print("      python main.py")
    print("\n   2. Real-time recognition:")
    print("      cd minggu-5-recognition-system\\learning\\lesson-2")
    print("      python main.py")

if __name__ == '__main__':
    setup_week5()
