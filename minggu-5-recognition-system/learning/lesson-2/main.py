"""Lesson 2: Performance Optimization & Metrics (MediaPipe)"""
import cv2
import pickle
import os
import time
import sys

# Add parent path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../project'))
from face_recognizer import FaceRecognizer

def main():
    print("="*60)
    print("LESSON 2: Performance Optimization (MediaPipe)")
    print("="*60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, '..', 'lesson-1', 'output', 'face_database.pkl')
    logs_dir = os.path.join(script_dir, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Load recognition database
    print("\n1. Loading recognition database...")
    recognizer = FaceRecognizer()
    recognizer.load_database(db_path)
    stats = recognizer.get_statistics()
    print(f"   ✅ Loaded {stats['total_faces']} encodings for {stats['unique_people']} persons")
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    # Performance metrics
    frame_count = 0
    recognition_count = 0
    total_time = 0
    fps_list = []
    
    print("\n2. Starting optimized recognition...")
    print("   Press ESC to exit\n")
    
    while True:
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            break
        
        # Optimization: Process every 3rd frame
        if frame_count % 3 == 0:
            # MediaPipe optimized for speed automatically!
            results = recognizer.recognize_faces_in_image(frame)
            recognition_count += len(results)
        
        frame_count += 1
        elapsed = time.time() - start_time
        total_time += elapsed
        
        # Calculate FPS
        fps = 1 / elapsed if elapsed > 0 else 0
        avg_fps = frame_count / total_time if total_time > 0 else 0
        
        # Display metrics
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Avg FPS: {int(avg_fps)}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Recognized: {recognition_count}", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('Optimized Recognition', frame)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Performance report
    print("\n" + "="*60)
    print("PERFORMANCE REPORT")
    print("="*60)
    print(f"Total frames: {frame_count}")
    print(f"Average FPS: {int(avg_fps)}")
    print(f"Total recognitions: {recognition_count}")
    print(f"Total time: {total_time:.2f}s")

if __name__ == '__main__':
    main()
