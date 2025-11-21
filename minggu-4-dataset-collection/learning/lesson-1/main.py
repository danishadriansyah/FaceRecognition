"""
Lesson 1: Capture Faces dengan Quality Check
Capture wajah dari webcam dengan quality validation
"""
import cv2
import os
import numpy as np

def check_quality(face_img):
    """Check if face image has good quality"""
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

def main():
    print("="*60)
    print("LESSON 1: Capture Faces dengan Quality Check")
    print("="*60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    captured_dir = os.path.join(script_dir, 'captured_faces')
    rejected_dir = os.path.join(script_dir, 'rejected')
    os.makedirs(captured_dir, exist_ok=True)
    os.makedirs(rejected_dir, exist_ok=True)
    
    # Input person name
    person_name = input("\nEnter person name: ").strip()
    if not person_name:
        print("❌ Name cannot be empty!")
        return
    
    person_dir = os.path.join(captured_dir, person_name)
    os.makedirs(person_dir, exist_ok=True)
    
    # Load face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Cannot open webcam")
        return
    
    print(f"\n✅ Ready to capture for: {person_name}")
    print("\nInstructions:")
    print("  SPACE - Capture photo")
    print("  ESC   - Done")
    print("\n💡 Move your face: left, right, up, down")
    print("   Target: 20+ good photos\n")
    
    captured_count = 0
    rejected_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))
        
        # Draw rectangle
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Display info
        cv2.putText(frame, f"Captured: {captured_count} | Rejected: {rejected_count}",
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
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
                print("⚠️ Multiple faces detected!")
                continue
            
            x, y, w, h = faces[0]
            face_img = frame[y:y+h, x:x+w]
            
            # Quality check
            is_good, reason = check_quality(face_img)
            
            if is_good:
                filename = f"{person_name}_{captured_count+1:03d}.jpg"
                filepath = os.path.join(person_dir, filename)
                cv2.imwrite(filepath, face_img)
                captured_count += 1
                print(f"✅ Captured: {filename}")
            else:
                filename = f"rejected_{rejected_count+1:03d}.jpg"
                filepath = os.path.join(rejected_dir, filename)
                cv2.imwrite(filepath, face_img)
                rejected_count += 1
                print(f"❌ Rejected: {reason}")
    
    cap.release()
    cv2.destroyAllWindows()
    
    print("\n" + "="*60)
    print("✅ CAPTURE COMPLETED!")
    print("="*60)
    print(f"Person: {person_name}")
    print(f"Captured: {captured_count} photos")
    print(f"Rejected: {rejected_count} photos")
    print(f"\n📁 Photos saved in: {person_dir}")
    
    if captured_count < 20:
        print(f"\n⚠️ Recommended: 20+ photos (you have {captured_count})")

if __name__ == '__main__':
    main()
