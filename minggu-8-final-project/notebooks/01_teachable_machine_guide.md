# 🎯 Opsi 1: Training dengan Teachable Machine
# Face Recognition Model - Simple & Fast

## 📋 Overview
Notebook ini adalah **panduan langkah-langkah** untuk membuat model face recognition
menggunakan Google Teachable Machine. Output akan kompatibel dengan Final Project.

---

## 🚀 Step 1: Prepare Dataset

### Struktur folder yang dibutuhkan:
```
dataset/
├── Person1/
│   ├── photo_001.jpg
│   ├── photo_002.jpg
│   └── ... (20-50 foto)
├── Person2/
│   ├── photo_001.jpg
│   └── ...
└── Person3/
    └── ...
```

### Tips foto yang bagus:
- ✅ Wajah menghadap kamera
- ✅ Pencahayaan cukup
- ✅ Berbagai ekspresi (senyum, serius, dll)
- ✅ Berbagai angle (depan, sedikit miring)
- ❌ Hindari blur
- ❌ Hindari backlight

---

## 🌐 Step 2: Buka Teachable Machine

1. Buka browser, pergi ke: **https://teachablemachine.withgoogle.com/**
2. Klik **"Get Started"**
3. Pilih **"Image Project"**
4. Pilih **"Standard image model"**

---

## 📤 Step 3: Upload Dataset

1. Rename "Class 1" → nama orang pertama (misal: "Queensya")
2. Klik **"Upload"** → pilih semua foto dari folder `dataset/Queensya/`
3. Klik **"Add a class"** untuk tambah orang baru
4. Ulangi untuk setiap orang

### Screenshot contoh:
```
┌─────────────────────────────────────────┐
│  Class: Queensya                    [▼] │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │
│  │ 📷  │ │ 📷  │ │ 📷  │ │ 📷  │  +20  │
│  └─────┘ └─────┘ └─────┘ └─────┘       │
├─────────────────────────────────────────┤
│  Class: Danisw                      [▼] │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │
│  │ 📷  │ │ 📷  │ │ 📷  │ │ 📷  │  +20  │
│  └─────┘ └─────┘ └─────┘ └─────┘       │
└─────────────────────────────────────────┘
```

---

## 🏋️ Step 4: Training

1. Klik tombol **"Train Model"**
2. Tunggu sampai selesai (biasanya 1-5 menit)
3. Test dengan webcam di preview panel

---

## 💾 Step 5: Export Model

1. Klik **"Export Model"**
2. Pilih tab **"Tensorflow"**
3. Pilih **"Keras"**
4. Klik **"Download my model"**
5. Extract ZIP file, akan dapat:
   - `keras_model.h5`
   - `labels.txt`

---

## 📁 Step 6: Copy ke Project

1. Copy kedua file ke folder:
   ```
   minggu-8-final-project/project/models/
   ```

2. Atau buat subfolder dengan timestamp:
   ```
   minggu-8-final-project/project/models/model_20260203_120000/
   ├── keras_model.h5
   └── labels.txt
   ```

3. Update `config.json` jika perlu

---

## ✅ Step 7: Test di Aplikasi

```bash
cd minggu-8-final-project/project
python main_app.py
```

Buka Attendance Window → Wajah harus terdeteksi dengan nama yang benar!

---

## 🔧 Troubleshooting

### Model tidak akurat?
- Tambah lebih banyak foto (min 30-50 per orang)
- Pastikan foto bervariasi (angle, ekspresi, pencahayaan)
- Hindari background yang terlalu mirip antar orang

### File tidak terbaca?
- Pastikan nama file `keras_model.h5` (bukan `.keras`)
- Pastikan `labels.txt` ada dan format benar

### Confidence rendah?
- Train ulang dengan foto lebih banyak
- Pastikan wajah terlihat jelas di foto

---

## 📊 Expected Output

| File | Size | Deskripsi |
|------|------|-----------|
| `keras_model.h5` | ~2-5 MB | Model Keras trained |
| `labels.txt` | ~100 bytes | Daftar nama class |

### Format labels.txt:
```
0 Queensya
1 Danisw
2 Person3
```

---

## ⏱️ Waktu yang Dibutuhkan
- Prepare dataset: 10-30 menit
- Upload & Train: 5-10 menit
- Export & Setup: 2 menit
- **Total: ~20-45 menit**

---

🎉 **Selesai!** Model Teachable Machine siap digunakan di Final Project.
