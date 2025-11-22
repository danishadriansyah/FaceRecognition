"""
Lesson 1: Face Recognition dari Static Image
Menggunakan MediaPipe FaceMesh untuk encoding yang akurat
"""
import cv2
import os
import numpy as np
import sys

# Add project path for imports
project_dir = os.path.join(os.path.dirname(__file__), '../../project')
sys.path.insert(0, project_dir)
from face_recognizer import FaceRecognizer  # type: ignore

def main():
    print("="*70)
    print("LESSON 1: Face Recognition dari Static Image (MediaPipe FaceMesh)")
    print("="*70)
    
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    known_faces_dir = os.path.join(script_dir, 'known_faces')
    images_dir = os.path.join(script_dir, 'images')
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize recognizer
    print("\n1️⃣  Initializing MediaPipe Face Recognizer...")
    recognizer = FaceRecognizer(tolerance=0.5)
    print("   ✅ FaceRecognizer ready (tolerance: 0.5)")
    print("   📊 Using 468-dimensional FaceMesh landmarks as encoding\n")
    
    # Load known faces
    print("2️⃣  Loading known faces...")
    known_encodings = []
    known_names = []
    
    if not os.path.exists(known_faces_dir):
        print(f"   ❌ Folder '{known_faces_dir}' tidak ada!")
        print("   💡 Buat struktur:")
        print("      known_faces/")
        print("      ├── alice/")
        print("      │   ├── alice1.jpg")
        print("      │   └── alice2.jpg")
        print("      └── bob/")
        print("          ├── bob1.jpg")
        print("          └── bob2.jpg")
        return
    
    person_count = 0
    for person_name in os.listdir(known_faces_dir):
        person_dir = os.path.join(known_faces_dir, person_name)
        if not os.path.isdir(person_dir):
            continue
        
        person_count += 1
        face_count = 0
        
        for filename in os.listdir(person_dir):
            if not filename.endswith(('.jpg', '.png', '.jpeg')):
                continue
                
            filepath = os.path.join(person_dir, filename)
            img = cv2.imread(filepath)
            
            if img is None:
                print(f"   ⚠️  Tidak bisa baca: {filename}")
                continue
            
            # Extract encoding
            encoding = recognizer.encode_face(img)
            
            if encoding is not None:
                known_encodings.append(encoding)
                known_names.append(person_name)
                recognizer.add_known_face(encoding, person_name)
                face_count += 1
        
        print(f"   ✅ {person_name}: {face_count} face(s) loaded")
    
    if len(known_encodings) == 0:
        print("   ❌ Tidak ada face yang berhasil di-load!")
        return
    
    print(f"\n   📊 Total: {len(known_encodings)} face(s) dari {person_count} person(s)")
    
    # Test recognition
    print("\n3️⃣  Testing recognition...")
    test_path = os.path.join(images_dir, 'test.jpg')
    
    if not os.path.exists(test_path):
        print(f"   ❌ Test image tidak ada: {test_path}")
        print("   💡 Letakkan test image di folder 'images/'")
        return
    
    # Load and recognize
    test_img = cv2.imread(test_path)
    print(f"   📷 Image loaded: {test_img.shape[1]}x{test_img.shape[0]} pixels")
    
    results = recognizer.recognize_faces_in_image(test_img)
    print(f"   🔍 Found {len(results)} face(s) in test image\n")
    
    # Process and display results
    if len(results) == 0:
        print("   ❌ Tidak ada wajah terdeteksi!")
    else:
        for i, result in enumerate(results, 1):
            name = result['name']
            confidence = result['confidence']
            x, y, w, h = result['bbox']
            
            # Draw bounding box
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(test_img, (x, y), (x+w, y+h), color, 2)
            
            # Draw label background
            cv2.rectangle(test_img, (x, y+h-35), (x+w, y+h), color, cv2.FILLED)
            
            # Add label text
            label = f"{name} ({confidence*100:.1f}%)"
            cv2.putText(test_img, label, (x+6, y+h-6),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
            
            status = "✅ MATCHED" if name != "Unknown" else "❓ UNKNOWN"
            print(f"   Face #{i}: {name} (confidence: {confidence*100:.1f}%) {status}")
    
    # Save result
    output_path = os.path.join(output_dir, 'recognized.jpg')
    cv2.imwrite(output_path, test_img)
    print(f"\n✅ Result saved: {output_path}")
    
    # Show result
    cv2.imshow('Face Recognition Result (Press any key)', test_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Statistics
    print("\n" + "="*70)
    print("LESSON 1 COMPLETED!")
    print("="*70)
    print("\n📚 What you learned:")
    print("   ✅ MediaPipe FaceMesh untuk face encoding (468 landmarks)")
    print("   ✅ Load multiple faces dari known_faces database")
    print("   ✅ Extract face encoding dengan cosine similarity")
    print("   ✅ Match wajah dengan confidence score")
    print("   ✅ Visualisasi hasil recognition dengan bounding boxes")
    
    print("\n📊 Statistics:")
    print(f"   - Known faces: {len(known_encodings)}")
    print(f"   - Test image faces detected: {len(results)}")
    print(f"   - Matched faces: {sum(1 for r in results if r['name'] != 'Unknown')}")
    print(f"   - Unknown faces: {sum(1 for r in results if r['name'] == 'Unknown')}")
    
    print("\n🚀 Next: Lesson 2 - Real-time webcam recognition\n")

if __name__ == '__main__':
    main()
