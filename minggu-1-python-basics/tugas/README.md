# 📝 TUGAS MINGGU 1 - Python & OpenCV Basics

## Deskripsi
Buat program sederhana untuk memproses gambar menggunakan OpenCV dengan fitur-fitur dasar.

---

## 🎯 Objektif
Menguasai dasar-dasar OpenCV:
- Load & save images
- Image transformations
- Drawing shapes
- Webcam operations

---

## 📋 Tugas: Photo Editor Sederhana

Buat program `photo_editor.py` yang bisa:

### Fitur Wajib (Minimum Requirements)
1. **Load Image** - User bisa pilih gambar
2. **Edit Menu** dengan pilihan:
   - Grayscale conversion
   - Resize (2x lebih kecil)
   - Rotate 90 derajat
   - Add border/frame
   - Add text watermark
3. **Save Result** - Simpan hasil edit
4. **Simple GUI** - Tampilan terminal menu interaktif

### Contoh Output Program:
```
========================================
    PHOTO EDITOR SEDERHANA
========================================

1. Load Image
2. Convert to Grayscale
3. Resize Image (50%)
4. Rotate 90°
5. Add Border
6. Add Watermark
7. Save Image
8. Exit

Pilih menu: _
```

---

## 📦 Deliverables

Kumpulkan file-file berikut di folder `tugas/`:

1. **photo_editor.py** - Main program
2. **input/** - Folder untuk input images (sertakan 2-3 sample)
3. **output/** - Folder untuk hasil edit
4. **README.md** - Dokumentasi:
   - Cara run program
   - Fitur yang dibuat
   - Screenshot hasil

---

## 💡 Hints & Tips

### Load Image
```python
import cv2

filename = input("Nama file: ")
img = cv2.imread(f'input/{filename}')

if img is None:
    print("Error: File not found")
```

### Menu Loop
```python
while True:
    print("\n1. Grayscale")
    print("2. Resize")
    print("3. Exit")
    
    choice = input("Pilih: ")
    
    if choice == '1':
        # Grayscale code
    elif choice == '3':
        break
```

### Add Border
```python
bordered = cv2.copyMakeBorder(
    img, 20, 20, 20, 20,  # top, bottom, left, right
    cv2.BORDER_CONSTANT,
    value=(0, 0, 255)  # Red border
)
```

### Add Watermark
```python
cv2.putText(
    img, 
    'My Photo Editor', 
    (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX,
    1, 
    (255, 255, 255), 
    2
)
```

---

## ✅ Kriteria Penilaian

| Kriteria | Bobot | Deskripsi |
|----------|-------|-----------|
| **Fungsionalitas** | 40% | Semua fitur wajib berfungsi |
| **Code Quality** | 30% | Clean code, ada comments |
| **Dokumentasi** | 20% | README jelas, ada screenshot |
| **Kreativitas** | 10% | Fitur tambahan/UI menarik |

### Breakdown:
- ✅ Load & save image bekerja: **10 pts**
- ✅ Minimal 4 fitur edit: **20 pts**
- ✅ Menu interaktif: **10 pts**
- ✅ Code rapi & commented: **30 pts**
- ✅ Dokumentasi lengkap: **20 pts**
- ✅ Fitur bonus/kreativitas: **10 pts**

**Total: 100 points**

---

## 🌟 Fitur Bonus (Optional)

Tambah nilai extra dengan:
- [ ] Multiple image support (batch processing)
- [ ] Flip horizontal/vertical
- [ ] Brightness/contrast adjustment
- [ ] Blur/sharpen effect
- [ ] Undo/redo functionality
- [ ] Save edit history
- [ ] Preview before save

---

## ⏰ Deadline

**3 hari** setelah menyelesaikan Minggu 1

---

## 📤 Cara Submit

1. Pastikan struktur folder:
   ```
   tugas/
   ├── photo_editor.py
   ├── input/
   │   ├── sample1.jpg
   │   └── sample2.jpg
   ├── output/
   │   └── (hasil edit)
   └── README.md
   ```

2. Test program sekali lagi
3. Screenshot hasil untuk dokumentasi
4. Update README.md dengan screenshots

---

## 🎓 Learning Outcomes

Setelah tugas ini, kamu akan bisa:
- ✅ Manipulasi gambar dengan OpenCV
- ✅ Handle user input
- ✅ Create interactive menu
- ✅ Manage file I/O operations
- ✅ Basic error handling

---

## 🆘 Troubleshooting

**Q: Image tidak terbaca?**  
A: Cek path file dan format (jpg/png)

**Q: Error saat save?**  
A: Pastikan folder output/ exists

**Q: Hasil blur/tidak jelas?**  
A: Cek ukuran resize, jangan terlalu kecil

---

## 📚 Resources

- [OpenCV Documentation](https://docs.opencv.org/4.x/)
- Minggu 1 Lesson 1 & 2
- File `01_hello_opencv.py` - `04_webcam_basics.py`

---

**Good luck! 🚀**
