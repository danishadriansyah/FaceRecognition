"""
Minggu 1 - File 3: Drawing Shapes
Konsep: Menggambar shapes, lines, dan text pada gambar

Tujuan:
- Menggambar rectangle, circle, line
- Menambahkan text pada gambar
- Memahami BGR color format
- Thickness dan line types

Author: AI Face Recognition Learning Project
"""

import cv2
import numpy as np
import os

def create_canvas():
    """Buat blank canvas putih"""
    # Buat array putih (255, 255, 255)
    canvas = np.ones((600, 800, 3), dtype=np.uint8) * 255
    return canvas


def drawing_lines_demo():
    """Demonstrasi menggambar garis"""
    
    print("\n" + "="*50)
    print("DRAWING LINES")
    print("="*50)
    
    canvas = create_canvas()
    
    # Line: start_point, end_point, color, thickness
    # Horizontal line
    cv2.line(canvas, (50, 100), (750, 100), (0, 0, 255), 2)  # Red
    
    # Vertical line
    cv2.line(canvas, (400, 50), (400, 550), (0, 255, 0), 2)  # Green
    
    # Diagonal line
    cv2.line(canvas, (50, 50), (750, 550), (255, 0, 0), 3)  # Blue
    
    # Multiple lines (grid)
    for i in range(0, 800, 100):
        cv2.line(canvas, (i, 0), (i, 600), (200, 200, 200), 1)
    
    for i in range(0, 600, 100):
        cv2.line(canvas, (0, i), (800, i), (200, 200, 200), 1)
    
    # Line types
    cv2.line(canvas, (50, 200), (350, 200), (0, 0, 0), 2, cv2.LINE_AA)  # Anti-aliased
    cv2.putText(canvas, "LINE_AA (smooth)", (50, 190), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    cv2.line(canvas, (50, 250), (350, 250), (0, 0, 0), 2, cv2.LINE_8)
    cv2.putText(canvas, "LINE_8", (50, 240), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    cv2.line(canvas, (50, 300), (350, 300), (0, 0, 0), 2, cv2.LINE_4)
    cv2.putText(canvas, "LINE_4", (50, 290), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    print("✅ Lines drawn")
    cv2.imshow("Drawing Lines", canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return canvas


def drawing_rectangles_demo():
    """Demonstrasi menggambar rectangle"""
    
    print("\n" + "="*50)
    print("DRAWING RECTANGLES")
    print("="*50)
    
    canvas = create_canvas()
    
    # Rectangle: top-left, bottom-right, color, thickness
    # Filled rectangle (thickness = -1)
    cv2.rectangle(canvas, (50, 50), (200, 150), (0, 0, 255), -1)
    cv2.putText(canvas, "Filled", (70, 110), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Outline rectangle
    cv2.rectangle(canvas, (250, 50), (400, 150), (0, 255, 0), 3)
    cv2.putText(canvas, "Outline", (260, 110), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # Different thicknesses
    for i, thickness in enumerate([1, 2, 3, 5, 7]):
        y_offset = i * 80 + 200
        cv2.rectangle(canvas, (50, y_offset), (150, y_offset + 60), 
                     (255, 0, 0), thickness)
        cv2.putText(canvas, f"thick={thickness}", (55, y_offset + 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    # Rounded rectangle (approximate with circles at corners)
    cv2.rectangle(canvas, (450, 50), (700, 200), (255, 165, 0), 3)
    cv2.putText(canvas, "Normal Rectangle", (460, 130), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    # Multiple rectangles (pattern)
    for i in range(5):
        offset = i * 15
        cv2.rectangle(canvas, (450 + offset, 250 + offset), 
                     (650 + offset, 400 + offset), 
                     (100 + i*30, 100, 200 - i*30), 2)
    
    print("✅ Rectangles drawn")
    cv2.imshow("Drawing Rectangles", canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return canvas


def drawing_circles_demo():
    """Demonstrasi menggambar circle"""
    
    print("\n" + "="*50)
    print("DRAWING CIRCLES")
    print("="*50)
    
    canvas = create_canvas()
    
    # Circle: center, radius, color, thickness
    # Filled circle
    cv2.circle(canvas, (150, 150), 80, (0, 0, 255), -1)
    cv2.putText(canvas, "Filled", (110, 155), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Outline circle
    cv2.circle(canvas, (400, 150), 80, (0, 255, 0), 3)
    cv2.putText(canvas, "Outline", (355, 155), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # Concentric circles
    center = (650, 150)
    for radius in range(20, 100, 15):
        cv2.circle(canvas, center, radius, (255, 0, 0), 2)
    
    # Circle pattern
    center_x, center_y = 400, 400
    for angle in range(0, 360, 30):
        x = int(center_x + 100 * np.cos(np.radians(angle)))
        y = int(center_y + 100 * np.sin(np.radians(angle)))
        cv2.circle(canvas, (x, y), 20, (255, 165, 0), -1)
    
    # Center point
    cv2.circle(canvas, (center_x, center_y), 25, (0, 0, 0), -1)
    cv2.putText(canvas, "Pattern", (center_x - 40, center_y + 5), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    print("✅ Circles drawn")
    cv2.imshow("Drawing Circles", canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return canvas


def drawing_text_demo():
    """Demonstrasi menambahkan text"""
    
    print("\n" + "="*50)
    print("DRAWING TEXT")
    print("="*50)
    
    canvas = create_canvas()
    
    # Text parameters: text, position, font, scale, color, thickness
    
    y_pos = 50
    fonts = [
        (cv2.FONT_HERSHEY_SIMPLEX, "SIMPLEX"),
        (cv2.FONT_HERSHEY_PLAIN, "PLAIN"),
        (cv2.FONT_HERSHEY_DUPLEX, "DUPLEX"),
        (cv2.FONT_HERSHEY_COMPLEX, "COMPLEX"),
        (cv2.FONT_HERSHEY_TRIPLEX, "TRIPLEX"),
        (cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, "SCRIPT_SIMPLEX"),
        (cv2.FONT_HERSHEY_SCRIPT_COMPLEX, "SCRIPT_COMPLEX"),
    ]
    
    for font, name in fonts:
        y_pos += 60
        cv2.putText(canvas, f"Font: {name}", (50, y_pos), 
                   font, 1, (0, 0, 0), 2)
    
    # Different sizes
    cv2.putText(canvas, "Size 0.5", (450, 80), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    cv2.putText(canvas, "Size 1.0", (450, 130), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    cv2.putText(canvas, "Size 1.5", (450, 190), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
    cv2.putText(canvas, "Size 2.0", (450, 260), 
               cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 0, 255), 3)
    
    # Text with background (for better readability)
    text = "Text with Background"
    position = (450, 350)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    
    # Get text size
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Draw background rectangle
    cv2.rectangle(canvas, 
                 (position[0] - 5, position[1] - text_height - 5),
                 (position[0] + text_width + 5, position[1] + baseline + 5),
                 (0, 0, 0), -1)
    
    # Draw text
    cv2.putText(canvas, text, position, font, font_scale, (255, 255, 255), thickness)
    
    # Multi-line text
    lines = ["Line 1: Hello", "Line 2: OpenCV", "Line 3: Face Recognition"]
    y = 450
    for line in lines:
        cv2.putText(canvas, line, (50, y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 100, 200), 2)
        y += 40
    
    print("✅ Text drawn")
    cv2.imshow("Drawing Text", canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return canvas


def complete_example():
    """Contoh lengkap: kombinasi semua shapes"""
    
    print("\n" + "="*50)
    print("COMPLETE EXAMPLE")
    print("="*50)
    
    canvas = create_canvas()
    
    # Title
    cv2.putText(canvas, "FACE RECOGNITION SYSTEM", (150, 50), 
               cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 0), 2)
    
    # Draw a "face" using shapes
    # Face outline (circle)
    face_center = (400, 300)
    cv2.circle(canvas, face_center, 120, (255, 200, 150), -1)  # Face
    cv2.circle(canvas, face_center, 120, (0, 0, 0), 2)  # Outline
    
    # Eyes
    left_eye = (360, 270)
    right_eye = (440, 270)
    cv2.circle(canvas, left_eye, 15, (0, 0, 0), -1)
    cv2.circle(canvas, right_eye, 15, (0, 0, 0), -1)
    
    # Pupils
    cv2.circle(canvas, left_eye, 5, (255, 255, 255), -1)
    cv2.circle(canvas, right_eye, 5, (255, 255, 255), -1)
    
    # Nose
    nose_points = np.array([[400, 300], [390, 330], [410, 330]], np.int32)
    cv2.polylines(canvas, [nose_points], True, (0, 0, 0), 2)
    
    # Mouth (smile)
    cv2.ellipse(canvas, (400, 340), (40, 25), 0, 0, 180, (0, 0, 0), 2)
    
    # Bounding box
    cv2.rectangle(canvas, (260, 150), (540, 450), (0, 255, 0), 3)
    
    # Label
    cv2.putText(canvas, "Detected!", (270, 140), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    # Info panel
    cv2.rectangle(canvas, (50, 480), (750, 570), (50, 50, 50), -1)
    cv2.putText(canvas, "Status: Face Detected", (60, 510), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(canvas, "Confidence: 98.5%", (60, 545), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    print("✅ Complete drawing created")
    cv2.imshow("Complete Example", canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Save
    os.makedirs("output", exist_ok=True)
    cv2.imwrite("output/drawing_example.jpg", canvas)
    print("💾 Saved: output/drawing_example.jpg")
    
    return canvas


def main():
    """Main program"""
    
    print("="*50)
    print("DRAWING SHAPES DEMO - Minggu 1")
    print("="*50)
    
    # Run all demos
    drawing_lines_demo()
    drawing_rectangles_demo()
    drawing_circles_demo()
    drawing_text_demo()
    complete_example()
    
    print("\n" + "="*50)
    print("✅ Semua demonstrasi selesai!")
    print("="*50)


# ======================================
# KONSEP PENTING
# ======================================
"""
1. DRAWING FUNCTIONS:
   - cv2.line(img, pt1, pt2, color, thickness)
   - cv2.rectangle(img, pt1, pt2, color, thickness)
   - cv2.circle(img, center, radius, color, thickness)
   - cv2.ellipse(img, center, axes, angle, startAngle, endAngle, color, thickness)
   - cv2.polylines(img, points, isClosed, color, thickness)

2. TEXT:
   - cv2.putText(img, text, org, font, fontScale, color, thickness)
   - cv2.getTextSize(): untuk mendapatkan ukuran text

3. COLORS (BGR Format):
   - Black: (0, 0, 0)
   - White: (255, 255, 255)
   - Red: (0, 0, 255)
   - Green: (0, 255, 0)
   - Blue: (255, 0, 0)
   - Yellow: (0, 255, 255)
   - Cyan: (255, 255, 0)
   - Magenta: (255, 0, 255)

4. THICKNESS:
   - Positive: outline thickness in pixels
   - -1: filled shape
   - LINE_AA: anti-aliased (smooth)

5. COORDINATES:
   - (x, y) where x = horizontal, y = vertical
   - (0, 0) = top-left corner
"""


# ======================================
# LATIHAN
# ======================================
"""
💪 LATIHAN:

1. Buat traffic light dengan circles (merah, kuning, hijau)
2. Buat emoji face (happy, sad, surprised)
3. Buat bounding box dengan label untuk face detection simulation
4. Buat progress bar dengan rectangle dan text
5. Buat logo sederhana menggunakan shapes

BONUS CHALLENGE:
Buat aplikasi drawing interaktif:
- Mouse click untuk draw circles
- Mouse drag untuk draw rectangles
- Keyboard untuk change colors
- Save hasil drawing
"""


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main()
