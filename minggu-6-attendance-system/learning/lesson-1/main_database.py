"""
Lesson 1: Attendance Logic & Real-time Tracking
Real-time attendance check-in with webcam + face recognition
"""
import os
import sys
import cv2
import time

# Add Week 5 modules
week5_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'minggu-5-recognition-system', 'learning', 'lesson-2')
sys.path.insert(0, week5_path)

from recognition_service import RecognitionService
from attendance_system import AttendanceSystem

def main():
    print("="*60)
    print("LESSON 1: Attendance Logic & Real-time Tracking")
    print("="*60)
    
    # XAMPP Default: root user, no password
    connection_string = "mysql+pymysql://root:@localhost:3306/face_recognition_db"
    
    # Step 1: Initialize Attendance System
    print("\n📊 Step 1: Initialize Attendance System")
    print("-" * 60)
    
    try:
        attendance_system = AttendanceSystem(connection_string)
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. XAMPP MySQL running")
        print("   2. Week 4 Lesson 2 completed (database setup)")
        print("   3. Check HeidiSQL: persons & face_encodings tables have data")
        return
    
    # Step 2: Initialize Recognition Service
    print("\n📊 Step 2: Initialize Recognition Service")
    print("-" * 60)
    
    try:
        recognition_service = RecognitionService(
            db_connection_string=connection_string,
            model_name='Facenet512',
            threshold=0.6
        )
    except Exception as e:
        print(f"❌ Failed to initialize recognition: {e}")
        print("\n💡 Complete Week 5 first (hybrid recognition)")
        print("   Check HeidiSQL: face_encodings table should have data")
        attendance_system.close()
        return
    
    if len(recognition_service.known_persons) == 0:
        print("❌ No persons in database!")
        print("\n💡 Complete Week 5 Lesson 1 (generate encodings)")
        recognition_service.close()
        attendance_system.close()
        return
    
    # Step 3: Display Business Rules
    print("\n📊 Step 3: Business Rules")
    print("-" * 60)
    print(f"Working hours: {attendance_system.WORK_START.strftime('%H:%M')} - {attendance_system.WORK_END.strftime('%H:%M')}")
    print(f"Late threshold: {attendance_system.LATE_THRESHOLD.strftime('%H:%M')}")
    print(f"Early leave: < {attendance_system.EARLY_LEAVE.strftime('%H:%M')}")
    print(f"Min confidence: {attendance_system.MIN_CONFIDENCE}%")
    
    # Step 4: Show Today's Statistics
    print("\n📊 Step 4: Today's Statistics (Before)")
    print("-" * 60)
    
    stats = attendance_system.get_statistics()
    print(f"Date: {stats['date']}")
    print(f"Total persons: {stats['total_persons']}")
    print(f"Present: {stats['present']}")
    print(f"Absent: {stats['absent']}")
    print(f"On time: {stats['on_time']}")
    print(f"Late: {stats['late']}")
    print(f"Attendance rate: {stats['attendance_rate']:.1f}%")
    
    # Step 5: Real-time Check-in
    print("\n📊 Step 5: Real-time Attendance Check-in")
    print("-" * 60)
    print("\n🎥 Opening webcam for automatic check-in...")
    print("📌 How it works:")
    print("   1. Face detected → Recognized")
    print("   2. If confidence >= 75% → Auto check-in")
    print("   3. Duplicate prevention (one check-in per day)")
    print("   4. Status calculated (On Time / Late)")
    print("\n💡 Press 'q' to quit\n")
    
    input("Press ENTER to start real-time check-in...")
    
    # Detect and select camera
    print("\n🔍 Detecting cameras...")
    available_cameras = detect_available_cameras()
    camera_id = select_camera(available_cameras)
    
    if camera_id is None:
        print("❌ Camera selection cancelled")
        recognition_service.close()
        attendance_system.close()
        return
    
    # Open selected webcam
    print(f"\n🎬 Opening camera {camera_id}...")
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"❌ Failed to open camera {camera_id}")
        recognition_service.close()
        attendance_system.close()
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print(f"Camera: {int(cap.get(3))}x{int(cap.get(4))}")
    print("Starting automatic check-in...\n")
    
    # Track already processed persons in this session
    processed_this_session = set()
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Process frame with recognition
        annotated_frame, recognitions = recognition_service.process_frame(frame)
        
        # Display info on frame
        cv2.putText(annotated_frame, "Attendance Check-in System", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(annotated_frame, f"Frame: {frame_count}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Process recognitions for check-in
        for name, confidence, bbox in recognitions:
            if name != "Unknown":
                # Find person ID
                person_id = None
                for person in recognition_service.known_persons:
                    if person.name == name:
                        person_id = person.id
                        break
                
                if person_id and person_id not in processed_this_session:
                    # Attempt check-in
                    success, message, record = attendance_system.check_in(person_id, confidence)
                    
                    print(f"\nFrame {frame_count:04d}:")
                    print(f"   👤 Recognized: {name} ({confidence:.1f}%)")
                    print(f"   {message}")
                    
                    if success:
                        # Add to processed set
                        processed_this_session.add(person_id)
                        
                        # Visual feedback
                        cv2.putText(annotated_frame, "CHECK-IN SUCCESS!", (10, 90),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Show frame
        cv2.imshow('Attendance Check-in System', annotated_frame)
        
        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Step 6: Final Statistics
    print("\n📊 Step 6: Today's Statistics (After)")
    print("-" * 60)
    
    stats = attendance_system.get_statistics()
    print(f"Date: {stats['date']}")
    print(f"Total persons: {stats['total_persons']}")
    print(f"Present: {stats['present']}")
    print(f"Absent: {stats['absent']}")
    print(f"On time: {stats['on_time']}")
    print(f"Late: {stats['late']}")
    print(f"Attendance rate: {stats['attendance_rate']:.1f}%")
    
    # Show attendance list
    print("\n📊 Today's Attendance List:")
    print("-" * 60)
    attendances = attendance_system.get_today_attendance()
    
    if attendances:
        print(f"{'Name':<20} {'Check-in':<10} {'Status':<20} {'Confidence':<12}")
        print("-" * 60)
        for att in attendances:
            check_in_str = att.check_in.strftime('%H:%M:%S')
            print(f"{att.person.name:<20} {check_in_str:<10} {att.status:<20} {att.confidence:.1f}%")
    else:
        print("No attendance records today")
    
    # Summary
    print("\n" + "="*60)
    print("✅ ATTENDANCE SESSION COMPLETE!")
    print("="*60)
    print(f"Processed {len(processed_this_session)} check-ins this session")
    print("\n💡 Next Steps:")
    print("   - Lesson 2: Generate reports & analytics")
    print("   - Export attendance to Excel/CSV")
    print("   - Monthly attendance summary")
    
    recognition_service.close()
    attendance_system.close()

if __name__ == '__main__':
    main()
