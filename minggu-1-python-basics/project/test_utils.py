"""
Test Suite for Image Utilities Module
Week 1 Project Testing

Run this file to test all functions in image_utils.py
"""

import cv2
import numpy as np
import os
import sys

# Add project directory to path
sys.path.insert(0, os.path.dirname(__file__))

from image_utils import (
    load_image,
    resize_image,
    preprocess_image,
    convert_to_grayscale,
    save_image,
    validate_image_quality
)


def create_test_image(filename="test_sample.jpg"):
    """Create a test image for testing"""
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    test_image[:, :] = (100, 150, 200)
    
    cv2.putText(test_image, "Test Image", (180, 220),
               cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    cv2.putText(test_image, "For Quality Testing", (140, 280),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    os.makedirs("test_output", exist_ok=True)
    cv2.imwrite(f"test_output/{filename}", test_image)
    return f"test_output/{filename}"


def test_load_image():
    """Test load_image function"""
    print("\nTesting: load_image()")
    print("-" * 50)
    
    # Create test image
    test_path = create_test_image()
    
    # Test color loading
    img_color = load_image(test_path, mode='color')
    assert img_color is not None, "Failed to load color image"
    assert len(img_color.shape) == 3, "Color image should have 3 dimensions"
    print(f"  PASS: Loaded color image - shape: {img_color.shape}")
    
    # Test grayscale loading
    img_gray = load_image(test_path, mode='grayscale')
    assert img_gray is not None, "Failed to load grayscale image"
    assert len(img_gray.shape) == 2, "Grayscale image should have 2 dimensions"
    print(f"  PASS: Loaded grayscale image - shape: {img_gray.shape}")
    
    # Test invalid path
    img_invalid = load_image("nonexistent.jpg")
    assert img_invalid is None, "Should return None for invalid path"
    print("  PASS: Correctly handles invalid path")
    
    return img_color


def test_resize_image(test_image):
    """Test resize_image function"""
    print("\nTesting: resize_image()")
    print("-" * 50)
    
    # Test resize with width and height
    resized = resize_image(test_image, width=320, height=240)
    assert resized.shape[1] == 320 and resized.shape[0] == 240, "Size mismatch"
    print(f"  PASS: Resized to 320x240 - shape: {resized.shape}")
    
    # Test resize with scale
    scaled = resize_image(test_image, scale=0.5)
    expected_width = int(test_image.shape[1] * 0.5)
    expected_height = int(test_image.shape[0] * 0.5)
    assert scaled.shape[1] == expected_width, "Scale width mismatch"
    assert scaled.shape[0] == expected_height, "Scale height mismatch"
    print(f"  PASS: Scaled to 50% - shape: {scaled.shape}")
    
    # Test resize with only width (maintain aspect ratio)
    resized_width = resize_image(test_image, width=400)
    assert resized_width.shape[1] == 400, "Width not set correctly"
    print(f"  PASS: Resized with aspect ratio - shape: {resized_width.shape}")
    
    return resized


def test_preprocess_image(test_image):
    """Test preprocess_image function"""
    print("\nTesting: preprocess_image()")
    print("-" * 50)
    
    # Test basic preprocessing
    preprocessed = preprocess_image(test_image, target_size=(224, 224))
    assert preprocessed.shape[1] == 224 and preprocessed.shape[0] == 224, "Size mismatch"
    print(f"  PASS: Preprocessed to 224x224 - shape: {preprocessed.shape}")
    
    # Test with normalization
    normalized = preprocess_image(test_image, target_size=(224, 224), normalize=True)
    assert normalized.max() <= 1.0 and normalized.min() >= 0.0, "Normalization failed"
    print(f"  PASS: Normalized values - range: [{normalized.min():.2f}, {normalized.max():.2f}]")
    
    # Test with grayscale conversion
    gray_processed = preprocess_image(test_image, target_size=(224, 224), 
                                     to_grayscale=True)
    assert len(gray_processed.shape) == 2, "Grayscale conversion failed"
    print(f"  PASS: Converted to grayscale - shape: {gray_processed.shape}")
    
    # Test combined (grayscale + normalize)
    combined = preprocess_image(test_image, target_size=(224, 224),
                               normalize=True, to_grayscale=True)
    assert len(combined.shape) == 2, "Grayscale failed"
    assert combined.max() <= 1.0, "Normalization failed"
    print(f"  PASS: Combined preprocessing - shape: {combined.shape}, range: [{combined.min():.2f}, {combined.max():.2f}]")
    
    return preprocessed


def test_convert_to_grayscale(test_image):
    """Test convert_to_grayscale function"""
    print("\nTesting: convert_to_grayscale()")
    print("-" * 50)
    
    # Test BGR to grayscale
    gray = convert_to_grayscale(test_image)
    assert len(gray.shape) == 2, "Should return 2D array"
    print(f"  PASS: Converted BGR to grayscale - shape: {gray.shape}")
    
    # Test already grayscale
    gray_again = convert_to_grayscale(gray)
    assert np.array_equal(gray, gray_again), "Should return same array"
    print("  PASS: Handles already grayscale image")
    
    return gray


def test_save_image(test_image):
    """Test save_image function"""
    print("\nTesting: save_image()")
    print("-" * 50)
    
    os.makedirs("test_output", exist_ok=True)
    
    # Test save with default quality
    output_path = "test_output/saved_test.jpg"
    success = save_image(test_image, output_path)
    assert success, "Save failed"
    assert os.path.exists(output_path), "File not created"
    print(f"  PASS: Saved image to {output_path}")
    
    # Test save with custom quality
    output_path_hq = "test_output/saved_test_hq.jpg"
    success_hq = save_image(test_image, output_path_hq, quality=100)
    assert success_hq, "Save with custom quality failed"
    print(f"  PASS: Saved high quality image to {output_path_hq}")
    
    # Check file sizes
    size_default = os.path.getsize(output_path)
    size_hq = os.path.getsize(output_path_hq)
    print(f"  INFO: Default quality size: {size_default} bytes")
    print(f"  INFO: High quality size: {size_hq} bytes")
    
    return success


def test_validate_image_quality(test_image):
    """Test validate_image_quality function"""
    print("\nTesting: validate_image_quality()")
    print("-" * 50)
    
    # Test valid image
    is_valid, message = validate_image_quality(test_image)
    assert is_valid, f"Should be valid: {message}"
    print(f"  PASS: Valid image - {message}")
    
    # Test image too small
    small_image = cv2.resize(test_image, (50, 50))
    is_valid, message = validate_image_quality(small_image, min_width=100, min_height=100)
    assert not is_valid, "Should reject small image"
    print(f"  PASS: Rejected small image - {message}")
    
    # Test blurry image
    blurry_image = cv2.GaussianBlur(test_image, (51, 51), 0)
    is_valid, message = validate_image_quality(blurry_image, max_blur=100.0)
    print(f"  INFO: Blur validation - {message}")
    
    # Test None image
    is_valid, message = validate_image_quality(None)
    assert not is_valid, "Should reject None"
    print(f"  PASS: Rejected None image - {message}")
    
    return True


def run_all_tests():
    """Run all tests"""
    print("="*50)
    print("IMAGE UTILITIES TEST SUITE")
    print("Week 1 Project Module Testing")
    print("="*50)
    
    try:
        # Test 1: Load image
        test_img = test_load_image()
        
        # Test 2: Resize image
        test_resize_image(test_img)
        
        # Test 3: Preprocess image
        test_preprocess_image(test_img)
        
        # Test 4: Convert to grayscale
        test_convert_to_grayscale(test_img)
        
        # Test 5: Save image
        test_save_image(test_img)
        
        # Test 6: Validate image quality
        test_validate_image_quality(test_img)
        
        print("\n" + "="*50)
        print("ALL TESTS PASSED!")
        print("="*50)
        print("\nImage utilities module is working correctly.")
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
