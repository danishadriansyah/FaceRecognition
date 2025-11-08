"""
Minggu 1 - Latihan: Mini Project
Konsep: Gabungan semua materi minggu 1

TUGAS:
Buat program "Photo Editor Sederhana" dengan fitur:
1. Load image dari file
2. Tampilkan di window
3. Keyboard controls untuk berbagai operasi:
   - 'g': Convert to grayscale
   - 'r': Rotate 90 derajat
   - 'f': Flip horizontal
   - 'b': Blur
   - 'e': Edge detection
   - '+': Zoom in (resize bigger)
   - '-': Zoom out (resize smaller)
   - 'c': Crop center
   - 's': Save edited image
   - 'z': Undo (kembali ke original)
   - 'q': Quit

BONUS:
- Tambahkan watermark text dengan nama kamu
- Buat histogram untuk show color distribution
- Multiple undo (history stack)

Author: AI Face Recognition Learning Project
"""

import cv2
import numpy as np
import os
from datetime import datetime

class PhotoEditor:
    """Simple Photo Editor"""
    
    def __init__(self, image_path):
        """Initialize editor with image"""
        self.original_image = cv2.imread(image_path)
        
        if self.original_image is None:
            raise ValueError(f"Cannot load image: {image_path}")
        
        self.current_image = self.original_image.copy()
        self.window_name = "Photo Editor - Minggu 1 Latihan"
        self.zoom_level = 1.0
        
        print("✅ Image loaded successfully")
        print(f"📏 Size: {self.original_image.shape[1]}x{self.original_image.shape[0]}")
    
    def show_instructions(self):
        """Display instructions"""
        print("\n" + "="*60)
        print("PHOTO EDITOR - KEYBOARD CONTROLS")
        print("="*60)
        print("📝 Transformations:")
        print("   'g' - Convert to Grayscale")
        print("   'r' - Rotate 90° clockwise")
        print("   'f' - Flip horizontal (mirror)")
        print("   'v' - Flip vertical")
        print("\n🎨 Effects:")
        print("   'b' - Blur")
        print("   'e' - Edge detection")
        print("   'n' - Negative")
        print("\n🔍 Zoom:")
        print("   '+' or '=' - Zoom in")
        print("   '-' or '_' - Zoom out")
        print("\n✂️  Crop:")
        print("   'c' - Crop center (50%)")
        print("\n💾 File Operations:")
        print("   's' - Save current image")
        print("   'z' - Undo (reset to original)")
        print("   'i' - Show image info")
        print("\n🚪 Exit:")
        print("   'q' or ESC - Quit")
        print("="*60 + "\n")
    
    def add_watermark(self, image, text="My Photo"):
        """Add watermark text to image"""
        # TUGAS: Implement watermark
        # Hint: Gunakan cv2.putText()
        # Letakkan di pojok kanan bawah
        # Gunakan background rectangle agar mudah dibaca
        
        result = image.copy()
        
        # YOUR CODE HERE
        # TODO: Tambahkan watermark
        
        # Hint untuk memulai:
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        
        # Get text size
        (text_width, text_height), baseline = cv2.getTextSize(
            text, font, font_scale, thickness
        )
        
        # Calculate position (bottom-right corner)
        height, width = result.shape[:2]
        x = width - text_width - 10
        y = height - 10
        
        # Draw background rectangle
        cv2.rectangle(result, 
                     (x - 5, y - text_height - 5),
                     (x + text_width + 5, y + baseline + 5),
                     (0, 0, 0), -1)
        
        # Draw text
        cv2.putText(result, text, (x, y), font, font_scale, 
                   (255, 255, 255), thickness)
        
        return result
    
    def grayscale(self):
        """Convert to grayscale"""
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        self.current_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        print("🎨 Applied: Grayscale")
    
    def rotate(self):
        """Rotate 90 degrees clockwise"""
        self.current_image = cv2.rotate(self.current_image, cv2.ROTATE_90_CLOCKWISE)
        print("🔄 Applied: Rotate 90°")
    
    def flip_horizontal(self):
        """Flip horizontal"""
        self.current_image = cv2.flip(self.current_image, 1)
        print("🪞 Applied: Flip Horizontal")
    
    def flip_vertical(self):
        """Flip vertical"""
        self.current_image = cv2.flip(self.current_image, 0)
        print("🪞 Applied: Flip Vertical")
    
    def blur(self):
        """Apply blur"""
        self.current_image = cv2.GaussianBlur(self.current_image, (15, 15), 0)
        print("✨ Applied: Blur")
    
    def edge_detection(self):
        """Apply edge detection"""
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        self.current_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        print("📐 Applied: Edge Detection")
    
    def negative(self):
        """Apply negative effect"""
        self.current_image = 255 - self.current_image
        print("🎭 Applied: Negative")
    
    def zoom_in(self):
        """Zoom in"""
        # TUGAS: Implement zoom in
        # Hint: Resize dengan scale > 1
        
        self.zoom_level *= 1.2
        height, width = self.original_image.shape[:2]
        new_width = int(width * self.zoom_level)
        new_height = int(height * self.zoom_level)
        
        # YOUR CODE HERE
        self.current_image = cv2.resize(self.current_image, 
                                       (new_width, new_height))
        
        print(f"🔍 Zoom In: {self.zoom_level:.2f}x")
    
    def zoom_out(self):
        """Zoom out"""
        # TUGAS: Implement zoom out
        # Hint: Resize dengan scale < 1
        
        self.zoom_level *= 0.8
        height, width = self.original_image.shape[:2]
        new_width = int(width * self.zoom_level)
        new_height = int(height * self.zoom_level)
        
        # YOUR CODE HERE
        self.current_image = cv2.resize(self.current_image, 
                                       (new_width, new_height))
        
        print(f"🔍 Zoom Out: {self.zoom_level:.2f}x")
    
    def crop_center(self):
        """Crop center 50%"""
        # TUGAS: Implement crop center
        # Hint: Ambil 50% dari tengah gambar
        
        height, width = self.current_image.shape[:2]
        
        # Calculate crop coordinates
        crop_width = width // 2
        crop_height = height // 2
        
        x1 = width // 4
        y1 = height // 4
        x2 = x1 + crop_width
        y2 = y1 + crop_height
        
        # YOUR CODE HERE
        self.current_image = self.current_image[y1:y2, x1:x2].copy()
        
        print(f"✂️  Cropped to: {self.current_image.shape[1]}x{self.current_image.shape[0]}")
    
    def save_image(self):
        """Save current image"""
        os.makedirs("output", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/edited_{timestamp}.jpg"
        
        # Add watermark before saving
        watermarked = self.add_watermark(self.current_image, "Edited with OpenCV")
        
        cv2.imwrite(filename, watermarked)
        print(f"💾 Image saved: {filename}")
    
    def reset(self):
        """Reset to original"""
        self.current_image = self.original_image.copy()
        self.zoom_level = 1.0
        print("↩️  Reset to original")
    
    def show_info(self):
        """Show image info"""
        height, width = self.current_image.shape[:2]
        print("\n" + "="*50)
        print("📊 IMAGE INFO")
        print("="*50)
        print(f"Size: {width} x {height}")
        print(f"Channels: {self.current_image.shape[2] if len(self.current_image.shape) == 3 else 1}")
        print(f"Data Type: {self.current_image.dtype}")
        print(f"Memory: {self.current_image.nbytes:,} bytes")
        print(f"Zoom Level: {self.zoom_level:.2f}x")
        print("="*50 + "\n")
    
    def run(self):
        """Run the editor"""
        self.show_instructions()
        
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        
        while True:
            # Display current image
            display_img = self.current_image.copy()
            
            # Add info overlay
            cv2.rectangle(display_img, (5, 5), (350, 40), (0, 0, 0), -1)
            cv2.putText(display_img, "Press 'i' for help", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow(self.window_name, display_img)
            
            # Wait for key
            key = cv2.waitKey(1) & 0xFF
            
            # Process key
            if key == ord('q') or key == 27:  # Quit
                print("\n👋 Exiting editor...")
                break
            
            elif key == ord('g'):  # Grayscale
                self.grayscale()
            
            elif key == ord('r'):  # Rotate
                self.rotate()
            
            elif key == ord('f'):  # Flip horizontal
                self.flip_horizontal()
            
            elif key == ord('v'):  # Flip vertical
                self.flip_vertical()
            
            elif key == ord('b'):  # Blur
                self.blur()
            
            elif key == ord('e'):  # Edge detection
                self.edge_detection()
            
            elif key == ord('n'):  # Negative
                self.negative()
            
            elif key in [ord('+'), ord('=')]:  # Zoom in
                self.zoom_in()
            
            elif key in [ord('-'), ord('_')]:  # Zoom out
                self.zoom_out()
            
            elif key == ord('c'):  # Crop
                self.crop_center()
            
            elif key == ord('s'):  # Save
                self.save_image()
            
            elif key == ord('z'):  # Reset
                self.reset()
            
            elif key == ord('i'):  # Info
                self.show_info()
        
        cv2.destroyAllWindows()
        print("✅ Editor closed")


def main():
    """Main function"""
    
    print("="*60)
    print("MINGGU 1 - LATIHAN: PHOTO EDITOR")
    print("="*60)
    
    # Check for sample image
    image_path = "samples/sample_image.jpg"
    
    if not os.path.exists(image_path):
        print(f"\n⚠️  Image not found: {image_path}")
        print("💡 Please run 1_hello_opencv.py first to create sample image")
        print("   Or place your own image in samples/sample_image.jpg")
        return
    
    try:
        # Create and run editor
        editor = PhotoEditor(image_path)
        editor.run()
        
        print("\n" + "="*60)
        print("LATIHAN SELESAI!")
        print("="*60)
        print("\n💡 TIPS UNTUK IMPROVEMENT:")
        print("   1. Tambahkan undo stack (multiple undo)")
        print("   2. Tambahkan histogram display")
        print("   3. Buat custom filter sendiri")
        print("   4. Tambahkan mouse crop (drag to select area)")
        print("   5. Save/load editor state")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


# ======================================
# CHALLENGE TAMBAHAN
# ======================================
"""
🏆 CHALLENGE UNTUK YANG MAU BELAJAR LEBIH:

1. UNDO STACK:
   - Simpan history of operations
   - Implement undo & redo
   - Limit history size (max 10)

2. HISTOGRAM:
   - Tampilkan color histogram
   - Show RGB distribution
   - Update real-time

3. CUSTOM FILTERS:
   - Brightness/Contrast adjustment
   - Sepia tone effect
   - Vignette effect
   - Sharpening

4. MOUSE INTERACTION:
   - Click and drag untuk crop
   - Draw on image
   - Color picker

5. BATCH PROCESSING:
   - Apply operation ke multiple images
   - Save all results
   - Progress bar

GOOD LUCK! 🚀
"""


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main()
