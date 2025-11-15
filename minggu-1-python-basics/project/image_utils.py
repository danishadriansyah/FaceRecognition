"""
Image Utilities Module
Week 1 Project Module - Progressive Web Application

This module provides core image processing functions for the face recognition system.
Functions defined here will be used throughout the project for preprocessing images.
"""

import cv2
import numpy as np
from typing import Tuple, Optional


def load_image(image_path: str, mode: str = 'color') -> Optional[np.ndarray]:
    """
    Load an image from file path
    
    Args:
        image_path: Path to the image file
        mode: 'color' for BGR, 'grayscale' for grayscale, 'unchanged' for original
        
    Returns:
        Image as numpy array, or None if loading failed
    """
    mode_map = {
        'color': cv2.IMREAD_COLOR,
        'grayscale': cv2.IMREAD_GRAYSCALE,
        'unchanged': cv2.IMREAD_UNCHANGED
    }
    
    if mode not in mode_map:
        raise ValueError(f"Invalid mode: {mode}. Use 'color', 'grayscale', or 'unchanged'")
    
    image = cv2.imread(image_path, mode_map[mode])
    
    if image is None:
        print(f"Warning: Failed to load image from {image_path}")
        return None
    
    return image


def resize_image(image: np.ndarray, width: int = None, height: int = None, 
                scale: float = None, interpolation: int = cv2.INTER_LINEAR) -> np.ndarray:
    """
    Resize image to specified dimensions or scale
    
    Args:
        image: Input image
        width: Target width (if None, calculated from height or scale)
        height: Target height (if None, calculated from width or scale)
        scale: Scale factor (used if width and height are None)
        interpolation: Interpolation method (INTER_LINEAR, INTER_CUBIC, INTER_AREA)
        
    Returns:
        Resized image
    """
    if scale is not None:
        # Resize by scale factor
        new_width = int(image.shape[1] * scale)
        new_height = int(image.shape[0] * scale)
        return cv2.resize(image, (new_width, new_height), interpolation=interpolation)
    
    if width is None and height is None:
        return image
    
    h, w = image.shape[:2]
    
    if width is None:
        # Calculate width from height maintaining aspect ratio
        aspect_ratio = w / h
        width = int(height * aspect_ratio)
    elif height is None:
        # Calculate height from width maintaining aspect ratio
        aspect_ratio = h / w
        height = int(width * aspect_ratio)
    
    return cv2.resize(image, (width, height), interpolation=interpolation)


def preprocess_image(image: np.ndarray, target_size: Tuple[int, int] = (224, 224),
                    normalize: bool = False, to_grayscale: bool = False) -> np.ndarray:
    """
    Preprocess image for face recognition
    
    Args:
        image: Input image
        target_size: Target size as (width, height)
        normalize: Whether to normalize pixel values to [0, 1]
        to_grayscale: Whether to convert to grayscale
        
    Returns:
        Preprocessed image
    """
    processed = image.copy()
    
    # Convert to grayscale if requested
    if to_grayscale and len(processed.shape) == 3:
        processed = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
    
    # Resize to target size
    processed = cv2.resize(processed, target_size, interpolation=cv2.INTER_AREA)
    
    # Normalize pixel values
    if normalize:
        processed = processed.astype(np.float32) / 255.0
    
    return processed


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Convert BGR image to grayscale
    
    Args:
        image: Input BGR image
        
    Returns:
        Grayscale image
    """
    if len(image.shape) == 2:
        # Already grayscale
        return image
    
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def save_image(image: np.ndarray, output_path: str, quality: int = 95) -> bool:
    """
    Save image to file
    
    Args:
        image: Image to save
        output_path: Output file path
        quality: JPEG quality (1-100), higher is better
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Set quality parameters for JPEG
        params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        
        success = cv2.imwrite(output_path, image, params)
        
        if success:
            print(f"Image saved: {output_path}")
        else:
            print(f"Failed to save image: {output_path}")
        
        return success
    except Exception as e:
        print(f"Error saving image: {e}")
        return False


def validate_image_quality(image: np.ndarray, min_width: int = 100, 
                          min_height: int = 100, max_blur: float = 100.0) -> Tuple[bool, str]:
    """
    Validate if image meets quality requirements
    
    Args:
        image: Input image
        min_width: Minimum acceptable width
        min_height: Minimum acceptable height
        max_blur: Maximum acceptable blur variance (Laplacian variance)
        
    Returns:
        Tuple of (is_valid, message)
    """
    if image is None:
        return False, "Image is None"
    
    # Check dimensions
    height, width = image.shape[:2]
    
    if width < min_width or height < min_height:
        return False, f"Image too small: {width}x{height} (minimum: {min_width}x{min_height})"
    
    # Check blur (using Laplacian variance)
    gray = convert_to_grayscale(image) if len(image.shape) == 3 else image
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    if laplacian_var < max_blur:
        return False, f"Image too blurry (variance: {laplacian_var:.2f}, threshold: {max_blur})"
    
    return True, "Image quality OK"


# Example usage and testing
if __name__ == "__main__":
    print("Image Utilities Module - Week 1 Project")
    print("="*50)
    
    # Create a test image
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    test_image[:, :] = (100, 150, 200)
    
    # Add text
    cv2.putText(test_image, "Test Image", (200, 240),
               cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    
    print("\n1. Testing image creation...")
    print(f"   Created test image: {test_image.shape}")
    
    print("\n2. Testing resize...")
    resized = resize_image(test_image, width=320, height=240)
    print(f"   Resized to: {resized.shape}")
    
    print("\n3. Testing scale...")
    scaled = resize_image(test_image, scale=0.5)
    print(f"   Scaled to 50%: {scaled.shape}")
    
    print("\n4. Testing grayscale conversion...")
    gray = convert_to_grayscale(test_image)
    print(f"   Grayscale shape: {gray.shape}")
    
    print("\n5. Testing preprocessing...")
    preprocessed = preprocess_image(test_image, target_size=(224, 224), 
                                   normalize=True, to_grayscale=True)
    print(f"   Preprocessed shape: {preprocessed.shape}")
    print(f"   Value range: [{preprocessed.min():.2f}, {preprocessed.max():.2f}]")
    
    print("\n6. Testing quality validation...")
    is_valid, message = validate_image_quality(test_image)
    print(f"   Quality check: {message}")
    
    print("\nAll functions tested successfully!")
