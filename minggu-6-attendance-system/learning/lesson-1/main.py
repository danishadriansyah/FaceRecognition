"""
Lesson 1: Attendance Logic & Real-time Tracking (File-Based)
Real-time attendance check-in with webcam + face recognition
Using MediaPipe for fast detection and recognition
"""
import os
import sys
import cv2
import time
import pickle
import json
from pathlib import Path
import mediapipe as mp
import numpy as np

# Add Week 6 project modules
project_path = os.path.join(os.path.dirname(__file__), '..', '..', 'project')
sys.path.insert(0, project_path)

from attendance_system import AttendanceSystem

def generate_encodings_from_dataset(dataset_path, output_path, model_name='MediaPipe'):
    """Generate face encodings from dataset folder using MediaPipe"""
    dataset_path = Path(dataset_path)
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize MediaPipe Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.3
    )
    
    all_encodings = []
    all_names = []
    metadata = {'persons': [], 'total_images': 0}
    
    # Iterate through person folders
    person_folders = [f for f in dataset_path.iterdir() if f.is_dir()]
    
    if not person_folders:
        print(f"❌ No person folders found in {dataset_path}")
        return False
    
    for person_folder in person_folders:
        person_name = person_folder.name
        image_files = list(person_folder.glob('*.jpg')) + list(person_folder.glob('*.png'))
        
        if not image_files:
            continue
        
        print(f"\n👤 Processing: {person_name}")
        print(f"   Images: {len(image_files)}")
        
        person_encodings = []
        
        for idx, img_file in enumerate(image_files, 1):
            try:
                start = time.time()
                
                # Load and process image
                image = cv2.imread(str(img_file))
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # Get face landmarks
                results = face_mesh.process(rgb_image)
                
                if results.multi_face_landmarks:
                    # Extract landmarks as encoding
                    face_landmarks = results.multi_face_landmarks[0]
                    encoding = []
                    for landmark in face_landmarks.landmark:
                        encoding.extend([landmark.x, landmark.y, landmark.z])
                    
                    encoding = np.array(encoding)
                    all_encodings.append(encoding)
                    all_names.append(person_name)
                    person_encodings.append(encoding)
                    
                    elapsed = time.time() - start
                    print(f"   [{idx}/{len(image_files)}] ✅ {img_file.name} ({elapsed:.2f}s)")
                else:
                    print(f"   [{idx}/{len(image_files)}] ❌ {img_file.name} - No face detected")
                
            except Exception as e:
                print(f"   [{idx}/{len(image_files)}] ❌ {img_file.name} - {str(e)[:50]}")
        
        # Add to metadata
        if person_encodings:
            metadata['persons'].append({
                'name': person_name,
                'encoding_count': len(person_encodings),
                'image_count': len(image_files)
            })
    
    face_mesh.close()
    
    # Save encodings and metadata
    metadata['total_images'] = len(all_encodings)
    metadata['model'] = model_name
    
    encodings_file = output_path / 'encodings.pkl'
    metadata_file = output_path / 'metadata.json'
    
    with open(encodings_file, 'wb') as f:
        pickle.dump({'encodings': all_encodings, 'names': all_names}, f)
    
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✅ Encodings generated!")
    print(f"   Total persons: {len(metadata['persons'])}")
    print(f"   Total encodings: {len(all_encodings)}")
    print(f"   Saved to: {encodings_file}")
    
    return True

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
                    'fps': fps
                }
                available_cameras.append(camera_info)
                print(f"  ✅ Camera {camera_id}: {name}")
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
        return available_cameras[0]['id']
    
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
        print("Invalid choice!")

