# Minggu 1 - Learning Tutorials

##  Overview
Folder ini berisi 5 tutorial files untuk belajar dasar-dasar Python, OpenCV, dan image processing. Setiap file adalah standalone tutorial yang bisa dijalankan langsung untuk memahami konsep step-by-step.

##  File Structure

```
learning/
 README.md (file ini)
 01_hello_opencv.py
 02_image_operations.py
 03_drawing_shapes.py
 04_webcam_basics.py
 latihan.py
 output/ (folder untuk menyimpan hasil)
```

---

##  Tutorial Files - Detailed Guide

### 01_hello_opencv.py
**Tujuan:** Pengenalan dasar OpenCV dan cara kerja image processing

**Apa yang dipelajari:**
- Install dan import OpenCV
- Load image dari file
- Display image di window
- Menyimpan image
- Basic image properties (width, height, channels)

**Cara menggunakan:**
```bash
cd minggu-1-python-basics/learning
python 01_hello_opencv.py
```

**Output yang diharapkan:**
- Window muncul menampilkan gambar
- Console print: dimensi image (width x height)
- File tersimpan di folder output/

**Konsep penting:**
- cv2.imread() - Membaca gambar
- cv2.imshow() - Menampilkan gambar  
- cv2.waitKey() - Menunggu input keyboard
- cv2.imwrite() - Menyimpan gambar

---

### 02_image_operations.py
**Tujuan:** Operasi dasar pada image (resize, crop, rotate, flip)

**Apa yang dipelajari:**
- Resize image ke ukuran tertentu
- Crop bagian tertentu dari image
- Rotate image dengan berbagai sudut
- Flip image (horizontal/vertical)
- Convert color spaces (BGR, RGB, Grayscale, HSV)

**Cara menggunakan:**
```bash
python 02_image_operations.py
```

**Output yang diharapkan:**
- Multiple windows menampilkan hasil operasi
- File hasil disimpan di output/
- Console print: ukuran sebelum dan sesudah resize

**Konsep penting:**
- cv2.resize() - Mengubah ukuran
- Array slicing untuk crop: image[y1:y2, x1:x2]
- cv2.getRotationMatrix2D() - Matrix rotasi
- cv2.flip() - Flip image
- cv2.cvtColor() - Convert color space

**Tips:**
- Image adalah NumPy array: rows x columns x channels
- Koordinat: (x, y) = (kolom, baris)
- BGR adalah default OpenCV (bukan RGB!)

---

### 03_drawing_shapes.py
**Tujuan:** Menggambar shapes dan text pada image

**Apa yang dipelajari:**
- Menggambar rectangle (kotak)
- Menggambar circle (lingkaran)
- Menggambar line (garis)
- Menulis text pada image
- Menggunakan berbagai colors dan thickness

**Cara menggunakan:**
```bash
python 03_drawing_shapes.py
```

**Output yang diharapkan:**
- Window dengan berbagai shapes
- Rectangle dengan berbagai warna
- Circle dan lines
- Text annotations

**Konsep penting:**
- cv2.rectangle() - Gambar kotak
- cv2.circle() - Gambar lingkaran
- cv2.line() - Gambar garis
- cv2.putText() - Tulis text
- Color format: (B, G, R) dalam tuple
- Thickness: -1 = filled, positive = outline

**Use case:**
- Drawing bounding boxes untuk face detection (minggu 2)
- Annotate images dengan labels
- Visualisasi hasil processing

---

### 04_webcam_basics.py
**Tujuan:** Akses webcam dan real-time video processing

**Apa yang dipelajari:**
- Initialize webcam dengan VideoCapture
- Read frames dari webcam
- Display real-time video
- Apply transformations pada live video
- Release camera resource dengan benar

**Cara menggunakan:**
```bash
python 04_webcam_basics.py
```

**Output yang diharapkan:**
- Window menampilkan live webcam feed
- Press 'g' untuk grayscale
- Press 'b' untuk blur
- Press 's' untuk save screenshot
- Press 'q' untuk quit

**Konsep penting:**
- cv2.VideoCapture(0) - Akses kamera (0 = default camera)
- cap.read() - Baca frame (returns: success, frame)
- Infinite loop untuk streaming: while True:
- cap.release() - Release camera saat selesai
- cv2.destroyAllWindows() - Tutup semua windows

**Troubleshooting:**
- Jika camera tidak terdeteksi, coba index 1 atau 2
- Tutup aplikasi lain yang pakai camera (Zoom, Skype)
- Check permission camera di system settings

**Tips:**
- Selalu release camera dengan cap.release()
- Gunakan waitKey(1) untuk real-time (bukan waitKey(0))
- Frame rate tergantung processing speed

---

### latihan.py
**Tujuan:** Mini project untuk praktik semua konsep yang sudah dipelajari

