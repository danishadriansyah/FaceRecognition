"""
📝 TUGAS MINGGU 3 - Face Recognition System (Fill in the Blanks)
Total: 8 soal

Import face_recognizer module dari ../project/
"""

import cv2
import sys
import os
import pickle

# Add project folder to path
sys.path.append('../project')

# SOAL 1: Import FaceRecognizer class
# Hint: from face_recognizer import ...
from face_recognizer import _____________

# Initialize recognizer
recognizer = FaceRecognizer()


def load_known_faces():
    """Load database dari file pickle"""
    if os.path.exists('encodings.pkl'):
        # SOAL 2: Load pickle file
        # Hint: pickle.load() dengan mode 'rb'
        with open('encodings.pkl', '__') as f:
            data = _______.load(f)
            
        for name, encoding in data.items():
            recognizer.add_known_face(name, encoding)
        
        print(f"✅ Loaded {len(data)} known faces")
    else:
        print("⚠️ No database found")


def save_known_faces():
    """Save database ke pickle file"""
    stats = recognizer.get_statistics()
    known_faces = stats['known_faces']
    
    # SOAL 3: Save dengan pickle
    # Hint: pickle.dump() dengan mode 'wb'
    with open('encodings.pkl', '__') as f:
        _______.dump(known_faces, f)
    
    print(f"💾 Database saved ({len(known_faces)} faces)")


def register_person():
    """Register new person ke database"""
    print("\n👤 REGISTER NEW PERSON")
    name = input("Nama: ")
    
    # SOAL 4: Buka webcam untuk capture
    # Hint: cv2.VideoCapture(0)
    cap = ______________(0)
    
    print("Tekan SPACE untuk capture, ESC untuk cancel")
    
    while True:
        ret, frame = cap.read()
        cv2.imshow('Capture Face', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        # SOAL 5: Capture saat tekan SPACE (ord(' '))
        if key == ord('_'):
            # Encode face
            encoding = recognizer.encode_face(frame)
            
            if encoding is not None:
                recognizer.add_known_face(name, encoding)
                print(f"✅ {name} registered!")
                
                # Save database
                save_known_faces()
                break
            else:
                print("❌ No face detected, try again")
        
        elif key == 27:  # ESC
            print("❌ Cancelled")
            break
    
    cap.release()
    cv2.destroyAllWindows()


def recognize_image():
    """Recognize faces dari image file"""
    print("\n🖼️ RECOGNIZE FROM IMAGE")
    filename = input("Path to image: ")
    
    # SOAL 6: Load image
    # Hint: cv2.imread()
    img = _________(filename)
    
    if img is None:
        print("❌ File not found!")
        return
    
    # Recognize all faces
    results = recognizer.recognize_faces_in_image(img)
    
    print(f"\n✅ Found {len(results)} faces:")
    
    # Draw results
    for result in results:
        x, y, w, h = result['bbox']
        name = result['name']
        conf = result['confidence']
        
        # SOAL 7: Draw rectangle (hijau jika known, merah jika unknown)
        # Hint: (0, 255, 0) = hijau, (0, 0, 255) = merah
        color = (0, 255, 0) if name != 'Unknown' else (0, 0, ___)
        
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
        
        label = f"{name} ({conf:.1f}%)"
        cv2.putText(img, label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        print(f"   - {name} ({conf:.1f}%)")
    
    # Save result
    output_path = f"output/recognized_{os.path.basename(filename)}"
    cv2.imwrite(output_path, img)
    print(f"\n💾 Saved to {output_path}")
    
    # Show result
    cv2.imshow('Recognition Result', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def webcam_recognition():
    """Real-time recognition dari webcam"""
    print("\n📹 WEBCAM RECOGNITION")
    print("Press 'q' to quit")
    
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # SOAL 8: Recognize faces di frame
        # Hint: recognizer.recognize_faces_in_image()
        results = recognizer._______________________(frame)
        
        # Draw results
        for result in results:
            x, y, w, h = result['bbox']
            name = result['name']
            conf = result['confidence']
            
            color = (0, 255, 0) if name != 'Unknown' else (0, 0, 255)
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            label = f"{name} ({conf:.1f}%)"
            cv2.putText(frame, label, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        cv2.imshow('Webcam Recognition', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


def main():
    """Main program"""
    os.makedirs('output', exist_ok=True)
    
    # Load database
    load_known_faces()
    
    print("="*40)
    print("   FACE RECOGNITION SYSTEM")
    print("="*40)
    
    while True:
        stats = recognizer.get_statistics()
        print(f"\nDatabase: {stats['total_faces']} persons")
        
        print("\nMain Menu:")
        print("1. Register New Person")
        print("2. Recognize from Image")
        print("3. Recognize from Webcam")
        print("4. Exit")
        
        choice = input("\nPilih: ")
        
        if choice == '1':
            register_person()
        elif choice == '2':
            recognize_image()
        elif choice == '3':
            webcam_recognition()
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    main()
