"""
Camera Helper - Detect and Select Available Cameras
Copy functions ini ke script yang pakai webcam
"""
import cv2

def detect_available_cameras(max_cameras=5):
    """Detect available cameras and return list of camera info"""
    available_cameras = []
    
    print("\n🔍 Detecting available cameras...")
    for camera_id in range(max_cameras):
        cap = cv2.VideoCapture(camera_id)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                # Get camera properties
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                backend = cap.getBackendName()
                
                # Common camera types
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
                print(f"     Resolution: {width}x{height} | FPS: {fps} | Backend: {backend}")
            cap.release()
        else:
            break
    
    return available_cameras

def select_camera(available_cameras):
    """Let user select camera from available options"""
    if len(available_cameras) == 0:
        print("\n❌ No cameras detected!")
        print("💡 Troubleshooting:")
        print("   1. Check if webcam is connected")
        print("   2. Close other apps using the camera (Zoom, Teams, etc.)")
        print("   3. Try reconnecting USB camera")
        return None
    
    if len(available_cameras) == 1:
        cam = available_cameras[0]
        print(f"\n✅ Found 1 camera:")
        print(f"   [{cam['id']}] {cam['name']}")
        print(f"       {cam['resolution']} @ {cam['fps']}fps")
        
        while True:
            confirm = input(f"\nUse this camera? (y/n): ").strip().lower()
            if confirm == 'y':
                print(f"✅ Selected: {cam['name']}")
                return cam['id']
            elif confirm == 'n':
                print("❌ Camera selection cancelled")
                return None
    
    print(f"\n📹 Found {len(available_cameras)} cameras:")
    for cam in available_cameras:
        print(f"  [{cam['id']}] {cam['name']}")
        print(f"      {cam['resolution']} @ {cam['fps']}fps | Backend: {cam['backend']}")
    
    while True:
        try:
            choice = input(f"\nSelect camera number [0-{max([c['id'] for c in available_cameras])}]: ").strip()
            camera_id = int(choice)
            
            selected = next((c for c in available_cameras if c['id'] == camera_id), None)
            if selected:
                print(f"✅ Selected: {selected['name']}")
                return camera_id
            else:
                available_ids = [c['id'] for c in available_cameras]
                print(f"❌ Camera {camera_id} not available. Choose from: {available_ids}")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n❌ Camera selection cancelled")
            return None
