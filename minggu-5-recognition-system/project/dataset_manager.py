"""
Dataset Manager Module
Week 4 Project Module - Progressive Web Application

This module manages face dataset collection and organization.
Builds on Week 2's face_detector.py and Week 3's face_recognizer.py.
"""

import cv2
import numpy as np
import os
import json
import pickle
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path


class DatasetManager:
    """
    Manage face datasets for recognition system
    """
    
    def __init__(self, dataset_root: str = "dataset"):
        """
        Initialize dataset manager
        
        Args:
            dataset_root: Root directory for dataset storage
        """
        self.dataset_root = Path(dataset_root)
        self.dataset_root.mkdir(parents=True, exist_ok=True)
        
        self.metadata_file = self.dataset_root / "metadata.json"
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        """Load dataset metadata"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {'people': {}, 'created_at': datetime.now().isoformat()}
    
    def _save_metadata(self):
        """Save dataset metadata"""
        self.metadata['updated_at'] = datetime.now().isoformat()
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def add_person(self, name: str, employee_id: str = None, 
                   department: str = None, metadata: Dict = None) -> str:
        """
        Add a new person to dataset
        
        Args:
            name: Person's name
            employee_id: Employee ID
            department: Department
            metadata: Additional metadata
            
        Returns:
            Person ID (directory name)
        """
        # Create safe directory name
        person_id = name.lower().replace(' ', '_')
        person_dir = self.dataset_root / person_id
        person_dir.mkdir(parents=True, exist_ok=True)
        
        # Store metadata
        person_data = {
            'name': name,
            'employee_id': employee_id,
            'department': department,
            'created_at': datetime.now().isoformat(),
            'image_count': 0,
            'metadata': metadata or {}
        }
        
        self.metadata['people'][person_id] = person_data
        self._save_metadata()
        
        return person_id
    
    def capture_face(self, person_id: str, image: np.ndarray, 
                    angle: str = 'frontal', validate: bool = True) -> Optional[str]:
        """
        Capture and save a face image
        
        Args:
            person_id: Person ID
            image: Face image
            angle: Image angle (frontal, left, right)
            validate: Whether to validate image quality
            
        Returns:
            Path to saved image, or None if validation failed
        """
        person_dir = self.dataset_root / person_id
        
        if not person_dir.exists():
            raise ValueError(f"Person not found: {person_id}")
        
        # Validate if requested
        if validate:
            is_valid, msg = self.validate_face_image(image)
            if not is_valid:
                print(f"Validation failed: {msg}")
                return None
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{angle}_{timestamp}.jpg"
        filepath = person_dir / filename
        
        # Save image
        cv2.imwrite(str(filepath), image)
        
        # Update metadata
        self.metadata['people'][person_id]['image_count'] += 1
        self._save_metadata()
        
        return str(filepath)
    
    def get_person_images(self, person_id: str) -> List[str]:
        """
        Get all images for a person
        
        Args:
            person_id: Person ID
            
        Returns:
            List of image paths
        """
        person_dir = self.dataset_root / person_id
        
        if not person_dir.exists():
            return []
        
        # Get all image files
        image_extensions = ['.jpg', '.jpeg', '.png']
        images = []
        
        for ext in image_extensions:
            images.extend(person_dir.glob(f"*{ext}"))
        
        return [str(img) for img in sorted(images)]
    
    def remove_person(self, person_id: str) -> bool:
        """
        Remove a person from dataset
        
        Args:
            person_id: Person ID
            
        Returns:
            True if removed, False if not found
        """
        person_dir = self.dataset_root / person_id
        
        if not person_dir.exists():
            return False
        
        # Remove directory and all images
        import shutil
        shutil.rmtree(person_dir)
        
        # Remove from metadata
        if person_id in self.metadata['people']:
            del self.metadata['people'][person_id]
            self._save_metadata()
        
        return True
    
    def validate_face_image(self, image: np.ndarray, 
                           min_size: int = 100) -> Tuple[bool, str]:
        """
        Validate face image quality
        
        Args:
            image: Face image
            min_size: Minimum image dimension
            
        Returns:
            Tuple of (is_valid, message)
        """
        if image is None:
            return False, "Image is None"
        
        # Check dimensions
        height, width = image.shape[:2]
        
        if width < min_size or height < min_size:
            return False, f"Image too small: {width}x{height}"
        
        # Check if image is too dark
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        mean_brightness = np.mean(gray)
        if mean_brightness < 40:
            return False, f"Image too dark: brightness={mean_brightness:.1f}"
        
        # Check blur (Laplacian variance)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        if laplacian_var < 100:
            return False, f"Image too blurry: variance={laplacian_var:.1f}"
        
        return True, "Image quality OK"
    
    def validate_dataset(self) -> Dict:
        """
        Validate entire dataset
        
        Returns:
            Validation report
        """
        report = {
            'total_people': len(self.metadata['people']),
            'total_images': 0,
            'issues': [],
            'valid_people': 0
        }
        
        for person_id, person_data in self.metadata['people'].items():
            images = self.get_person_images(person_id)
            image_count = len(images)
            
            report['total_images'] += image_count
            
            if image_count == 0:
                report['issues'].append(f"{person_id}: No images")
            elif image_count < 3:
                report['issues'].append(f"{person_id}: Only {image_count} images (recommend 5+)")
            else:
                report['valid_people'] += 1
        
        return report
    
    def export_encodings(self, recognizer_class) -> str:
        """
        Generate face encodings for all dataset images
        
        Args:
            recognizer_class: FaceRecognizer class instance
            
        Returns:
            Path to encodings file
        """
        encodings_file = self.dataset_root / "encodings.pkl"
        all_encodings = []
        all_names = []
        all_metadata = []
        
        for person_id, person_data in self.metadata['people'].items():
            images = self.get_person_images(person_id)
            
            for image_path in images:
                # Load image
                image = cv2.imread(image_path)
                if image is None:
                    continue
                
                # Generate encoding
                encoding = recognizer_class.encode_face(image)
                if encoding is not None:
                    all_encodings.append(encoding)
                    all_names.append(person_data['name'])
                    all_metadata.append({
                        'person_id': person_id,
                        'employee_id': person_data.get('employee_id'),
                        'department': person_data.get('department')
                    })
        
        # Save encodings
        data = {
            'encodings': all_encodings,
            'names': all_names,
            'metadata': all_metadata,
            'created_at': datetime.now().isoformat()
        }
        
        with open(encodings_file, 'wb') as f:
            pickle.dump(data, f)
        
        print(f"Exported {len(all_encodings)} encodings for {len(set(all_names))} people")
        return str(encodings_file)
    
    def get_statistics(self) -> Dict:
        """
        Get dataset statistics
        
        Returns:
            Statistics dictionary
        """
        stats = {
            'total_people': len(self.metadata['people']),
            'total_images': 0,
            'people_by_department': {},
            'images_per_person': {}
        }
        
        for person_id, person_data in self.metadata['people'].items():
            image_count = len(self.get_person_images(person_id))
            stats['total_images'] += image_count
            stats['images_per_person'][person_id] = image_count
            
            dept = person_data.get('department', 'Unknown')
            stats['people_by_department'][dept] = stats['people_by_department'].get(dept, 0) + 1
        
        return stats
    
    def list_people(self) -> List[Dict]:
        """
        List all people in dataset
        
        Returns:
            List of people with metadata
        """
        people = []
        
        for person_id, person_data in self.metadata['people'].items():
            person_info = {
                'person_id': person_id,
                'name': person_data['name'],
                'employee_id': person_data.get('employee_id'),
                'department': person_data.get('department'),
                'image_count': len(self.get_person_images(person_id)),
                'created_at': person_data.get('created_at')
            }
            people.append(person_info)
        
        return people


# Example usage and testing
if __name__ == "__main__":
    print("Dataset Manager Module - Week 4 Project")
    print("="*50)
    
    # Create manager
    manager = DatasetManager(dataset_root="test_dataset")
    print("\n1. Dataset manager initialized")
    print(f"   Dataset root: {manager.dataset_root}")
    
    # Add people
    print("\n2. Adding people...")
    alice_id = manager.add_person("Alice Smith", employee_id="EMP001", department="IT")
    bob_id = manager.add_person("Bob Johnson", employee_id="EMP002", department="HR")
    print(f"   Added: {alice_id}, {bob_id}")
    
    # Create test images
    print("\n3. Creating test face images...")
    test_face = np.ones((200, 200, 3), dtype=np.uint8) * 180
    cv2.circle(test_face, (70, 80), 10, (0, 0, 0), -1)
    cv2.circle(test_face, (130, 80), 10, (0, 0, 0), -1)
    cv2.ellipse(test_face, (100, 130), (30, 15), 0, 0, 180, (0, 0, 0), 2)
    
    # Capture faces
    print("\n4. Capturing faces...")
    path1 = manager.capture_face(alice_id, test_face, angle='frontal')
    path2 = manager.capture_face(alice_id, test_face, angle='left')
    path3 = manager.capture_face(bob_id, test_face, angle='frontal')
    print(f"   Captured 3 images")
    
    # Get person images
    print("\n5. Getting person images...")
    alice_images = manager.get_person_images(alice_id)
    print(f"   Alice has {len(alice_images)} images")
    
    # Validate dataset
    print("\n6. Validating dataset...")
    report = manager.validate_dataset()
    print(f"   Total people: {report['total_people']}")
    print(f"   Total images: {report['total_images']}")
    print(f"   Valid people: {report['valid_people']}")
    if report['issues']:
        print(f"   Issues: {report['issues']}")
    
    # Statistics
    print("\n7. Dataset statistics...")
    stats = manager.get_statistics()
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for k, v in value.items():
                print(f"     {k}: {v}")
        else:
            print(f"   {key}: {value}")
    
    # List people
    print("\n8. Listing people...")
    people = manager.list_people()
    for person in people:
        print(f"   {person['name']} ({person['person_id']}): {person['image_count']} images")
    
    print("\n" + "="*50)
    print("Module ready for integration!")
    print("\nIntegration path:")
    print("  1. Copy to ../../core/dataset_manager.py")
    print("  2. Import in week 5: recognition_service.py")
    print("  3. Use in API: api/persons.py")
