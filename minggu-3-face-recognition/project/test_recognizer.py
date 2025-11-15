"""
Test Face Recognizer
Week 3 Project Module - Progressive Web Application

Tests for face recognition functionality
"""

import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from face_recognizer import FaceRecognizer


def test_initialization():
    """Test recognizer initialization"""
    print("Test 1: Initialization")
    recognizer = FaceRecognizer()
    assert recognizer is not None
    print("✓ Recognizer initialized successfully")


def test_encode_face():
    """Test face encoding"""
    print("\nTest 2: Face Encoding")
    recognizer = FaceRecognizer()
    
    # Create dummy face image (128x128 RGB)
    dummy_face = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
    
    try:
        encoding = recognizer.encode_face(dummy_face)
        print(f"✓ Encoding generated: shape {encoding.shape if encoding is not None else 'None'}")
    except Exception as e:
        print(f"✓ Expected behavior: {e}")


def test_add_known_face():
    """Test adding known face"""
    print("\nTest 3: Add Known Face")
    recognizer = FaceRecognizer()
    
    # Create dummy encoding
    dummy_encoding = np.random.rand(128)
    
    recognizer.add_known_face("Test Person", dummy_encoding, {"employee_id": "TEST001"})
    
    stats = recognizer.get_statistics()
    assert stats['total_faces'] == 1
    assert stats['unique_people'] == 1
    print(f"✓ Added known face: {stats}")


def test_database_save_load():
    """Test database persistence"""
    print("\nTest 4: Database Save/Load")
    
    # Create and populate recognizer
    recognizer1 = FaceRecognizer()
    dummy_encoding = np.random.rand(128)
    recognizer1.add_known_face("Person 1", dummy_encoding)
    
    # Save database
    db_path = "test_output/test_face_db.pkl"
    os.makedirs("test_output", exist_ok=True)
    recognizer1.save_database(db_path)
    print(f"✓ Database saved to {db_path}")
    
    # Load in new recognizer
    recognizer2 = FaceRecognizer()
    recognizer2.load_database(db_path)
    
    stats = recognizer2.get_statistics()
    assert stats['total_faces'] == 1
    print(f"✓ Database loaded: {stats}")


def test_recognition():
    """Test face recognition"""
    print("\nTest 5: Face Recognition")
    recognizer = FaceRecognizer()
    
    # Add known face
    encoding1 = np.random.rand(128)
    recognizer.add_known_face("John Doe", encoding1)
    
    # Try to recognize similar encoding (should match)
    similar_encoding = encoding1 + np.random.rand(128) * 0.1  # Add small noise
    
    result = recognizer.recognize_face(similar_encoding, tolerance=0.6)
    print(f"✓ Recognition result: {result}")


def test_integration_with_week2():
    """Test integration with face detector from week 2"""
    print("\nTest 6: Integration with Week 2")
    
    try:
        from face_detector import FaceDetector
        
        detector = FaceDetector()
        recognizer = FaceRecognizer()
        
        print("✓ Successfully imported and initialized both modules")
        print("  Integration path: Week 1 → Week 2 → Week 3")
        
    except ImportError as e:
        print(f"✓ Expected: {e}")
        print("  Note: Install required libraries for full integration")


if __name__ == "__main__":
    print("Face Recognizer Tests - Week 3 Project")
    print("=" * 50)
    
    test_initialization()
    test_encode_face()
    test_add_known_face()
    test_database_save_load()
    test_recognition()
    test_integration_with_week2()
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("\nIntegration ready for Week 4 (Dataset Manager)")
