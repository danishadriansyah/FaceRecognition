"""
Lesson 2: Real-Time Face Recognition dari Webcam
"""
import face_recognition
import cv2
import os
import numpy as np

def main():
    print("="*60)
    print("LESSON 2: Real-Time Face Recognition")
    print("="*60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    known_faces_dir = os.path.join(script_dir, 'known_faces')
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Load known faces
    print("\n1. Loading known faces...")
    known_encodings = []
    known_names = []
    
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
    
    print(f"✅ Loaded {len(known_encodings)} face(s)")
    
    # Open webcam
    print("\n2. Opening webcam...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Cannot open webcam")
        return
    
    print("✅ Webcam ready")
    print("\nControls: ESC=Exit, SPACE=Snapshot")
    
    frame_count = 0
    face_locations = []
    face_encodings_list = []
    face_names = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process every 3rd frame for speed
        if frame_count % 3 == 0:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            face_locations = face_recognition.face_locations(rgb_small, model="hog")
            face_encodings_list = face_recognition.face_encodings(rgb_small, face_locations)
            
            face_names = []
            for face_encoding in face_encodings_list:
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
                name = "Unknown"
                
                if True in matches:
                    face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_names[best_match_index]
                
                face_names.append(name)
        
        frame_count += 1
        
        # Draw results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6),
                       cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
        
        cv2.imshow('Face Recognition - ESC to exit', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key == 32:  # SPACE
            import time
            filename = f"snapshot_{int(time.time())}.jpg"
            cv2.imwrite(os.path.join(output_dir, filename), frame)
            print(f"📸 Saved: {filename}")
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n✅ LESSON 2 COMPLETED!")

if __name__ == '__main__':
    main()
