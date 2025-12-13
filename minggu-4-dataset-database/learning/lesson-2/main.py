"""
Lesson 2: Generate Face Encodings (File-Based)
Generate DeepFace encodings from captured faces and save to pickle file
"""
import os
import sys
import pickle
import json
import cv2
import numpy as np
from datetime import datetime
from pathlib import Path

# Add Week 3 path for face_recognizer
week3_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'minggu-3-face-recognition', 'project')
sys.path.insert(0, week3_path)

try:
    from face_recognizer import FaceRecognizer
except ImportError:
    print("❌ Cannot import FaceRecognizer from Week 3")
    print("💡 Make sure minggu-3-face-recognition/project/face_recognizer.py exists")
    sys.exit(1)

def main():
    print("="*60)
    print("LESSON 2: Generate Face Encodings (File-Based)")
    print("="*60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    captured_dir = Path(script_dir) / '..' / 'captured_faces'
    output_dir = Path(script_dir) / '..' / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Check if we have captured faces
    if not captured_dir.exists() or not any(captured_dir.iterdir()):
        print("\n❌ No captured faces found!")
        print(f"   Looking in: {captured_dir.absolute()}")
        print("💡 Run Lesson 1 first to capture faces")
        return
    
    # Step 1: Initialize FaceRecognizer
    print("\n🔧 Step 1: Initialize FaceRecognizer")
    print("-" * 60)
    
    model_name = 'Facenet512'
    print(f"📦 Loading model: {model_name}")
    print("   This may take a few seconds...")
    
    recognizer = FaceRecognizer(model=model_name)
    print(f"✅ Model loaded: {model_name}")
    
    # Step 2: Generate encodings for all captured faces
    print("\n🔧 Step 2: Generate Face Encodings")
    print("-" * 60)
    
    encodings_data = {
        "model": model_name,
        "generated_at": datetime.now().isoformat(),
        "encodings": [],
        "names": [],
        "metadata": []
    }
    
    total_count = 0
    person_count = 0
    
    for person_dir in captured_dir.iterdir():
        if not person_dir.is_dir():
            continue
        
        person_name = person_dir.name
        person_count += 1
        
        print(f"\n👤 Processing: {person_name}")
        
        image_files = list(person_dir.glob("*.jpg")) + list(person_dir.glob("*.png"))
        
        if not image_files:
            print(f"   ⚠️  No images found")
            continue
        
        print(f"   📸 Found {len(image_files)} images")
        
        person_encodings = 0
        for img_file in image_files:
            try:
                # Load image
                image = cv2.imread(str(img_file))
                if image is None:
                    print(f"      ⚠️  {img_file.name}: Cannot read")
                    continue
                
                # Generate encoding
                encoding = recognizer.encode_face(image)
                
                if encoding is not None:
                    encodings_data["encodings"].append(encoding.tolist())
                    encodings_data["names"].append(person_name)
                    encodings_data["metadata"].append({
                        "person_name": person_name,
                        "image_file": img_file.name,
                        "image_path": str(img_file.relative_to(captured_dir)),
                        "encoded_at": datetime.now().isoformat()
                    })
                    person_encodings += 1
                    total_count += 1
                    print(f"      ✅ {img_file.name}")
                else:
                    print(f"      ⚠️  {img_file.name}: No face detected")
                
            except Exception as e:
                print(f"      ❌ {img_file.name}: {e}")
        
        print(f"   ✅ Generated {person_encodings} encodings for {person_name}")
    
    # Step 3: Save encodings to pickle file
    print(f"\n💾 Step 3: Save Encodings")
    print("-" * 60)
    
    if total_count == 0:
        print("❌ No encodings generated!")
        return
    
    # Save pickle
    encodings_file = output_dir / "face_encodings.pkl"
    with open(encodings_file, 'wb') as f:
        pickle.dump(encodings_data, f)
    
    print(f"✅ Saved {total_count} encodings to pickle")
    print(f"   File: {encodings_file}")
    print(f"   Size: {encodings_file.stat().st_size / 1024:.1f} KB")
    
    # Save metadata JSON
    metadata_file = output_dir / "encodings_metadata.json"
    metadata_summary = {
        "model": encodings_data["model"],
        "generated_at": encodings_data["generated_at"],
        "total_persons": person_count,
        "total_encodings": total_count,
        "persons": {}
    }
    
    # Group by person
    for name, meta in zip(encodings_data["names"], encodings_data["metadata"]):
        if name not in metadata_summary["persons"]:
            metadata_summary["persons"][name] = {
                "name": name,
                "encoding_count": 0,
                "images": []
            }
        metadata_summary["persons"][name]["encoding_count"] += 1
        metadata_summary["persons"][name]["images"].append(meta["image_file"])
    
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata_summary, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved metadata to JSON")
    print(f"   File: {metadata_file}")
    
    # Step 4: Summary
    print(f"\n📊 Summary")
    print("-" * 60)
    print(f"✅ Total persons: {person_count}")
    print(f"✅ Total encodings: {total_count}")
    print(f"✅ Average encodings per person: {total_count/person_count:.1f}")
    print(f"\n💾 Output files:")
    print(f"   - {encodings_file.name} (pickle)")
    print(f"   - {metadata_file.name} (JSON)")
    
    # Test load
    print(f"\n🧪 Step 5: Test Loading Encodings")
    print("-" * 60)
    
    with open(encodings_file, 'rb') as f:
        loaded_data = pickle.load(f)
    
    print(f"✅ Successfully loaded encodings")
    print(f"   Model: {loaded_data['model']}")
    print(f"   Encodings: {len(loaded_data['encodings'])}")
    print(f"   Names: {len(loaded_data['names'])}")
    print(f"   Encoding shape: {np.array(loaded_data['encodings'][0]).shape}")
    
    print("\n" + "="*60)
    print("✅ LESSON 2 COMPLETE!")
    print("="*60)
    print("\n💡 Next Steps:")
    print("   1. These encodings will be used in Week 5 for recognition")
    print("   2. You can copy this file to Week 5 project/dataset folder")
    print("   3. Or generate encodings directly using DatasetManager")

if __name__ == "__main__":
    main()
