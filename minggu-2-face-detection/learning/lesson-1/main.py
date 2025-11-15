"""
Lesson 1: Face Detection dengan Haar Cascade (Gambar)

Tujuan:
- Load dan gunakan Haar Cascade classifier
- Detect wajah dari gambar
- Gambar rectangle di wajah yang terdeteksi
- Save hasil detection

Baca README.md untuk penjelasan detail!
"""

import cv2
import os


def get_script_dir():
    """Get directory dimana script dijalankan"""
    return os.path.dirname(os.path.abspath(__file__))


def get_output_path(filename):
    """Get path untuk output file"""
    output_dir = os.path.join(get_script_dir(), 'output')
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, filename)


def get_input_path(filename):
    """Get path untuk input file"""
    return os.path.join(get_script_dir(), 'images', filename)


def detect_faces_image():
    """Main function untuk detect faces dari gambar"""
    
    print("="*60)
    print("LESSON 1: Face Detection dengan Haar Cascade (Gambar)")
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
    
    # 2. Load test image
    print("\n2. Loading test image...")
    input_path = get_input_path('sample.jpg')
    
    img = cv2.imread(input_path)
    
    if img is None:
        print(f"   ❌ Error: Image not found at {input_path}")
        print(f"   💡 Tip: Put your test image (with faces) as 'sample.jpg'")
        print(f"           in the 'images/' folder")
        return
    
    print(f"   ✅ Image loaded: {img.shape[1]}x{img.shape[0]} pixels")
    
    # 3. Convert to grayscale (Haar Cascade butuh grayscale)
    print("\n3. Converting to grayscale...")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print("   ✅ Converted to grayscale")
    
    # 4. Detect faces
    print("\n4. Detecting faces...")
    print("   Parameters:")
    print("   - scaleFactor: 1.1")
    print("   - minNeighbors: 5")
    print("   - minSize: (30, 30)")
    
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,      # Resize step (1.1 = 10% smaller each step)
        minNeighbors=5,       # Minimum neighbors (higher = more strict)
        minSize=(30, 30)      # Minimum face size
    )
    
    # 5. Print hasil detection
    print(f"\n   ✅ Found {len(faces)} face(s)")
    
    if len(faces) == 0:
        print("\n   ⚠️  No faces detected!")
        print("   💡 Tips:")
        print("      - Pastikan gambar ada wajah yang jelas (frontal)")
        print("      - Coba kurangi minNeighbors jadi 3")
        print("      - Coba kurangi minSize jadi (20, 20)")
        print("      - Pastikan lighting gambar bagus")
        return
    
    # 6. Draw rectangles dan print info
    print("\n5. Drawing rectangles...")
    for i, (x, y, w, h) in enumerate(faces, 1):
        # Draw rectangle (hijau, thickness 2)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Print info setiap wajah
        print(f"   Face {i}: Position ({x}, {y}), Size {w}x{h}")
        
        # Tambahkan label (opsional)
        cv2.putText(
            img,
            f'Face {i}',
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )
    
    # 7. Save hasil
    print("\n6. Saving result...")
    output_path = get_output_path('detected.jpg')
    cv2.imwrite(output_path, img)
    print(f"   ✅ Result saved to: {output_path}")
    
    # 8. Show hasil (window akan muncul)
    print("\n7. Displaying result...")
    print("   Press any key to close the window...")
    cv2.imshow('Detected Faces - Press any key to close', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("\n" + "="*60)
    print("✅ LESSON 1 COMPLETED!")
    print("="*60)
    print("\n💡 Next Steps:")
    print("   1. Try with different images")
    print("   2. Experiment with parameters (scaleFactor, minNeighbors)")
    print("   3. Try group photos (multiple faces)")
    print("   4. Move to Lesson 2 (Real-time webcam detection)")


if __name__ == '__main__':
    detect_faces_image()
