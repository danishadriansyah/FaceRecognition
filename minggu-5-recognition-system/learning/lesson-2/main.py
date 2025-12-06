"""
Lesson 2: Recognition Service & Real-time Recognition
Real-time webcam recognition with hybrid approach
"""
import os
import sys

# Add Week 4 modules
week4_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'minggu-4-dataset-database', 'learning', 'lesson-2')
sys.path.insert(0, week4_path)

from recognition_service import RecognitionService

def main():
    print("="*60)
    print("LESSON 2: Real-time Recognition with Hybrid Approach")
    print("="*60)
    
    # Step 1: Initialize Recognition Service
    print("\n📊 Step 1: Initialize Recognition Service")
    print("-" * 60)
    
    # XAMPP Default: root user, no password
    connection_string = "mysql+pymysql://root:@localhost:3306/face_recognition_db"
    
    print("💡 Initializing hybrid system:")
    print("   - MediaPipe: Detection (10-15ms)")
    print("   - DeepFace: Recognition (100-150ms)")
    print("   - Target: 6-9 FPS real-time\n")
    
    try:
        service = RecognitionService(
            db_connection_string=connection_string,
            model_name='Facenet512',
            threshold=0.6  # Adjust for accuracy
        )
    except Exception as e:
        print(f"\n❌ Failed to initialize service: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. XAMPP MySQL running")
        print("   2. Week 4 Lesson 2 completed (database with persons)")
        print("   3. Week 5 Lesson 1 completed (encodings generated)")
        print("   4. Check HeidiSQL: face_encodings table has data")
        print("   5. Install: pip install deepface mediapipe")
        return
    
    # Step 2: Check loaded data
    print("\n📊 Step 2: Loaded Data")
    print("-" * 60)
    
    if len(service.known_persons) == 0:
        print("❌ No persons found in database!")
        print("\n💡 Complete these first:")
        print("   1. Week 4 Lesson 1: Capture faces")
        print("   2. Week 4 Lesson 2: Store to database")
        print("   3. Week 5 Lesson 1: Generate encodings")
        service.close()
        return
    
    print(f"✅ Ready for recognition!")
    print(f"   Known persons: {len(service.known_persons)}")
    print(f"   Total encodings: {len(service.known_encodings)}")
    print(f"   Recognition threshold: {service.threshold}")
    
    # Step 3: Threshold explanation
    print("\n📊 Step 3: Understanding Threshold")
    print("-" * 60)
    print("Threshold determines matching strictness:")
    print("   • 0.4: Very strict (high security, may reject valid faces)")
    print("   • 0.6: Balanced (default, good for general use)")
    print("   • 0.8: Lenient (more matches, some false positives)")
    print(f"\nCurrent threshold: {service.threshold}")
    
    # Step 4: Real-time Recognition
    print("\n📊 Step 4: Start Real-time Recognition")
    print("-" * 60)
    print("\n🎥 Opening webcam...")
    print("📌 Tips:")
    print("   - Look directly at camera")
    print("   - Ensure good lighting")
    print("   - Face should be 100+ pixels")
    print("   - Press 'q' to quit\n")
    
    input("Press ENTER to start webcam recognition...")
    
    # Start recognition
    service.process_webcam(camera_id=0)
    
    # Summary
    print("\n" + "="*60)
    print("✅ RECOGNITION SESSION COMPLETE!")
    print("="*60)
    
    stats = service.get_stats()
    
    print(f"\n📊 Session Statistics:")
    print(f"   Total frames processed: {stats['frames']}")
    print(f"   Session duration: {stats['elapsed']:.2f}s")
    print(f"   Average FPS: {stats['fps']:.2f}")
    print(f"   Detection speed: {stats['avg_detection_ms']:.2f}ms")
    print(f"   Recognition speed: {stats['avg_recognition_ms']:.2f}ms")
    print(f"   Total per frame: {stats['total_avg_ms']:.2f}ms")
    
    # Performance Analysis
    print(f"\n📊 Performance Analysis:")
    target_fps = 6
    actual_fps = stats['fps']
    
    if actual_fps >= target_fps:
        print(f"   ✅ Real-time capable! ({actual_fps:.1f} FPS >= {target_fps} FPS)")
    else:
        print(f"   ⚠️  Below target ({actual_fps:.1f} FPS < {target_fps} FPS)")
        print("   💡 Optimization tips:")
        print("      - Process every Nth frame (frame skipping)")
        print("      - Lower camera resolution")
        print("      - Use SFace model (faster, 95% accuracy)")
    
    # Comparison with other methods
    print(f"\n📊 Comparison with Other Methods:")
    print("-" * 60)
    print("Method                 | Speed      | Accuracy | Real-time?")
    print("-" * 60)
    print("MediaPipe only (Week 3)| 30+ FPS    | ~85%     | ✅ Yes")
    print("DeepFace only          | 3-4 FPS    | 97%+     | ❌ No")
    print(f"Hybrid (current)       | {actual_fps:.1f} FPS    | 97%+     | {'✅ Yes' if actual_fps >= 6 else '⚠️  Borderline'}")
    print("-" * 60)
    
    print("\n💡 Next Steps:")
    print("   - Week 6: Build attendance system using this recognition")
    print("   - Week 7: Desktop GUI with webcam integration")
    print("   - Tune threshold for your use case")
    print("   - Add more persons to database")
    
    service.close()

if __name__ == '__main__':
    main()
