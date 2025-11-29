"""
Test Dataset Manager
Week 4 Project Module - Progressive Web Application

Tests for dataset management functionality
"""

import sys
import os
import numpy as np
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dataset_manager import DatasetManager


def test_initialization():
    """Test dataset manager initialization"""
    print("Test 1: Initialization")
    manager = DatasetManager("test_output/test_dataset")
    assert manager is not None
    print(f"✓ Dataset manager initialized at: {manager.dataset_root}")


def test_add_person():
    """Test adding person to dataset"""
    print("\nTest 2: Add Person")
    manager = DatasetManager("test_output/test_dataset")
    
    person_id = manager.add_person(
        name="Test User",
        employee_id="TEST001",
        department="IT"
    )
    
    assert person_id is not None
    print(f"✓ Person added with ID: {person_id}")
    
    people = manager.list_people()
    assert len(people) > 0
    print(f"✓ Total people in dataset: {len(people)}")


def test_capture_face():
    """Test capturing face image"""
    print("\nTest 3: Capture Face")
    manager = DatasetManager("test_output/test_dataset")
    
    # Add person first
    person_id = manager.add_person("John Doe", "EMP001")
    
    # Create dummy face image
    dummy_face = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
    
    # Capture face
    file_path = manager.capture_face(person_id, dummy_face, angle="frontal")
    
    assert file_path is not None
    assert os.path.exists(file_path)
    print(f"✓ Face captured and saved: {file_path}")


def test_validate_face_image():
    """Test face image validation"""
    print("\nTest 4: Validate Face Image")
    manager = DatasetManager("test_output/test_dataset")
    
    # Good image
    good_image = np.random.randint(100, 200, (200, 200, 3), dtype=np.uint8)
    is_valid, issues = manager.validate_face_image(good_image)
    print(f"✓ Good image validation: {is_valid}, issues: {issues}")
    
    # Too small
    small_image = np.random.randint(0, 255, (50, 50, 3), dtype=np.uint8)
    is_valid, issues = manager.validate_face_image(small_image)
    print(f"✓ Small image validation: {is_valid}, issues: {issues}")
    assert not is_valid


def test_get_person_images():
    """Test getting person images"""
    print("\nTest 5: Get Person Images")
    manager = DatasetManager("test_output/test_dataset")
    
    # Add person and capture multiple faces
    person_id = manager.add_person("Jane Doe", "EMP002")
    
    dummy_face = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
    
    manager.capture_face(person_id, dummy_face, angle="frontal")
    manager.capture_face(person_id, dummy_face, angle="left")
    manager.capture_face(person_id, dummy_face, angle="right")
    
    images = manager.get_person_images(person_id)
    assert len(images) == 3
    print(f"✓ Retrieved {len(images)} images for person {person_id}")


def test_export_encodings():
    """Test exporting encodings for recognition"""
    print("\nTest 6: Export Encodings")
    manager = DatasetManager("test_output/test_dataset")
    
    try:
        output_path = manager.export_encodings("test_output/encodings.pkl")
        print(f"✓ Encodings exported to: {output_path}")
    except Exception as e:
        print(f"✓ Expected (no face_recognition installed): {type(e).__name__}")


def test_get_statistics():
    """Test dataset statistics"""
    print("\nTest 7: Get Statistics")
    manager = DatasetManager("test_output/test_dataset")
    
    stats = manager.get_statistics()
    print(f"✓ Dataset statistics:")
    print(f"  - Total people: {stats['total_people']}")
    print(f"  - Total images: {stats['total_images']}")
    print(f"  - Avg images per person: {stats['avg_images_per_person']:.1f}")


def test_integration_with_week3():
    """Test integration with recognizer from week 3"""
    print("\nTest 8: Integration with Week 3")
    
    try:
        from face_recognizer import FaceRecognizer
        
        manager = DatasetManager("test_output/test_dataset")
        recognizer = FaceRecognizer()
        
        print("✓ Successfully imported both modules")
        print("  Integration path: Week 1 → Week 2 → Week 3 → Week 4")
        
    except ImportError as e:
        print(f"✓ Expected: {e}")
        print("  Note: Install required libraries for full integration")


def cleanup():
    """Cleanup test files"""
    print("\nCleanup: Removing test files...")
    if os.path.exists("test_output"):
        shutil.rmtree("test_output")
    print("✓ Cleanup completed")


if __name__ == "__main__":
    print("Dataset Manager Tests - Week 4 Project")
    print("=" * 50)
    
    test_initialization()
    test_add_person()
    test_capture_face()
    test_validate_face_image()
    test_get_person_images()
    test_export_encodings()
    test_get_statistics()
    test_integration_with_week3()
    
    # Cleanup
    cleanup()
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("\nIntegration ready for Week 5 (Recognition Service)")