def main():
    print("="*60)
    print("LESSON 1: Attendance Logic & Real-time Tracking (File-Based)")
    print("="*60)
    
    # Setup paths
    script_dir = Path(__file__).parent
    dataset_path = script_dir / 'dataset'
    log_dir = script_dir / 'output'
    encodings_file = log_dir / 'encodings.pkl'
    
    # Check if encodings exist
    if not encodings_file.exists():
        print("\n⚠️  No encodings found!")
        print("   Generate encodings dari dataset? (Y/n)")
        choice = input(">> ").strip().lower()
        
        if choice != 'n':
            print("\n🔄 Generating encodings from dataset...")
            print("   This may take 1-2 minutes depending on dataset size\n")
            
            if not generate_encodings_from_dataset(str(dataset_path), str(log_dir)):
                print("\n❌ Failed to generate encodings")
                return
        else:
            print("\n💡 Cannot proceed without encodings!")
            print("   Run: python -c \"from __main__ import generate_encodings_from_dataset; generate_encodings_from_dataset('dataset', 'output')\"")
            return
    
    # Step 1: Initialize Attendance System
    print("\n📊 Step 1: Initialize Attendance System")
    print("-" * 60)
    
    try:
        attendance_system = AttendanceSystem(
            dataset_path=str(dataset_path),
            log_dir=str(log_dir)
        )
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check encodings.pkl exists in output/")
        print("   2. Run: python -c \"from __main__ import generate_encodings_from_dataset; generate_encodings_from_dataset('dataset', 'output')\"")
        return
    
    # Step 2: Check loaded encodings
    print("\n📊 Step 2: Loaded Data")
    print("-" * 60)
    
    stats = attendance_system.recognition.get_statistics()
    print(f"Known persons: {stats['known_persons']}")
    print(f"Known encodings: {stats['known_encodings']}")
    
    if stats['known_encodings'] == 0:
        print("\n❌ No encodings loaded!")
        print("💡 Dataset setup belum lengkap. Run setup_week6.py dulu!")
        print("   cd ../.. && python setup_week6.py")
        return
    
    # Step 3: Show Today's Statistics
    print("\n📊 Step 3: Today's Statistics")
    print("-" * 60)
    
    today_records = attendance_system.get_today_attendance()
    print(f"Total records today: {len(today_records)}")
    
    if today_records:
        print("\nToday's attendance:")
        for record in today_records:
            print(f"  {record['time']} - {record['person_name']} ({record['type']})")
    else:
        print("  No attendance records yet today")
    
    # Step 4: Real-time Check-in
    print("\n📊 Step 4: Real-time Attendance Check-in")
    print("-" * 60)
    print("\n🎥 Opening webcam for automatic check-in...")
    print("📌 How it works:")
    print("   1. Face detected → Recognized")
    print("   2. Press SPACE to record attendance")
    print("   3. Duplicate prevention (one check-in per day)")
    print("   4. Photos saved automatically")
    print("\n💡 Press 'q' to quit\n")
    
    input("Press ENTER to start real-time check-in...")
    
    # Detect and select camera
    available_cameras = detect_available_cameras()
    camera_id = select_camera(available_cameras)
    
    if camera_id is None:
        print("❌ No camera available")
        return
    
    # Run attendance system
    try:
        attendance_system.process_camera_attendance(
            camera_id=camera_id,
            mode='check_in'
        )
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 5: Final Statistics
    print("\n📊 Step 5: Final Statistics")
    print("-" * 60)
    
    today_records = attendance_system.get_today_attendance()
    print(f"Total records: {len(today_records)}")
    
    check_ins = [r for r in today_records if r['type'] == 'check_in']
    check_outs = [r for r in today_records if r['type'] == 'check_out']
    
    print(f"Check-ins: {len(check_ins)}")
    print(f"Check-outs: {len(check_outs)}")
    
    print("\n" + "="*60)
    print("✅ LESSON 1 COMPLETE!")
    print("="*60)
    print("\n💡 Next Steps:")
    print("   1. Check output folder for attendance.csv")
    print("   2. Check output/photos for captured images")
    print("   3. Continue to Lesson 2 (Reports & Analytics)")

if __name__ == "__main__":
    main()
