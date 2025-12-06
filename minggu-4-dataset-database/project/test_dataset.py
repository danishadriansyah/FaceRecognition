"""
Test Dataset Manager
Week 4 Project Module - Progressive Web Application (Database Mode)

Tests for dataset management functionality with MySQL database
"""

import sys
import os
import numpy as np
import cv2

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from dataset_manager import DatasetManager


# Database connection string (XAMPP default)
TEST_DB_CONNECTION = "mysql+pymysql://root:@localhost:3306/face_recognition_db"


def test_initialization():
    """Test dataset manager initialization"""
    print("Test 1: Initialization")
    
    try:
        manager = DatasetManager(
            connection_string=TEST_DB_CONNECTION,
            image_storage_path="test_output/test_images"
        )
        print("✓ Dataset manager initialized (Database mode)")
        print(f"  Database: face_recognition_db")
        print(f"  Image storage: test_output/test_images")
        manager.close()
        return True
    except ConnectionError as e:
        print(f"✗ Connection failed: {e}")
        print("  💡 Make sure XAMPP MySQL is running")
        return False


def test_add_person():
    """Test adding person to database"""
    print("\nTest 2: Add Person to Database")
    
    try:
        manager = DatasetManager(TEST_DB_CONNECTION, "test_output/test_images")
        
        person_id = manager.add_person(
            name="Test User Alice",
            employee_id="TEST001",
            department="IT"
        )
        
        assert person_id is not None
        print(f"✓ Person added to database with ID: {person_id}")
        
        people = manager.list_people()
        print(f"✓ Total people in database: {len(people)}")
        
        manager.close()
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_capture_face():
    """Test capturing face image to database"""
    print("\nTest 3: Capture Face to Database")
    
    try:
        manager = DatasetManager(TEST_DB_CONNECTION, "test_output/test_images")
        
        # Add person first
        person_id = manager.add_person("Test User Bob", "TEST002", "HR")
        
        # Create test face image
        test_face = np.ones((200, 200, 3), dtype=np.uint8) * 180
        cv2.circle(test_face, (70, 80), 10, (0, 0, 0), -1)
        cv2.circle(test_face, (130, 80), 10, (0, 0, 0), -1)
        
        # Capture face
        image_id = manager.capture_face(person_id, test_face, angle="frontal")
        
        assert image_id is not None
        print(f"✓ Face captured and saved to database (ID: {image_id})")
        
        # Verify in database
        images = manager.get_person_images(person_id)
        print(f"✓ Verified: {len(images)} images in database for person {person_id}")
        
        manager.close()
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_validate_face_image():
    """Test face image validation"""
    print("\nTest 4: Validate Face Image")
    
    try:
        manager = DatasetManager(TEST_DB_CONNECTION, "test_output/test_images")
        
        # Good image
        good_image = np.ones((200, 200, 3), dtype=np.uint8) * 150
        is_valid, msg, score = manager.validate_face_image(good_image)
        print(f"✓ Good image validation: {is_valid}, score: {score:.2f}")
        
        # Too small
        small_image = np.ones((50, 50, 3), dtype=np.uint8) * 150
        is_valid, msg, score = manager.validate_face_image(small_image)
        print(f"✓ Small image validation: {is_valid}, reason: {msg}")
        assert not is_valid
        
        # Too dark
        dark_image = np.ones((200, 200, 3), dtype=np.uint8) * 20
        is_valid, msg, score = manager.validate_face_image(dark_image)
        print(f"✓ Dark image validation: {is_valid}, reason: {msg}")
        assert not is_valid
        
        manager.close()
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_get_person_images():
    """Test getting person images from database"""
    print("\nTest 5: Get Person Images from Database")
    
    try:
        manager = DatasetManager(TEST_DB_CONNECTION, "test_output/test_images")
        
        # Add person and capture multiple faces
        person_id = manager.add_person("Test User Charlie", "TEST003", "Engineering")
        
        test_face = np.ones((200, 200, 3), dtype=np.uint8) * 180
        cv2.circle(test_face, (70, 80), 10, (0, 0, 0), -1)
        cv2.circle(test_face, (130, 80), 10, (0, 0, 0), -1)
        
        manager.capture_face(person_id, test_face, angle="frontal")
        manager.capture_face(person_id, test_face, angle="left")
        manager.capture_face(person_id, test_face, angle="right")
        
        images = manager.get_person_images(person_id)
        assert len(images) == 3
        print(f"✓ Retrieved {len(images)} images for person {person_id}")
        for img in images:
            print(f"  - {img['angle']}: quality={img['quality_score']:.2f}")
        
        manager.close()
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_generate_encodings():
    """Test generating encodings with DeepFace"""
    print("\nTest 6: Generate Encodings with DeepFace")
    
    try:
        manager = DatasetManager(TEST_DB_CONNECTION, "test_output/test_images")
        
        # Get all people
        people = manager.list_people()
        if len(people) == 0:
            print("⚠️  No people in database, skipping encoding test")
            manager.close()
            return True
        
        print(f"  Generating encodings for {len(people)} people...")
        count = manager.generate_encodings(model_name='Facenet512')
        
        print(f"✓ Generated {count} encodings")
        print("  💡 View in HeidiSQL: SELECT * FROM face_encodings;")
        
        manager.close()
        return True
    except ImportError:
        print("⚠️  DeepFace not installed")
        print("  Install: pip install deepface tensorflow")
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_get_statistics():
    """Test dataset statistics from database"""
    print("\nTest 7: Get Statistics from Database")
    
    try:
        manager = DatasetManager(TEST_DB_CONNECTION, "test_output/test_images")
        
        stats = manager.get_statistics()
        print(f"✓ Dataset statistics:")
        print(f"  - Total persons: {stats.get('total_persons', 0)}")
        print(f"  - Total images: {stats.get('total_images', 0)}")
        print(f"  - Total encodings: {stats.get('total_encodings', 0)}")
        
        if 'people_by_department' in stats:
            print(f"  - By department:")
            for dept, count in stats['people_by_department'].items():
                print(f"      {dept}: {count}")
        
        manager.close()
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_validate_dataset():
    """Test dataset validation"""
    print("\nTest 8: Validate Dataset")
    
    try:
        manager = DatasetManager(TEST_DB_CONNECTION, "test_output/test_images")
        
        report = manager.validate_dataset()
        print(f"✓ Validation report:")
        print(f"  - Total people: {report['total_people']}")
        print(f"  - Total images: {report['total_images']}")
        print(f"  - Total encodings: {report['total_encodings']}")
        print(f"  - Valid people: {report['valid_people']}")
        
        if report['issues']:
            print(f"  - Issues ({len(report['issues'])}):")
            for issue in report['issues'][:5]:  # Show first 5
                print(f"      {issue}")
        
        manager.close()
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def cleanup():
    """Cleanup test images (keep database for Week 5)"""
    print("\nCleanup: Removing test image files...")
    import shutil
    if os.path.exists("test_output"):
        shutil.rmtree("test_output")
        print("✓ Test images removed")
    print("💡 Database entries kept for Week 5 integration")
    print("   To clear database: Use HeidiSQL or run Week 4 Lesson 2")


