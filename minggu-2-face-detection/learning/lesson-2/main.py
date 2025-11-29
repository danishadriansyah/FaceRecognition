"""
Lesson 2: Face Detection Real-Time dari Webcam

Tujuan:
- Akses webcam untuk video stream
- Face detection real-time (setiap frame)
- Optimize performance untuk video
- Display FPS counter
- Capture snapshots

Baca README.md untuk penjelasan detail!
"""

import cv2
import time
import os


def get_script_dir():
    """Get directory dimana script dijalankan"""
    return os.path.dirname(os.path.abspath(__file__))


def get_output_path(filename):
    """Get path untuk output file"""
    output_dir = os.path.join(get_script_dir(), 'output')
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, filename)


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

def detect_faces_webcam():
    """Main function untuk detect faces dari webcam"""
    
    print("="*60)
    print("LESSON 2: Face Detection Real-Time dari Webcam")
    print("="*60)
    
    # 1. Load Haar Cascade classifier
    print("\n1. Loading Haar Cascade classifier...")
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    if face_cascade.empty():
        print("❌ Error: Haar Cascade file not found!")
        return
    
    print("   ✅ Haar Cascade loaded successfully")
    
    # 2. Detect and select camera
    print("\n2. Detecting cameras...")
    available_cameras = detect_available_cameras()
    camera_id = select_camera(available_cameras)
    
    if camera_id is None:
        print("   ❌ Camera selection cancelled")
        return
    
    # 3. Open selected webcam
    print(f"\n3. Opening camera {camera_id}...")
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"   ❌ Error: Cannot open camera {camera_id}!")
        return
    
    # Get webcam properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"   ✅ Camera opened successfully")
    print(f"   Resolution: {width}x{height}")
    
    # 4. Setup variables
    prev_time = time.time()
    fps = 0
    show_fps = True
    show_count = True
    snapshot_count = 0
    
    print("\n4. Starting face detection...")
    print("\nKeyboard Controls:")
    print("   ESC   - Exit program")
    print("   SPACE - Save snapshot")
    print("   C     - Toggle face count display")
    print("   F     - Toggle FPS display")
    print("\n" + "="*60)
    
    # 5. Main detection loop
    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Error: Cannot read frame from webcam")
            break
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            # Color: hijau untuk 1 wajah, kuning untuk banyak
            color = (0, 255, 0) if len(faces) == 1 else (0, 255, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Label setiap wajah
            cv2.putText(
                frame,
                'Face',
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )
        
        # Calculate FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        
        # Display FPS (pojok kiri atas)
        if show_fps:
            cv2.putText(
                frame,
                f'FPS: {int(fps)}',
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
        
        # Display face count (pojok kanan atas)
        if show_count:
            face_text = f'Faces: {len(faces)}'
            text_size = cv2.getTextSize(
                face_text,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                2
            )[0]
            text_x = frame.shape[1] - text_size[0] - 10
            
            cv2.putText(
                frame,
                face_text,
                (text_x, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
        
        # Display instructions (pojok kiri bawah)
        cv2.putText(
            frame,
            'ESC:Exit | SPACE:Snapshot | C:Count | F:FPS',
            (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )
        
        # Show frame
        cv2.imshow('Face Detection - Lesson 2', frame)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        
        if key == 27:  # ESC - Exit
            print("\n✅ Exiting...")
            break
            
        elif key == 32:  # SPACE - Save snapshot
            snapshot_count += 1
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f'snapshot_{timestamp}.jpg'
            output_path = get_output_path(filename)
            cv2.imwrite(output_path, frame)
            print(f"📸 Snapshot {snapshot_count} saved: {filename}")
            
        elif key == ord('c') or key == ord('C'):  # Toggle face count
            show_count = not show_count
            status = "ON" if show_count else "OFF"
            print(f"Face count display: {status}")
            
        elif key == ord('f') or key == ord('F'):  # Toggle FPS
            show_fps = not show_fps
            status = "ON" if show_fps else "OFF"
            print(f"FPS display: {status}")
    
    # 5. Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    print("\n" + "="*60)
    print("✅ LESSON 2 COMPLETED!")
    print("="*60)
    print(f"\nStatistics:")
    print(f"   Snapshots saved: {snapshot_count}")
    print(f"   Final FPS: {int(fps)}")
    
    if snapshot_count > 0:
        print(f"\n📁 Snapshots saved in: {os.path.join(get_script_dir(), 'output')}/")
    
    print("\n💡 Next Steps:")
    print("   1. Try different lighting conditions")
    print("   2. Test with multiple people")
    print("   3. Experiment with parameters for better performance")
    print("   4. Move to Minggu 3 (Face Recognition)")


if __name__ == '__main__':
    detect_faces_webcam()
