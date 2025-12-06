"""
Face Recognizer Module  
Week 3 Project Module - Progressive Web Application

This module provides face recognition functionality using DeepFace.
DeepFace provides state-of-the-art face recognition with 97%+ accuracy.
Builds on Week 2's face_detector.py for face detection.
Uses DeepFace with Facenet512 model for 512-dimensional face encodings.
"""

import numpy as np
import pickle
import os
from typing import List, Tuple, Optional, Dict
from pathlib import Path
import cv2

try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("⚠️  DeepFace not available. Install: pip install deepface tensorflow")


class FaceRecognizer:
    """
    Face recognition using DeepFace with Facenet512 model
    Provides 512-dimensional face encodings for accurate recognition
    """
    
    def __init__(self, tolerance: float = 0.6, model: str = 'Facenet512'):
        """
        Initialize face recognizer with DeepFace
        
        Args:
            tolerance: Distance threshold for face matching (default 0.6)
            model: DeepFace model name ('Facenet512', 'ArcFace', 'SFace', etc.)
        """
        if not DEEPFACE_AVAILABLE:
            raise ImportError(
                "DeepFace not installed!\n"
                "Install with: pip install deepface==0.0.89\n"
                "              pip install tensorflow==2.15.0"
            )
        
        self.tolerance = tolerance
        self.model = model
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_metadata = []
        
        # DeepFace will auto-download model on first use (~100MB for Facenet512)
        print(f"✅ FaceRecognizer initialized (DeepFace {model})")
        print(f"   Tolerance: {tolerance}")
        print(f"   Note: Model will download on first use (~100MB)")
    
    def encode_face(self, image: np.ndarray, face_location: Tuple[int, int, int, int] = None) -> Optional[np.ndarray]:
        """
        Generate face encoding from image using DeepFace
        
        Args:
            image: Input image (BGR format from OpenCV)
            face_location: Optional face location (x, y, w, h) - if None, will detect automatically
            
        Returns:
            512-dimension face encoding, or None if no face found
        """
        try:
            # If face_location provided, crop the face region
            if face_location is not None:
                x, y, w, h = face_location
                face_crop = image[y:y+h, x:x+w]
            else:
                face_crop = image
            
            # DeepFace expects RGB but can handle BGR too
            # represent() returns embeddings for the face
            embedding_objs = DeepFace.represent(
                img_path=face_crop,
                model_name=self.model,
                enforce_detection=False,  # Don't fail if face not detected
                detector_backend='skip'  # Skip detection since we may have cropped face
            )
            
            if len(embedding_objs) == 0:
                return None
            
            # Get first face encoding (512-d for Facenet512)
            encoding = np.array(embedding_objs[0]['embedding'])
            
            return encoding
            
        except Exception as e:
            print(f"⚠️  Encoding failed: {e}")
            return None
    
    def add_known_face(self, encoding: np.ndarray, name: str, metadata: Dict = None):
        """
        Add a known face to the database
        
        Args:
            encoding: Face encoding (512-d vector for Facenet512)
            name: Person's name
            metadata: Additional information (employee_id, department, etc.)
        """
        self.known_face_encodings.append(encoding)
        self.known_face_names.append(name)
        self.known_face_metadata.append(metadata or {})
    
    def recognize_face(self, face_encoding: np.ndarray) -> Tuple[Optional[str], float, Optional[Dict]]:
        """
        Recognize a face from its encoding using Euclidean distance
        
        Args:
            face_encoding: Face encoding to identify (512-d)
            
        Returns:
            Tuple of (name, confidence, metadata) or (None, 0.0, None) if unknown
        """
        if len(self.known_face_encodings) == 0:
            return None, 0.0, None
        
        # Calculate distances (Euclidean)
        known_encodings = np.array(self.known_face_encodings)
        distances = np.linalg.norm(known_encodings - face_encoding, axis=1)
        
        # Find best match
        best_match_index = np.argmin(distances)
        best_distance = distances[best_match_index]
        
        # Check if match is good enough
        if best_distance <= self.tolerance:
            name = self.known_face_names[best_match_index]
            # Convert distance to confidence (inverse relationship)
            confidence = max(0.0, 1.0 - (best_distance / self.tolerance))
            metadata = self.known_face_metadata[best_match_index]
            return name, confidence, metadata
        
        return None, 0.0, None
    
    def recognize_faces_in_image(self, image: np.ndarray, face_detector=None) -> List[Dict]:
        """
        Recognize all faces in an image
        Requires a face_detector instance from Week 2 for face detection
        
        Args:
            image: Input image (BGR format)
            face_detector: FaceDetector instance from Week 2 (required)
            
        Returns:
            List of recognition results with bounding boxes
        """
        if face_detector is None:
            raise ValueError(
                "face_detector is required!\n"
                "Import from Week 2: from face_detector import FaceDetector\n"
                "Then pass detector instance: recognizer.recognize_faces_in_image(image, detector)"
            )
        
        # Detect faces using Week 2 detector
        faces = face_detector.detect_faces(image)
        
        if not faces:
            return []
        
        results_list = []
        
        for i, (x, y, w, h) in enumerate(faces):
            # Get encoding for this face
            encoding = self.encode_face(image, face_location=(x, y, w, h))
            
            if encoding is None:
                continue
            
            # Recognize
            name, confidence, metadata = self.recognize_face(encoding)
            
            result = {
                'id': i,
                'name': name if name else 'Unknown',
                'confidence': confidence,
                'bbox': (x, y, w, h),
                'location': (y, x+w, y+h, x),  # top, right, bottom, left format
                'encoding': encoding,
                'metadata': metadata or {}
            }
            results_list.append(result)
        
        return results_list
    
    def compare_faces(self, encoding1: np.ndarray, encoding2: np.ndarray) -> Tuple[bool, float]:
        """
        Compare two face encodings
        
        Args:
            encoding1: First face encoding
            encoding2: Second face encoding
            
        Returns:
            Tuple of (is_match, distance)
        """
        distance = np.linalg.norm(encoding1 - encoding2)
        is_match = distance <= self.tolerance
        return is_match, distance
    
    def calculate_confidence(self, distance: float) -> float:
        """
        Convert distance to confidence score
        
        Args:
            distance: Face distance (Euclidean)
            
        Returns:
            Confidence score (0-1)
        """
        # Inverse relationship: smaller distance = higher confidence
        confidence = max(0.0, 1.0 - (distance / self.tolerance))
        return confidence
    
    def save_database(self, filepath: str):
        """
        Save known faces database to file
        
        Args:
            filepath: Path to save file (.pkl)
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
        
        print(f"✅ Database saved: {len(self.known_face_names)} faces → {filepath}")
    
    def load_database(self, filepath: str):
        """
        Load known faces database from file
        
        Args:
            filepath: Path to database file (.pkl)
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Database file not found: {filepath}")
        
        with open(filepath, 'rb') as f:
            database = pickle.load(f)
        
        self.known_face_encodings = database['encodings']
        self.known_face_names = database['names']
        self.known_face_metadata = database['metadata']
        self.tolerance = database.get('tolerance', 0.6)
        self.model = database.get('model', 'Facenet512')
        
        print(f"✅ Database loaded: {len(self.known_face_names)} faces from {filepath}")
    
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
    print("Face Recognizer Module - Week 3 Project (DeepFace)")
    print("="*50)
    
    try:
        # Create recognizer
        recognizer = FaceRecognizer(tolerance=0.6, model='Facenet512')
        print("\n✅ DeepFace recognizer initialized")
        print(f"   Model: {recognizer.model}")
        print(f"   Tolerance: {recognizer.tolerance}")
        print(f"   Encoding dimensions: 512")
        
    except ImportError as e:
        print(f"\n❌ {e}")
        print("   Install: pip install deepface==0.0.89")
        print("            pip install tensorflow==2.15.0")
        exit(1)
    
    print("\n📦 Module ready for integration!")
    print("\n🔗 Integration with other modules:")
    print("   • Week 1: image_utils.py (image preprocessing)")
    print("   • Week 2: face_detector.py (MediaPipe detection)")
    print("   • Week 3: face_recognizer.py (DeepFace recognition) ← YOU ARE HERE")
    print("   • Week 4: dataset_manager.py (MySQL database)")
    print("   • Week 5: recognition_service.py (complete system)")
    
    print("\n💡 Example usage:")
    print("   from face_detector import FaceDetector")
    print("   from face_recognizer import FaceRecognizer")
    print("")
    print("   detector = FaceDetector()")
    print("   recognizer = FaceRecognizer()")
    print("")
    print("   # Detect & encode faces")
    print("   faces = detector.detect_faces(image)")
    print("   for (x, y, w, h) in faces:")
    print("       encoding = recognizer.encode_face(image, (x, y, w, h))")
    print("       recognizer.add_known_face(encoding, 'Alice')")
    print("")
    print("   # Recognize")
    print("   results = recognizer.recognize_faces_in_image(image, detector)")

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

