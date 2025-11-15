"""
Face Recognizer Module  
Week 3 Project Module - Progressive Web Application

This module provides face recognition functionality using face_recognition library.
Builds on Week 2's face_detector.py for face detection.
"""

import face_recognition
import numpy as np
import pickle
import os
from typing import List, Tuple, Optional, Dict
from pathlib import Path


class FaceRecognizer:
    """
    Face recognition using face_recognition library
    """
    
    def __init__(self, tolerance: float = 0.6, model: str = 'large'):
        """
        Initialize face recognizer
        
        Args:
            tolerance: Distance threshold for face matching (default 0.6)
            model: Model to use ('large' or 'small')
        """
        self.tolerance = tolerance
        self.model = model
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_metadata = []
    
    def encode_face(self, image: np.ndarray, face_location: Tuple[int, int, int, int] = None) -> Optional[np.ndarray]:
        """
        Generate face encoding from image
        
        Args:
            image: Input image (RGB format)
            face_location: Optional face location (top, right, bottom, left)
            
        Returns:
            128-dimension face encoding, or None if no face found
        """
        # Convert BGR to RGB if needed
        if len(image.shape) == 3 and image.shape[2] == 3:
            rgb_image = image[:, :, ::-1]
        else:
            rgb_image = image
        
        # Get face encodings
        if face_location:
            encodings = face_recognition.face_encodings(rgb_image, [face_location], model=self.model)
        else:
            face_locations = face_recognition.face_locations(rgb_image, model='hog')
            if len(face_locations) == 0:
                return None
            encodings = face_recognition.face_encodings(rgb_image, face_locations, model=self.model)
        
        if len(encodings) == 0:
            return None
        
        return encodings[0]
    
    def add_known_face(self, encoding: np.ndarray, name: str, metadata: Dict = None):
        """
        Add a known face to the database
        
        Args:
            encoding: Face encoding (128-d vector)
            name: Person's name
            metadata: Additional information (employee_id, department, etc.)
        """
        self.known_face_encodings.append(encoding)
        self.known_face_names.append(name)
        self.known_face_metadata.append(metadata or {})
    
    def recognize_face(self, face_encoding: np.ndarray) -> Tuple[Optional[str], float, Optional[Dict]]:
        """
        Recognize a face from its encoding
        
        Args:
            face_encoding: Face encoding to identify
            
        Returns:
            Tuple of (name, confidence, metadata) or (None, 0.0, None) if unknown
        """
        if len(self.known_face_encodings) == 0:
            return None, 0.0, None
        
        # Calculate distances
        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
        
        # Find best match
        best_match_index = np.argmin(face_distances)
        best_distance = face_distances[best_match_index]
        
        # Check if match is good enough
        if best_distance <= self.tolerance:
            name = self.known_face_names[best_match_index]
            confidence = 1.0 - best_distance  # Convert distance to confidence
            metadata = self.known_face_metadata[best_match_index]
            return name, confidence, metadata
        
        return None, 0.0, None
    
    def recognize_faces_in_image(self, image: np.ndarray) -> List[Dict]:
        """
        Recognize all faces in an image
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            List of recognition results with bounding boxes
        """
        # Convert BGR to RGB
        rgb_image = image[:, :, ::-1]
        
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_image, model='hog')
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations, model=self.model)
        
        results = []
        for i, (face_encoding, face_location) in enumerate(zip(face_encodings, face_locations)):
            name, confidence, metadata = self.recognize_face(face_encoding)
            
            # Convert location format from (top, right, bottom, left) to (x, y, w, h)
            top, right, bottom, left = face_location
            x, y, w, h = left, top, right - left, bottom - top
            
            result = {
                'id': i,
                'name': name if name else 'Unknown',
                'confidence': confidence,
                'bbox': (x, y, w, h),
                'location': face_location,
                'encoding': face_encoding,
                'metadata': metadata or {}
            }
            results.append(result)
        
        return results
    
    def compare_faces(self, encoding1: np.ndarray, encoding2: np.ndarray) -> Tuple[bool, float]:
        """
        Compare two face encodings
        
        Args:
            encoding1: First face encoding
            encoding2: Second face encoding
            
        Returns:
            Tuple of (is_match, distance)
        """
        distance = face_recognition.face_distance([encoding1], encoding2)[0]
        is_match = distance <= self.tolerance
        return is_match, distance
    
    def calculate_confidence(self, distance: float) -> float:
        """
        Convert distance to confidence score
        
        Args:
            distance: Face distance
            
        Returns:
            Confidence score (0-1)
        """
        return max(0.0, min(1.0, 1.0 - distance))
    
    def save_database(self, filepath: str):
        """
        Save known faces database to file
        
        Args:
            filepath: Path to save file
        """
        database = {
            'encodings': self.known_face_encodings,
            'names': self.known_face_names,
            'metadata': self.known_face_metadata,
            'tolerance': self.tolerance,
            'model': self.model
        }
        
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(database, f)
        
        print(f"Database saved: {len(self.known_face_names)} faces")
    
    def load_database(self, filepath: str):
        """
        Load known faces database from file
        
        Args:
            filepath: Path to database file
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Database file not found: {filepath}")
        
        with open(filepath, 'rb') as f:
            database = pickle.load(f)
        
        self.known_face_encodings = database['encodings']
        self.known_face_names = database['names']
        self.known_face_metadata = database['metadata']
        self.tolerance = database.get('tolerance', 0.6)
        self.model = database.get('model', 'large')
        
        print(f"Database loaded: {len(self.known_face_names)} faces")
    
    def get_all_encodings(self) -> Dict[str, np.ndarray]:
        """
        Get all known face encodings
        
        Returns:
            Dictionary mapping names to encodings
        """
        return {
            name: encoding 
            for name, encoding in zip(self.known_face_names, self.known_face_encodings)
        }
    
    def remove_person(self, name: str) -> bool:
        """
        Remove a person from known faces
        
        Args:
            name: Person's name to remove
            
        Returns:
            True if removed, False if not found
        """
        indices_to_remove = [i for i, n in enumerate(self.known_face_names) if n == name]
        
        if not indices_to_remove:
            return False
        
        # Remove in reverse to avoid index issues
        for idx in sorted(indices_to_remove, reverse=True):
            del self.known_face_encodings[idx]
            del self.known_face_names[idx]
            del self.known_face_metadata[idx]
        
        return True
    
    def get_statistics(self) -> Dict:
        """
        Get database statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'total_faces': len(self.known_face_names),
            'unique_people': len(set(self.known_face_names)),
            'tolerance': self.tolerance,
            'model': self.model
        }


