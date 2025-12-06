"""
Recognition Service Module
Week 5 Project Module - Progressive Web Application (Database Mode)

This module integrates all previous modules into a complete recognition pipeline.
Integrates: face_detector (Week 2), face_recognizer (Week 3), and database-backed dataset manager (Week 4).
Loads person encodings from MySQL database for recognition.
"""

import cv2
import numpy as np
import time
import sys
import os
import pickle
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from datetime import datetime

# Import Week 2 face_detector (MediaPipe)
week2_path = os.path.join(os.path.dirname(__file__), '..', '..', 'minggu-2-face-detection', 'project')
sys.path.insert(0, week2_path)

# Import Week 3 face_recognizer (DeepFace)
week3_path = os.path.join(os.path.dirname(__file__), '..', '..', 'minggu-3-face-recognition', 'project')
sys.path.insert(0, week3_path)

# Import database modules from Week 4 project
week4_path = os.path.join(os.path.dirname(__file__), '..', '..', 'minggu-4-dataset-database', 'project')
sys.path.insert(0, week4_path)

from face_detector import FaceDetector
from face_recognizer import FaceRecognizer
from dataset_manager import DatasetManager


class RecognitionService:
    """
    Complete face recognition service with database integration
    """
    
    def __init__(self, connection_string: str = None, tolerance: float = 0.6):
        """
        Initialize recognition service with database
        
        Args:
            connection_string: MySQL connection string (default: XAMPP local)
            tolerance: Recognition tolerance threshold (default: 0.6)
        """
        # Database connection (XAMPP default)
        if connection_string is None:
            connection_string = "mysql+pymysql://root:@localhost:3306/face_recognition_db"
        
        self.connection_string = connection_string
        self.tolerance = tolerance
        
        # Initialize dataset manager (database-backed)
        try:
            self.dataset_manager = DatasetManager(
                connection_string=connection_string,
                image_storage_path="recognition_images"
            )
            print("✅ RecognitionService initialized (Database mode)")
        except ConnectionError as e:
            raise Exception(f"❌ Failed to connect to database: {e}")
        
        # Initialize face detector (Week 2 - MediaPipe)
        try:
            self.face_detector = FaceDetector(model_selection=1, min_detection_confidence=0.7)
            print("✅ FaceDetector loaded (MediaPipe)")
        except Exception as e:
            print(f"⚠️  FaceDetector initialization warning: {e}")
            self.face_detector = None
        
        # Initialize face recognizer (Week 3 - DeepFace)
        try:
            self.face_recognizer = FaceRecognizer(tolerance=tolerance, model='Facenet512')
            print("✅ FaceRecognizer loaded (DeepFace Facenet512)")
        except Exception as e:
            print(f"⚠️  FaceRecognizer initialization warning: {e}")
            self.face_recognizer = None
        
        # Load encodings from database
        self.known_encodings = []
        self.known_names = []
        self.known_metadata = []
        self._load_encodings_from_database()
        
        # Statistics tracking
        self.stats = {
            'total_processed': 0,
            'total_recognized': 0,
            'total_unknown': 0,
            'avg_processing_time': 0
        }
    
    def _load_encodings_from_database(self):
        """
        Load person encodings from database
        Uses encodings stored during dataset creation
        """
        try:
            self.known_encodings = []
            self.known_names = []
            self.known_metadata = []
            
            # Get all people from database
            people = self.dataset_manager.get_all_people()
            
            # Load encodings for each person
            for person in people:
                # Get first encoding for this person
                # In production, could use all encodings and average them
                encodings = self.dataset_manager.get_person_encodings(person['id'])
                
                if encodings:
                    # Use first encoding (or average if multiple)
                    encoding = encodings[0]  # In numpy format from database
                    self.known_encodings.append(encoding)
                    self.known_names.append(person['name'])
                    self.known_metadata.append({
                        'person_id': person['id'],
                        'employee_id': person['employee_id'],
                        'department': person['department']
                    })
            
            print(f"✅ Loaded {len(self.known_names)} encodings from database\n")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not load encodings from database: {e}")
            print("   Encodings will be generated on first use")

    
    def generate_encodings_for_all(self, model_name: str = 'Facenet512'):
        """
        Generate encodings for all people in database
        
        Args:
            model_name: DeepFace model name
            
        Returns:
            Number of encodings generated
        """
        try:
            count = self.dataset_manager.generate_encodings(model_name=model_name)
            # Reload encodings after generation
            self._load_encodings_from_database()
            return count
        except Exception as e:
            print(f"❌ Failed to generate encodings: {e}")
            return 0
    
    def _find_best_match(self, encoding: np.ndarray, threshold: float = 0.6) -> Dict:
        """
        Find best match for encoding in known encodings
        
        Args:
            encoding: Person encoding (512-dim for Facenet512)
            threshold: Match threshold
            
        Returns:
            Match result dictionary
        """
        if len(self.known_encodings) == 0:
            return {
                "person_id": None,
                "name": "Unknown",
                "confidence": 0.0
            }
        
        # Calculate distances using euclidean distance
        distances = []
        for known_encoding in self.known_encodings:
            distance = np.linalg.norm(encoding - known_encoding)
            distances.append(distance)
        
        min_distance = min(distances)
        best_match_index = distances.index(min_distance)
        
        # Convert distance to confidence (lower distance = higher confidence)
        confidence = 1 - (min_distance / 2.0)  # Normalize to 0-1
        
        if min_distance < threshold:
            return {
                "person_id": self.known_metadata[best_match_index]['person_id'],
                "name": self.known_names[best_match_index],
                "confidence": float(confidence),
                "metadata": self.known_metadata[best_match_index]
            }
        else:
            return {
                "person_id": None,
                "name": "Unknown",
                "confidence": 0.0
            }
    
    def process_image(self, image: np.ndarray, 
                     return_faces: bool = True) -> Dict:
        """
        Process image with detection and recognition
        
        Args:
            image: Input image (BGR format from OpenCV)
            return_faces: Include face regions in output
            
        Returns:
            Dictionary with recognized people and their faces
        """
        if self.face_detector is None or self.face_recognizer is None:
            raise Exception("Face detector or recognizer not initialized!")
        
        try:
            # Detect faces using Week 2 MediaPipe detector
            faces = self.face_detector.detect_faces(image)
            
            if len(faces) == 0:
                return {
                    "people": [],
                    "faces": [],
                    "count": 0,
                    "timestamp": self.get_timestamp()
                }
            
            recognized_people = []
            
            for face_idx, (x, y, w, h) in enumerate(faces):
                # Generate encoding using Week 3 DeepFace recognizer
                encoding = self.face_recognizer.encode_face(image, face_location=(x, y, w, h))
                
                if encoding is None:
                    continue
                
                # Match against database
                match_result = self._find_best_match(encoding, threshold=self.tolerance)
                
                recognized_people.append({
                    "face_idx": face_idx,
                    "person_id": match_result["person_id"],
                    "name": match_result["name"],
                    "confidence": match_result["confidence"],
                    "position": {"x": int(x), "y": int(y), "w": int(w), "h": int(h)}
                })
                
                # Update stats
                if match_result["person_id"] is not None:
                    self.stats['total_recognized'] += 1
                else:
                    self.stats['total_unknown'] += 1
            
            result = {
                "people": recognized_people,
                "count": len(recognized_people),
                "timestamp": self.get_timestamp()
            }
            
            if return_faces:
                result["faces"] = detected_faces
            
            self.stats['total_processed'] += 1
            return result
            
        except Exception as e:
            print(f"❌ Error processing image: {e}")
            return {
                "people": [],
                "faces": [],
                "count": 0,
                "error": str(e)
            }
    
    def process_webcam_frame(self, frame: np.ndarray,
                            draw_boxes: bool = True,
                            draw_labels: bool = True) -> Tuple[np.ndarray, List[Dict]]:
        """
        Process webcam frame with visualization
        
        Args:
            frame: Input frame (BGR format)
            draw_boxes: Draw bounding boxes
            draw_labels: Draw labels and confidence
            
        Returns:
            Tuple of (annotated frame, recognition results)
        """
        result = self.process_image(frame, return_faces=False)
        annotated_frame = frame.copy()
        
        try:
            for person in result['people']:
                pos = person['position']
                x, y, w, h = pos['x'], pos['y'], pos['w'], pos['h']
                name = person['name']
                confidence = person['confidence']
                
                # Choose color based on recognition
                if person['person_id'] is not None:
                    color = (0, 255, 0)  # Green for known
                else:
                    color = (0, 0, 255)  # Red for unknown
                
                if draw_boxes:
                    cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), color, 2)
                
                if draw_labels:
                    label = name
                    if person['person_id'] is not None:
                        label += f" ({confidence:.2f})"
                    
                    # Draw background for text
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.6
                    thickness = 2
                    (text_w, text_h), baseline = cv2.getTextSize(label, font, font_scale, thickness)
                    
                    cv2.rectangle(annotated_frame,
                                (x, y - text_h - 10),
                                (x + text_w, y),
                                color, -1)
                    cv2.putText(annotated_frame, label,
                              (x, y - 5),
                              font, font_scale, (255, 255, 255), thickness)
        
        except Exception as e:
            print(f"⚠️  Error drawing on frame: {e}")
        
        return annotated_frame, result['people']
    
    def get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()
    
    def get_statistics(self) -> Dict:
        """Get recognition statistics"""
        return {
            "total_processed": self.stats['total_processed'],
            "total_recognized": self.stats['total_recognized'],
            "total_unknown": self.stats['total_unknown'],
            "recognition_rate": (
                self.stats['total_recognized'] / self.stats['total_processed']
                if self.stats['total_processed'] > 0 else 0
            ),
            "avg_processing_time": self.stats['avg_processing_time']
        }
    
    def reset_statistics(self):
        """Reset all statistics"""
        self.stats = {
            'total_processed': 0,
            'total_recognized': 0,
            'total_unknown': 0,
            'avg_processing_time': 0
        }
