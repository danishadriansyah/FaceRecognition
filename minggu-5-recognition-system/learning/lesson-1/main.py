"""Lesson 1: Build Complete Recognition Pipeline (MediaPipe)"""
import cv2
import pickle
import os
import sys

# Add parent path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../project'))
from face_recognizer import FaceRecognizer

def main():
    print("="*60)
    print("LESSON 1: Recognition Pipeline (MediaPipe)")
    print("="*60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(script_dir, 'dataset')
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize MediaPipe recognizer
    print("\n1. Initializing MediaPipe recognizer...")
    recognizer = FaceRecognizer()
    print("   ✅ MediaPipe initialized")
    
    # Load dataset and generate encodings
    print("\n2. Loading dataset and generating encodings...")
    encodings = []
    names = []
    
    for person_folder in os.listdir(dataset_dir):
        person_path = os.path.join(dataset_dir, person_folder)
        if not os.path.isdir(person_path):
            continue
        
        person_name = person_folder.split('_')[-1]  # Get name from folder
        
        for photo in os.listdir(person_path):
            if photo.endswith(('.jpg', '.png')):
                photo_path = os.path.join(person_path, photo)
                img = cv2.imread(photo_path)
                if img is None:
                    continue
                
                # Extract encoding using MediaPipe
                encoding = recognizer.encode_face(img)
                
                if encoding is not None:
                    encodings.append(encoding)
                    names.append(person_name)
                    recognizer.add_known_face(encoding, person_name)
                    print(f"   ✅ {person_name}: {photo}")
    
    print(f"\n✅ Generated {len(encodings)} encodings for {len(set(names))} persons")
    
    # Save recognizer database
    print("\n3. Saving recognition database...")
    db_path = os.path.join(output_dir, 'face_database.pkl')
    recognizer.save_database(db_path)
    print(f"   ✅ Database saved: {db_path}")
    
    # Also save legacy format for compatibility
    data = {"encodings": encodings, "names": names}
    legacy_path = os.path.join(output_dir, 'encodings.pkl')
    with open(legacy_path, 'wb') as f:
        pickle.dump(data, f)
    print(f"   ✅ Legacy format saved: {legacy_path}")
    
    print("\n✅ PIPELINE READY! Use face_database.pkl for recognition")

if __name__ == '__main__':
    main()
