"""
Face Detector Module
Week 2 Project Module - Progressive Web Application

This module provides face detection functionality using Haar Cascade.
Builds on Week 1's image_utils.py for preprocessing.
"""

import cv2
import numpy as np
import os
from typing import List, Tuple, Optional, Dict


class FaceDetector:
    """
    Face detection using Haar Cascade Classifier
    """
    
    def __init__(self, cascade_path: str = None):
        """
        Initialize face detector
        
        Args:
            cascade_path: Path to Haar Cascade XML file
        """
        if cascade_path is None:
            # Use OpenCV's built-in cascade
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        
        if not os.path.exists(cascade_path):
            raise FileNotFoundError(f"Cascade file not found: {cascade_path}")
        
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if self.face_cascade.empty():
            raise ValueError("Failed to load cascade classifier")
        
        # Default detection parameters
        self.scale_factor = 1.1
        self.min_neighbors = 5
        self.min_size = (30, 30)
    
    def detect_faces(self, image: np.ndarray, 
                    return_confidence: bool = False) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in image
        
        Args:
            image: Input image (BGR or grayscale)
            return_confidence: Whether to return confidence scores
            
        Returns:
            List of face bounding boxes as (x, y, w, h)
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors,
            minSize=self.min_size,
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # Convert to list of tuples
        if len(faces) == 0:
            return []
        
        return [tuple(face) for face in faces]
    
    def detect_faces_detailed(self, image: np.ndarray) -> List[Dict]:
        """
        Detect faces with detailed information
        
        Args:
            image: Input image
            
        Returns:
            List of dictionaries with face info
        """
        faces = self.detect_faces(image)
        
        results = []
        for i, (x, y, w, h) in enumerate(faces):
            face_info = {
                'id': i,
                'bbox': (x, y, w, h),
                'center': (x + w // 2, y + h // 2),
                'area': w * h,
                'aspect_ratio': w / h if h > 0 else 0
            }
            results.append(face_info)
        
        return results
    
    def get_face_region(self, image: np.ndarray, bbox: Tuple[int, int, int, int],
                       padding: int = 0) -> np.ndarray:
        """
        Extract face region from image
        
        Args:
            image: Input image
            bbox: Bounding box (x, y, w, h)
            padding: Additional padding around face
            
        Returns:
            Cropped face region
        """
        x, y, w, h = bbox
        
        # Add padding
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(image.shape[1], x + w + padding)
        y2 = min(image.shape[0], y + h + padding)
        
        return image[y1:y2, x1:x2].copy()
    
    def draw_detections(self, image: np.ndarray, faces: List[Tuple[int, int, int, int]],
                       color: Tuple[int, int, int] = (0, 255, 0),
                       thickness: int = 2,
                       show_count: bool = True) -> np.ndarray:
        """
        Draw bounding boxes on image
        
        Args:
            image: Input image
            faces: List of face bounding boxes
            color: Box color (BGR)
            thickness: Line thickness
            show_count: Whether to show face count
            
        Returns:
            Image with drawn boxes
        """
        result = image.copy()
        
        for i, (x, y, w, h) in enumerate(faces):
            # Draw rectangle
            cv2.rectangle(result, (x, y), (x + w, y + h), color, thickness)
            
            # Draw label
            label = f"Face {i+1}"
            cv2.putText(result, label, (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Show count
        if show_count and len(faces) > 0:
            count_text = f"Faces: {len(faces)}"
            cv2.putText(result, count_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        return result
    
    def validate_detection(self, bbox: Tuple[int, int, int, int],
                          image_shape: Tuple[int, int],
                          min_face_size: int = 30) -> Tuple[bool, str]:
        """
        Validate if detected face meets quality requirements
        
        Args:
            bbox: Face bounding box (x, y, w, h)
            image_shape: Image shape (height, width)
            min_face_size: Minimum acceptable face size
            
        Returns:
            Tuple of (is_valid, message)
        """
        x, y, w, h = bbox
        height, width = image_shape[:2]
        
        # Check if face is too small
        if w < min_face_size or h < min_face_size:
            return False, f"Face too small: {w}x{h}"
        
        # Check if face is at image border (might be cropped)
        border_threshold = 10
        if (x < border_threshold or y < border_threshold or 
            x + w > width - border_threshold or y + h > height - border_threshold):
            return False, "Face at image border (might be cropped)"
        
        # Check aspect ratio (face should be roughly square)
        aspect_ratio = w / h if h > 0 else 0
        if aspect_ratio < 0.7 or aspect_ratio > 1.5:
            return False, f"Unusual aspect ratio: {aspect_ratio:.2f}"
        
        return True, "Face detection valid"
    
    def set_parameters(self, scale_factor: float = None,
                      min_neighbors: int = None,
                      min_size: Tuple[int, int] = None):
        """
        Update detection parameters
        
        Args:
            scale_factor: How much to reduce size at each scale
            min_neighbors: How many neighbors to retain detection
            min_size: Minimum face size
        """
        if scale_factor is not None:
            self.scale_factor = scale_factor
        if min_neighbors is not None:
            self.min_neighbors = min_neighbors
        if min_size is not None:
            self.min_size = min_size


# Example usage and testing
if __name__ == "__main__":
    print("Face Detector Module - Week 2 Project")
    print("="*50)
    
    # Create detector
    detector = FaceDetector()
    print("\n1. Detector initialized")
    print(f"   Scale factor: {detector.scale_factor}")
    print(f"   Min neighbors: {detector.min_neighbors}")
    print(f"   Min size: {detector.min_size}")
    
    # Create test image
    print("\n2. Creating test image...")
    test_image = np.ones((480, 640, 3), dtype=np.uint8) * 200
    
    # Draw fake face (rectangle)
    cv2.rectangle(test_image, (200, 150), (400, 400), (150, 150, 150), -1)
    cv2.circle(test_image, (270, 250), 20, (100, 100, 100), -1)  # Left eye
    cv2.circle(test_image, (330, 250), 20, (100, 100, 100), -1)  # Right eye
    cv2.ellipse(test_image, (300, 320), (40, 20), 0, 0, 180, (100, 100, 100), 2)  # Smile
    
    print("   Test image created: 640x480")
    
    # Detect faces
    print("\n3. Testing detection...")
    faces = detector.detect_faces(test_image)
    print(f"   Faces detected: {len(faces)}")
    
    if len(faces) > 0:
        for i, (x, y, w, h) in enumerate(faces):
            print(f"   Face {i+1}: x={x}, y={y}, w={w}, h={h}")
    
    # Test detailed detection
    print("\n4. Testing detailed detection...")
    detailed = detector.detect_faces_detailed(test_image)
    for face in detailed:
        print(f"   Face {face['id']}: area={face['area']}, ratio={face['aspect_ratio']:.2f}")
    
    # Test validation
    print("\n5. Testing validation...")
    if len(faces) > 0:
        is_valid, msg = detector.validate_detection(faces[0], test_image.shape)
        print(f"   Valid: {is_valid}, Message: {msg}")
    
    print("\n" + "="*50)
    print("Module ready for integration!")
    print("\nIntegration path:")
    print("  1. Copy to ../../core/face_detector.py")
    print("  2. Import in week 3: face_recognizer.py")
    print("  3. Use in API: api/detection.py")
