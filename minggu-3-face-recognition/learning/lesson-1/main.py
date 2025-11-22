"""
Lesson 1: Face Encoding & Recognition (Gambar)
Build simple face recognition dari known faces database
Using MediaPipe (NO dlib needed!)
"""
import mediapipe as mp
import cv2
import os
import numpy as np
import sys

# Add parent path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../project'))
from face_recognizer import FaceRecognizer  # type: ignore

def main():
    print("="*60)
    print("LESSON 1: Face Encoding & Recognition (MediaPipe)")
    print("="*60)
    
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    known_faces_dir = os.path.join(script_dir, 'known_faces')
    images_dir = os.path.join(script_dir, 'images')
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize MediaPipe recognizer
    print("\n1. Initializing MediaPipe recognizer...")
    recognizer = FaceRecognizer(tolerance=0.6)
    print("   ✅ MediaPipe FaceMesh initialized")
    
    # Load known faces
    print("\n2. Loading known faces...")
    known_encodings = []
    known_names = []
    
    if not os.path.exists(known_faces_dir):
        print(f"❌ Folder 'known_faces' not found!")
        print("💡 Create folders: known_faces/alice/, known_faces/bob/")
        return
    
    for person_name in os.listdir(known_faces_dir):
        person_dir = os.path.join(known_faces_dir, person_name)
        if not os.path.isdir(person_dir):
            continue
            
        for filename in os.listdir(person_dir):
            if filename.endswith(('.jpg', '.png')):
                filepath = os.path.join(person_dir, filename)
                img = cv2.imread(filepath)
                if img is None:
                    continue
                
                # Extract encoding using MediaPipe
                encoding = recognizer.encode_face(img)
                
                if encoding is not None:
                    known_encodings.append(encoding)
                    known_names.append(person_name)
                    recognizer.add_known_face(encoding, person_name)
                    print(f"   ✅ Loaded: {person_name}/{filename}")
    
    if len(known_encodings) == 0:
        print("❌ No faces loaded!")
        return
    
    print(f"\n✅ Loaded {len(known_encodings)} face(s) from {len(set(known_names))} person(s)")
    
    # Test recognition
    print("\n3. Testing recognition...")
    test_path = os.path.join(images_dir, 'test.jpg')
    
    if not os.path.exists(test_path):
        print(f"❌ Test image not found at: {test_path}")
        return
    
    # Load and recognize
    test_img = cv2.imread(test_path)
    results = recognizer.recognize_faces_in_image(test_img)
    
    print(f"   Found {len(results)} face(s) in test image")
    
    # Recognize each face
    for result in results:
        name = result['name']
        confidence = result['confidence']
        x, y, w, h = result['bbox']
        
        # Draw rectangle and name
        cv2.rectangle(test_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.rectangle(test_img, (x, y+h-35), (x+w, y+h), (0, 255, 0), cv2.FILLED)
        label = f"{name} ({confidence*100:.1f}%)"
        cv2.putText(test_img, label, (x+6, y+h-6),
                    cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        print(f"   ✅ Recognized: {name} (confidence: {confidence*100:.1f}%)")
    
    # Save result
    output_path = os.path.join(output_dir, 'recognized.jpg')
    cv2.imwrite(output_path, test_img)
    print(f"\n✅ Result saved: {output_path}")
    
    # Show result
    cv2.imshow('Face Recognition - Press any key', test_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("\n" + "="*60)
    print("✅ LESSON 1 COMPLETED!")
    print("="*60)

if __name__ == '__main__':
    main()
