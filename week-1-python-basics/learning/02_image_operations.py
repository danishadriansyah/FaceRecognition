"""
Minggu 1 - File 2: Image Operations
Konsep: Manipulasi Gambar Dasar - Resize, Crop, Rotate, Flip, Color Conversion

Tujuan:
- Resize gambar ke berbagai ukuran
- Crop bagian tertentu dari gambar
- Rotate dan flip gambar
- Convert color spaces
- Memahami aspect ratio

Author: AI Face Recognition Learning Project
"""

import cv2
import numpy as np
import os

def resize_demo(image):
    """Demonstrasi berbagai cara resize gambar"""
    
    print("\n" + "="*50)
    print("RESIZE OPERATIONS")
    print("="*50)
    
    height, width = image.shape[:2]
    print(f"📏 Original size: {width}x{height}")
    
    # Method 1: Resize dengan ukuran spesifik
    resized_specific = cv2.resize(image, (400, 300))  # (width, height)
    print(f"✅ Resized (specific): {resized_specific.shape[1]}x{resized_specific.shape[0]}")
    
    # Method 2: Resize dengan scale factor
    scale_percent = 50  # 50% dari ukuran asli
    new_width = int(width * scale_percent / 100)
    new_height = int(height * scale_percent / 100)
    resized_scale = cv2.resize(image, (new_width, new_height))
    print(f"✅ Resized (50% scale): {new_width}x{new_height}")
    
    # Method 3: Resize dengan fx, fy
    resized_fx = cv2.resize(image, None, fx=0.5, fy=0.5)
    print(f"✅ Resized (fx=0.5, fy=0.5): {resized_fx.shape[1]}x{resized_fx.shape[0]}")
    
    # Method 4: Resize dengan interpolation berbeda
    resized_linear = cv2.resize(image, (300, 300), interpolation=cv2.INTER_LINEAR)
    resized_cubic = cv2.resize(image, (300, 300), interpolation=cv2.INTER_CUBIC)
    resized_area = cv2.resize(image, (300, 300), interpolation=cv2.INTER_AREA)
    
    print("\n📐 Interpolation Methods:")
    print("   - INTER_LINEAR: Baik untuk enlarging")
    print("   - INTER_CUBIC: Lebih smooth, tapi lebih lambat")
    print("   - INTER_AREA: Baik untuk shrinking")
    
    # Display comparison
    cv2.imshow("Original", image)
    cv2.imshow("Resized - Specific Size", resized_specific)
    cv2.imshow("Resized - 50% Scale", resized_scale)
    cv2.imshow("Interpolation - LINEAR", resized_linear)
    cv2.imshow("Interpolation - CUBIC", resized_cubic)
    cv2.imshow("Interpolation - AREA", resized_area)
    
    print("\n⌨️  Tekan any key untuk lanjut...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return resized_specific


def crop_demo(image):
    """Demonstrasi cropping gambar"""
    
    print("\n" + "="*50)
    print("CROP OPERATIONS")
    print("="*50)
    
    height, width = image.shape[:2]
    
    # Cropping = array slicing
    # Format: image[y1:y2, x1:x2]
    
    # Crop tengah
    center_x, center_y = width // 2, height // 2
    crop_size = 200
    
    x1 = center_x - crop_size // 2
    y1 = center_y - crop_size // 2
    x2 = center_x + crop_size // 2
    y2 = center_y + crop_size // 2
    
    cropped_center = image[y1:y2, x1:x2]
    print(f"✅ Cropped center: {cropped_center.shape[1]}x{cropped_center.shape[0]}")
    
    # Crop pojok kiri atas (25%)
    cropped_top_left = image[0:height//2, 0:width//2]
    print(f"✅ Cropped top-left: {cropped_top_left.shape[1]}x{cropped_top_left.shape[0]}")
    
    # Crop pojok kanan bawah (25%)
    cropped_bottom_right = image[height//2:height, width//2:width]
    print(f"✅ Cropped bottom-right: {cropped_bottom_right.shape[1]}x{cropped_bottom_right.shape[0]}")
    
    # Gambar bounding box untuk visualisasi
    image_with_box = image.copy()
    cv2.rectangle(image_with_box, (x1, y1), (x2, y2), (0, 255, 0), 3)
    cv2.putText(image_with_box, "Cropped Area", (x1, y1-10), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.imshow("Original with Crop Area", image_with_box)
    cv2.imshow("Cropped - Center", cropped_center)
    cv2.imshow("Cropped - Top Left", cropped_top_left)
    cv2.imshow("Cropped - Bottom Right", cropped_bottom_right)
    
    print("\n⌨️  Tekan any key untuk lanjut...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return cropped_center


def rotate_demo(image):
    """Demonstrasi rotasi gambar"""
    
    print("\n" + "="*50)
    print("ROTATION OPERATIONS")
    print("="*50)
    
    # Method 1: Rotate 90 derajat (built-in)
    rotated_90_cw = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    rotated_90_ccw = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    rotated_180 = cv2.rotate(image, cv2.ROTATE_180)
    
    print("✅ Rotated 90° clockwise")
    print("✅ Rotated 90° counter-clockwise")
    print("✅ Rotated 180°")
    
    # Method 2: Rotate dengan angle custom
    height, width = image.shape[:2]
    center = (width // 2, height // 2)
    
    # Rotation matrix untuk 45 derajat
    angle = 45
    scale = 1.0
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
    
    # Apply rotation
    rotated_45 = cv2.warpAffine(image, rotation_matrix, (width, height))
    print(f"✅ Rotated {angle}° dengan rotation matrix")
    
    # Rotation tanpa crop (auto-expand canvas)
    angle = 30
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
    
    # Hitung ukuran canvas baru
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])
    new_width = int((height * sin) + (width * cos))
    new_height = int((height * cos) + (width * sin))
    
    # Adjust translation
    rotation_matrix[0, 2] += (new_width / 2) - center[0]
    rotation_matrix[1, 2] += (new_height / 2) - center[1]
    
    rotated_expanded = cv2.warpAffine(image, rotation_matrix, (new_width, new_height))
    print(f"✅ Rotated {angle}° with expanded canvas")
    
    cv2.imshow("Original", image)
    cv2.imshow("Rotated 90° CW", rotated_90_cw)
    cv2.imshow("Rotated 90° CCW", rotated_90_ccw)
    cv2.imshow("Rotated 180°", rotated_180)
    cv2.imshow("Rotated 45°", rotated_45)
    cv2.imshow("Rotated 30° (Expanded)", rotated_expanded)
    
    print("\n⌨️  Tekan any key untuk lanjut...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return rotated_45


def flip_demo(image):
    """Demonstrasi flipping gambar"""
    
    print("\n" + "="*50)
    print("FLIP OPERATIONS")
    print("="*50)
    
    # Flip horizontal (mirror)
    flipped_horizontal = cv2.flip(image, 1)
    print("✅ Flipped horizontal (mirror)")
    
    # Flip vertical
    flipped_vertical = cv2.flip(image, 0)
    print("✅ Flipped vertical")
    
    # Flip both (= rotate 180°)
    flipped_both = cv2.flip(image, -1)
    print("✅ Flipped both directions")
    
    cv2.imshow("Original", image)
    cv2.imshow("Flipped Horizontal", flipped_horizontal)
    cv2.imshow("Flipped Vertical", flipped_vertical)
    cv2.imshow("Flipped Both", flipped_both)
    
    print("\n⌨️  Tekan any key untuk lanjut...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return flipped_horizontal


def color_conversion_demo(image):
    """Demonstrasi konversi color space"""
    
    print("\n" + "="*50)
    print("COLOR CONVERSION")
    print("="*50)
    
    # BGR to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print("✅ Converted to Grayscale")
    
    # BGR to RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    print("✅ Converted to RGB")
    
    # BGR to HSV (Hue, Saturation, Value)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    print("✅ Converted to HSV")
    
    # Split HSV channels
    h, s, v = cv2.split(hsv)
    print("   - H (Hue): Warna")
    print("   - S (Saturation): Intensitas warna")
    print("   - V (Value): Brightness")
    
    # Split BGR channels
    b, g, r = cv2.split(image)
    
    # Buat colored version dari grayscale
    gray_colored = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    cv2.imshow("Original (BGR)", image)
    cv2.imshow("Grayscale", gray)
    cv2.imshow("HSV", hsv)
    cv2.imshow("Hue Channel", h)
    cv2.imshow("Saturation Channel", s)
    cv2.imshow("Value Channel", v)
    cv2.imshow("Blue Channel", b)
    cv2.imshow("Green Channel", g)
    cv2.imshow("Red Channel", r)
    
    print("\n💡 Catatan:")
    print("   - BGR adalah default di OpenCV")
    print("   - RGB digunakan oleh matplotlib dan PIL")
    print("   - HSV bagus untuk color filtering")
    print("   - Grayscale untuk simplifikasi dan speed")
    
    print("\n⌨️  Tekan any key untuk lanjut...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return gray


def main():
    """Main program"""
    
    print("="*50)
    print("IMAGE OPERATIONS DEMO - Minggu 1")
    print("="*50)
    
    # Load image
    image_path = "samples/sample_image.jpg"
    
    if not os.path.exists(image_path):
        print("⚠️  Sample image tidak ditemukan!")
        print("💡 Jalankan 1_hello_opencv.py terlebih dahulu")
        return
    
    image = cv2.imread(image_path)
    
    if image is None:
        print("❌ Error loading image!")
        return
    
    print(f"✅ Image loaded: {image.shape[1]}x{image.shape[0]}\n")
    
    # Jalankan semua demo
    print("🎬 Memulai demonstrasi...\n")
    
    # 1. Resize
    resized = resize_demo(image)
    
    # 2. Crop
    cropped = crop_demo(image)
    
    # 3. Rotate
    rotated = rotate_demo(image)
    
    # 4. Flip
    flipped = flip_demo(image)
    
    # 5. Color Conversion
    gray = color_conversion_demo(image)
    
    # Save results
    os.makedirs("output", exist_ok=True)
    cv2.imwrite("output/resized.jpg", resized)
    cv2.imwrite("output/cropped.jpg", cropped)
    cv2.imwrite("output/rotated.jpg", rotated)
    cv2.imwrite("output/flipped.jpg", flipped)
    cv2.imwrite("output/grayscale.jpg", gray)
    
    print("\n" + "="*50)
    print("✅ Semua operasi selesai!")
    print("💾 Hasil disimpan di folder 'output/'")
    print("="*50)


# ======================================
# KONSEP PENTING
# ======================================
"""
1. RESIZE:
   - cv2.resize(img, (width, height))
   - Atau dengan fx, fy: cv2.resize(img, None, fx=0.5, fy=0.5)
   - Interpolation: LINEAR (default), CUBIC (smooth), AREA (shrinking)

2. CROP:
   - Array slicing: img[y1:y2, x1:x2]
   - Koordinat: (0,0) di top-left
   - Buat copy jika mau modify: img[y1:y2, x1:x2].copy()

3. ROTATE:
   - Built-in: cv2.rotate() untuk 90°, 180°, 270°
   - Custom angle: cv2.getRotationMatrix2D() + cv2.warpAffine()
   - Center rotation: around image center

4. FLIP:
   - Horizontal: cv2.flip(img, 1)
   - Vertical: cv2.flip(img, 0)
   - Both: cv2.flip(img, -1)

5. COLOR SPACES:
   - BGR: OpenCV default
   - RGB: Standard (matplotlib, PIL)
   - GRAY: Single channel (0-255)
   - HSV: Hue, Saturation, Value (good for color filtering)
"""


# ======================================
# LATIHAN
# ======================================
"""
💪 LATIHAN:

1. Buat function untuk maintain aspect ratio saat resize
2. Buat interactive crop tool (mouse drag)
3. Buat function untuk rotate dengan keyboard arrow keys
4. Buat color filter (hanya tampilkan red/green/blue channel)
5. Combine multiple operations: crop → resize → rotate

BONUS CHALLENGE:
Buat program yang:
- Load image
- Resize ke 800x600
- Crop center 400x400
- Rotate 45 derajat
- Convert to grayscale
- Save hasil akhir
"""


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main()
