"""
Lesson 2: Real-Time Face Recognition dari Webcam
Using MediaPipe (NO dlib needed!)
"""
import cv2
import os
import numpy as np
import sys
import time

# Add parent path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../project'))
from face_recognizer import FaceRecognizer  # type: ignore

def main():
    print("="*60)
    print("LESSON 2: Real-Time Face Recognition (MediaPipe)")
    print("="*60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    known_faces_dir = os.path.join(script_dir, 'known_faces')
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize MediaPipe recognizer
    print("\n1. Initializing MediaPipe recognizer...")
    recognizer = FaceRecognizer(tolerance=0.6)
    
    # Load known faces
    print("\n2. Loading known faces...")
    known_encodings = []
    known_names = []
    
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
    
    print(f"✅ Loaded {len(known_encodings)} face(s)")
    
    # Open webcam
    print("\n3. Opening webcam...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Cannot open webcam")
        return
    
    print("✅ Webcam ready")
    print("\nControls: ESC=Exit, SPACE=Snapshot")
    
    frame_count = 0
    results = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process every 3rd frame for speed (MediaPipe sudah cepat!)
        if frame_count % 3 == 0:
            # Recognize faces in frame
            results = recognizer.recognize_faces_in_image(frame)
        
        frame_count += 1
        
        # Draw results
        for result in results:
            x, y, w, h = result['bbox']
            name = result['name']
            confidence = result['confidence']
            
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.rectangle(frame, (x, y+h-35), (x+w, y+h), color, cv2.FILLED)
            label = f"{name} ({confidence*100:.1f}%)"
            cv2.putText(frame, label, (x+6, y+h-6),
                       cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
        
        # Show FPS
        cv2.putText(frame, f"Frame: {frame_count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('Face Recognition - ESC to exit', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key == 32:  # SPACE
            filename = f"snapshot_{int(time.time())}.jpg"
            cv2.imwrite(os.path.join(output_dir, filename), frame)
            print(f"📸 Saved: {filename}")
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n✅ LESSON 2 COMPLETED!")

if __name__ == '__main__':
    main()
