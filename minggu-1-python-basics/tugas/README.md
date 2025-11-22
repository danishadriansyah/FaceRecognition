# 📝 TUGAS MINGGU 1 - Photo Editor Sederhana (Fill in the Blanks)

## 📖 Deskripsi
Lengkapi program photo editor dengan mengisi bagian-bagian yang kosong (_____)

## 🎯 Objektif
Menguasai dasar-dasar OpenCV:
- Load & save images dengan `cv2.imread()` dan `cv2.imwrite()`
- Image transformations (grayscale, resize, rotate)
- Drawing (border, text watermark)
- Error handling

---

## 📋 SOAL - Isi Bagian yang Kosong!

File template: `photo_editor_template.py`

### ✏️ Daftar Soal

### ✏️ Daftar Soal

**SOAL 1** (Baris 51): Load image menggunakan fungsi OpenCV
```python
img = _________(f'input/{filename}')
```
💡 Hint: Fungsi untuk membaca image

**SOAL 2** (Baris 54): Cek apakah image berhasil dibaca
```python
if img is _________:
```
💡 Hint: Nilai yang dikembalikan jika file tidak ditemukan

**SOAL 3** (Baris 74): Convert ke grayscale
```python
gray = cv2.cvtColor(current_image, _________)
```
💡 Hint: Constant untuk BGR to GRAY

**SOAL 4** (Baris 92-93): Hitung ukuran baru untuk resize 50%
```python
new_width = int(width * _______)
new_height = int(height * _______)
```
💡 Hint: 50% dalam desimal

**SOAL 5** (Baris 97): Resize image ke ukuran baru
```python
current_image = cv2.resize(current_image, (___________, ___________))
```
💡 Hint: Tuple (width, height) yang baru

**SOAL 6** (Baris 112): Rotate image 90 derajat
```python
current_image = cv2.rotate(current_image, _________)
```
💡 Hint: Constant untuk rotate 90 clockwise

**SOAL 7** (Baris 132): Tambahkan border
```python
current_image = cv2.copyMakeBorder(
    current_image,
    _________, _________, _________, _________,  # top, bottom, left, right
    cv2.BORDER_CONSTANT,
    value=(0, 0, 255)
)
```
💡 Hint: Semua sisi gunakan variable `border_size`

**SOAL 8** (Baris 154, 159): Tambahkan text watermark
```python
cv2.putText(
    current_image,
    _________,              # text
    (10, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.2,
    (255, 255, 255),
    _________              # thickness
)
```
💡 Hint: Text dari variable `text`, thickness = 2

**SOAL 9** (Baris 177): Save image ke file
```python
success = _________(f'output/{filename}', current_image)
```
💡 Hint: Fungsi untuk write/save image

**SOAL 10** (Baris 180): Cek hasil save
```python
if _________:
```
💡 Hint: Variable yang menyimpan status success

**SOAL 11** (Baris 196): Reset ke original image
```python
current_image = _________.copy()
```
💡 Hint: Variable yang menyimpan image asli

**SOAL 12** (Baris 210): Ambil input dari user
```python
choice = _________("Pilih menu (1-9): ")
```
💡 Hint: Fungsi built-in Python untuk input string

**SOAL 13** (Baris 226): Condition untuk exit
```python
elif choice == '_____':
```
💡 Hint: Menu nomor berapa untuk exit?

---

## 📦 Struktur File

Siapkan struktur folder berikut:

```
tugas/
├── photo_editor_template.py    # Template dengan blanks (JANGAN EDIT INI)
├── photo_editor.py             # ISI JAWABAN KAMU DI SINI
├── input/                      # Taruh foto-foto untuk di-edit
│   ├── sample1.jpg
│   └── sample2.jpg
├── output/                     # Hasil edit akan tersimpan di sini
└── README.md
```

---

## 🚀 Cara Mengerjakan

### Step 1: Copy Template
```bash
cd tugas
copy photo_editor_template.py photo_editor.py
```

### Step 2: Isi Blanks
Buka `photo_editor.py` dan isi semua bagian yang kosong (_______)

### Step 3: Test Program
```bash
python photo_editor.py
```

### Step 4: Pastikan Semua Fitur Bekerja
- ✅ Load image dari folder input/
- ✅ Convert to grayscale
- ✅ Resize 50%
- ✅ Rotate 90°
- ✅ Add border merah
- ✅ Add watermark text
- ✅ Save ke folder output/
- ✅ Reset ke original

