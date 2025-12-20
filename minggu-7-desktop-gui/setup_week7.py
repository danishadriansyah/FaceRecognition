"""
Setup Week 7: Desktop GUI
Auto-setup untuk Week 7 dengan sample dataset
"""
import os
import sys
from pathlib import Path

# Import camera capture library
sys.path.insert(0, str(Path(__file__).parent.parent))
from camera_capture_lib import capture_faces_interactive

def setup_week7():
    """Setup Week 7 project structure"""
    print("="*60)
    print("SETUP WEEK 7: Desktop GUI")
    print("="*60)
    
    base_path = Path(__file__).parent / "project"
    
    # Create directories
    print("\n📁 Creating directories...")
    dirs_to_create = [
        base_path / "dataset",
        base_path / "logs",
        base_path / "logs" / "photos",
        base_path / "reports",
        base_path / "snapshots",
        base_path / "api"
    ]
    
    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {dir_path}")
    
    # Create setup instructions
    instructions = base_path / "dataset" / "SETUP_INSTRUCTIONS.txt"
    instructions.write_text(
        "Week 7 - Desktop GUI Setup\n"
        "==========================\n\n"
        "This desktop application needs dataset with encodings.\n\n"
        "Quick Setup Options:\n"
        "====================\n\n"
        "OPTION A - Copy from Week 6 (Recommended):\n"
        "  Copy-Item ..\\..\\minggu-6-attendance-system\\learning\\lesson-1\\dataset\\* dataset\\ -Recurse -Force\n\n"
        "OPTION B - Copy from Week 5:\n"
        "  Copy-Item ..\\..\\minggu-5-recognition-system\\learning\\lesson-1\\dataset\\* dataset\\ -Recurse -Force\n"
        "  Copy-Item ..\\..\\minggu-5-recognition-system\\learning\\lesson-1\\output\\* dataset\\ -Force\n\n"
        "OPTION C - Copy from Week 4:\n"
        "  Copy-Item ..\\..\\minggu-4-dataset-database\\project\\dataset\\* dataset\\ -Recurse -Force\n\n"
        "OPTION D - Fresh Start with Camera:\n"
        "  cd c:\\Ngoding\\Kerja\\ExtraQueensya\n"
        "  python camera_helper.py\n"
        "  Move-Item captured_faces\\* minggu-7-desktop-gui\\project\\dataset\\ -Force\n"
        "  cd minggu-7-desktop-gui\\project\n"
        "  python -c \"from dataset_manager import DatasetManager; dm = DatasetManager('dataset'); dm.generate_encodings()\"\n\n"
        "Verify Setup:\n"
        "  Test-Path dataset\\encodings.pkl\n"
        "  Get-ChildItem dataset -Directory\n\n"
        "Run Application:\n"
        "  python app.py\n\n"
        "Features:\n"
        "  - Real-time face recognition\n"
        "  - Attendance tracking with GUI\n"
        "  - Report generation\n"
        "  - Dataset management\n"
        "  - Photo capture and storage\n",
        encoding='utf-8'
    )
    print(f"\n📄 {instructions}")
    
    # Create API directory instructions
    api_readme = base_path / "api" / "README.txt"
    api_readme.write_text(
        "Desktop GUI Application\n"
        "========================\n\n"
        "Week 7 focuses on pure Python Desktop GUI with Tkinter.\n\n"
        "To use the application:\n"
        "1. Ensure all dependencies installed: pip install -r requirements.txt\n"
        "2. Run the main application: python main_app.py\n"
        "3. Use the Desktop GUI for all operations\n\n"
        "Main Features:\n"
        "  - Live webcam preview and face detection\n"
        "  - Register new persons with photo capture\n"
        "  - Real-time attendance marking\n"
        "  - View and export attendance reports\n",
        encoding='utf-8'
    )
    print(f"   📄 {api_readme}")
    
    # Create sample persons template
    sample_persons = ["Employee1", "Employee2", "Employee3"]
    print("\n👤 Creating sample person folders...")
    for person in sample_persons:
        person_folder = base_path / "dataset" / person
        person_folder.mkdir(exist_ok=True)
        
        placeholder = person_folder / "README.txt"
        placeholder.write_text(
            f"Add {person}'s face images here\n"
            f"================================\n\n"
            f"Requirements:\n"
            f"  - 3-5 images minimum\n"
            f"  - JPG or PNG format\n"
            f"  - Clear face visible\n"
            f"  - Good lighting\n"
            f"  - Different angles\n\n"
            f"Then generate encodings using dataset_manager.py\n",
            encoding='utf-8'
        )
        print(f"   ✅ {person_folder}")
    
    print("\n" + "="*60)
    print("✅ WEEK 7 SETUP COMPLETE!")
    print("="*60)
    
    # Interactive dataset population
    print("\n📋 Populate Dataset:")
    print("="*60)
    print("1. Copy dari Week 6 (Recommended - with encodings)")
    print("2. Copy dari Week 5 (with encodings)")
    print("3. Copy dari Week 4 (need generate encodings)")
    print("4. Capture faces dengan camera")
    print("5. Skip (populate manual nanti)")
    
    choice = input("\nPilih opsi (1/2/3/4/5): ").strip()
    
    if choice == "1":
        week6_dataset = Path(__file__).parent.parent / "minggu-6-attendance-system" / "learning" / "lesson-1" / "dataset"
        if week6_dataset.exists():
            print("\n📂 Copying dari Week 6...")
            import shutil
            try:
                for item in week6_dataset.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        dest = base_path / "dataset" / item.name
                        if dest.exists():
                            shutil.rmtree(dest)
                        shutil.copytree(item, dest)
                        print(f"   ✅ Copied: {item.name}")
                
                # Copy encodings
                for file in ["encodings.pkl", "metadata.json"]:
                    src = week6_dataset / file
                    if src.exists():
                        shutil.copy(src, base_path / "dataset")
                        print(f"   ✅ Copied: {file}")
                
                print("\n✅ Dataset copied from Week 6!")
            except Exception as e:
                print(f"\n❌ Error: {e}")
        else:
            print("\n⚠️  Week 6 dataset tidak ditemukan.")
    
    elif choice == "2":
        week5_dataset = Path(__file__).parent.parent / "minggu-5-recognition-system" / "learning" / "lesson-1" / "dataset"
        week5_output = Path(__file__).parent.parent / "minggu-5-recognition-system" / "learning" / "lesson-1" / "output"
        
        if week5_dataset.exists():
            print("\n📂 Copying dari Week 5...")
            import shutil
            try:
                for item in week5_dataset.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        dest = base_path / "dataset" / item.name
                        if dest.exists():
                            shutil.rmtree(dest)
                        shutil.copytree(item, dest)
                        print(f"   ✅ Copied: {item.name}")
                
                if week5_output.exists():
                    for file in ["encodings.pkl", "metadata.json"]:
                        src = week5_output / file
                        if src.exists():
                            shutil.copy(src, base_path / "dataset")
                            print(f"   ✅ Copied: {file}")
                
                print("\n✅ Dataset copied from Week 5!")
            except Exception as e:
                print(f"\n❌ Error: {e}")
        else:
            print("\n⚠️  Week 5 dataset tidak ditemukan.")
    
    elif choice == "3":
        week4_dataset = Path(__file__).parent.parent / "minggu-4-dataset-database" / "project" / "dataset"
        if week4_dataset.exists():
            print("\n📂 Copying dari Week 4...")
            import shutil
            try:
                for item in week4_dataset.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        dest = base_path / "dataset" / item.name
                        if dest.exists():
                            shutil.rmtree(dest)
                        shutil.copytree(item, dest)
                        print(f"   ✅ Copied: {item.name}")
                
                print("\n✅ Dataset copied from Week 4!")
                print("⚠️  Generate encodings:")
                print("   cd minggu-7-desktop-gui\\project")
                print("   python -c \"from dataset_manager import DatasetManager; dm = DatasetManager('dataset'); dm.generate_encodings()\"")
            except Exception as e:
                print(f"\n❌ Error: {e}")
        else:
            print("\n⚠️  Week 4 dataset tidak ditemukan.")
    
    elif choice == "4":
        print("\n🎥 Starting face capture...")
        print("=" * 60)
        
        # Capture faces directly into project dataset
        results = capture_faces_interactive(base_path / "dataset", target_count=20)
        
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
            print("   cd minggu-7-desktop-gui\\project")
            print("   python -c \"from dataset_manager import DatasetManager; dm = DatasetManager('dataset'); dm.generate_encodings()\"")
        else:
            print("\n⚠️ No faces captured. Try again or add images manually.")
    
    print("\n📋 Next Steps:")
    print("   1. Run desktop app:")
    print("      cd minggu-7-desktop-gui\\project")
    print("      python app.py")

if __name__ == '__main__':
    setup_week7()
