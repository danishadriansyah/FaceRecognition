"""
📝 TUGAS MINGGU 4 - Dataset Manager (Fill in the Blanks)
Total: 6 soal - Dataset collection & management
"""

import cv2
import os
import shutil
from datetime import datetime

# SOAL 1: Import DatasetManager dari ../project/
import sys
sys.path.append('../project')
from dataset_manager import _____________


def capture_dataset():
    """Capture multiple photos untuk dataset"""
    manager = DatasetManager('dataset/')
    
    name = input("Nama person: ")
    count = int(input("Jumlah foto (recommended: 10-20): "))
    
    # SOAL 2: Buka webcam
    cap = _____________(0)
    
    captured = 0
    
    print("\nTekan SPACE untuk capture, ESC untuk stop")
    
    while captured < count:
        ret, frame = cap.read()
        cv2.putText(frame, f'Captured: {captured}/{count}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Capture Dataset', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):
            # SOAL 3: Save image ke dataset
            # Hint: manager.add_face(name, frame)
            success = manager._________(name, frame)
            
            if success:
                captured += 1
                print(f"✅ Captured {captured}/{count}")
        
        elif key == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n✅ Dataset created: {captured} photos")


def validate_dataset():
    """Validate quality dataset"""
    manager = DatasetManager('dataset/')
    
    # SOAL 4: Get statistics
    # Hint: manager.get_statistics()
    stats = manager._____________()
    
    print("\n📊 DATASET STATISTICS")
    print(f"Total persons: {stats['total_persons']}")
    print(f"Total images: {stats['total_images']}")
    print(f"Average per person: {stats['average_per_person']:.1f}")


def export_dataset():
    """Export dataset untuk training"""
    manager = DatasetManager('dataset/')
    
    export_path = 'exported_dataset/'
    
    # SOAL 5: Export dataset
    # Hint: manager.export_dataset(path)
    success = manager._____________(export_path)
    
    if success:
        print(f"✅ Dataset exported to {export_path}")


def backup_dataset():
    """Backup dataset"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f'backups/dataset_{timestamp}'
    
    # SOAL 6: Copy directory tree
    # Hint: shutil.copytree(src, dst)
    _______.copytree('dataset/', backup_path)
    
    print(f"✅ Backup created: {backup_path}")


def main():
    os.makedirs('dataset', exist_ok=True)
    os.makedirs('backups', exist_ok=True)
    
    while True:
        print("\n" + "="*40)
        print("   DATASET MANAGER")
        print("="*40)
        print("1. Capture Dataset")
        print("2. Validate Dataset")
        print("3. Export Dataset")
        print("4. Backup Dataset")
        print("5. Exit")
        
        choice = input("\nPilih: ")
        
        if choice == '1':
            capture_dataset()
        elif choice == '2':
            validate_dataset()
        elif choice == '3':
            export_dataset()
        elif choice == '4':
            backup_dataset()
        elif choice == '5':
            break


if __name__ == "__main__":
    main()
