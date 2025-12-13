"""
Reusable Camera Capture Library
Untuk digunakan oleh setup scripts week 4-7
"""
import cv2
import os
import numpy as np
from pathlib import Path

def check_quality(face_img):
    """Check if face image has good quality"""
    try:
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        
        # 1. Check brightness
        brightness = np.mean(gray)
        if brightness < 40 or brightness > 220:
            return False, f"Bad brightness: {brightness:.1f}"
        
        # 2. Check sharpness (blur detection)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        if laplacian_var < 100:
            return False, f"Too blurry: {laplacian_var:.1f}"
        
        # 3. Check size
        if face_img.shape[0] < 100 or face_img.shape[1] < 100:
            return False, f"Too small: {face_img.shape}"
        
        return True, "OK"
    except Exception as e:
        return False, str(e)

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
                
                if camera_id == 0:
                    name = "Built-in Webcam / Default Camera"
                elif camera_id == 1:
                    name = "External USB Camera / Secondary Camera"
                else:
                    name = f"Camera Device {camera_id}"
                
                camera_info = {
                    'id': camera_id,
                    'name': name,
                    'resolution': f"{width}x{height}",
                    'fps': fps,
                    'backend': backend
                }
                available_cameras.append(camera_info)
                print(f"  ✅ Camera {camera_id}: {name}")
                print(f"     {width}x{height} @ {fps}fps")
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
        return cam['id']
    
    print(f"\n📹 Found {len(available_cameras)} cameras:")
    for cam in available_cameras:
        print(f"  [{cam['id']}] {cam['name']} - {cam['resolution']}")
    
    while True:
        try:
            choice = int(input(f"\nSelect camera (0-{len(available_cameras)-1}): "))
            if 0 <= choice < len(available_cameras):
                return choice
        except ValueError:
            pass
        print("❌ Invalid choice!")

def capture_faces_interactive(dataset_path, target_count=20):
    """
    Interactive face capture with quality check
    
    Args:
        dataset_path: Path to dataset folder
        target_count: Target number of photos
    
    Returns:
        dict with capture results
    """
    dataset_path = Path(dataset_path)
    dataset_path.mkdir(parents=True, exist_ok=True)
    
    results = {
        'persons': {},
        'total_captured': 0,
        'total_rejected': 0
    }
    
    # Detect and select camera
    available_cameras = detect_available_cameras()
    camera_id = select_camera(available_cameras)
    
    if camera_id is None:
        return results
    
    # Load face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    print(f"\n🎥 Opening camera {camera_id}...")
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"❌ Cannot open camera {camera_id}")
        return results
    
    # Capture multiple persons
    while True:
        person_name = input("\n👤 Enter person name (or 'q' to finish): ").strip()
        if person_name.lower() == 'q':
            break
        
        if not person_name:
            print("❌ Name cannot be empty!")
            continue
        
        person_dir = dataset_path / person_name
        person_dir.mkdir(exist_ok=True)
        
        print(f"\n✅ Capturing for: {person_name}")
        print("Instructions:")
        print("  SPACE - Capture photo")
        print("  ESC   - Next person (or finish)\n")
        print("💡 Move your face: left, right, up, down\n")
        
        captured_count = 0
        rejected_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))
            
            # Draw rectangles
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Display info
            cv2.putText(frame, f"Captured: {captured_count} | Rejected: {rejected_count}",
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Person: {person_name}",
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame, "SPACE=Capture | ESC=Done",
                       (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow('Capture Faces', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == 27:  # ESC
                break
            elif key == 32:  # SPACE
                if len(faces) == 0:
                    print("⚠️ No face detected!")
                    continue
                
                if len(faces) > 1:
                    print("⚠️ Multiple faces detected! Keep only yourself in frame.")
                    continue
                
                x, y, w, h = faces[0]
                face_img = frame[y:y+h, x:x+w]
                
                # Quality check
                is_good, reason = check_quality(face_img)
                
                if is_good:
                    filename = f"{person_name}_{captured_count+1:03d}.jpg"
                    filepath = person_dir / filename
                    cv2.imwrite(str(filepath), face_img)
                    captured_count += 1
                    print(f"✅ Captured: {filename}")
                else:
                    rejected_count += 1
                    print(f"❌ Rejected: {reason}")
        
        results['persons'][person_name] = {
            'captured': captured_count,
            'rejected': rejected_count
        }
        results['total_captured'] += captured_count
        results['total_rejected'] += rejected_count
        
        print(f"\n📊 {person_name}: {captured_count} captured, {rejected_count} rejected")
    
    cap.release()
    cv2.destroyAllWindows()
    
    return results
