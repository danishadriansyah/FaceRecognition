"""
Lesson 1: Dataset Capture dengan Quality Check
Menggunakan camera_capture_lib untuk face capture

ATAU lebih mudah:
Run setup_week4.py dulu untuk capture faces!
"""
import sys
from pathlib import Path

# Import shared camera library
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from camera_capture_lib import capture_faces_interactive

def main():
    print("=" * 60)
    print("LESSON 1: Dataset Capture")
    print("=" * 60)
    
    print("\n📌 RECOMMENDED: Use setup script instead!")
    print("   This lesson demonstrates face capture with quality check.")
    print("\n✅ EASIER METHOD:")
    print("   cd minggu-4-dataset-database")
    print("   python setup_week4.py")
    print("   Pilih opsi [1] Capture faces\n")
    
    print("=" * 60)
    print("OR run capture here:")
    print("=" * 60)
    
    dataset_path = Path(__file__).parent / "dataset"
    dataset_path.mkdir(parents=True, exist_ok=True)
    
    print("\n🎥 Starting face capture...")
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
    
    print("\n📚 Learn about quality checking:")
    print("   - Brightness check (40-220 range)")
    print("   - Sharpness check (Laplacian variance)")
    print("   - Size check (minimum 100x100)")
    print("\n📖 See README.md for more details")

if __name__ == "__main__":
    main()
