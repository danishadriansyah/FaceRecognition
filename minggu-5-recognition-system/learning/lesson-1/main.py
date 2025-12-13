"""
Lesson 1: Hybrid Approach Introduction
Generate face encodings from database using DeepFace
"""
import os
import sys
from pathlib import Path
import pickle
import json
from deepface import DeepFace
import time

def generate_encodings_from_dataset(dataset_path, output_path, model_name='Facenet512'):
    """Generate face encodings from dataset folder"""
    from pathlib import Path
    import cv2
    
    dataset_path = Path(dataset_path)
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    all_encodings = []
    all_names = []
    metadata = {'persons': [], 'total_images': 0}
    
    # Iterate through person folders
    person_folders = [f for f in dataset_path.iterdir() if f.is_dir()]
    
    for person_folder in person_folders:
        person_name = person_folder.name
        image_files = list(person_folder.glob('*.jpg')) + list(person_folder.glob('*.png'))
        
        if not image_files:
            continue
        
        print(f"\n👤 Processing: {person_name}")
        print(f"   Images: {len(image_files)}")
        
        person_encodings = []
        
        for img_file in image_files:
            try:
                # Generate encoding using DeepFace
                start = time.time()
                embedding = DeepFace.represent(
                    img_path=str(img_file),
                    model_name=model_name,
                    enforce_detection=False
                )
                
                encoding = embedding[0]['embedding']
                person_encodings.append(encoding)
                elapsed = (time.time() - start) * 1000
                
                print(f"   ✅ {img_file.name}: {len(encoding)}D vector ({elapsed:.0f}ms)")
                
            except Exception as e:
                print(f"   ❌ {img_file.name}: {e}")
        
        if person_encodings:
            all_encodings.extend(person_encodings)
            all_names.extend([person_name] * len(person_encodings))
            
            metadata['persons'].append({
                'name': person_name,
                'image_count': len(person_encodings),
                'encoding_count': len(person_encodings)
            })
            metadata['total_images'] += len(person_encodings)
    
    # Save to pickle
    import pickle
    encodings_file = output_path / 'encodings.pkl'
    with open(encodings_file, 'wb') as f:
        pickle.dump({
            'encodings': all_encodings,
            'names': all_names
        }, f)
    
    # Save metadata
    metadata_file = output_path / 'metadata.json'
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return len(all_encodings), encodings_file, metadata_file

def main():
    print("="*60)
    print("LESSON 1: Generate Face Encodings (File-Based)")
    print("="*60)
    
    # Setup paths
    script_dir = Path(__file__).parent
    dataset_path = script_dir / 'dataset'
    output_path = script_dir / 'output'
    
    # Step 1: Check dataset
    print("\n📊 Step 1: Check Dataset")
    print("-" * 60)
    
    if not dataset_path.exists():
        print(f"❌ Dataset not found: {dataset_path}")
        print("\n💡 Create dataset structure:")
        print("   dataset/")
        print("     person1/")
        print("       image_001.jpg")
        print("       image_002.jpg")
        print("     person2/")
        print("       image_001.jpg")
        return
    
    person_folders = [f for f in dataset_path.iterdir() if f.is_dir()]
    if not person_folders:
        print(f"❌ No person folders found in {dataset_path}")
        return
    
    print(f"✅ Found {len(person_folders)} persons in dataset")
    for folder in person_folders:
        images = list(folder.glob('*.jpg')) + list(folder.glob('*.png'))
        print(f"   - {folder.name}: {len(images)} images")
    
    # Step 2: Initialize DeepFace
    print("\n📊 Step 2: Initialize DeepFace")
    print("-" * 60)
    
    try:
        # Test DeepFace model loading
        print("   Loading Facenet512 model...")
        DeepFace.build_model('Facenet512')
        print("   ✅ DeepFace ready (512-dimensional encodings)")
    except Exception as e:
        print(f"   ❌ Failed to initialize DeepFace: {e}")
        print("\n💡 Install dependencies:")
        print("   pip install deepface==0.0.89")
        print("   pip install tensorflow==2.15.0")
        return
    
    # Step 3: Generate encodings
    print("\n📊 Step 3: Generate Face Encodings")
    print("-" * 60)
    
    start_time = time.time()
    
    try:
        total_encodings, encodings_file, metadata_file = generate_encodings_from_dataset(
            dataset_path=dataset_path,
            output_path=output_path,
            model_name='Facenet512'
        )
        
        elapsed = time.time() - start_time
        
        print("\n" + "="*60)
        print("✅ ENCODING GENERATION COMPLETE")
        print("="*60)
        print(f"Total encodings: {total_encodings}")
        print(f"Time elapsed: {elapsed:.1f}s")
        print(f"\nOutput files:")
        print(f"   📄 {encodings_file}")
        print(f"   📄 {metadata_file}")
        
        # Performance info
        print("\n📊 Performance Comparison")
        print("-" * 60)
        print("Method                 | Detection | Recognition | Total   | Real-time?")
        print("-" * 60)
        print("MediaPipe only (Week 3)| 10-15ms   | N/A         | 10-15ms | ✅ 30+ FPS")
        print("DeepFace only          | 150-200ms | 100-150ms   | 250-350ms| ❌ 3-4 FPS")
        print("Hybrid (Week 5)        | 10-15ms   | 100-150ms   | 110-165ms| ✅ 6-9 FPS")
        print("-" * 60)
        
        print("\n💡 Hybrid Advantage:")
        print("   - 2x faster than pure DeepFace")
        print("   - 97%+ accuracy vs 85% MediaPipe-only")
        print("   - Real-time capable (6-9 FPS)")
        print("   - Production-ready accuracy")
        
        print("\n💡 Next: Run Lesson 2 for real-time recognition")
        
    except Exception as e:
        print(f"\n❌ Encoding generation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
