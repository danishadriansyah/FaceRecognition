"""
EXAMPLE: Cara menggunakan path_utils.py di tutorial files

Copy helper functions ini ke file tutorial kamu, atau
import dari path_utils.py di project root.
"""

import cv2
import os


# ==================== HELPER FUNCTIONS ====================
# Copy functions ini ke tutorial kamu untuk handle paths dengan benar

def get_script_dir():
    """Get directory dimana script dijalankan"""
    return os.path.dirname(os.path.abspath(__file__))


def get_output_path(filename, subfolder='output'):
    """
    Get full path untuk output file & create folder kalau belum ada
    
    Example:
        output_path = get_output_path('result.jpg')
        # Returns: C:/path/to/minggu-X/learning/output/result.jpg
    """
    output_dir = os.path.join(get_script_dir(), subfolder)
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, filename)


def get_input_path(filename, subfolder='images'):
    """
    Get full path untuk input file
    
    Example:
        input_path = get_input_path('sample.jpg')
        # Returns: C:/path/to/minggu-X/learning/images/sample.jpg
    """
    return os.path.join(get_script_dir(), subfolder, filename)


# ==================== USAGE EXAMPLES ====================

def example_1_basic_usage():
    """Example 1: Basic image read & write"""
    print("\n" + "="*50)
    print("Example 1: Basic Image Read & Write")
    print("="*50)
    
    # ❌ JANGAN seperti ini (hardcoding)
    # img = cv2.imread('C:/Users/nama/Desktop/sample.jpg')
    # cv2.imwrite('C:/Users/nama/Desktop/result.jpg', img)
    
    # ✅ GUNAKAN helper functions
    # Buat dummy image untuk demo
    img = cv2.imread(cv2.samples.findFile('lena.jpg'))
    
    if img is not None:
        # Save dengan path helper
        output_path = get_output_path('example1_result.jpg')
        cv2.imwrite(output_path, img)
        print(f"✅ Image saved to: {output_path}")
    else:
        print("ℹ️ Lena image not found, skipping...")


def example_2_with_input_folder():
    """Example 2: Read from images/ folder"""
    print("\n" + "="*50)
    print("Example 2: Read from images/ Folder")
    print("="*50)
    
    # Put your test images in: minggu-X/learning/images/
    # Then read like this:
    
    input_path = get_input_path('sample.jpg')
    print(f"Looking for image at: {input_path}")
    
    img = cv2.imread(input_path)
    
    if img is not None:
        # Process image...
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Save result
        output_path = get_output_path('example2_grayscale.jpg')
        cv2.imwrite(output_path, gray)
        print(f"✅ Grayscale image saved to: {output_path}")
    else:
        print(f"⚠️ Image not found at: {input_path}")
        print(f"   Please put test image at: {os.path.dirname(input_path)}/")


def example_3_multiple_outputs():
    """Example 3: Save multiple output files"""
    print("\n" + "="*50)
    print("Example 3: Multiple Output Files")
    print("="*50)
    
    # Create sample image
    img = cv2.imread(cv2.samples.findFile('lena.jpg'))
    
    if img is not None:
        # Different processing results
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(img, (15, 15), 0)
        edges = cv2.Canny(gray, 100, 200)
        
        # Save all results (otomatis ke output/ folder)
        cv2.imwrite(get_output_path('step1_grayscale.jpg'), gray)
        cv2.imwrite(get_output_path('step2_blur.jpg'), blur)
        cv2.imwrite(get_output_path('step3_edges.jpg'), edges)
        
        print("✅ Saved 3 output files:")
        print(f"   - {get_output_path('step1_grayscale.jpg')}")
        print(f"   - {get_output_path('step2_blur.jpg')}")
        print(f"   - {get_output_path('step3_edges.jpg')}")
    else:
        print("ℹ️ Sample image not found, skipping...")