# Example usage and testing
if __name__ == "__main__":
    print("Face Recognizer Module - Week 3 Project")
    print("="*50)
    
    # Create recognizer
    recognizer = FaceRecognizer(tolerance=0.6)
    print("\n1. Recognizer initialized")
    print(f"   Tolerance: {recognizer.tolerance}")
    print(f"   Model: {recognizer.model}")
    
    # Create test encodings (random for demo)
    print("\n2. Creating test face encodings...")
    test_encoding1 = np.random.rand(128)
    test_encoding2 = np.random.rand(128)
    test_encoding3 = np.random.rand(128)
    
    # Add known faces
    print("\n3. Adding known faces...")
    recognizer.add_known_face(test_encoding1, "Alice", {'employee_id': '001', 'department': 'IT'})
    recognizer.add_known_face(test_encoding2, "Bob", {'employee_id': '002', 'department': 'HR'})
    recognizer.add_known_face(test_encoding3, "Charlie", {'employee_id': '003', 'department': 'Finance'})
    print(f"   Added 3 known faces")
    
    # Test recognition
    print("\n4. Testing recognition...")
    name, confidence, metadata = recognizer.recognize_face(test_encoding1)
    print(f"   Recognized: {name}, Confidence: {confidence:.2f}")
    print(f"   Metadata: {metadata}")
    
    # Test comparison
    print("\n5. Testing face comparison...")
    is_match, distance = recognizer.compare_faces(test_encoding1, test_encoding2)
    print(f"   Alice vs Bob: Match={is_match}, Distance={distance:.4f}")
    
    # Test statistics
    print("\n6. Database statistics...")
    stats = recognizer.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test save/load
    print("\n7. Testing save/load...")
    os.makedirs("test_output", exist_ok=True)
    recognizer.save_database("test_output/face_db.pkl")
    
    # Create new recognizer and load
    recognizer2 = FaceRecognizer()
    recognizer2.load_database("test_output/face_db.pkl")
    print(f"   Loaded {len(recognizer2.known_face_names)} faces")
    
    print("\n" + "="*50)
    print("Module ready for integration!")
    print("\nIntegration path:")
    print("  1. Copy to ../../core/face_recognizer.py")
    print("  2. Import in week 4: dataset_manager.py")
    print("  3. Use in week 5: recognition_service.py")
    print("  4. Use in API: api/recognition.py")
