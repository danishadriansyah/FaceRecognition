# 🔨 App Build - Face Recognition Attendance System

Build project menjadi aplikasi standalone (.exe) yang bisa langsung dijalankan **tanpa install Python**.

## Cara Build

### Prasyarat
- Python 3.11 (sudah terinstall di komputer ini)
- Koneksi internet (untuk download PyInstaller pertama kali)

### Langkah Build
```bash
cd app-build
python build.py
```

Tunggu 10-20 menit. Hasil ada di `dist/FaceAttendance/`.

## Struktur Hasil Build

```
dist/
├── Jalankan_Aplikasi.bat      ← Double-click untuk jalankan!
└── FaceAttendance/
    ├── FaceAttendance.exe     ← Aplikasi utama
    ├── config.json            ← Pengaturan
    ├── models/                ← Taruh model di sini
    │   └── default_.../
    │       ├── keras_model.h5
    │       └── labels.txt
    ├── logs/                  ← Data absensi tersimpan di sini
    │   ├── attendance.csv
    │   └── photos/
    ├── reports/               ← Report yang di-generate
    ├── dataset/               ← Dataset foto (opsional)
    └── _internal/             ← File system (jangan dihapus)
```

## Distribusi ke Student

1. Copy **seluruh folder** `dist/FaceAttendance/` ke USB / upload ke Google Drive
2. Pastikan folder `models/` sudah berisi `keras_model.h5` + `labels.txt`
3. Student tinggal extract dan **double-click** `Jalankan_Aplikasi.bat`
4. Tidak perlu install Python, pip, atau library apapun!

## ⚠️ Catatan Penting
- File .exe hanya bisa dijalankan di **Windows**
- Ukuran total ~500MB - 1GB (karena bundle TensorFlow + OpenCV)
- Jika Windows Defender memblokir, klik "More info" → "Run anyway"
- Webcam harus tersedia dan tidak sedang dipakai aplikasi lain
