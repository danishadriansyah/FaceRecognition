"""
Lesson 2: Drawing Shapes & Webcam Basics
Interactive webcam with shapes
"""
import cv2
import os
from datetime import datetime

# Create output directory
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

print("="*60)
print("LESSON 2: Drawing Shapes & Webcam Basics")
print("="*60)

# Part 1: Drawing shapes
print("\n📝 PART 1: Drawing Shapes")
print("-"*60)

import numpy as np
canvas = np.ones((400, 600, 3), dtype=np.uint8) * 255

# Draw rectangle
cv2.rectangle(canvas, (50, 50), (250, 200), (0, 0, 255), 3)
cv2.putText(canvas, 'Rectangle', (70, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# Draw circle
cv2.circle(canvas, (450, 125), 80, (0, 255, 0), 3)
cv2.putText(canvas, 'Circle', (415, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# Draw line
cv2.line(canvas, (50, 250), (550, 250), (255, 0, 0), 3)
cv2.putText(canvas, 'Line', (270, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

# Add title
cv2.putText(canvas, 'OpenCV Shapes Demo', (150, 350), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

cv2.imwrite(f'{output_dir}/shapes.jpg', canvas)
print("   ✅ Shapes drawn and saved")

# Part 2: Webcam
print("\n📹 PART 2: Webcam Access")
print("-"*60)

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

available_cameras = detect_available_cameras()
camera_id = select_camera(available_cameras)

if camera_id is None:
    print("   ❌ Camera selection cancelled")
else:
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"   ❌ Cannot open camera {camera_id}")
    else:
        print("   ✅ Webcam opened successfully")
        print("\n🎮 Controls:")
    print("   's' - Save snapshot")
    print("   'q' - Quit")
    
    snapshot_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("   ❌ Failed to read frame")
            break
        
        # Add text overlay
        cv2.putText(frame, 'Press S to save, Q to quit', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Add rectangle overlay
        h, w = frame.shape[:2]
        cv2.rectangle(frame, (w//4, h//4), (3*w//4, 3*h//4), (0, 255, 0), 2)
        
        # Display
        cv2.imshow('Lesson 2: Webcam Demo', frame)
        
        # Keyboard controls
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("\n   👋 Quitting...")
            break
        elif key == ord('s'):
            snapshot_count += 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'{output_dir}/snapshot_{timestamp}.jpg'
            cv2.imwrite(filename, frame)
            print(f"   📸 Snapshot {snapshot_count} saved: {filename}")
    
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()

# Summary
print("\n" + "="*60)
print("✅ LESSON 2 COMPLETED!")
print("="*60)
print(f"\nOutput files saved to: {output_dir}/")
print("  - shapes.jpg")
if snapshot_count > 0:
    print(f"  - {snapshot_count} snapshot(s)")

print("\n📚 You learned:")
print("  ✅ Draw rectangles, circles, lines")
print("  ✅ Add text to images")
print("  ✅ Access webcam with VideoCapture")
print("  ✅ Read frames from webcam")
print("  ✅ Handle keyboard input")
print("  ✅ Save snapshots")

print("\n🎉 Minggu 1 completed! Ready for face detection!")
print("Next: Minggu 2 - Face Detection\n")