---

## 💡 Cheat Sheet - Fungsi OpenCV yang Dibutuhkan

| Fungsi | Kegunaan | Contoh |
|--------|----------|--------|
| `cv2.imread()` | Baca image dari file | `img = cv2.imread('photo.jpg')` |
| `cv2.imwrite()` | Save image ke file | `cv2.imwrite('result.jpg', img)` |
| `cv2.cvtColor()` | Convert color space | `gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` |
| `cv2.resize()` | Resize image | `small = cv2.resize(img, (320, 240))` |
| `cv2.rotate()` | Rotate image | `rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)` |
| `cv2.copyMakeBorder()` | Tambah border | `bordered = cv2.copyMakeBorder(img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(0,0,255))` |
| `cv2.putText()` | Tambah text | `cv2.putText(img, 'Hello', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)` |

### Constants Penting
- `cv2.COLOR_BGR2GRAY` - Convert BGR ke grayscale
- `cv2.COLOR_GRAY2BGR` - Convert grayscale ke BGR
- `cv2.ROTATE_90_CLOCKWISE` - Rotate 90° searah jarum jam
- `cv2.BORDER_CONSTANT` - Border dengan warna solid

---

## ✅ Checklist Pengerjaan

```
[ ] SOAL 1: cv2.imread() - Load image
[ ] SOAL 2: None - Cek error loading
[ ] SOAL 3: cv2.COLOR_BGR2GRAY - Grayscale conversion
[ ] SOAL 4: 0.5, 0.5 - Resize 50%
[ ] SOAL 5: new_width, new_height - Parameter resize
[ ] SOAL 6: cv2.ROTATE_90_CLOCKWISE - Rotate
[ ] SOAL 7: border_size (4x) - Border parameters
[ ] SOAL 8: text, 2 - Watermark text dan thickness
[ ] SOAL 9: cv2.imwrite() - Save image
[ ] SOAL 10: success - Cek hasil save
[ ] SOAL 11: original_image - Reset image
[ ] SOAL 12: input - Input dari user
[ ] SOAL 13: '9' - Exit condition
[ ] Program running tanpa error
[ ] Semua fitur berfungsi
```

---

---

## ✅ Kriteria Penilaian

| No | Soal | Poin |
|----|------|------|
| 1 | cv2.imread() | 8 pts |
| 2 | None check | 7 pts |
| 3 | cv2.COLOR_BGR2GRAY | 8 pts |
| 4 | Resize 0.5 (2 blanks) | 7 pts |
| 5 | new_width, new_height | 7 pts |
| 6 | cv2.ROTATE_90_CLOCKWISE | 8 pts |
| 7 | border_size (4 blanks) | 10 pts |
| 8 | text, thickness | 8 pts |
| 9 | cv2.imwrite() | 8 pts |
| 10 | success check | 7 pts |
| 11 | original_image.copy() | 7 pts |
| 12 | input() | 7 pts |
| 13 | '9' exit condition | 8 pts |
| **TOTAL** | | **100 pts** |

### Bonus
- ✅ Semua fitur working: +10 pts
- ✅ Code rapi & commented: +5 pts

---

## 🎓 Learning Outcomes

Setelah tugas ini, kamu akan bisa:
- ✅ Load dan save images dengan OpenCV
- ✅ Manipulasi image (grayscale, resize, rotate)
- ✅ Menambahkan border dan text
- ✅ Handle user input dan menu loop
- ✅ Basic error handling

---

## 🆘 Troubleshooting

**Q: Dimana saya cari jawabannya?**  
A: Lihat file-file di `minggu-1-python-basics/learning/lesson-1/` dan `lesson-2/`

**Q: Masih bingung fungsi apa yang dipakai?**  
A: Cek "Cheat Sheet" di atas atau OpenCV documentation

**Q: Error "module not found"?**  
A: Pastikan sudah `pip install opencv-python`

**Q: Image tidak terbaca?**  
A: Pastikan folder `input/` ada dan ada file image di dalamnya

---

## 📚 Resources

- Minggu 1 Lesson 1 & 2 (`learning/lesson-1/main.py`, `learning/lesson-2/main.py`)
- [OpenCV Documentation](https://docs.opencv.org/4.x/)
- Cheat sheet di README ini

---

**Good luck! 🚀 Semangat ngisi blanks-nya!**
