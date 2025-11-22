"""
📝 TUGAS MINGGU 1 - Photo Editor Sederhana
Fill in the blanks untuk melengkapi program!

Petunjuk:
- Isi bagian yang ditandai dengan _________
- Setiap blank diberi nomor untuk memudahkan
- Cek README.md untuk hints!
"""

import cv2
import os

# Pastikan folder output exists
if not os.path.exists('output'):
    os.makedirs('output')

# Global variable untuk menyimpan image
current_image = None
original_image = None


def show_menu():
    """Tampilkan menu utama"""
    print("\n" + "="*40)
    print("    PHOTO EDITOR SEDERHANA")
    print("="*40)
    print("1. Load Image")
    print("2. Convert to Grayscale")
    print("3. Resize Image (50%)")
    print("4. Rotate 90°")
    print("5. Add Border")
    print("6. Add Watermark")
    print("7. Save Image")
    print("8. Reset to Original")
    print("9. Exit")
    print("="*40)


def load_image():
    """
    Load image dari folder input
    Return: True jika berhasil, False jika gagal
    """
    global current_image, original_image
    
    filename = input("Nama file (contoh: photo.jpg): ")
    
    # SOAL 1: Baca image menggunakan cv2.imread()
    # Hint: Gunakan path 'input/{filename}'
    img = _________(f'input/{filename}')
    
    # SOAL 2: Cek apakah image berhasil dibaca (img is None atau tidak)
    if img is _________:
        print("❌ Error: File tidak ditemukan!")
        return False
    
    current_image = img.copy()
    original_image = img.copy()
    print(f"✅ Image loaded: {img.shape}")
    return True


def convert_grayscale():
    """Convert image ke grayscale"""
    global current_image
    
    if current_image is None:
        print("⚠️ Load image terlebih dahulu!")
        return
    
    # SOAL 3: Convert ke grayscale menggunakan cv2.cvtColor()
    # Hint: Gunakan cv2.COLOR_BGR2GRAY
    gray = cv2.cvtColor(current_image, _________)
    
    # Convert back to BGR agar bisa di-combine dengan operasi lain
    current_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    print("✅ Converted to grayscale")


def resize_image():
    """Resize image menjadi 50% dari ukuran asli"""
    global current_image
    
    if current_image is None:
        print("⚠️ Load image terlebih dahulu!")
        return
    
    # SOAL 4: Hitung ukuran baru (50% dari original)
    # Hint: width dan height adalah current_image.shape[1] dan shape[0]
    height, width = current_image.shape[:2]
    new_width = int(width * _______)   # 50% = 0.5
    new_height = int(height * _______)
    
    # SOAL 5: Resize menggunakan cv2.resize()
    # Hint: cv2.resize(image, (new_width, new_height))
    current_image = cv2.resize(current_image, (___________, ___________))
    
    print(f"✅ Resized to {new_width}x{new_height}")


def rotate_image():
    """Rotate image 90 derajat searah jarum jam"""
    global current_image
    
    if current_image is None:
        print("⚠️ Load image terlebih dahulu!")
        return
    
    # SOAL 6: Rotate 90 derajat menggunakan cv2.rotate()
    # Hint: Gunakan cv2.ROTATE_90_CLOCKWISE
    current_image = cv2.rotate(current_image, _________)
    
    print("✅ Rotated 90° clockwise")


def add_border():
    """Tambahkan border merah di sekitar image"""
    global current_image
    
    if current_image is None:
        print("⚠️ Load image terlebih dahulu!")
        return
    
    border_size = 20
    
    # SOAL 7: Tambahkan border menggunakan cv2.copyMakeBorder()
    # Hint: Parameter: (image, top, bottom, left, right, border_type, value)
    # Border merah = (0, 0, 255) dalam BGR
    current_image = cv2.copyMakeBorder(
        current_image,
        _________, _________, _________, _________,  # top, bottom, left, right (semua = border_size)
        cv2.BORDER_CONSTANT,
        value=(0, 0, 255)  # Red border
    )
    
    print("✅ Border added")


def add_watermark():
    """Tambahkan text watermark"""
    global current_image
    
    if current_image is None:
        print("⚠️ Load image terlebih dahulu!")
        return
    
    text = input("Watermark text (default: 'My Photo'): ") or "My Photo"
    
    # SOAL 8: Tambahkan text menggunakan cv2.putText()
    # Hint: Parameter: (image, text, position, font, scale, color, thickness)
    cv2.putText(
        current_image,
        _________,              # text
        (10, 40),              # position
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,                   # scale
        (255, 255, 255),       # white color
        _________              # thickness (gunakan 2)
    )
    
    print("✅ Watermark added")


def save_image():
    """Save image hasil edit"""
    global current_image
    
    if current_image is None:
        print("⚠️ Tidak ada image untuk disimpan!")
        return
    
    filename = input("Nama file output (contoh: result.jpg): ")
    
    # SOAL 9: Save image menggunakan cv2.imwrite()
    # Hint: cv2.imwrite(path, image)
    success = _________(f'output/{filename}', current_image)
    
    # SOAL 10: Cek apakah save berhasil
    if _________:
        print(f"✅ Image saved to output/{filename}")
    else:
        print("❌ Error saving image!")


def reset_image():
    """Reset ke image original"""
    global current_image, original_image
    
    if original_image is None:
        print("⚠️ Tidak ada image original!")
        return
    
    # SOAL 11: Copy original_image ke current_image
    # Hint: Gunakan .copy() agar tidak reference yang sama
    current_image = _________.copy()
    
    print("✅ Reset to original image")


def main():
    """Main program loop"""
    print("🎨 Selamat datang di Photo Editor Sederhana!")
    print("📂 Pastikan ada folder 'input/' dengan foto-foto kamu")
    
    while True:
        show_menu()
        
        # SOAL 12: Ambil input pilihan dari user
        choice = _________("Pilih menu (1-9): ")
        
        if choice == '1':
            load_image()
        elif choice == '2':
            convert_grayscale()
        elif choice == '3':
            resize_image()
        elif choice == '4':
            rotate_image()
        elif choice == '5':
            add_border()
        elif choice == '6':
            add_watermark()
        elif choice == '7':
            save_image()
        elif choice == '8':
            reset_image()
        # SOAL 13: Tambahkan condition untuk exit (choice == '9')
        elif choice == '_____':
            print("👋 Terima kasih! Sampai jumpa!")
            break
        else:
            print("❌ Pilihan tidak valid!")


if __name__ == "__main__":
    main()
