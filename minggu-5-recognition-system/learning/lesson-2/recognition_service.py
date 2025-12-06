"""
Recognition Service: Hybrid Face Recognition System
Combines MediaPipe detection + DeepFace recognition for real-time accuracy
"""
import os
import sys
import cv2
import numpy as np
import time
from collections import defaultdict

# Add Week 4 and Lesson 1 modules
week4_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'minggu-4-dataset-database', 'learning', 'lesson-2')
lesson1_path = os.path.join(os.path.dirname(__file__), '..', 'lesson-1')
sys.path.insert(0, week4_path)
sys.path.insert(0, lesson1_path)

from database import Database
from models import Person, FaceEncoding
from encoding_generator import EncodingGenerator

# Try to import MediaPipe
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("⚠️  MediaPipe not installed. Install: pip install mediapipe")


class RecognitionService:
    """
    Hybrid Recognition Service
    - MediaPipe: Fast face detection (10-15ms)
    - DeepFace: Accurate recognition (100-150ms, 97%+)
    """
    
    def __init__(self, db_connection_string, model_name='Facenet512', threshold=0.6):
        """
        Initialize recognition service
        
        Args:
            db_connection_string: MySQL connection URL
            model_name: DeepFace model (Facenet512, ArcFace, SFace)
            threshold: Distance threshold for matching (0.4-0.8)
        """
        self.threshold = threshold
        self.model_name = model_name
        
        # Initialize MediaPipe detector
        if MEDIAPIPE_AVAILABLE:
            self.mp_face_detection = mp.solutions.face_detection
            self.face_detection = self.mp_face_detection.FaceDetection(
                model_selection=1,  # 1 = full range (better for webcam)
                min_detection_confidence=0.7
            )
            print("✅ MediaPipe detector loaded")
        else:
            self.face_detection = None
            print("❌ MediaPipe not available")
        
        # Initialize DeepFace encoder
        try:
            self.encoder = EncodingGenerator(model_name=model_name)
            print(f"✅ DeepFace model loaded ({model_name})")
        except Exception as e:
            print(f"❌ Failed to load DeepFace: {e}")
            self.encoder = None
        
        # Connect to database
        self.db = Database(db_connection_string)
        if not self.db.connect():
            raise Exception("Failed to connect to database")
        
        # Load known encodings from database
        self.known_encodings = []
        self.known_persons = []
        self.load_encodings()
        
        # Performance tracking
        self.frame_count = 0
        self.detection_times = []
        self.recognition_times = []
        self.start_time = time.time()
    
    def load_encodings(self):
        """Load face encodings from database"""
        session = self.db.get_session()
        
        # Get all persons with encodings
        persons = session.query(Person).all()
        
        for person in persons:
            if person.face_encodings:
                # Get first encoding for each person
                encoding_record = person.face_encodings[0]
                encoding = self.encoder.deserialize_encoding(encoding_record.encoding_data)
                
                self.known_encodings.append(encoding)
                self.known_persons.append(person)
        
        print(f"✅ Loaded {len(self.known_encodings)} encodings for {len(self.known_persons)} persons")
        for person in self.known_persons:
            print(f"   - {person.name} ({person.employee_id})")
    
    def detect_faces(self, image):
        """
        Detect faces using MediaPipe
        
        Args:
            image: BGR image from OpenCV
            
        Returns:
            list of (x, y, w, h) bounding boxes
        """
        if not MEDIAPIPE_AVAILABLE or self.face_detection is None:
            return []
        
        start_time = time.time()
        
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w = image.shape[:2]
        
        # Detect faces
        results = self.face_detection.process(rgb_image)
        
        detection_time = (time.time() - start_time) * 1000
        self.detection_times.append(detection_time)
        
        bboxes = []
        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                
                # Convert relative coordinates to absolute
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                
                # Ensure within bounds
                x = max(0, x)
                y = max(0, y)
                width = min(width, w - x)
                height = min(height, h - y)
                
                bboxes.append((x, y, width, height))
        
        return bboxes
    
    def recognize_face(self, image, bbox):
        """
        Recognize face using DeepFace encoding
        
        Args:
            image: Full BGR image
            bbox: (x, y, w, h) bounding box
            
        Returns:
            tuple: (person_id, name, confidence, distance) or (None, "Unknown", 0, 999)
        """
        if self.encoder is None or len(self.known_encodings) == 0:
            return None, "Unknown", 0, 999
        
        start_time = time.time()
        
        # Crop face region
        x, y, w, h = bbox
        face_img = image[y:y+h, x:x+w]
        
        if face_img.size == 0:
            return None, "Unknown", 0, 999
        
        # Generate encoding for unknown face
        try:
            unknown_encoding = self.encoder.generate_from_image_array(face_img)
            
            if unknown_encoding is None:
                return None, "Unknown", 0, 999
            
            # Compare with all known encodings
            best_match_idx = None
            best_distance = 999
            
            for idx, known_encoding in enumerate(self.known_encodings):
                # Calculate Euclidean distance
                distance = np.linalg.norm(unknown_encoding - known_encoding)
                
                if distance < best_distance:
                    best_distance = distance
                    best_match_idx = idx
            
            recognition_time = (time.time() - start_time) * 1000
            self.recognition_times.append(recognition_time)
            
            # Check if match is good enough
            if best_distance <= self.threshold:
                person = self.known_persons[best_match_idx]
                confidence = max(0, min(100, (1 - best_distance) * 100))
                return person.id, person.name, confidence, best_distance
            else:
                return None, "Unknown", 0, best_distance
                
        except Exception as e:
            print(f"❌ Recognition error: {e}")
            return None, "Unknown", 0, 999
    
    def process_frame(self, frame):
        """
        Process single frame: detect + recognize
        
        Args:
            frame: BGR image from webcam
            
        Returns:
            tuple: (annotated_frame, recognitions)
                recognitions = [(name, confidence, bbox), ...]
        """
        self.frame_count += 1
        
        # Detect faces
        bboxes = self.detect_faces(frame)
        
        recognitions = []
        
        # Recognize each face
        for bbox in bboxes:
            x, y, w, h = bbox
            
            person_id, name, confidence, distance = self.recognize_face(frame, bbox)
            
            recognitions.append((name, confidence, bbox))
            
            # Draw bounding box
            if name == "Unknown":
                color = (0, 0, 255)  # Red for unknown
            else:
                color = (0, 255, 0)  # Green for recognized
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Draw name and confidence
            label = f"{name} ({confidence:.1f}%)"
            label_y = y - 10 if y - 10 > 20 else y + h + 20
            
            # Background for text
            (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, (x, label_y - label_h - 5), (x + label_w, label_y + 5), color, -1)
            
            cv2.putText(frame, label, (x, label_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame, recognitions
    
    def get_stats(self):
        """Get performance statistics"""
        elapsed = time.time() - self.start_time
        fps = self.frame_count / elapsed if elapsed > 0 else 0
        
        avg_detection = np.mean(self.detection_times) if self.detection_times else 0
        avg_recognition = np.mean(self.recognition_times) if self.recognition_times else 0
        
        return {
            'fps': fps,
            'frames': self.frame_count,
            'elapsed': elapsed,
            'avg_detection_ms': avg_detection,
            'avg_recognition_ms': avg_recognition,
            'total_avg_ms': avg_detection + avg_recognition
        }
    
    def process_webcam(self, camera_id=0):
        """
        Real-time webcam recognition
        
        Args:
            camera_id: Camera index (default: 0, can be selected via detect_cameras)
                      Use detect_available_cameras() to see all cameras
        """
        print("\n" + "="*60)
        print("🎥 REAL-TIME RECOGNITION")
        print("="*60)
        
        # Detect and list available cameras
        print("\n🔍 Detecting available cameras...")
        available_cameras = []
        for cam_id in range(5):
            test_cap = cv2.VideoCapture(cam_id)
            if test_cap.isOpened():
                ret, frame = test_cap.read()
                if ret and frame is not None:
                    width = int(test_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(test_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = int(test_cap.get(cv2.CAP_PROP_FPS))
                    name = "Built-in Webcam / Default Camera" if cam_id == 0 else (
                        "External USB Camera / Secondary Camera" if cam_id == 1 else f"Camera Device {cam_id}")
                    available_cameras.append({'id': cam_id, 'name': name, 'resolution': f"{width}x{height}", 'fps': fps})
                    print(f"  ✅ Camera {cam_id}: {name} - {width}x{height} @ {fps}fps")
                test_cap.release()
            else:
                break
        
        if len(available_cameras) == 0:
            print("❌ No cameras detected!")
            return
        
        # Select camera
        if camera_id >= len(available_cameras):
            print(f"⚠️  Camera {camera_id} not available, using camera 0")
            camera_id = 0
        
        selected_cam = available_cameras[camera_id]
        print(f"\n✅ Using: {selected_cam['name']}")
        print("Press 'q' to quit\n")
        
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            print("❌ Failed to open webcam")
            return
        
        # Set resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print(f"Camera resolution: {int(cap.get(3))}x{int(cap.get(4))}")
        print("Press 'q' to quit\n")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame
            annotated_frame, recognitions = self.process_frame(frame)
            
            # Display stats on frame
            stats = self.get_stats()
            cv2.putText(annotated_frame, f"FPS: {stats['fps']:.1f}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(annotated_frame, f"Frame: {self.frame_count}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            # Show frame
            cv2.imshow('Hybrid Recognition System', annotated_frame)
            
            # Print recognition results
            if recognitions:
                for name, confidence, bbox in recognitions:
                    if name != "Unknown":
                        print(f"Frame {self.frame_count:04d}: ✅ {name} ({confidence:.1f}%)")
            
            # Quit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        
        # Final stats
        print("\n" + "="*60)
        print("📊 PERFORMANCE STATISTICS")
        print("="*60)
        final_stats = self.get_stats()
        print(f"Total frames: {final_stats['frames']}")
        print(f"Total time: {final_stats['elapsed']:.2f}s")
        print(f"Average FPS: {final_stats['fps']:.2f}")
        print(f"Avg detection time: {final_stats['avg_detection_ms']:.2f}ms")
        print(f"Avg recognition time: {final_stats['avg_recognition_ms']:.2f}ms")
        print(f"Total avg per frame: {final_stats['total_avg_ms']:.2f}ms")
    
    def close(self):
        """Cleanup resources"""
        if self.db:
            self.db.close()


def test_recognition_service():
    """Test recognition service"""
    print("="*60)
    print("TEST: Recognition Service")
    print("="*60)
    
    # XAMPP Default: root user, no password
    connection_string = "mysql+pymysql://root:@localhost:3306/face_recognition_db"
    
    try:
        service = RecognitionService(
            db_connection_string=connection_string,
            model_name='Facenet512',
            threshold=0.6
        )
        
        print("\n✅ Recognition service initialized")
        print(f"   Known persons: {len(service.known_persons)}")
        print(f"   Threshold: {service.threshold}")
        
        # Test with webcam
        service.process_webcam()
        
        service.close()
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")


if __name__ == '__main__':
    test_recognition_service()
