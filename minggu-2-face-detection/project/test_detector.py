"""
Test Suite for Face Detector Module
Week 2 Project Testing
"""

import cv2
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from face_detector import FaceDetector


def create_test_image_with_face():
    """Create test image with a face-like pattern"""
    image = np.ones((480, 640, 3), dtype=np.uint8) * 200
    
    # Draw face-like pattern
    cv2.rectangle(image, (200, 150), (400, 400), (150, 150, 150), -1)
    cv2.circle(image, (270, 250), 20, (100, 100, 100), -1)
    cv2.circle(image, (330, 250), 20, (100, 100, 100), -1)
    cv2.ellipse(image, (300, 320), (40, 20), 0, 0, 180, (100, 100, 100), 2)
    
    return image


def test_detector_initialization():
    """Test detector initialization"""
    print("\nTesting: FaceDetector initialization")
    print("-" * 50)
    
    detector = FaceDetector()
    assert detector.face_cascade is not None, "Cascade not loaded"
    assert detector.scale_factor == 1.1, "Default scale factor incorrect"
    assert detector.min_neighbors == 5, "Default min neighbors incorrect"
    print("  PASS: Detector initialized successfully")
    
    return detector


def test_face_detection(detector):
    """Test basic face detection"""
    print("\nTesting: detect_faces()")
    print("-" * 50)
    
    test_image = create_test_image_with_face()
    faces = detector.detect_faces(test_image)
    
    assert isinstance(faces, list), "Should return list"
    print(f"  PASS: Detected {len(faces)} face(s)")
    
    if len(faces) > 0:
        x, y, w, h = faces[0]
        assert x >= 0 and y >= 0, "Invalid coordinates"
        assert w > 0 and h > 0, "Invalid dimensions"
        print(f"  PASS: Face bbox: ({x}, {y}, {w}, {h})")
    
    return faces


def test_detailed_detection(detector):
    """Test detailed face detection"""
    print("\nTesting: detect_faces_detailed()")
    print("-" * 50)
    
    test_image = create_test_image_with_face()
    detailed = detector.detect_faces_detailed(test_image)
    
    assert isinstance(detailed, list), "Should return list"
    print(f"  PASS: Detailed detection returned {len(detailed)} result(s)")
    
    if len(detailed) > 0:
        face = detailed[0]
        assert 'bbox' in face, "Missing bbox key"
        assert 'center' in face, "Missing center key"
        assert 'area' in face, "Missing area key"
        assert 'aspect_ratio' in face, "Missing aspect_ratio key"
        print(f"  PASS: Face area: {face['area']}, ratio: {face['aspect_ratio']:.2f}")
    
    return detailed


def test_face_region_extraction(detector):
    """Test face region extraction"""
    print("\nTesting: get_face_region()")
    print("-" * 50)
    
    test_image = create_test_image_with_face()
    faces = detector.detect_faces(test_image)
    
    if len(faces) > 0:
        face_region = detector.get_face_region(test_image, faces[0])
        assert face_region is not None, "Failed to extract region"
        assert len(face_region.shape) >= 2, "Invalid region shape"
        print(f"  PASS: Extracted face region: {face_region.shape}")
        
        # Test with padding
        face_region_padded = detector.get_face_region(test_image, faces[0], padding=10)
        assert face_region_padded.shape[0] >= face_region.shape[0], "Padding not applied"
        print(f"  PASS: Extracted with padding: {face_region_padded.shape}")
    else:
        print("  SKIP: No faces detected for extraction test")


def test_draw_detections(detector):
    """Test drawing detections"""
    print("\nTesting: draw_detections()")
    print("-" * 50)
    
    test_image = create_test_image_with_face()
    faces = detector.detect_faces(test_image)
    
    result = detector.draw_detections(test_image, faces)
    assert result is not None, "Failed to draw detections"
    assert result.shape == test_image.shape, "Shape mismatch"
    assert not np.array_equal(result, test_image), "Image not modified"
    print(f"  PASS: Drew {len(faces)} detection(s) on image")
    
    # Save result for visual inspection
    os.makedirs("test_output", exist_ok=True)
    cv2.imwrite("test_output/detection_result.jpg", result)
    print("  INFO: Saved result to test_output/detection_result.jpg")
    
    return result


def test_validation(detector):
    """Test detection validation"""
    print("\nTesting: validate_detection()")
    print("-" * 50)
    
    test_image = create_test_image_with_face()
    image_shape = test_image.shape
    
    # Test valid face
    valid_bbox = (200, 150, 100, 100)
    is_valid, msg = detector.validate_detection(valid_bbox, image_shape)
    print(f"  Valid bbox: {is_valid}, {msg}")
    
    # Test small face
    small_bbox = (200, 150, 20, 20)
    is_valid, msg = detector.validate_detection(small_bbox, image_shape, min_face_size=30)
    assert not is_valid, "Should reject small face"
    print(f"  Small bbox: {is_valid}, {msg}")
    
    # Test border face
    border_bbox = (5, 5, 100, 100)
    is_valid, msg = detector.validate_detection(border_bbox, image_shape)
    assert not is_valid, "Should reject border face"
    print(f"  Border bbox: {is_valid}, {msg}")
    
    print("  PASS: Validation working correctly")


def test_parameter_update(detector):
    """Test parameter updates"""
    print("\nTesting: set_parameters()")
    print("-" * 50)
    
    detector.set_parameters(scale_factor=1.2, min_neighbors=3, min_size=(50, 50))
    
    assert detector.scale_factor == 1.2, "Scale factor not updated"
    assert detector.min_neighbors == 3, "Min neighbors not updated"
    assert detector.min_size == (50, 50), "Min size not updated"
    print("  PASS: Parameters updated successfully")
    print(f"  New params: scale={detector.scale_factor}, neighbors={detector.min_neighbors}, size={detector.min_size}")


def test_integration_with_image_utils():
    """Test integration with Week 1's image_utils"""
    print("\nTesting: Integration with image_utils")
    print("-" * 50)
    
    # Try to import image_utils from same folder
    try:
        from image_utils import preprocess_image, load_image
        
        detector = FaceDetector()
        test_image = create_test_image_with_face()
        
        # Preprocess using week 1's module
        preprocessed = preprocess_image(test_image, target_size=(640, 480))
        
        # Detect on preprocessed
        faces = detector.detect_faces(preprocessed)
        
        print(f"  PASS: Integration successful, detected {len(faces)} face(s)")
        print("  INFO: Can use image_utils.preprocess_image() before detection")
        
    except ImportError:
        print("  SKIP: image_utils not found (Week 1 module)")


def run_all_tests():
    """Run all tests"""
    print("="*50)
    print("FACE DETECTOR TEST SUITE")
    print("Week 2 Project Module Testing")
    print("="*50)
    
    try:
        # Test 1: Initialization
        detector = test_detector_initialization()
        
        # Test 2: Basic detection
        faces = test_face_detection(detector)
        
        # Test 3: Detailed detection
        test_detailed_detection(detector)
        
        # Test 4: Face region extraction
        test_face_region_extraction(detector)
        
        # Test 5: Draw detections
        test_draw_detections(detector)
        
        # Test 6: Validation
        test_validation(detector)
        
        # Test 7: Parameter update
        test_parameter_update(detector)
        
        # Test 8: Integration
        test_integration_with_image_utils()
        
        print("\n" + "="*50)
        print("ALL TESTS PASSED!")
        print("="*50)
        print("\nFace detector module is working correctly.")
        print("Ready to integrate into main project.\n")
        
        return True
        
    except AssertionError as e:
        print(f"\n[FAILED] Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    run_all_tests()
