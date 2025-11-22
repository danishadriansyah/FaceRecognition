"""
📝 TUGAS MINGGU 2 - Multi-Face Detector (Fill in the Blanks)

Lengkapi program ini dengan mengisi bagian yang kosong!
Total: 10 soal
"""

import cv2
import os
from datetime import datetime

# SOAL 1: Load Haar Cascade classifier
# Hint: cv2.CascadeClassifier() dengan path haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + '_______________________________________'
)

def detect_faces(image):
    """
    Detect faces dalam image
    Return: list of face rectangles (x, y, w, h)
    """
    # SOAL 2: Convert ke grayscale
    # Hint: cv2.cvtColor dengan COLOR_BGR2GRAY
    gray = cv2.cvtColor(image, _________________)
    
    # SOAL 3: Detect faces menggunakan detectMultiScale
    # Hint: Parameters: (gray, scaleFactor, minNeighbors)
    # Gunakan 1.1 untuk scaleFactor, 5 untuk minNeighbors
    faces = face_cascade._____________________(gray, _____, _____)
    
    return faces


def draw_faces(image, faces):
    """Draw rectangles dan labels pada wajah yang terdeteksi"""
    for i, (x, y, w, h) in enumerate(faces, 1):
        # SOAL 4: Draw rectangle di sekitar wajah
        # Hint: cv2.rectangle(image, (x,y), (x+w,y+h), color, thickness)
        # Gunakan warna hijau (0, 255, 0) dan thickness 2
        cv2.rectangle(image, (x, y), (_____, _____), (0, 255, 0), 2)
        
        # SOAL 5: Tambahkan label nomor wajah
        # Hint: cv2.putText dengan text f'Face {i}'
        cv2.putText(image, f'Face {i}', (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    return image


def image_mode():
    """Mode deteksi dari single image"""
    print("\n📸 IMAGE MODE")
    filename = input("Nama file (di folder input_images/): ")
    
    # SOAL 6: Load image
    # Hint: cv2.imread() dengan path
    img = _________(f'input_images/{filename}')
    
    if img is None:
        print("❌ File tidak ditemukan!")
        return
    
    # Detect faces
    faces = detect_faces(img)
    print(f"✅ Terdeteksi {len(faces)} wajah")
    
    # Draw rectangles
    result = draw_faces(img.copy(), faces)
    
    # SOAL 7: Save hasil detection
    # Hint: cv2.imwrite() ke folder output/
    output_path = f'output/detected_{filename}'
    _________(output_path, result)
    
    print(f"💾 Hasil disimpan: {output_path}")
    
    # Show result
    cv2.imshow('Detection Result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def webcam_mode():
    """Mode deteksi real-time dari webcam"""
    print("\n📹 WEBCAM MODE")
    print("Tekan 's' untuk screenshot, 'q' untuk quit")
    
    # SOAL 8: Buka webcam
    # Hint: cv2.VideoCapture(0) untuk default webcam
    cap = _________(0)
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect faces
        faces = detect_faces(frame)
        
        # Draw rectangles
        result = draw_faces(frame, faces)
        
        # Display face count
        cv2.putText(result, f'Faces: {len(faces)}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('Webcam Face Detection', result)
        
        key = cv2.waitKey(1) & 0xFF
        
        # SOAL 9: Save screenshot saat tekan 's'
        # Hint: Cek if key == ord('s')
        if key == ord('_'):
            screenshot_name = f'output/webcam_{frame_count}.jpg'
            cv2.imwrite(screenshot_name, result)
            print(f"📸 Screenshot saved: {screenshot_name}")
            frame_count += 1
        elif key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


def batch_mode():
    """Mode batch processing multiple images"""
    print("\n📂 BATCH MODE")
    
    if not os.path.exists('input_images'):
        print("❌ Folder input_images/ tidak ditemukan!")
        return
    
    results = []
    total_faces = 0
    
    # Process semua file di folder
    files = [f for f in os.listdir('input_images') if f.endswith(('.jpg', '.png', '.jpeg'))]
    
    for filename in files:
        img = cv2.imread(f'input_images/{filename}')
        
        if img is None:
            continue
        
        # Detect faces
        faces = detect_faces(img)
        face_count = len(faces)
        total_faces += face_count
        
        # Draw and save
        result = draw_faces(img, faces)
        cv2.imwrite(f'output/batch_{filename}', result)
        
        results.append({
            'filename': filename,
            'faces': face_count
        })
        
        print(f"✅ {filename}: {face_count} wajah")
    
    # Generate report
    generate_report(results, total_faces)


def generate_report(results, total_faces):
    """Generate text report"""
    report_path = 'output/report.txt'
    
    # SOAL 10: Buka file untuk write
    # Hint: open() dengan mode 'w'
    with _______('output/report.txt', '_') as f:
        f.write("FACE DETECTION REPORT\n")
        f.write("=" * 40 + "\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Mode: Batch Processing\n\n")
        
        f.write("Results:\n")
        f.write("-" * 40 + "\n")
        for r in results:
            f.write(f"{r['filename']}: {r['faces']} wajah\n")
        
        f.write("\nStatistics:\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total images: {len(results)}\n")
        f.write(f"Total faces: {total_faces}\n")
        if len(results) > 0:
            avg = total_faces / len(results)
            f.write(f"Average: {avg:.1f} wajah/image\n")
    
    print(f"\n📄 Report saved: {report_path}")


def main():
    """Main program"""
    # Pastikan folder output exists
    if not os.path.exists('output'):
        os.makedirs('output')
    
    print("="*40)
    print("   MULTI-FACE DETECTOR")
    print("="*40)
    
    while True:
        print("\nMode:")
        print("1. Image Mode (single)")
        print("2. Webcam Mode (real-time)")
        print("3. Batch Mode (multiple)")
        print("4. Exit")
        
        choice = input("\nPilih: ")
        
        if choice == '1':
            image_mode()
        elif choice == '2':
            webcam_mode()
        elif choice == '3':
            batch_mode()
        elif choice == '4':
            print("👋 Terima kasih!")
            break
        else:
            print("❌ Pilihan tidak valid!")


if __name__ == "__main__":
    main()
