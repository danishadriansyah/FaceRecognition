"""
Lesson 1: Face Encoding & Recognition (Gambar)
Build simple face recognition dari known faces database
"""
import face_recognition
import cv2
import os
import numpy as np

def main():
    print("="*60)
    print("LESSON 1: Face Encoding & Recognition")
    print("="*60)
    
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    known_faces_dir = os.path.join(script_dir, 'known_faces')
    images_dir = os.path.join(script_dir, 'images')
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Load known faces
    print("\n1. Loading known faces...")
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
                img = face_recognition.load_image_file(filepath)
                encodings = face_recognition.face_encodings(img)
                
                if len(encodings) > 0:
                    known_encodings.append(encodings[0])
                    known_names.append(person_name)
                    print(f"   ✅ Loaded: {person_name}/{filename}")
    
    if len(known_encodings) == 0:
        print("❌ No faces loaded!")
        return
    
    print(f"\n✅ Loaded {len(known_encodings)} face(s) from {len(set(known_names))} person(s)")
    
    # Test recognition
    print("\n2. Testing recognition...")
    test_path = os.path.join(images_dir, 'test.jpg')
    
    if not os.path.exists(test_path):
        print(f"❌ Test image not found at: {test_path}")
        return
    
    # Load and recognize
    test_img = face_recognition.load_image_file(test_path)
    test_img_cv = cv2.cvtColor(test_img, cv2.COLOR_RGB2BGR)
    test_encodings = face_recognition.face_encodings(test_img)
    face_locations = face_recognition.face_locations(test_img)
    
    print(f"   Found {len(test_encodings)} face(s) in test image")
    
    # Recognize each face
    for (top, right, bottom, left), face_encoding in zip(face_locations, test_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
        name = "Unknown"
        confidence = 0
        
        if True in matches:
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]
                confidence = (1 - face_distances[best_match_index]) * 100
        
        # Draw rectangle and name
        cv2.rectangle(test_img_cv, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(test_img_cv, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(test_img_cv, f"{name} ({confidence:.1f}%)", (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        print(f"   ✅ Recognized: {name} (confidence: {confidence:.1f}%)")
    
    # Save result
    output_path = os.path.join(output_dir, 'recognized.jpg')
    cv2.imwrite(output_path, test_img_cv)
    print(f"\n✅ Result saved: {output_path}")
    
    # Show result
    cv2.imshow('Face Recognition - Press any key', test_img_cv)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("\n" + "="*60)
    print("✅ LESSON 1 COMPLETED!")
    print("="*60)

if __name__ == '__main__':
    main()
