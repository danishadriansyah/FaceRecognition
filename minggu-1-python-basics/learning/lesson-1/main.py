"""
Lesson 1: Python & OpenCV Basics
Basic image operations
"""
import cv2
import os

# Create output directory
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

print("="*60)
print("LESSON 1: Python & OpenCV Basics")
print("="*60)

# 1. Load image
print("\n1. Loading image...")
# Create a sample image if none exists
img = cv2.imread('../images/sample.jpg')

if img is None:
    print("   Creating sample image (no sample.jpg found)")
    import numpy as np
    img = np.ones((400, 600, 3), dtype=np.uint8) * 200
    cv2.putText(img, 'Sample Image', (150, 200), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    cv2.imwrite('../images/sample.jpg', img)
    img = cv2.imread('../images/sample.jpg')

print(f"   ✅ Image loaded: {img.shape}")

# 2. Convert to grayscale
print("\n2. Converting to grayscale...")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite(f'{output_dir}/gray.jpg', gray)
print(f"   ✅ Grayscale saved: {gray.shape}")

# 3. Resize image
print("\n3. Resizing image...")
resized = cv2.resize(img, (300, 200))
cv2.imwrite(f'{output_dir}/resized.jpg', resized)
print(f"   ✅ Resized saved: {resized.shape}")

# 4. Crop image
print("\n4. Cropping image...")
h, w = img.shape[:2]
cropped = img[h//4:3*h//4, w//4:3*w//4]
cv2.imwrite(f'{output_dir}/cropped.jpg', cropped)
print(f"   ✅ Cropped saved: {cropped.shape}")

# 5. Rotate image
print("\n5. Rotating image...")
center = (w//2, h//2)
matrix = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(img, matrix, (w, h))
cv2.imwrite(f'{output_dir}/rotated.jpg', rotated)
print(f"   ✅ Rotated saved: {rotated.shape}")

# Display results
print("\n" + "="*60)
print("✅ LESSON 1 COMPLETED!")
print("="*60)
print(f"\nOutput files saved to: {output_dir}/")
print("  - gray.jpg")
print("  - resized.jpg")
print("  - cropped.jpg")
print("  - rotated.jpg")

print("\n📚 You learned:")
print("  ✅ Load images with cv2.imread()")
print("  ✅ Convert to grayscale")
print("  ✅ Resize images")
print("  ✅ Crop images")
print("  ✅ Rotate images")
print("  ✅ Save images with cv2.imwrite()")

print("\nNext: Lesson 2 - Drawing Shapes & Webcam\n")
