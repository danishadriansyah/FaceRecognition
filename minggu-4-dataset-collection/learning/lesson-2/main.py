"""
Lesson 2: Dataset Management & Organization
Organize captured faces into proper dataset structure
"""
import os
import json
import shutil
from datetime import datetime
import zipfile

def main():
    print("="*60)
    print("LESSON 2: Dataset Management")
    print("="*60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(script_dir, '..', 'lesson-1', 'captured_faces')
    dataset_dir = os.path.join(script_dir, 'dataset')
    backups_dir = os.path.join(script_dir, 'backups')
    
    os.makedirs(dataset_dir, exist_ok=True)
    os.makedirs(backups_dir, exist_ok=True)
    
    if not os.path.exists(source_dir):
        print("❌ No captured_faces found!")
        print("💡 Run Lesson 1 first to capture faces")
        return
    
    # Organize dataset
    print("\n1. Organizing dataset...")
    person_id = 1
    
    for person_name in os.listdir(source_dir):
        person_source = os.path.join(source_dir, person_name)
        if not os.path.isdir(person_source):
            continue
        
        # Create person folder
        person_folder = f"person_{person_id:03d}_{person_name}"
        person_dest = os.path.join(dataset_dir, person_folder)
        os.makedirs(person_dest, exist_ok=True)
        
        # Copy photos
        photo_count = 0
        for filename in os.listdir(person_source):
            if filename.endswith(('.jpg', '.png')):
                src = os.path.join(person_source, filename)
                dst = os.path.join(person_dest, f"photo_{photo_count+1:03d}.jpg")
                shutil.copy2(src, dst)
                photo_count += 1
        
        # Create metadata
        metadata = {
            "person_id": person_id,
            "name": person_name,
            "photo_count": photo_count,
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "folder": person_folder
        }
        
        metadata_path = os.path.join(person_dest, "metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"   ✅ {person_folder}: {photo_count} photos")
        person_id += 1
    
    total_persons = person_id - 1
    
    # Create backup
    print("\n2. Creating backup...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"dataset_backup_{timestamp}.zip"
    backup_path = os.path.join(backups_dir, backup_name)
    
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dataset_dir):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, dataset_dir)
                zipf.write(filepath, arcname)
    
    backup_size = os.path.getsize(backup_path) / (1024 * 1024)
    print(f"   ✅ Backup created: {backup_name} ({backup_size:.2f} MB)")
    
    # Summary
    print("\n" + "="*60)
    print("✅ DATASET ORGANIZED!")
    print("="*60)
    print(f"Total persons: {total_persons}")
    print(f"Dataset location: {dataset_dir}")
    print(f"Backup location: {backup_path}")
    
    print("\n💡 Next: Use this dataset for recognition system")

if __name__ == '__main__':
    main()