def example_4_webcam_capture():
    """Example 4: Capture from webcam & save"""
    print("\n" + "="*50)
    print("Example 4: Webcam Capture")
    print("="*50)
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("⚠️ Cannot access webcam")
        return
    
    print("📷 Press SPACE to capture, ESC to exit...")
    
    capture_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Webcam - Press SPACE to capture', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == 27:  # ESC
            break
        elif key == 32:  # SPACE
            capture_count += 1
            
            # Save captured frame (otomatis ke output/)
            filename = f'capture_{capture_count:03d}.jpg'
            output_path = get_output_path(filename)
            cv2.imwrite(output_path, frame)
            
            print(f"✅ Captured: {filename}")
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n✅ Total captures: {capture_count}")
    print(f"   Saved to: {os.path.join(get_script_dir(), 'output')}/")


def example_5_custom_subfolder():
    """Example 5: Use custom subfolder"""
    print("\n" + "="*50)
    print("Example 5: Custom Subfolder")
    print("="*50)
    
    # Create sample image
    img = cv2.imread(cv2.samples.findFile('lena.jpg'))
    
    if img is not None:
        # Save to different subfolders
        output_path_1 = get_output_path('result.jpg', subfolder='output')
        output_path_2 = get_output_path('backup.jpg', subfolder='backups')
        
        cv2.imwrite(output_path_1, img)
        cv2.imwrite(output_path_2, img)
        
        print("✅ Saved to multiple folders:")
        print(f"   - {output_path_1}")
        print(f"   - {output_path_2}")
    else:
        print("ℹ️ Sample image not found, skipping...")


def example_6_list_output_files():
    """Example 6: List all output files"""
    print("\n" + "="*50)
    print("Example 6: List Output Files")
    print("="*50)
    
    output_dir = os.path.join(get_script_dir(), 'output')
    
    if os.path.exists(output_dir):
        files = [f for f in os.listdir(output_dir) if f.endswith(('.jpg', '.png'))]
        
        if files:
            print(f"📂 Found {len(files)} image(s) in output/ folder:")
            for i, filename in enumerate(files, 1):
                filepath = os.path.join(output_dir, filename)
                size_kb = os.path.getsize(filepath) / 1024
                print(f"   {i}. {filename} ({size_kb:.1f} KB)")
        else:
            print("ℹ️ No images in output/ folder yet")
    else:
        print("ℹ️ output/ folder not created yet")


# ==================== MAIN ====================

if __name__ == '__main__':
    print("\n" + "="*70)
    print(" "*20 + "PATH UTILITIES - USAGE EXAMPLES")
    print("="*70)
    
    print("\n📋 Konsep Penting:")
    print("   1. Semua input files di: learning/images/ atau project/test_images/")
    print("   2. Semua output files di: learning/output/ atau project/output/")
    print("   3. Gunakan helper functions, JANGAN hardcode paths!")
    print("   4. Output otomatis terorganisir dalam folder mingguannya")
    
    # Run all examples
    example_1_basic_usage()
    example_2_with_input_folder()
    example_3_multiple_outputs()
    # example_4_webcam_capture()  # Uncomment untuk test webcam
    example_5_custom_subfolder()
    example_6_list_output_files()
    
    print("\n" + "="*70)
    print("✅ All examples completed!")
    print("="*70)
    
    print("\n📝 Tips:")
    print("   - Copy helper functions ke file tutorial kamu")
    print("   - Atau import dari: ../../path_utils.py")
    print("   - Selalu gunakan get_output_path() untuk save files")
    print("   - Selalu gunakan get_input_path() untuk read files")
    print("   - Output akan otomatis ke folder yang benar!")
    
    print("\n🎯 Next Steps:")
    print("   1. Buat file di minggu-X/learning/images/sample.jpg")
    print("   2. Jalankan example ini lagi")
    print("   3. Check hasil di minggu-X/learning/output/")
    print("   4. Terapkan di tutorial files kamu!\n")
