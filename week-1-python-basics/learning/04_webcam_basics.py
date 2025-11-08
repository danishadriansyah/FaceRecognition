"""
Minggu 1 - File 4: Webcam Basics
Konsep: Akses webcam, capture frame, real-time video processing

Tujuan:
- Membuka dan mengakses webcam
- Capture frame by frame
- Display real-time video
- Save snapshot dari webcam
- FPS calculation

Author: AI Face Recognition Learning Project
"""

import cv2
import numpy as np
import os
from datetime import datetime

def test_webcam():
    """Test apakah webcam bisa diakses"""
    
    print("\n" + "="*50)
    print("TESTING WEBCAM")
    print("="*50)
    
    # Try different camera indices
    for i in range(3):
        print(f"\n🔍 Trying camera index {i}...")
        cap = cv2.VideoCapture(i)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✅ Camera {i} is working!")
                print(f"   Resolution: {frame.shape[1]}x{frame.shape[0]}")
                cap.release()
                return i
            else:
                print(f"⚠️  Camera {i} opened but can't read frame")
        else:
            print(f"❌ Camera {i} not available")
        
        cap.release()
    
    print("\n❌ No working camera found!")
    return None


def basic_webcam_demo(camera_index=0):
    """Demonstrasi dasar webcam"""
    
    print("\n" + "="*50)
    print("BASIC WEBCAM DEMO")
    print("="*50)
    
    # Open webcam
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("❌ Error: Cannot open camera")
        return
    
    # Set resolution (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Get actual resolution
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print(f"✅ Webcam opened successfully")
    print(f"📺 Resolution: {width}x{height}")
    print(f"🎬 FPS: {fps}")
    print("\n⌨️  Controls:")
    print("   - Press 'q' or ESC to quit")
    print("   - Press 's' to save snapshot")
    print("   - Press 'i' for info")
    
    snapshot_count = 0
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Error: Can't receive frame")
            break
        
        # Display info on frame
        cv2.putText(frame, "Press 'q' to quit, 's' to save", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Display frame
        cv2.imshow('Webcam - Basic Demo', frame)
        
        # Wait for key press
        key = cv2.waitKey(1) & 0xFF
        
        # Quit
        if key == ord('q') or key == 27:
            print("\n👋 Exiting...")
            break
        
        # Save snapshot
        elif key == ord('s'):
            os.makedirs("output", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output/snapshot_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            snapshot_count += 1
            print(f"📸 Snapshot saved: {filename}")
        
        # Info
        elif key == ord('i'):
            print(f"\n📊 Frame Info:")
            print(f"   Shape: {frame.shape}")
            print(f"   Size: {frame.nbytes} bytes")
            print(f"   Snapshots taken: {snapshot_count}")
    
    # Release webcam
    cap.release()
    cv2.destroyAllWindows()
    print(f"\n✅ Total snapshots: {snapshot_count}")


def fps_counter_demo(camera_index=0):
    """Demonstrasi dengan FPS counter"""
    
    print("\n" + "="*50)
    print("FPS COUNTER DEMO")
    print("="*50)
    
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("❌ Error: Cannot open camera")
        return
    
    print("✅ Webcam opened")
    print("⌨️  Press 'q' to quit")
    
    # Variables untuk FPS calculation
    import time
    prev_time = time.time()
    fps_display = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Calculate FPS
        current_time = time.time()
        time_diff = current_time - prev_time
        
        if time_diff > 0:
            fps_display = 1.0 / time_diff
        
        prev_time = current_time
        
        # Display FPS on frame
        cv2.putText(frame, f"FPS: {fps_display:.2f}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Draw a rectangle for FPS background
        cv2.rectangle(frame, (5, 5), (200, 50), (0, 0, 0), -1)
        cv2.putText(frame, f"FPS: {fps_display:.2f}", (10, 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('Webcam - FPS Counter', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


def effects_demo(camera_index=0):
    """Demonstrasi berbagai efek real-time"""
    
    print("\n" + "="*50)
    print("REAL-TIME EFFECTS DEMO")
    print("="*50)
    
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("❌ Error: Cannot open camera")
        return
    
    print("✅ Webcam opened")
    print("\n⌨️  Controls:")
    print("   - Press '1': Normal")
    print("   - Press '2': Grayscale")
    print("   - Press '3': Blur")
    print("   - Press '4': Edge Detection")
    print("   - Press '5': Negative")
    print("   - Press 'q': Quit")
    
    current_effect = 1
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Apply effect based on current selection
        if current_effect == 1:
            # Normal
            display_frame = frame.copy()
            effect_name = "Normal"
        
        elif current_effect == 2:
            # Grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            display_frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            effect_name = "Grayscale"
        
        elif current_effect == 3:
            # Blur
            display_frame = cv2.GaussianBlur(frame, (15, 15), 0)
            effect_name = "Blur"
        
        elif current_effect == 4:
            # Edge Detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            display_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            effect_name = "Edge Detection"
        
        elif current_effect == 5:
            # Negative
            display_frame = 255 - frame
            effect_name = "Negative"
        
        # Display effect name
        cv2.rectangle(display_frame, (5, 5), (300, 50), (0, 0, 0), -1)
        cv2.putText(display_frame, f"Effect: {effect_name}", (10, 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Instructions
        cv2.putText(display_frame, "Press 1-5 for effects, 'q' to quit", (10, 470),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow('Webcam - Effects Demo', display_frame)
        
        # Key controls
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
            current_effect = int(chr(key))
            print(f"🎨 Effect changed to: {effect_name}")
    
    cap.release()
    cv2.destroyAllWindows()


def mirror_mode_demo(camera_index=0):
    """Demonstrasi mirror mode"""
    
    print("\n" + "="*50)
    print("MIRROR MODE DEMO")
    print("="*50)
    
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("❌ Error: Cannot open camera")
        return
    
    print("✅ Webcam opened")
    print("⌨️  Press 'm' to toggle mirror, 'q' to quit")
    
    mirror_mode = True
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Apply mirror if enabled
        if mirror_mode:
            frame = cv2.flip(frame, 1)
            mode_text = "Mirror: ON"
        else:
            mode_text = "Mirror: OFF"
        
        # Display mode
        cv2.rectangle(frame, (5, 5), (200, 50), (0, 0, 0), -1)
        cv2.putText(frame, mode_text, (10, 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        cv2.imshow('Webcam - Mirror Mode', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('m'):
            mirror_mode = not mirror_mode
            print(f"🪞 Mirror mode: {'ON' if mirror_mode else 'OFF'}")
    
    cap.release()
    cv2.destroyAllWindows()


def main():
    """Main program"""
    
    print("="*50)
    print("WEBCAM BASICS DEMO - Minggu 1")
    print("="*50)
    
    # Test webcam
    camera_index = test_webcam()
    
    if camera_index is None:
        print("\n❌ No camera available. Cannot continue.")
        print("💡 Make sure your webcam is connected and not used by another app")
        return
    
    print(f"\n✅ Using camera index: {camera_index}\n")
    
    while True:
        print("\n" + "="*50)
        print("PILIH DEMO:")
        print("="*50)
        print("1. Basic Webcam Demo")
        print("2. FPS Counter Demo")
        print("3. Real-time Effects Demo")
        print("4. Mirror Mode Demo")
        print("5. Run All Demos")
        print("0. Exit")
        print("="*50)
        
        choice = input("\nPilih (0-5): ").strip()
        
        if choice == '1':
            basic_webcam_demo(camera_index)
        elif choice == '2':
            fps_counter_demo(camera_index)
        elif choice == '3':
            effects_demo(camera_index)
        elif choice == '4':
            mirror_mode_demo(camera_index)
        elif choice == '5':
            basic_webcam_demo(camera_index)
            fps_counter_demo(camera_index)
            effects_demo(camera_index)
            mirror_mode_demo(camera_index)
        elif choice == '0':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")


# ======================================
# KONSEP PENTING
# ======================================
"""
1. VIDEO CAPTURE:
   - cv2.VideoCapture(index): Open camera (0 = default camera)
   - cap.read(): Returns (ret, frame)
   - cap.isOpened(): Check if camera is open
   - cap.release(): Close camera

2. CAMERA PROPERTIES:
   - CAP_PROP_FRAME_WIDTH: Frame width
   - CAP_PROP_FRAME_HEIGHT: Frame height
   - CAP_PROP_FPS: Frames per second
   - CAP_PROP_BRIGHTNESS, CONTRAST, etc.
   - Use cap.get() to read, cap.set() to write

3. FRAME PROCESSING:
   - Each frame is a numpy array (like image)
   - Can apply all image operations on frames
   - Process in real-time loop

4. FPS CALCULATION:
   - fps = 1 / time_between_frames
   - Use time.time() for timing

5. BEST PRACTICES:
   - Always check ret before using frame
   - Always release camera when done
   - Use cv2.destroyAllWindows() to close windows
   - Mirror webcam for natural feeling (flip horizontal)
"""


# ======================================
# LATIHAN
# ======================================
"""
💪 LATIHAN:

1. Tambahkan recording video feature (save to video file)
   Hint: cv2.VideoWriter()

2. Buat auto-capture setiap 5 detik

3. Tambahkan zoom in/out feature
   Hint: Crop center dan resize

4. Buat split screen (4 effects sekaligus)

5. Tambahkan brightness/contrast adjustment dengan keyboard

BONUS CHALLENGE:
Buat photo booth app:
- Countdown timer sebelum capture
- Multiple filters
- Auto-save dengan timestamp
- Display gallery of captured photos
"""


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main()
