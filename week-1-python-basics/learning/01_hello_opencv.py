"""
Minggu 1 - File 1: Hello OpenCV
Konsep: Pengenalan OpenCV, Membaca dan Menampilkan Gambar

Tujuan:
- Memahami cara import OpenCV
- Membaca gambar dari file
- Menampilkan gambar di window
- Menyimpan gambar
- Handle keyboard input
"""

import cv2
import numpy as np
import os

def main():
    """
    Program pertama OpenCV: Hello World of Computer Vision
    """
    
    print("="*50)
    print("HELLO OPENCV - Minggu 1")
    print("="*50)
    print("\nProgram ini akan:")
    print("1. Membaca gambar")
    print("2. Menampilkan informasi gambar")
    print("3. Menampilkan gambar di window")
    print("4. Menyimpan hasil\n")
    
    # STEP 1: Membaca Gambar
    image_path = "samples/sample_image.jpg"
    
    # Cek apakah file ada
    if not os.path.exists(image_path):
        print(f"File {image_path} tidak ditemukan!")
        print("Membuat gambar placeholder...")
        
        os.makedirs("samples", exist_ok=True)
        
        # Buat gambar placeholder (kotak berwarna)
        placeholder = np.zeros((400, 600, 3), dtype=np.uint8)
        placeholder[:, :] = (100, 150, 200)  # BGR: Orange-ish color
        
        # Tambahkan text
        cv2.putText(placeholder, "SAMPLE IMAGE", (150, 180), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        cv2.putText(placeholder, "Ganti dengan gambar sendiri", (120, 230), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        cv2.imwrite(image_path, placeholder)
        print(f"Placeholder created: {image_path}")
    
    # Baca gambar
    image = cv2.imread(image_path)
    
    # Cek apakah berhasil dibaca
    if image is None:
        print("Error: Tidak bisa membaca gambar!")
        return
    
    print(f"Gambar berhasil dibaca: {image_path}")
    
    # STEP 2: Informasi Gambar
    height, width, channels = image.shape
    
    print("\n" + "="*50)
    print("INFORMASI GAMBAR")
    print("="*50)
    print(f"Ukuran (Height x Width): {height} x {width}")
    print(f"Jumlah Channel: {channels}")
    print(f"Total Pixels: {height * width:,}")
    print(f"Data Type: {image.dtype}")
    print(f"Size in Memory: {image.nbytes:,} bytes")
    
    # Pixel di pojok kiri atas
    top_left_pixel = image[0, 0]
    print(f"\nPixel di (0,0) [BGR]: {top_left_pixel}")
    print(f"   Blue: {top_left_pixel[0]}, Green: {top_left_pixel[1]}, Red: {top_left_pixel[2]}")
    
    # STEP 3: Menampilkan Gambar
    print("\n" + "="*50)
    print("MENAMPILKAN GAMBAR")
    print("="*50)
    print("Window akan terbuka...")
    print("Controls:")
    print("   - Tekan 'q' atau ESC untuk keluar")
    print("   - Tekan 's' untuk save gambar")
    print("   - Tekan 'i' untuk info gambar")
    
    # Buat window dengan nama
    window_name = "Hello OpenCV - Image Viewer"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    # Tampilkan gambar
    cv2.imshow(window_name, image)
    
    # STEP 4: Keyboard Control Loop
    while True:
        key = cv2.waitKey(1) & 0xFF
        
        # ESC or 'q' = quit
        if key == 27 or key == ord('q'):
            print("\nKeluar dari program...")
            break
        
        # 's' = save
        elif key == ord('s'):
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, "saved_image.jpg")
            
            cv2.imwrite(output_path, image)
            print(f"Gambar disimpan: {output_path}")
        
        # 'i' = info
        elif key == ord('i'):
            print("\nImage Info:")
            print(f"   Shape: {image.shape}")
            print(f"   Min pixel value: {image.min()}")
            print(f"   Max pixel value: {image.max()}")
            print(f"   Mean pixel value: {image.mean():.2f}")
    
    # STEP 5: Cleanup
    cv2.destroyAllWindows()
    print("Program selesai!\n")


# KONSEP PENTING
"""
1. OpenCV Image Format:
   - Disimpan sebagai NumPy array
   - Format: BGR (bukan RGB)
   - Shape: (height, width, channels)
   - Data type: uint8 (0-255)

2. cv2.imread() Flags:
   - cv2.IMREAD_COLOR: Load sebagai BGR (default)
   - cv2.IMREAD_GRAYSCALE: Load sebagai grayscale
   - cv2.IMREAD_UNCHANGED: Load dengan alpha channel

3. Window Types:
   - cv2.WINDOW_NORMAL: Resizable window
   - cv2.WINDOW_AUTOSIZE: Fixed size (default)

4. cv2.waitKey():
   - Parameter: delay dalam milliseconds
   - Return: ASCII code dari key yang ditekan
   - 0 = wait forever
   - & 0xFF = untuk compatibility 64-bit systems
"""


# LATIHAN
"""
LATIHAN:

1. Ganti sample image dengan foto kamu sendiri
2. Tambahkan fitur untuk rotate image (tekan 'r')
3. Tambahkan counter untuk berapa kali image di-save
4. Buat window yang menampilkan image asli dan grayscale side-by-side
5. Tampilkan koordinat mouse saat di-hover (gunakan cv2.setMouseCallback)

HINTS:
- Rotate: cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
- Grayscale: cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
- Horizontal stack: np.hstack([img1, img2])
"""


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main()
