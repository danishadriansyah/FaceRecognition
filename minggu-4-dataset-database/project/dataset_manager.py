"""
Dataset Manager Module (File-Based Version)
Week 4 Project Module - Progressive Web Application

This module manages face dataset collection and organization using FILES.
Stores data in local filesystem with JSON metadata and pickle encodings.
Builds on Week 2's face_detector.py and Week 3's face_recognizer.py.
"""

import cv2
import numpy as np
import os
import sys
import pickle
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path

# Add Week 2 and Week 3 paths
week2_path = os.path.join(os.path.dirname(__file__), '..', '..', 'minggu-2-face-detection', 'project')
week3_path = os.path.join(os.path.dirname(__file__), '..', '..', 'minggu-3-face-recognition', 'project')
sys.path.insert(0, week2_path)
sys.path.insert(0, week3_path)

try:
    from face_detector import FaceDetector
    from face_recognizer import FaceRecognizer
except ImportError:
    print("⚠️  Warning: Could not import face_detector or face_recognizer")
    FaceDetector = None
    FaceRecognizer = None


class DatasetManager:
    """
    Manage face datasets for recognition system using local files
    """
    
    def __init__(self, dataset_path: str = "dataset"):
        """
        Initialize dataset manager with local file storage
        
        Args:
            dataset_path: Path to dataset folder (default: "dataset")
        """
        self.dataset_path = Path(dataset_path)
        self.dataset_path.mkdir(parents=True, exist_ok=True)
        
        # Metadata file
        self.metadata_file = self.dataset_path / "metadata.json"
        self.encodings_file = self.dataset_path / "encodings.pkl"
        
        # Load existing metadata
        self.metadata = self._load_metadata()
        
        print("✅ DatasetManager initialized (File-based mode)")
        print(f"   Dataset path: {self.dataset_path.absolute()}")
    
    def _load_metadata(self) -> Dict:
        """Load metadata from JSON file"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"persons": {}, "created_at": datetime.now().isoformat()}
    
    def _save_metadata(self):
        """Save metadata to JSON file"""
        self.metadata["updated_at"] = datetime.now().isoformat()
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
    
    def add_person(self, name: str, employee_id: str = None, 
                   department: str = None) -> str:
        """
        Add a new person to dataset
        
        Args:
            name: Person's name
            employee_id: Employee ID (optional)
            department: Department (optional)
            
        Returns:
            Person ID (folder name)
        """
        # Create person ID (safe folder name)
        person_id = name.lower().replace(' ', '_')
        
        # Create person folder
        person_folder = self.dataset_path / person_id
        person_folder.mkdir(parents=True, exist_ok=True)
        
        # Add to metadata
        self.metadata["persons"][person_id] = {
            "name": name,
            "employee_id": employee_id,
            "department": department,
            "created_at": datetime.now().isoformat(),
            "image_count": 0,
            "encoding_count": 0
        }
        self._save_metadata()
        
        print(f"✅ Person added: {name} (ID: {person_id})")
        if employee_id:
            print(f"   Employee ID: {employee_id}")
        if department:
            print(f"   Department: {department}")
        print(f"   Folder: {person_folder}")
        
        return person_id
    
    def capture_faces(self, person_id: str, target_count: int = 20, 
                     camera_id: int = 0) -> int:
        """
        Capture faces from webcam for a person
        
        Args:
            person_id: Person ID (folder name)
            target_count: Number of photos to capture
            camera_id: Camera device ID
            
        Returns:
            Number of photos captured
        """
        if person_id not in self.metadata["persons"]:
            raise ValueError(f"Person '{person_id}' not found. Use add_person() first.")
        
        person_folder = self.dataset_path / person_id
        
        # Initialize detector
        if FaceDetector is None:
            raise ImportError("FaceDetector not available. Check Week 2 module.")
        
        detector = FaceDetector()
        
        # Open camera
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open camera {camera_id}")
        
        captured = 0
        print(f"\n📸 Capturing faces for {self.metadata['persons'][person_id]['name']}")
        print(f"   Target: {target_count} photos")
        print(f"   Press SPACE to capture, 'q' to quit\n")
        
        while captured < target_count:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detect faces
            faces = detector.detect_faces(frame)
            
            # Draw boxes
            display = frame.copy()
            for (x, y, w, h) in faces:
                cv2.rectangle(display, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Show count
            cv2.putText(display, f"Captured: {captured}/{target_count}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(display, "SPACE: Capture | Q: Quit", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Capture Faces', display)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' '):  # Space to capture
                if len(faces) == 1:
                    # Save image
                    filename = f"{person_id}_{captured+1:03d}.jpg"
                    filepath = person_folder / filename
                    cv2.imwrite(str(filepath), frame)
                    captured += 1
                    print(f"   ✅ Captured {captured}/{target_count}: {filename}")
                elif len(faces) == 0:
                    print(f"   ⚠️  No face detected!")
                else:
                    print(f"   ⚠️  Multiple faces detected ({len(faces)})")
            
            elif key == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Update metadata
        self.metadata["persons"][person_id]["image_count"] = captured
        self._save_metadata()
        
        print(f"\n✅ Capture complete: {captured} photos saved")
        return captured
    
    def generate_encodings(self, model_name: str = 'Facenet512') -> int:
        """
        Generate face encodings for all persons and save to pickle
        
        Args:
            model_name: DeepFace model name
            
        Returns:
            Total number of encodings generated
        """
        if FaceRecognizer is None:
            raise ImportError("FaceRecognizer not available. Check Week 3 module.")
        
        recognizer = FaceRecognizer(model=model_name)
        
        encodings_data = {
            "model": model_name,
            "generated_at": datetime.now().isoformat(),
            "encodings": [],
            "names": [],
            "metadata": []
        }
        
        total_count = 0
        
        print(f"\n🔧 Generating encodings with {model_name}...")
        
        for person_id, person_info in self.metadata["persons"].items():
            person_folder = self.dataset_path / person_id
            
            if not person_folder.exists():
                continue
            
            image_files = list(person_folder.glob("*.jpg")) + list(person_folder.glob("*.png"))
            
            if not image_files:
                print(f"   ⚠️  {person_info['name']}: No images found")
                continue
            
            print(f"\n   👤 {person_info['name']} ({len(image_files)} images)")
            
            person_encodings = 0
            for img_file in image_files:
                try:
                    # Load image
                    image = cv2.imread(str(img_file))
                    if image is None:
                        continue
                    
                    # Generate encoding
                    encoding = recognizer.encode_face(image)
                    
                    if encoding is not None:
                        encodings_data["encodings"].append(encoding)
                        encodings_data["names"].append(person_info["name"])
                        encodings_data["metadata"].append({
                            "person_id": person_id,
                            "employee_id": person_info.get("employee_id"),
                            "department": person_info.get("department"),
                            "image_file": img_file.name
                        })
                        person_encodings += 1
                        total_count += 1
                        print(f"      ✅ {img_file.name}")
                    
                except Exception as e:
                    print(f"      ⚠️  {img_file.name}: {e}")
            
            # Update metadata
            self.metadata["persons"][person_id]["encoding_count"] = person_encodings
            print(f"   ✅ Generated {person_encodings} encodings")
        
        # Save encodings to pickle
        with open(self.encodings_file, 'wb') as f:
            pickle.dump(encodings_data, f)
        
        self._save_metadata()
        
        print(f"\n✅ Total encodings generated: {total_count}")
        print(f"   Saved to: {self.encodings_file}")
        
        return total_count
    
    def load_encodings(self) -> Tuple[List, List, List]:
        """
        Load encodings from pickle file
        
        Returns:
            Tuple of (encodings, names, metadata)
        """
        if not self.encodings_file.exists():
            print("⚠️  No encodings file found. Run generate_encodings() first.")
            return [], [], []
        
        with open(self.encodings_file, 'rb') as f:
            data = pickle.load(f)
        
        print(f"✅ Loaded {len(data['encodings'])} encodings")
        print(f"   Model: {data['model']}")
        print(f"   Generated: {data['generated_at']}")
        
        return data["encodings"], data["names"], data["metadata"]
    
    def get_person_list(self) -> List[Dict]:
        """Get list of all persons in dataset"""
        persons = []
        for person_id, info in self.metadata["persons"].items():
            persons.append({
                "person_id": person_id,
                **info
            })
        return persons
    
    def get_statistics(self) -> Dict:
        """Get dataset statistics"""
        total_persons = len(self.metadata["persons"])
        total_images = sum(p.get("image_count", 0) for p in self.metadata["persons"].values())
        total_encodings = sum(p.get("encoding_count", 0) for p in self.metadata["persons"].values())
        
        return {
            "total_persons": total_persons,
            "total_images": total_images,
            "total_encodings": total_encodings,
            "dataset_path": str(self.dataset_path.absolute()),
            "has_encodings": self.encodings_file.exists()
        }
    
    def export_metadata(self, output_file: str = None) -> str:
        """Export dataset metadata to JSON"""
        if output_file is None:
            output_file = self.dataset_path / "dataset_export.json"
        else:
            output_file = Path(output_file)
        
        export_data = {
            "dataset_path": str(self.dataset_path.absolute()),
            "exported_at": datetime.now().isoformat(),
            "statistics": self.get_statistics(),
            "persons": self.metadata["persons"]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Metadata exported to: {output_file}")
        return str(output_file)


# Example usage
if __name__ == "__main__":
    print("Dataset Manager Module - Week 4 Project (File-Based)")
    print("="*50)
    
    # Initialize
    manager = DatasetManager(dataset_path="test_dataset")
    
    # Show commands
    print("\n💡 Available commands:")
    print("   manager.add_person('Alice', 'EMP001', 'IT')")
    print("   manager.capture_faces('alice', target_count=20)")
    print("   manager.generate_encodings()")
    print("   encodings, names, metadata = manager.load_encodings()")
    print("   manager.get_person_list()")
    print("   manager.get_statistics()")
    print("   manager.export_metadata()")
