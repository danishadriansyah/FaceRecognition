"""
Lesson 2: Database Setup & Store Dataset
Setup MySQL database and store captured faces to database
"""
import os
import sys
from datetime import datetime
import numpy as np
import pickle

# Import our database modules
from database import Database
from models import Person, FaceImage, FaceEncoding, Base

def main():
    print("="*60)
    print("LESSON 2: Database Setup & Store Dataset")
    print("="*60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    captured_dir = os.path.join(script_dir, '..', 'lesson-1', 'captured_faces')
    
    # Check if we have captured faces
    if not os.path.exists(captured_dir) or not os.listdir(captured_dir):
        print("\n❌ No captured faces found!")
        print("💡 Run Lesson 1 first to capture faces")
        return
    
    # Step 1: Connect to database
    print("\n📊 Step 1: Connect to Database")
    print("-" * 60)
    
    # XAMPP Default: root user, no password
    # If you set password in XAMPP: mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/face_recognition_db
    connection_string = "mysql+pymysql://root:@localhost:3306/face_recognition_db"
    
    print("💡 Connection string:")
    print(f"   {connection_string}")
    print("\n⚠️  Make sure:")
    print("   1. XAMPP Control Panel → MySQL is running (green status)")
    print("   2. Database 'face_recognition_db' created in HeidiSQL")
    print("   3. Username: root, Password: (empty for default XAMPP)")
    
    db = Database(connection_string)
    
    if not db.connect():
        print("\n❌ Database connection failed!")
        print("\n💡 Create database in HeidiSQL:")
        print("   1. Open HeidiSQL")
        print("   2. Right-click → Create new → Database")
        print("   3. Name: face_recognition_db")
        print("   4. Collation: utf8mb4_general_ci")
        print("\n   OR use MySQL command: CREATE DATABASE face_recognition_db;")
        return
    
    # Step 2: Create tables
    print("\n📊 Step 2: Create Tables")
    print("-" * 60)
    
    if not db.create_tables():
        print("❌ Failed to create tables")
        return
    
    print("✅ Tables created:")
    print("   - persons (id, employee_id, name, department)")
    print("   - face_images (id, person_id, image_path, quality_score)")
    print("   - face_encodings (id, person_id, encoding_data)")
    
    # Step 3: Store captured faces to database
    print("\n📊 Step 3: Store Captured Faces to Database")
    print("-" * 60)
    
    session = db.get_session()
    stored_count = 0
    
    for person_name in os.listdir(captured_dir):
        person_path = os.path.join(captured_dir, person_name)
        if not os.path.isdir(person_path):
            continue
        
        # Generate employee ID
        employee_id = f"EMP{stored_count + 1:04d}"
        
        # Create Person record
        person = Person(
            employee_id=employee_id,
            name=person_name,
            department="Engineering"  # Default department
        )
        session.add(person)
        session.flush()  # Get person.id
        
        print(f"\n👤 Storing: {person_name} (ID: {employee_id})")
        
        # Store face images
        image_count = 0
        for filename in os.listdir(person_path):
            if filename.endswith(('.jpg', '.png', '.jpeg')):
                image_path = os.path.join(person_path, filename)
                
                # Get image info
                file_size = os.path.getsize(image_path)
                
                # Create FaceImage record
                face_image = FaceImage(
                    person_id=person.id,
                    image_path=image_path,
                    quality_score=0.95,  # Placeholder (will be real score in Week 5)
                    file_size=file_size
                )
                session.add(face_image)
                image_count += 1
        
        # Create placeholder encoding (real encoding will be generated in Week 5)
        # For now, just store dummy data to complete the schema
        dummy_encoding = np.random.rand(512).astype(np.float32)  # 512-d vector
        encoding_bytes = pickle.dumps(dummy_encoding)
        
        face_encoding = FaceEncoding(
            person_id=person.id,
            encoding_data=encoding_bytes,
            model_name='Facenet512',
            confidence=0.0  # Will be real confidence in Week 5
        )
        session.add(face_encoding)
        
        print(f"   ✅ Stored {image_count} images")
        stored_count += 1
    
    # Commit all changes
    session.commit()
    
    # Step 4: Display statistics
    print("\n📊 Step 4: Database Statistics")
    print("-" * 60)
    
    stats = db.get_statistics()
    
    print(f"✅ Total Persons: {stats['total_persons']}")
    print(f"✅ Total Face Images: {stats['total_images']}")
    print(f"✅ Total Encodings: {stats['total_encodings']}")
    
    # Summary
    print("\n" + "="*60)
    print("✅ DATABASE SETUP COMPLETE!")
    print("="*60)
    print(f"Database: face_recognition_db")
    print(f"Stored persons: {stats['total_persons']}")
    print(f"Stored images: {stats['total_images']}")
    
    print("\n💡 View in HeidiSQL:")
    print("   1. Refresh database (F5)")
    print("   2. Check tables: persons, face_images, face_encodings")
    print("   3. Double-click table to view data")
    
    print("\n💡 Next Steps:")
    print("   - Week 5: Generate real face encodings with DeepFace")
    print("   - Week 5: Build recognition system")
    print("   - Week 6: Attendance tracking")
    
    db.close()

if __name__ == '__main__':
    main()
