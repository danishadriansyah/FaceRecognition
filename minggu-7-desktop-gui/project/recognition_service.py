"""
Recognition Service Module
Week 5 Project Module - Progressive Web Application

This module integrates all previous modules into a complete recognition pipeline.
Integrates: image_utils, face_detector, face_recognizer, dataset_manager
"""

import cv2
import numpy as np
import time
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from datetime import datetime


class RecognitionService:
    """
    Complete face recognition service integrating all modules
    """
    
    def __init__(self, dataset_root: str = "dataset", tolerance: float = 0.6):
        """
        Initialize recognition service
        
        Args:
            dataset_root: Root directory for dataset
            tolerance: Recognition tolerance threshold
        """
        self.dataset_root = Path(dataset_root)
        self.tolerance = tolerance
        
        # Will be initialized with actual modules in production
        self.face_detector = None
        self.face_recognizer = None
        self.dataset_manager = None
        
        # Performance metrics
        self.stats = {
            'total_processed': 0,
            'total_recognized': 0,
            'total_unknown': 0,
            'avg_processing_time': 0.0
        }
    
    def initialize(self, face_detector, face_recognizer, dataset_manager):
        """
        Initialize with module instances
        
        Args:
            face_detector: FaceDetector instance from week 2
            face_recognizer: FaceRecognizer instance from week 3
            dataset_manager: DatasetManager instance from week 4
        """
        self.face_detector = face_detector
        self.face_recognizer = face_recognizer
        self.dataset_manager = dataset_manager
    
    def process_image(self, image: np.ndarray, 
                     return_faces: bool = True) -> Dict:
        """
        Complete recognition pipeline for single image
        
        Args:
            image: Input image (BGR format)
            return_faces: Whether to return face images
            
        Returns:
            Recognition results dictionary
        """
        start_time = time.time()
        
        # Step 1: Detect faces
        faces = self.face_detector.detect_faces(image) if self.face_detector else []
        
        # Step 2: Recognize each face
        results = []
        for i, bbox in enumerate(faces):
            x, y, w, h = bbox
            
            # Extract face region
            face_region = self.face_detector.get_face_region(image, bbox, padding=20)
            
            # Generate encoding
            if self.face_recognizer:
                encoding = self.face_recognizer.encode_face(face_region)
                
                if encoding is not None:
                    # Recognize
                    name, confidence, metadata = self.face_recognizer.recognize_face(encoding)
                    
                    result = {
                        'id': i,
                        'bbox': bbox,
                        'name': name if name else 'Unknown',
                        'confidence': confidence,
                        'metadata': metadata or {},
                        'is_known': name is not None
                    }
                    
                    if return_faces:
                        result['face_image'] = face_region
                    
                    results.append(result)
                    
                    # Update stats
                    if name:
                        self.stats['total_recognized'] += 1
                    else:
                        self.stats['total_unknown'] += 1
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Update average processing time
        self.stats['total_processed'] += 1
        self.stats['avg_processing_time'] = (
            (self.stats['avg_processing_time'] * (self.stats['total_processed'] - 1) + processing_time) 
            / self.stats['total_processed']
        )
        
        return {
            'success': True,
            'image_shape': image.shape,
            'faces_detected': len(faces),
            'faces_recognized': len([r for r in results if r['is_known']]),
            'results': results,
            'processing_time': processing_time,
            'timestamp': datetime.now().isoformat()
        }
    
    def process_webcam_frame(self, frame: np.ndarray, 
                            draw_boxes: bool = True) -> Tuple[np.ndarray, List[Dict]]:
        """
        Process single webcam frame
        
        Args:
            frame: Input frame (BGR format)
            draw_boxes: Whether to draw bounding boxes
            
        Returns:
            Tuple of (annotated frame, recognition results)
        """
        # Process image
        result = self.process_image(frame, return_faces=False)
        
        # Draw on frame
        annotated_frame = frame.copy()
        
        if draw_boxes:
            for face_result in result['results']:
                x, y, w, h = face_result['bbox']
                name = face_result['name']
                confidence = face_result['confidence']
                is_known = face_result['is_known']
                
                # Choose color based on recognition
                color = (0, 255, 0) if is_known else (0, 0, 255)
                
                # Draw rectangle
                cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), color, 2)
                
                # Draw label
                label = f"{name}"
                if is_known:
                    label += f" ({confidence:.2f})"
                
                # Background for text
                (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(annotated_frame, (x, y - text_h - 10), (x + text_w, y), color, -1)
                cv2.putText(annotated_frame, label, (x, y - 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return annotated_frame, result['results']
    
    def batch_recognize(self, image_paths: List[str]) -> List[Dict]:
        """
        Process multiple images in batch
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            List of recognition results
        """
        results = []
        
        for image_path in image_paths:
            image = cv2.imread(image_path)
            if image is None:
                results.append({
                    'success': False,
                    'error': f'Failed to load image: {image_path}'
                })
                continue
            
            result = self.process_image(image, return_faces=False)
            result['image_path'] = image_path
            results.append(result)
        
        return results
    
    def get_statistics(self) -> Dict:
        """
        Get service statistics
        
        Returns:
            Statistics dictionary
        """
        stats = self.stats.copy()
        
        if self.stats['total_processed'] > 0:
            stats['recognition_rate'] = (
                self.stats['total_recognized'] / 
                (self.stats['total_recognized'] + self.stats['total_unknown'])
            ) if (self.stats['total_recognized'] + self.stats['total_unknown']) > 0 else 0
        
        return stats
    
    def reload_database(self):
        """
        Reload face recognition database
        """
        if self.face_recognizer and self.dataset_manager:
            # Clear current database
            self.face_recognizer.known_face_encodings = []
            self.face_recognizer.known_face_names = []
            self.face_recognizer.known_face_metadata = []
            
            # Load from dataset
            people = self.dataset_manager.list_people()
            
            for person in people:
                person_id = person['person_id']
                images = self.dataset_manager.get_person_images(person_id)
                
                for image_path in images:
                    image = cv2.imread(image_path)
                    if image is None:
                        continue
                    
                    encoding = self.face_recognizer.encode_face(image)
                    if encoding is not None:
                        self.face_recognizer.add_known_face(
                            encoding,
                            person['name'],
                            {
                                'person_id': person_id,
                                'employee_id': person.get('employee_id'),
                                'department': person.get('department')
                            }
                        )
            
            print(f"Database reloaded: {len(self.face_recognizer.known_face_names)} encodings")
    
    def validate_system(self) -> Dict:
        """
        Validate entire recognition system
        
        Returns:
            Validation report
        """
        report = {
            'detector_initialized': self.face_detector is not None,
            'recognizer_initialized': self.face_recognizer is not None,
            'dataset_initialized': self.dataset_manager is not None,
            'known_faces': 0,
            'dataset_people': 0,
            'issues': []
        }
        
        if self.face_recognizer:
            report['known_faces'] = len(self.face_recognizer.known_face_names)
        else:
            report['issues'].append("Face recognizer not initialized")
        
        if self.dataset_manager:
            report['dataset_people'] = len(self.dataset_manager.metadata.get('people', {}))
        else:
            report['issues'].append("Dataset manager not initialized")
        
        if not self.face_detector:
            report['issues'].append("Face detector not initialized")
        
        report['is_ready'] = len(report['issues']) == 0 and report['known_faces'] > 0
        
        return report


# Example usage and testing
if __name__ == "__main__":
    print("Recognition Service Module - Week 5 Project")
    print("="*50)
    
    # Create service
    service = RecognitionService(dataset_root="dataset", tolerance=0.6)
    print("\n1. Recognition service initialized")
    print(f"   Dataset root: {service.dataset_root}")
    print(f"   Tolerance: {service.tolerance}")
    
    # Note: In production, initialize with actual modules:
    # service.initialize(face_detector, face_recognizer, dataset_manager)
    
    print("\n2. Service components:")
    print(f"   Face detector: {'Not initialized (demo mode)' if not service.face_detector else 'Ready'}")
    print(f"   Face recognizer: {'Not initialized (demo mode)' if not service.face_recognizer else 'Ready'}")
    print(f"   Dataset manager: {'Not initialized (demo mode)' if not service.dataset_manager else 'Ready'}")
    
    # Create test image
    print("\n3. Creating test image...")
    test_image = np.ones((480, 640, 3), dtype=np.uint8) * 200
    cv2.putText(test_image, "Test Recognition", (150, 240),
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
    
    # Get statistics
    print("\n4. Service statistics...")
    stats = service.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Validate system
    print("\n5. System validation...")
    validation = service.validate_system()
    for key, value in validation.items():
        if isinstance(value, list) and value:
            print(f"   {key}:")
            for item in value:
                print(f"     - {item}")
        else:
            print(f"   {key}: {value}")
    
    print("\n" + "="*50)
    print("Module ready for integration!")
    print("\nIntegration example:")
    print("""
# In production app.py:
from core.face_detector import FaceDetector
from core.face_recognizer import FaceRecognizer
from core.dataset_manager import DatasetManager
from core.recognition_service import RecognitionService

# Initialize modules
detector = FaceDetector()
recognizer = FaceRecognizer()
dataset_mgr = DatasetManager()

# Initialize service
service = RecognitionService()
service.initialize(detector, recognizer, dataset_mgr)
service.reload_database()

# Process image
result = service.process_image(image)
    """)