if __name__ == "__main__":
    print("="*60)
    print("Dataset Manager Tests - Database Mode (Week 4 Project)")
    print("="*60)
    
    print("\n💡 Prerequisites:")
    print("   1. XAMPP MySQL running")
    print("   2. Database 'face_recognition_db' created")
    print("   3. Run Week 4 Lesson 2 first")
    print("   4. Check HeidiSQL: Tables should exist")
    
    response = input("\nPress Enter to start tests, or 'q' to quit: ")
    if response.lower() == 'q':
        print("Tests cancelled")
        sys.exit(0)
    
    # Run tests
    tests = [
        test_initialization,
        test_add_person,
        test_capture_face,
        test_validate_face_image,
        test_get_person_images,
        test_generate_encodings,
        test_get_statistics,
        test_validate_dataset
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
            else:
                failed += 1
        except KeyboardInterrupt:
            print("\n\nTests interrupted by user")
            break
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("✅ All tests passed!")
        print("\nNext steps:")
        print("  1. Verify in HeidiSQL: Press F5 to refresh")
        print("  2. Check tables: persons, face_images, face_encodings")
        print("  3. Use in Week 5: RecognitionService")
    else:
        print("⚠️  Some tests failed")
        print("\nTroubleshooting:")
        print("  1. Check XAMPP MySQL is running")
        print("  2. Verify database exists in HeidiSQL")
        print("  3. Run Week 4 Lesson 2 to create tables")
    
    # Ask for cleanup
    response = input("\nCleanup test images? (y/n): ")
    if response.lower() == 'y':
        cleanup()

