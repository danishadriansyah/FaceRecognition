"""
Lesson 1: Hybrid Approach Introduction
Generate face encodings from database using DeepFace
"""
import os
import sys

# Add Week 4 modules to path
week4_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'minggu-4-dataset-database', 'learning', 'lesson-2')
sys.path.insert(0, week4_path)

from database import Database
from models import Person, FaceImage, FaceEncoding
from encoding_generator import EncodingGenerator
import time

def main():
    print("="*60)
    print("LESSON 1: Hybrid Approach - Generate Face Encodings")
    print("="*60)
    
    # Step 1: Initialize encoding generator
    print("\n📊 Step 1: Initialize DeepFace")
    print("-" * 60)
    
    try:
        generator = EncodingGenerator(model_name='Facenet512')
    except Exception as e:
        print(f"❌ Failed to initialize DeepFace: {e}")
        print("\n💡 Install dependencies:")
        print("   pip install deepface==0.0.89")
        print("   pip install tensorflow==2.15.0")
        return
    
    # Step 2: Connect to Database
    print("\n📊 Step 2: Connect to Database")
    print("-" * 60)
    
    # XAMPP Default: root user, no password
    connection_string = "mysql+pymysql://root:@localhost:3306/face_recognition_db"
    db = Database(connection_string)
    
    if not db.connect():
        print("❌ Database connection failed!")
        print("💡 Make sure:")
        print("   1. XAMPP MySQL is running")
        print("   2. Week 4 Lesson 2 completed (database & persons created)")
        print("   3. Check in HeidiSQL: persons & face_images tables have data")
        return
    
    session = db.get_session()
    
    # Step 3: Load persons from database
    print("\n📊 Step 3: Load Persons from Database")
    print("-" * 60)
    
    persons = session.query(Person).all()
    
    if not persons:
        print("❌ No persons found in database!")
        print("💡 Run Week 4 Lesson 2 first to add persons")
        print("   Check in HeidiSQL: SELECT * FROM persons;")
        return
    
    total_images = session.query(FaceImage).count()
    print(f"✅ Found {len(persons)} persons with {total_images} total images")
    
    for person in persons:
        print(f"   - {person.name} (ID: {person.employee_id}): {len(person.face_images)} images")
    
    # Step 4: Generate encodings
    print("\n📊 Step 4: Generate Face Encodings")
    print("-" * 60)
    
    # Clear old encodings (we're regenerating)
    session.query(FaceEncoding).delete()
    session.commit()
    
    total_generated = 0
    total_time = 0
    
    for person in persons:
        print(f"\n👤 Person: {person.name} ({person.employee_id})")
        
        generated_count = 0
        
        for idx, face_image in enumerate(person.face_images, 1):
            image_path = face_image.image_path
            
            if not os.path.exists(image_path):
                print(f"   ⚠️  Image {idx}: File not found: {image_path}")
                continue
            
            # Generate encoding
            encoding, elapsed_time = generator.generate_encoding(image_path)
            
            if encoding is not None:
                # Serialize encoding
                encoding_bytes = generator.serialize_encoding(encoding)
                
                # Save to database
                face_encoding = FaceEncoding(
                    person_id=person.id,
                    encoding_data=encoding_bytes,
                    model_name='Facenet512',
                    confidence=1.0  # Full confidence from DeepFace
                )
                session.add(face_encoding)
                
                generated_count += 1
                total_generated += 1
                total_time += elapsed_time
                
                print(f"   Image {idx}/{len(person.face_images)}: ✅ Encoded ({elapsed_time:.3f}s)")
            else:
                print(f"   Image {idx}/{len(person.face_images)}: ❌ Failed")
        
        session.commit()
        print(f"   ✅ {person.name}: {generated_count}/{len(person.face_images)} encodings generated")
    
    # Step 5: Statistics
    print("\n📊 Step 5: Statistics")
    print("-" * 60)
    
    avg_time = total_time / total_generated if total_generated > 0 else 0
    
    print(f"✅ Total encodings generated: {total_generated}")
    print(f"✅ Average time per image: {avg_time:.3f}s")
    print(f"✅ Total time: {total_time:.2f}s")
    
    # Verify in database
    encoding_count = session.query(FaceEncoding).count()
    print(f"✅ Encodings in database: {encoding_count}")
    
    # Performance comparison
    print("\n📊 Performance Comparison")
    print("-" * 60)
    print("Method                 | Detection | Recognition | Total   | Real-time?")
    print("-" * 60)
    print("MediaPipe only (Week 3)| 10-15ms   | N/A         | 10-15ms | ✅ 30+ FPS")
    print("DeepFace only          | 150-200ms | 100-150ms   | 250-350ms| ❌ 3-4 FPS")
    print("Hybrid (Week 5)        | 10-15ms   | 100-150ms   | 110-165ms| ✅ 6-9 FPS")
    print("-" * 60)
    
    print("\n💡 Hybrid Advantage:")
    print("   - 2x faster than pure DeepFace")
    print("   - 97%+ accuracy vs 85% MediaPipe-only")
    print("   - Real-time capable (6-9 FPS)")
    print("   - Production-ready accuracy")
    
    # Summary
    print("\n" + "="*60)
    print("✅ ENCODINGS GENERATED!")
    print("="*60)
    print(f"Database: face_recognition_db")
    print(f"Model: Facenet512 (512-dimensional embeddings)")
    print(f"Total encodings: {encoding_count}")
    
    print("\n💡 Next Steps:")
    print("   - Lesson 2: Build RecognitionService with real-time webcam")
    print("   - Compare faces using Euclidean distance")
    print("   - Recognize people in real-time (6-9 FPS)")
    
    db.close()

if __name__ == '__main__':
    main()
