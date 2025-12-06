"""
Face Detector Module
Week 2 Project Module - Progressive Web Application

This module provides face detection functionality using MediaPipe.
MediaPipe provides fast, accurate face detection with 10-15ms performance.
Builds on Week 1's image_utils.py for preprocessing.
"""

import cv2
import numpy as np
import os
from typing import List, Tuple, Optional, Dict

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("⚠️  MediaPipe not available. Install: pip install mediapipe")


class FaceDetector:
    """
    Face detection using MediaPipe Face Detection
    Provides fast and accurate face detection suitable for real-time applications
    """
    
    def __init__(self, model_selection: int = 1, min_detection_confidence: float = 0.7):
        """
        Initialize face detector with MediaPipe
        
        Args:
            model_selection: 0 for short-range (within 2m), 1 for full-range (within 5m)
            min_detection_confidence: Minimum confidence threshold (0.0-1.0)
        """
        if not MEDIAPIPE_AVAILABLE:
            raise ImportError(
                "MediaPipe not installed!\n"
                "Install with: pip install mediapipe==0.10.8"
            )
        
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=model_selection,
            min_detection_confidence=min_detection_confidence
        )
        
        self.model_selection = model_selection
        self.min_detection_confidence = min_detection_confidence
    
    def detect_faces(self, image: np.ndarray, 
                    return_confidence: bool = False) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in image using MediaPipe
        
        Args:
            image: Input image (BGR format from OpenCV)
            return_confidence: Whether to return confidence scores
            
        Returns:
            List of face bounding boxes as (x, y, w, h)
            If return_confidence=True, returns list of ((x, y, w, h), confidence)
        """
        # Convert BGR to RGB for MediaPipe
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        results = self.face_detection.process(rgb_image)
        
        if not results.detections:
            return []
        
        h, w, c = image.shape
        face_boxes = []
        
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            
            # Convert normalized coordinates to pixel coordinates
            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            width = int(bbox.width * w)
            height = int(bbox.height * h)
            
            # Ensure coordinates are within image bounds
            x = max(0, x)
            y = max(0, y)
            width = min(w - x, width)
            height = min(h - y, height)
            
            if return_confidence:
                confidence = detection.score[0]
                face_boxes.append(((x, y, width, height), confidence))
            else:
                face_boxes.append((x, y, width, height))
        
        return face_boxes
    
    def detect_faces_detailed(self, image: np.ndarray) -> List[Dict]:
        """
        Detect faces with detailed information including confidence scores
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            List of dictionaries with face info including:
            - id: Face index
            - bbox: Bounding box (x, y, w, h)
            - center: Face center point (x, y)
            - area: Face area in pixels
            - aspect_ratio: Width/height ratio
            - confidence: Detection confidence score (0.0-1.0)
            - keypoints: Face keypoints (6 points: eyes, nose, mouth)
        """
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_image)
        
        if not results.detections:
            return []
        
        h, w, c = image.shape
        detailed_faces = []
        
        for i, detection in enumerate(results.detections):
            bbox = detection.location_data.relative_bounding_box
            
            # Bounding box
            x = max(0, int(bbox.xmin * w))
            y = max(0, int(bbox.ymin * h))
            width = min(w - x, int(bbox.width * w))
            height = min(h - y, int(bbox.height * h))
            
            # Keypoints
            keypoints = {}
            if detection.location_data.relative_keypoints:
                kp_names = ['right_eye', 'left_eye', 'nose_tip', 'mouth_center', 'right_ear', 'left_ear']
                for idx, kp in enumerate(detection.location_data.relative_keypoints):
                    if idx < len(kp_names):
                        keypoints[kp_names[idx]] = (int(kp.x * w), int(kp.y * h))
            
            face_info = {
                'id': i,
                'bbox': (x, y, width, height),
                'center': (x + width // 2, y + height // 2),
                'area': width * height,
                'aspect_ratio': width / height if height > 0 else 0,
                'confidence': detection.score[0],
                'keypoints': keypoints
            }
            detailed_faces.append(face_info)
        
        return detailed_faces
    
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
    
    def get_face_regions(self, image: np.ndarray, padding: int = 20) -> List[np.ndarray]:
        """
        Extract all face regions from image
        
        Args:
            image: Input image (BGR format)
            padding: Padding around face in pixels
            
        Returns:
            List of cropped face images
        """
        faces = self.detect_faces(image)
        
        face_regions = []
        for (x, y, w, h) in faces:
            face_region = self.get_face_region(image, (x, y, w, h), padding)
            face_regions.append(face_region)
        
        return face_regions
    
    def draw_detections(self, image: np.ndarray, faces: List = None,
                       color: Tuple[int, int, int] = (0, 255, 0),
                       thickness: int = 2, show_confidence: bool = True) -> np.ndarray:
        """
        Draw face bounding boxes on image
        
        Args:
            image: Input image (BGR format)
            faces: List of face detections (if None, will detect automatically)
            color: Box color (B, G, R)
            thickness: Line thickness
            show_confidence: Whether to show confidence scores
            
        Returns:
            Image with drawn boxes
        """
        output = image.copy()
        
        if faces is None:
            faces = self.detect_faces_detailed(image)
        
        for face in faces:
            if isinstance(face, dict):
                bbox = face['bbox']
                x, y, w, h = bbox
                
                # Draw rectangle
                cv2.rectangle(output, (x, y), (x + w, y + h), color, thickness)
                
                # Draw confidence
                if show_confidence and 'confidence' in face:
                    conf_text = f"{face['confidence']*100:.1f}%"
                    cv2.putText(output, conf_text, (x, y - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                # Draw keypoints
                if 'keypoints' in face:
                    for kp_name, (kp_x, kp_y) in face['keypoints'].items():
                        cv2.circle(output, (kp_x, kp_y), 3, (0, 0, 255), -1)
            else:
                # Simple bbox tuple
                x, y, w, h = face
                cv2.rectangle(output, (x, y), (x + w, y + h), color, thickness)
        
        return output
    
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
    
    def detect_faces_webcam(self, camera_id: int = 0, window_name: str = "MediaPipe Face Detection"):
        """
        Real-time face detection from webcam using MediaPipe
        
        Args:
            camera_id: Camera device ID
            window_name: Display window name
        """
        import time
        
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            print(f"❌ Cannot open camera {camera_id}")
            return
        
        print("🎥 Webcam opened. Press 'q' to quit.")
        
        prev_time = time.time()
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("❌ Failed to read frame")
                break
            
            # Detect faces
            faces = self.detect_faces_detailed(frame)
            
            # Draw detections
            output = self.draw_detections(frame, faces, show_confidence=True)
            
            # Calculate FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
            prev_time = curr_time
            
            # Show statistics
            cv2.putText(output, f"Faces: {len(faces)} | FPS: {fps:.1f}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Display
            cv2.imshow(window_name, output)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Webcam closed")
    
    def set_parameters(self, min_detection_confidence: float = None,
                      model_selection: int = None):
        """
        Update detection parameters
        
        Args:
            min_detection_confidence: Minimum confidence threshold (0.0-1.0)
            model_selection: 0 for short-range, 1 for full-range
        """
        if min_detection_confidence is not None:
            self.min_detection_confidence = min_detection_confidence
            self.face_detection = self.mp_face_detection.FaceDetection(
                model_selection=self.model_selection,
                min_detection_confidence=min_detection_confidence
            )
        
        if model_selection is not None:
            self.model_selection = model_selection
            self.face_detection = self.mp_face_detection.FaceDetection(
                model_selection=model_selection,
                min_detection_confidence=self.min_detection_confidence
            )


# Example usage and testing
if __name__ == "__main__":
    print("Face Detector Module - Week 2 Project (MediaPipe)")
    print("="*50)
    
    # Create detector
    try:
        detector = FaceDetector(model_selection=1, min_detection_confidence=0.7)
        print("\n✅ MediaPipe detector initialized")
        print(f"   Model: Full-range (5m)")
        print(f"   Min confidence: 0.7")
    except ImportError as e:
        print(f"\n❌ {e}")
        print("   Install: pip install mediapipe==0.10.8")
        exit(1)
    
    # Test with webcam
    print("\n🎥 Starting webcam test...")
    print("   Press 'q' to quit")
    
    try:
        detector.detect_faces_webcam(camera_id=0)
    except KeyboardInterrupt:
        print("\n✅ Test stopped by user")
    except Exception as e:
        print(f"\n⚠️  Error: {e}")
    
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
