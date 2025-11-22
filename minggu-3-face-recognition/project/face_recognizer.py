"""
Face Recognizer Module  
Week 3 Project Module - Progressive Web Application

This module provides face recognition functionality using MediaPipe.
Builds on Week 2's face_detector.py for face detection.
Uses MediaPipe FaceMesh for facial landmarks and encoding.
"""

import mediapipe as mp
import numpy as np
import pickle
import os
from typing import List, Tuple, Optional, Dict
from pathlib import Path
import cv2


class FaceRecognizer:
    """
    Face recognition menggunakan MediaPipe FaceMesh dengan feature extraction
    
    Features:
    - Uses MediaPipe FaceMesh untuk 468 facial landmarks
    - 1404-dimensional encoding (468 landmarks × 3 coordinates: x, y, z)
    - Cosine similarity untuk face matching
    - Database persistence (pickle format)
    - Real-time processing
    
    Example:
        recognizer = FaceRecognizer(tolerance=0.5)
        encoding = recognizer.encode_face(image)
        recognizer.add_known_face(encoding, "Alice")
        results = recognizer.recognize_faces_in_image(image)
    """
    
    def __init__(self, tolerance: float = 0.6, model: str = 'large'):
        """
        Initialize face recognizer with MediaPipe
        
        Args:
            tolerance: Distance threshold for face matching (default 0.6)
            model: Model type (kept for compatibility, 'large' or 'small')
        """
        self.tolerance = tolerance
        self.model = model
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_metadata = []
        
        # Initialize MediaPipe
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_detection = self.mp_face_detection.FaceDetection()
        self.face_mesh = self.mp_face_mesh.FaceMesh()
    
    def _extract_face_features(self, image: np.ndarray, face_location: Tuple[int, int, int, int] = None) -> Optional[np.ndarray]:
        """
        Extract face features/encoding from image using MediaPipe FaceMesh
        
        Args:
            image: Input image (RGB format)
            face_location: Optional face location (top, right, bottom, left)
            
        Returns:
            Face encoding (468-d landmark vector from FaceMesh)
        """
        # Convert BGR to RGB if needed
        if len(image.shape) == 3 and image.shape[2] == 3:
            rgb_image = image[:, :, ::-1]
        else:
            rgb_image = image
        
        h, w, c = rgb_image.shape
        
        # Use face mesh to extract landmarks directly (more reliable than detection)
        mesh_results = self.face_mesh.process(rgb_image)
        
        if not mesh_results.multi_face_landmarks:
            return None
        
        # Extract first detected face
        landmarks = mesh_results.multi_face_landmarks[0]
        
        # Convert landmarks to feature vector (468 landmarks * 3 coords = 1404 dimensions)
        feature_vector = []
        for landmark in landmarks.landmark:
            feature_vector.extend([landmark.x, landmark.y, landmark.z])
        
        # Convert to numpy array and normalize
        encoding = np.array(feature_vector, dtype=np.float32)
        
        # Normalize to unit vector (L2 normalization)
        norm = np.linalg.norm(encoding)
        if norm > 0:
            encoding = encoding / norm
        
        return encoding
    
    def encode_face(self, image: np.ndarray, face_location: Tuple[int, int, int, int] = None) -> Optional[np.ndarray]:
        """
        Generate face encoding dari image menggunakan MediaPipe FaceMesh
        
        Args:
            image: Input image (RGB atau BGR format)
            face_location: Optional face location (top, right, bottom, left) - unused with FaceMesh
            
        Returns:
            1404-dimensional face encoding (468 landmarks × 3 coordinates), atau None jika tidak ada face
        """
        return self._extract_face_features(image, face_location)
    
    def add_known_face(self, encoding: np.ndarray, name: str, metadata: Dict = None):
        """
        Add a known face ke database
        
        Args:
            encoding: Face encoding (1404-d vector dari MediaPipe FaceMesh)
            name: Person's name
            metadata: Additional information seperti employee_id, department, etc.
            
        Example:
            recognizer.add_known_face(encoding, "Alice", {"emp_id": "E001", "dept": "IT"})
        """
        self.known_face_encodings.append(encoding)
        self.known_face_names.append(name)
        self.known_face_metadata.append(metadata or {})
    
    def recognize_face(self, face_encoding: np.ndarray) -> Tuple[Optional[str], float, Optional[Dict]]:
        """
        Recognize a face from its encoding using cosine similarity
        
        Args:
            face_encoding: Face encoding (468-d vector from MediaPipe FaceMesh)
            
        Returns:
            Tuple of (name, confidence, metadata) or (None, 0.0, None) if unknown
        """
        if len(self.known_face_encodings) == 0:
            return None, 0.0, None
        
        # Calculate cosine distances
        known_encodings = np.array(self.known_face_encodings)
        similarities = np.dot(known_encodings, face_encoding)
        distances = 1.0 - similarities
        
        # Find best match
        best_match_index = np.argmin(distances)
        best_distance = distances[best_match_index]
        
        # Check if match is good enough
        if best_distance <= self.tolerance:
            name = self.known_face_names[best_match_index]
            confidence = 1.0 - best_distance  # Direct conversion from cosine distance
            confidence = max(0.0, min(1.0, confidence))  # Clamp between 0-1
            metadata = self.known_face_metadata[best_match_index]
            return name, confidence, metadata
        
        return None, 0.0, None
    
    def recognize_faces_in_image(self, image: np.ndarray) -> List[Dict]:
        """
        Recognize all faces in an image using MediaPipe FaceMesh
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            List of recognition results with bounding boxes
        """
        # Convert BGR to RGB
        rgb_image = image[:, :, ::-1] if len(image.shape) == 3 else image
        
        h, w = rgb_image.shape[:2]
        
        # Get face mesh landmarks for ALL faces in image
        mesh_results = self.face_mesh.process(rgb_image)
        
        if not mesh_results.multi_face_landmarks:
            return []
        
        results_list = []
        
        for face_idx, landmarks in enumerate(mesh_results.multi_face_landmarks):
            # Calculate bounding box from landmarks
            xs = [lm.x for lm in landmarks.landmark]
            ys = [lm.y for lm in landmarks.landmark]
            
            x_min, x_max = min(xs), max(xs)
            y_min, y_max = min(ys), max(ys)
            
            # Convert to pixel coordinates
            x = int(x_min * w)
            y = int(y_min * h)
            width = int((x_max - x_min) * w)
            height = int((y_max - y_min) * h)
            
            # Add padding
            padding = 10
            x = max(0, x - padding)
            y = max(0, y - padding)
            width = min(w - x, width + padding * 2)
            height = min(h - y, height + padding * 2)
            
            # Extract encoding from landmarks
            feature_vector = []
            for landmark in landmarks.landmark:
                feature_vector.extend([landmark.x, landmark.y, landmark.z])
            
            encoding = np.array(feature_vector, dtype=np.float32)
            norm = np.linalg.norm(encoding)
            if norm > 0:
                encoding = encoding / norm
            
            # Recognize face
            name, confidence, metadata = self.recognize_face(encoding)
            
            result = {
                'id': face_idx,
                'name': name if name else 'Unknown',
                'confidence': confidence,
                'bbox': (x, y, width, height),
                'location': (y, x+width, y+height, x),  # top, right, bottom, left format
                'encoding': encoding,
                'metadata': metadata or {}
            }
            results_list.append(result)
        
        return results_list
    
    def compare_faces(self, encoding1: np.ndarray, encoding2: np.ndarray) -> Tuple[bool, float]:
        """
        Compare two face encodings using cosine similarity (better for normalized vectors)
        
        Args:
            encoding1: First face encoding (468-d vector)
            encoding2: Second face encoding (468-d vector)
            
        Returns:
            Tuple of (is_match, distance)
        """
        # Use cosine distance for normalized vectors (more stable than Euclidean)
        # Cosine distance = 1 - cosine_similarity
        similarity = np.dot(encoding1, encoding2)
        distance = 1.0 - similarity
        
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
        confidence = 1.0 - (distance / 2.0)
        return max(0.0, min(1.0, confidence))
    
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
    print("Face Recognizer Module - Week 3 Project (MediaPipe Version)")
    print("="*50)
    
    # Create recognizer
    recognizer = FaceRecognizer(tolerance=0.6)
    print("\n1. Recognizer initialized")
    print(f"   Using: MediaPipe FaceMesh")
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

