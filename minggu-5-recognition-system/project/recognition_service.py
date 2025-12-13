"""
Recognition Service Module
Week 5 Project Module - Progressive Web Application (File-Based Mode)

This module integrates all previous modules into a complete recognition pipeline.
Uses MediaPipe for BOTH detection AND recognition for faster performance.
"""

import cv2
import numpy as np
import time
import sys
import os
import pickle
import json
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from datetime import datetime
import mediapipe as mp

# Import Week 2 face_detector (MediaPipe)
week2_path = os.path.join(os.path.dirname(__file__), '..', '..', 'minggu-2-face-detection', 'project')
week2_path = os.path.abspath(week2_path)

# Remove any existing paths that might conflict
sys.path = [p for p in sys.path if 'minggu-' not in p.lower()]

# Insert Week 2 for FaceDetector (MediaPipe)
sys.path.insert(0, week2_path)

from face_detector import FaceDetector

print(f"🔍 Using MediaPipe for detection AND recognition")


class RecognitionService:
    """
    Complete face recognition service using MediaPipe (fast and accurate)
    """
    
    def __init__(self, dataset_path: str = "dataset", tolerance: float = 0.6):
        """
        Initialize recognition service with MediaPipe
        
        Args:
            dataset_path: Path to dataset folder (default: "dataset")
            tolerance: Recognition tolerance threshold (default: 0.6)
        """
        self.dataset_path = Path(dataset_path)
        self.encodings_file = self.dataset_path / "encodings.pkl"
        self.tolerance = tolerance
        
        # Initialize MediaPipe Face Detection (optimized)
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=0,  # 0 for close-range (2m), 1 for full-range (5m)
            min_detection_confidence=0.3  # Lower = more sensitive
        )
        
        # Initialize MediaPipe Face Mesh for landmarks (used for encoding)
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=5,
            refine_landmarks=True,
            min_detection_confidence=0.3,
            min_tracking_confidence=0.3
        )
        
        print("✅ MediaPipe Face Detection loaded (Confidence: 0.3 - More Sensitive)")
        print("✅ MediaPipe Face Mesh loaded (for encoding)")
        
        # Load encodings from pickle file
        self.known_encodings = []
        self.known_names = []
        self.known_metadata = []
        self._load_encodings_from_file()
        
        # Statistics tracking
        self.stats = {
            'total_processed': 0,
            'total_recognized': 0,
            'total_unknown': 0,
            'avg_processing_time': 0
        }
        
        print(f"✅ RecognitionService initialized (MediaPipe Full Mode)")
    
    def _extract_face_encoding_mediapipe(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract face encoding using MediaPipe Face Mesh landmarks
        Returns 468 landmarks x 3 coordinates = 1404 dimensional vector
        """
        try:
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process with Face Mesh
            results = self.face_mesh.process(rgb_image)
            
            if not results.multi_face_landmarks:
                return None
            
            # Get first face landmarks
            face_landmarks = results.multi_face_landmarks[0]
            
            # Extract landmarks as encoding (468 landmarks x 3 coords)
            encoding = []
            for landmark in face_landmarks.landmark:
                encoding.extend([landmark.x, landmark.y, landmark.z])
            
            return np.array(encoding)
            
        except Exception as e:
            return None
    
    def _load_encodings_from_file(self):
        """
        Load person encodings from pickle file
        """
        if not self.encodings_file.exists():
            print("⚠️  No encodings file found")
            print(f"   Looking for: {self.encodings_file.absolute()}")
            print("   💡 Run DatasetManager.generate_encodings() first")
            return
        
        try:
            with open(self.encodings_file, 'rb') as f:
                data = pickle.load(f)
            
            self.known_encodings = [np.array(enc) for enc in data["encodings"]]
            self.known_names = data["names"]
            self.known_metadata = data.get("metadata", [])
            
            print(f"✅ Loaded {len(self.known_names)} encodings from file")
            print(f"   Model: {data.get('model', 'Unknown')}")
            print(f"   Generated: {data.get('generated_at', 'Unknown')}\n")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not load encodings from file: {e}")
            print("   Encodings will be generated on first use")
    
    def reload_encodings(self):
        """
        Reload encodings from file (useful after adding new persons)
        """
        print("🔄 Reloading encodings...")
        self._load_encodings_from_file()
    
    def recognize_faces(self, image: np.ndarray, return_frames: bool = False) -> List[Dict]:
        """
        Recognize faces in an image using MediaPipe
        
        Args:
            image: Input image (BGR format from cv2)
            return_frames: If True, return cropped face images
            
        Returns:
            List of recognition results
        """
        start_time = time.time()
        results = []
        
        if image is None or image.size == 0:
            return results
        
        # Check if we have loaded encodings
        if len(self.known_encodings) == 0:
            return results
        
        # Convert BGR to RGB for MediaPipe
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w = image.shape[:2]
        
        # Step 1: Detect faces with MediaPipe
        detection_results = self.face_detection.process(rgb_image)
        
        if not detection_results.detections:
            return results
        
        # Step 2: Process each detected face
        for detection in detection_results.detections:
            # Get bounding box
            bbox = detection.location_data.relative_bounding_box
            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            width = int(bbox.width * w)
            height = int(bbox.height * h)
            
            # Ensure coordinates are within image bounds
            x = max(0, x)
            y = max(0, y)
            width = min(width, w - x)
            height = min(height, h - y)
            
            if width <= 0 or height <= 0:
                continue
            
            # Extract face ROI
            face_roi = image[y:y+height, x:x+width]
            
            if face_roi.size == 0:
                continue
            
            # Generate encoding using MediaPipe landmarks
            face_encoding = self._extract_face_encoding_mediapipe(face_roi)
            
            if face_encoding is None:
                results.append({
                    'name': 'Unknown',
                    'confidence': 0.0,
                    'bbox': (x, y, width, height),
                    'metadata': {},
                    'face_image': face_roi if return_frames else None
                })
                continue
            
            # Compare with known encodings using cosine similarity
            best_match = None
            best_distance = float('inf')
            
            for idx, known_encoding in enumerate(self.known_encodings):
                # Normalize vectors for cosine similarity
                face_norm = face_encoding / (np.linalg.norm(face_encoding) + 1e-6)
                known_norm = known_encoding / (np.linalg.norm(known_encoding) + 1e-6)
                
                # Cosine distance = 1 - cosine similarity
                similarity = np.dot(face_norm, known_norm)
                distance = 1.0 - similarity
                
                if distance < best_distance:
                    best_distance = distance
                    best_match = idx
            
            # Check if match is within tolerance
            if best_match is not None and best_distance <= self.tolerance:
                confidence = 1.0 - (best_distance / self.tolerance)
                confidence = max(0.0, min(1.0, confidence))
                
                result = {
                    'name': self.known_names[best_match],
                    'confidence': confidence,
                    'distance': best_distance,
                    'bbox': (x, y, width, height),
                    'metadata': self.known_metadata[best_match] if best_match < len(self.known_metadata) else {},
                    'face_image': face_roi if return_frames else None
                }
                
                self.stats['total_recognized'] += 1
            else:
                result = {
                    'name': 'Unknown',
                    'confidence': 0.0,
                    'distance': best_distance if best_match is not None else float('inf'),
                    'bbox': (x, y, width, height),
                    'metadata': {},
                    'face_image': face_roi if return_frames else None
                }
                
                self.stats['total_unknown'] += 1
            
            results.append(result)
        
        # Update stats
        processing_time = time.time() - start_time
        self.stats['total_processed'] += len(results)
        
        if self.stats['total_processed'] > 0:
            old_avg = self.stats['avg_processing_time']
            self.stats['avg_processing_time'] = (old_avg * (self.stats['total_processed'] - len(results)) + processing_time) / self.stats['total_processed']
        
        return results
    
    def recognize_from_file(self, image_path: str) -> List[Dict]:
        """
        Recognize faces from image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            List of recognition results
        """
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError(f"Cannot read image: {image_path}")
        
        return self.recognize_faces(image)
    
    def recognize_from_camera(self, camera_id: int = 0, duration: int = 30, 
                            save_results: bool = True, output_dir: str = "output"):
        """
        Run recognition from camera feed
        
        Args:
            camera_id: Camera device ID
            duration: Duration in seconds (0 for infinite)
            save_results: Save annotated frames
            output_dir: Output directory for saved frames
        """
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open camera {camera_id}")
        
        if save_results:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
        
        start_time = time.time()
        frame_count = 0
        
        print(f"\n📹 Starting camera recognition...")
        print(f"   Duration: {duration}s (press 'q' to quit)")
        print(f"   Known persons: {len(set(self.known_names))}")
        print(f"   Known encodings: {len(self.known_encodings)}\n")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Check duration
            if duration > 0 and (time.time() - start_time) > duration:
                break
            
            # Recognize faces
            results = self.recognize_faces(frame)
            
            # Draw results
            display_frame = self.draw_results(frame, results)
            
            # Show FPS
            fps = frame_count / (time.time() - start_time) if time.time() > start_time else 0
            cv2.putText(display_frame, f"FPS: {fps:.1f}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Show stats
            cv2.putText(display_frame, f"Recognized: {self.stats['total_recognized']}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(display_frame, f"Unknown: {self.stats['total_unknown']}", (10, 100),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            cv2.imshow('Face Recognition', display_frame)
            
            # Save frame if requested
            if save_results and frame_count % 30 == 0:  # Save every 30 frames
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = output_path / f"recognition_{timestamp}_{frame_count}.jpg"
                cv2.imwrite(str(save_path), display_frame)
            
            frame_count += 1
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n✅ Recognition complete")
        print(f"   Frames processed: {frame_count}")
        print(f"   Total faces: {self.stats['total_processed']}")
        print(f"   Recognized: {self.stats['total_recognized']}")
        print(f"   Unknown: {self.stats['total_unknown']}")
    
    def draw_results(self, image: np.ndarray, results: List[Dict]) -> np.ndarray:
        """
        Draw recognition results on image
        
        Args:
            image: Input image
            results: Recognition results
            
        Returns:
            Annotated image
        """
        output = image.copy()
        
        for result in results:
            x, y, w, h = result['bbox']
            name = result['name']
            confidence = result['confidence']
            
            # Choose color based on recognition
            if name == 'Unknown':
                color = (0, 0, 255)  # Red
                label = "Unknown"
            else:
                color = (0, 255, 0)  # Green
                label = f"{name} ({confidence:.2f})"
            
            # Draw bounding box
            cv2.rectangle(output, (x, y), (x+w, y+h), color, 2)
            
            # Draw label background
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(output, (x, y - label_size[1] - 10), (x + label_size[0], y), color, -1)
            
            # Draw label text
            cv2.putText(output, label, (x, y - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return output
    
    def get_statistics(self) -> Dict:
        """
        Get recognition statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            **self.stats,
            'known_persons': len(set(self.known_names)),
            'known_encodings': len(self.known_encodings),
            'dataset_path': str(self.dataset_path.absolute()),
            'encodings_file': str(self.encodings_file)
        }
    
    def save_log(self, results: List[Dict], log_file: str = "logs/recognition_log.json"):
        """
        Save recognition results to JSON log
        
        Args:
            results: Recognition results
            log_file: Path to log file
        """
        log_path = Path(log_file)
        log_path.parent.mkdir(exist_ok=True)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'results': [
                {
                    'name': r['name'],
                    'confidence': r['confidence'],
                    'bbox': r['bbox'],
                    'metadata': r.get('metadata', {})
                }
                for r in results
            ]
        }
        
        # Append to log file
        logs = []
        if log_path.exists():
            with open(log_path, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)


# Example usage
if __name__ == "__main__":
    print("Recognition Service Module - Week 5 Project (File-Based)")
    print("="*60)
    
    # Initialize service
    service = RecognitionService(dataset_path="dataset", tolerance=0.6)
    
    print("\n💡 Available methods:")
    print("   results = service.recognize_from_file('photo.jpg')")
    print("   service.recognize_from_camera(camera_id=0, duration=30)")
    print("   service.reload_encodings()  # After adding new persons")
    print("   stats = service.get_statistics()")
    print("   service.save_log(results, 'logs/recognition.json')")