**Apa yang harus dibuat:**
Aplikasi webcam sederhana dengan fitur:
1. Live webcam display
2. Apply grayscale filter (press 'g')
3. Apply blur filter (press 'b')
4. Draw rectangle di tengah frame
5. Save screenshot (press 's')
6. Quit (press 'q')

**Cara mengerjakan:**
```bash
python latihan.py
```

**Langkah-langkah pengerjaan:**
1. Initialize webcam menggunakan cv2.VideoCapture(0)
2. Buat infinite loop untuk streaming
3. Read frame dari camera
4. Implement keyboard controls:
   - 'g'  convert to grayscale
   - 'b'  apply Gaussian blur
   - 's'  save current frame
   - 'q'  quit
5. Draw rectangle hijau di tengah frame
6. Display frame dengan cv2.imshow()
7. Release resources saat quit

**Expected behavior:**
- Window menampilkan webcam
- Rectangle hijau di tengah layar
- Filters bekerja saat tombol ditekan
- Screenshot tersimpan ke file
- Aplikasi close dengan bersih

**Konsep yang digunakan:**
- VideoCapture untuk webcam
- waitKey untuk keyboard input
- cvtColor untuk grayscale
- GaussianBlur untuk blur effect
- rectangle untuk drawing
- imwrite untuk save

**Tips:**
- Gunakan variable mode untuk track filter state
- Reset ke normal saat filter ditekan lagi
- Format filename: screenshot_timestamp.jpg

---

##  Cara Belajar yang Efektif

### Step 1: Baca Code
Buka file, baca line by line, pahami setiap fungsi

### Step 2: Run Program
Jalankan dan lihat output:
```bash
python 01_hello_opencv.py
```

### Step 3: Eksperimen
Ubah parameter, lihat apa yang terjadi:
- Ganti ukuran resize
- Ubah warna rectangle
- Ganti angle rotasi

### Step 4: Debug
Jika error, baca error message dengan teliti:
- Module not found  install package
- File not found  check path
- Camera error  check permissions

### Step 5: Praktik
Kerjakan latihan.py tanpa lihat code lain

---

##  Checklist Progress

```
[ ] 01_hello_opencv.py - Selesai dibaca dan dijalankan
[ ] 02_image_operations.py - Selesai dibaca dan dijalankan
[ ] 03_drawing_shapes.py - Selesai dibaca dan dijalankan
[ ] 04_webcam_basics.py - Selesai dibaca dan dijalankan
[ ] latihan.py - Selesai dikerjakan dan berfungsi
[ ] Semua konsep dipahami dengan baik
```

---

##  Common Issues & Solutions

**Import Error: No module named 'cv2'**
```bash
pip install opencv-python
```

**Image tidak muncul**
- Pastikan file image ada di path yang benar
- Gunakan absolute path atau relative path yang benar
- Check apakah cv2.waitKey() dipanggil

**Webcam tidak terdeteksi**
- Coba camera index 0, 1, atau 2
- Close aplikasi lain yang pakai camera
- Check system permissions untuk camera access

**Window freeze**
- Pastikan ada cv2.waitKey() di dalam loop
- Jangan pakai waitKey(0) untuk video streaming
- Gunakan waitKey(1) untuk real-time

**Error: (-215:Assertion failed)**
- Check apakah image berhasil di-load (not None)
- Verify file path benar
- Pastikan image format supported (jpg, png)

---

##  Key Concepts Summary

### Image Representation
- Images adalah NumPy arrays
- Shape: (height, width, channels)
- Color format: BGR (not RGB)
- Data type: uint8 (0-255)

### Coordinates System
- Origin (0,0) is top-left corner
- X-axis: left to right (width)
- Y-axis: top to bottom (height)

### Color Spaces
- BGR: Default OpenCV format
- RGB: Standard image format
- Grayscale: Single channel (0-255)
- HSV: Hue, Saturation, Value

### Best Practices
- Always check if image loaded successfully
- Use .copy() to avoid modifying original
- Call cv2.destroyAllWindows() after display
- Release camera with cap.release()
- Handle keyboard input properly

---

##  Additional Resources

- OpenCV Documentation: https://docs.opencv.org/
- OpenCV Python Tutorials: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
- NumPy Documentation: https://numpy.org/doc/
- Python Image Processing: https://opencv-python-tutroals.readthedocs.io/

---

##  Next Steps

Setelah selesai semua tutorial di folder ini:

1.  Pastikan semua file berjalan tanpa error
2.  Kerjakan latihan.py sampai selesai
3.  Pindah ke folder ../project/ untuk lihat implementasi module
4.  Jalankan test: python ../project/test_utils.py
5.  Lanjut ke Minggu 2: Face Detection

---

**Selamat Belajar! **

*Remember: Practice makes perfect. Coding adalah skill yang harus dipraktikkan setiap hari!*
