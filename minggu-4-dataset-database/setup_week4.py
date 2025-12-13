"""
Setup Week 4: Dataset Management
Auto-setup untuk Week 4 tanpa dependency ke week lain
"""
import os
import sys
from pathlib import Path

# Import camera capture library
sys.path.insert(0, str(Path(__file__).parent.parent))
from camera_capture_lib import capture_faces_interactive

def setup_week4():
    """Setup Week 4 project structure"""
    print("="*60)
    print("SETUP WEEK 4: Dataset Management")
    print("="*60)
    
    base_path = Path(__file__).parent / "project"
    dataset_path = base_path / "dataset"
    
    # Create directories
    print("\n📁 Creating directories...")
    dataset_path.mkdir(parents=True, exist_ok=True)
    (base_path / "rejected").mkdir(exist_ok=True)
    (base_path / "backups").mkdir(exist_ok=True)
    print(f"   ✅ {dataset_path}")
    print(f"   ✅ {base_path / 'rejected'}")
    print(f"   ✅ {base_path / 'backups'}")
    
    # Create sample README in dataset
    readme_content = """# Dataset Folder - Week 4

Dataset ini untuk Week 4 Dataset Management.

## Cara Populate Dataset

### Option 1: Gunakan Camera Helper (Recommended)
```bash
cd c:\\Ngoding\\Kerja\\ExtraQueensya
python camera_helper.py
```

Program akan:
1. Buka camera untuk capture wajah
2. Minta nama person
3. Capture multiple angles (frontal, left, right, up, down)
4. Save ke `captured_faces/nama_person/`
5. Move ke `minggu-4-dataset-database/project/dataset/`

### Option 2: Manual Copy
1. Buat folder per person: `dataset/Alice/`, `dataset/Bob/`
2. Isi dengan images (JPG/PNG)
3. Minimal 3 images per person

### Option 3: Gunakan Test Images
```bash
# Copy test images yang sudah ada
Copy-Item test_images\\* dataset\\ -Recurse -Force
```

## Generate Encodings

Setelah ada images:
```bash
cd minggu-4-dataset-database/project
python dataset_manager.py
```

Pilih menu:
- **1** - Add person (capture more faces)
- **2** - Generate encodings (from existing images)
- **3** - List all persons
- **4** - Export dataset

Encodings akan disimpan di `dataset/encodings.pkl`.
"""
    
    readme_file = dataset_path / "README.md"
    readme_file.write_text(readme_content, encoding='utf-8')
    print(f"\n📄 Created: {readme_file}")
    
    # Create sample persons (empty folders as template)
    sample_persons = ["Alice", "Bob", "Charlie"]
    print("\n👤 Creating sample person folders...")
    for person in sample_persons:
        person_folder = dataset_path / person
        person_folder.mkdir(exist_ok=True)
        
        # Create placeholder README
        placeholder = person_folder / "README.txt"
        placeholder.write_text(
            f"Place {person}'s face images here (3-5 images recommended)\n"
            f"Formats: JPG, PNG\n"
            f"Tips: Different angles, good lighting, clear face\n",
            encoding='utf-8'
        )
        print(f"   ✅ {person_folder}")
    
    print("\n" + "="*60)
    print("✅ WEEK 4 SETUP COMPLETE!")
    print("="*60)
    
    # Interactive dataset population
    print("\n📋 Populate Dataset:")
    print("="*60)
    print("1. Capture faces dengan camera (Recommended)")
    print("2. Skip (populate manual nanti)")
    
    choice = input("\nPilih opsi (1/2): ").strip()
    
    if choice == "1":
        print("\n🎥 Starting face capture...")
        print("=" * 60)
        
        # Capture faces directly into dataset
        results = capture_faces_interactive(dataset_path, target_count=20)
        
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
            print("   cd minggu-4-dataset-database\\project")
            print("   python dataset_manager.py")
            print("   Pilih menu [2] Generate encodings")
        else:
            print("\n⚠️ No faces captured. Try again or add images manually.")
                else:
                    print("\n⚠️  Camera helper exited. Check if faces were captured.")
                    
            except Exception as e:
                print(f"\n❌ Error running camera helper: {e}")
    
    print("\n📋 Next Steps:")
    print("   1. Generate encodings:")
    print("      cd minggu-4-dataset-database\\project")
    print("      python dataset_manager.py")
    print("\n   2. Verify:")
    print("      Test-Path minggu-4-dataset-database\\project\\dataset\\encodings.pkl")

if __name__ == '__main__':
    setup_week4()
