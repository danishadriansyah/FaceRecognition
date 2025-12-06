"""
📝 TUGAS MINGGU 5 - Recognition Service (Fill in the Blanks)
Total: 5 soal - Complete recognition pipeline with database

Soal:
1. Import RecognitionService dari recognition_service
2. Set up detector dan recognizer modules
3. Process image dan tampilkan hasil
4. Implementasi webcam processing dengan visualization
5. Get dan display statistics
"""

import cv2
import sys
import os
import numpy as np
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'project'))

# SOAL 1: Import RecognitionService
# Hint: from recognition_service import RecognitionService
from recognition_service import _____________


def setup_service():
    """Setup recognition service with database"""
    print("Setting up Recognition Service...")
    
    # Initialize service with database
    try:
        # SOAL 2: Initialize RecognitionService with MySQL database
        # Hint: service = RecognitionService(connection_string="mysql+pymysql://...")
        service = ________________(
            connection_string="mysql+pymysql://root:@localhost:3306/face_recognition_db"
        )
        print("✅ Service initialized with database")
        return service
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def process_single_image(service):
    """Process single image"""
    print("\nProcess Single Image")
    print("-" * 50)
    
    # Get image path from user
    img_path = input("Enter image path: ").strip()
    
    if not os.path.exists(img_path):
        print(f"❌ Image not found: {img_path}")
        return
    
    try:
        # Load image
        image = cv2.imread(img_path)
        
        # SOAL 3: Process image using service
        # Hint: result = service.process_image(image)
        result = service._____________(image)
        
        # Display results
        print(f"\nResults:")
        print(f"  Faces detected: {result['count']}")
        for person in result['people']:
            print(f"    - {person['name']} (confidence: {person['confidence']:.2f})")
        
        # Show image with annotations
        if 'faces' in result and result['faces']:
            print(f"  Faces extracted: {len(result['faces'])}")
    
    except Exception as e:
        print(f"❌ Error processing image: {e}")


def process_webcam(service):
    """Real-time webcam recognition"""
    print("\nWebcam Recognition")
    print("-" * 50)
    print("Press 'q' to quit, 's' to save screenshot")
    
    try:
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame")
                break
            
            frame_count += 1
            
            # SOAL 4: Process webcam frame
            # Hint: annotated_frame, results = service.process_webcam_frame(frame)
            annotated_frame, results = service._________________(frame)
            
            # Add frame info
            cv2.putText(annotated_frame, f"Frame: {frame_count}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Faces: {len(results)}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Display
            cv2.imshow('Recognition', annotated_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                filename = f"screenshot_{frame_count}.jpg"
                cv2.imwrite(filename, annotated_frame)
                print(f"  Saved: {filename}")
        
        cap.release()
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"❌ Error: {e}")


def show_statistics(service):
    """Display recognition statistics"""
    print("\nStatistics")
    print("-" * 50)
    
    # SOAL 5: Get and display statistics
    # Hint: stats = service.get_statistics()
    stats = service._____________()
    
    print(f"  Total processed: {stats['total_processed']}")
    print(f"  Total recognized: {stats['total_recognized']}")
    print(f"  Total unknown: {stats['total_unknown']}")
    print(f"  Recognition rate: {stats['recognition_rate']:.1%}")
    print(f"  Avg processing time: {stats['avg_processing_time']:.3f}s")


def main():
    """Main menu"""
    print("\n" + "="*50)
    print("MINGGU 5 - RECOGNITION SERVICE TEST")
    print("="*50)
    
    # Setup service
    service = setup_service()
    if service is None:
        print("Failed to setup service")
        return
    
    while True:
        print("\n" + "-"*50)
        print("1. Process single image")
        print("2. Real-time webcam")
        print("3. Show statistics")
        print("4. Reset statistics")
        print("5. Exit")
        print("-"*50)
        
        choice = input("Choose option (1-5): ").strip()
        
        if choice == '1':
            process_single_image(service)
        elif choice == '2':
            process_webcam(service)
        elif choice == '3':
            show_statistics(service)
        elif choice == '4':
            service.reset_statistics()
            print("✅ Statistics reset")
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
