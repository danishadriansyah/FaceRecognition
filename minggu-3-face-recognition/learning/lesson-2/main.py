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

def detect_available_cameras(max_cameras=5):
    """Detect available cameras"""
    available_cameras = []
    print("\n🔍 Detecting available cameras...")
    for camera_id in range(max_cameras):
        cap = cv2.VideoCapture(camera_id)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                backend = cap.getBackendName()
                name = "Built-in Webcam / Default Camera" if camera_id == 0 else ("External USB Camera / Secondary Camera" if camera_id == 1 else f"Camera Device {camera_id}")
                camera_info = {'id': camera_id, 'name': name, 'resolution': f"{width}x{height}", 'fps': fps, 'backend': backend}
                available_cameras.append(camera_info)
                print(f"  ✅ Camera {camera_id}: {name}")
                print(f"     Resolution: {width}x{height} | FPS: {fps} | Backend: {backend}")
            cap.release()
        else:
            break
    return available_cameras

def select_camera(available_cameras):
    """Let user select camera"""
    if len(available_cameras) == 0:
        print("\n❌ No cameras detected!")
        return None
    if len(available_cameras) == 1:
        cam = available_cameras[0]
        print(f"\n✅ Found 1 camera: {cam['name']}")
        confirm = input(f"Use this camera? (y/n): ").strip().lower()
        return cam['id'] if confirm == 'y' else None
    print(f"\n📹 Found {len(available_cameras)} cameras:")
    for cam in available_cameras:
        print(f"  [{cam['id']}] {cam['name']} - {cam['resolution']} @ {cam['fps']}fps")
    while True:
        try:
            choice = int(input(f"\nSelect camera [0-{max([c['id'] for c in available_cameras])}]: ").strip())
            selected = next((c for c in available_cameras if c['id'] == choice), None)
            if selected:
                print(f"✅ Selected: {selected['name']}")
                return choice
            print(f"❌ Camera {choice} not available")
        except (ValueError, KeyboardInterrupt):
            return None

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
    
    # Detect and select camera
    available_cameras = detect_available_cameras()
    camera_id = select_camera(available_cameras)
    
    if camera_id is None:
        print("❌ Camera selection cancelled")
        return
    
    # Open webcam
    print(f"\n3. Opening camera {camera_id}...")
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"❌ Cannot open camera {camera_id}")
        return
    
    print("✅ Camera ready")
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
