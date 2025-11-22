"""
Lesson 2: Real-Time Face Recognition dari Webcam
Menggunakan MediaPipe FaceMesh untuk fast & accurate recognition
"""
import cv2
import os
import numpy as np
import sys
import time

# Add parent path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../project'))
from face_recognizer import FaceRecognizer

def main():
    print("="*70)
    print("LESSON 2: Real-Time Face Recognition (MediaPipe Webcam)")
    print("="*70)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    known_faces_dir = os.path.join(script_dir, 'known_faces')
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize recognizer
    print("\n1️⃣  Initializing recognizer...")
    recognizer = FaceRecognizer(tolerance=0.5)
    print("   ✅ FaceRecognizer ready")
    
    # Load known faces
    print("\n2️⃣  Loading known faces...")
    known_encodings = []
    known_names = []
    
    if not os.path.exists(known_faces_dir):
        print(f"   ❌ Folder '{known_faces_dir}' tidak ada!")
        return
    
    total_loaded = 0
    for person_name in os.listdir(known_faces_dir):
        person_dir = os.path.join(known_faces_dir, person_name)
        if not os.path.isdir(person_dir):
            continue
            
        person_faces = 0
        for filename in os.listdir(person_dir):
            if not filename.endswith(('.jpg', '.png', '.jpeg')):
                continue
                
            filepath = os.path.join(person_dir, filename)
            img = cv2.imread(filepath)
            if img is None:
                continue
            
            encoding = recognizer.encode_face(img)
            if encoding is not None:
                known_encodings.append(encoding)
                known_names.append(person_name)
                recognizer.add_known_face(encoding, person_name)
                person_faces += 1
                total_loaded += 1
        
        if person_faces > 0:
            print(f"   ✅ {person_name}: {person_faces} face(s)")
    
    if total_loaded == 0:
        print("   ❌ Tidak ada face yang di-load!")
        return
    
    print(f"   📊 Total loaded: {total_loaded} faces")
    
    # Open webcam
    print("\n3️⃣  Opening webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("   ❌ Tidak bisa akses webcam!")
        print("   💡 Pastikan:")
        print("      - Webcam terpasang")
        print("      - Webcam tidak digunakan aplikasi lain")
        print("      - Permission untuk camera sudah diberikan")
        return
    
    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("   ✅ Webcam ready")
    print("\n" + "="*70)
    print("🎮 LIVE RECOGNITION")
    print("="*70)
    print("\n📺 Controls:")
    print("   SPACE: Capture screenshot")
    print("   ESC or 'Q': Exit")
    print("\n" + "-"*70)
    
    frame_count = 0
    fps_start = time.time()
    fps_count = 0
    current_fps = 0
    
    cached_results = []
    cache_interval = 3  # Detect every 3 frames for speed
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("   ❌ Failed to read frame")
            break
        
        # Process every Nth frame for efficiency
        if frame_count % cache_interval == 0:
            cached_results = recognizer.recognize_faces_in_image(frame)
        
        frame_count += 1
        fps_count += 1
        
        # Calculate FPS
        elapsed = time.time() - fps_start
        if elapsed >= 1.0:
            current_fps = fps_count / elapsed
            fps_start = time.time()
            fps_count = 0
        
        # Draw results
        for result in cached_results:
            x, y, w, h = result['bbox']
            name = result['name']
            confidence = result['confidence']
            
            # Choose color based on match
            if name != "Unknown":
                color = (0, 255, 0)  # Green for known
                thickness = 2
            else:
                color = (0, 0, 255)  # Red for unknown
                thickness = 1
            
            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, thickness)
            
            # Draw label background
            label_height = 30
            cv2.rectangle(frame, (x, y+h-label_height), (x+w, y+h), color, cv2.FILLED)
            
            # Draw label text
            label = f"{name} {confidence*100:.0f}%"
            cv2.putText(frame, label, (x+5, y+h-8),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Draw statistics overlay
        cv2.putText(frame, f"FPS: {current_fps:.1f}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Faces: {len(cached_results)}", (10, 65),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Frame: {frame_count}", (10, 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw instruction at bottom
        cv2.putText(frame, "SPACE=Capture | ESC=Exit", (10, frame.shape[0]-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        cv2.imshow('Real-Time Face Recognition (MediaPipe)', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):  # ESC or Q
            print("\n👋 Exiting...")
            break
        elif key == 32:  # SPACE
            filename = f"capture_{int(time.time())}.jpg"
            filepath = os.path.join(output_dir, filename)
            cv2.imwrite(filepath, frame)
            
            matched = sum(1 for r in cached_results if r['name'] != 'Unknown')
            unknown = len(cached_results) - matched
            print(f"   📸 Captured: {filename}")
            print(f"      - Faces: {len(cached_results)} (Matched: {matched}, Unknown: {unknown})")
    
    cap.release()
    cv2.destroyAllWindows()
    
    print("\n" + "="*70)
    print("✅ LESSON 2 COMPLETED!")
    print("="*70)
    print("\n📚 What you learned:")
    print("   ✅ Real-time face detection menggunakan MediaPipe")
    print("   ✅ Frame caching untuk performa optimal")
    print("   ✅ FPS calculation dan monitoring")
    print("   ✅ Live recognition dengan confidence scores")
    print("   ✅ Snapshot capture dari live stream")
    
    print(f"\n📊 Session statistics:")
    print(f"   - Total frames processed: {frame_count}")
    print(f"   - Output folder: {output_dir}")
    
    print("\n🚀 Next: Lesson 3 (Advanced) - Multi-person detection & tracking\n")

if __name__ == '__main__':
    main()
