# Lesson 2: Real-Time Face Recognition dari Webcam

## Tujuan
- Real-time face recognition dari webcam
- Display nama dan confidence score
- Optimize performance untuk smooth video
- Handle multiple faces simultaneously

## Perbedaan Lesson 1 vs 2

| Lesson 1 | Lesson 2 |
|----------|----------|
| Static images dari **folder `images/`** | Live video dari **webcam** |
| Slow OK (process per image) | Must be FAST! (real-time) |
| Test images disimpan di file | Input langsung dari camera |

**Lesson 2 ga perlu folder `images/`** karena input-nya **langsung dari webcam**, bukan file gambar!

## Setup Known Faces

Lesson 2 pakai database yang sama seperti Lesson 1:

```
known_faces/
├── alice/
│   ├── photo1.jpg      ← Database untuk recognize
│   └── photo2.jpg
└── bob/
    ├── photo1.jpg
    └── photo2.jpg
```

**Cara kerjanya:**
1. Program **baca known_faces/** → Build database encoding (Alice, Bob)
2. Program **buka webcam** → Live video stream
3. Setiap frame → Detect faces → Compare dengan database
4. Show nama di atas wajah: "Alice" atau "Bob" atau "Unknown"

## Optimization Tips

Real-time video butuh speed! Berikut cara optimize:

1. **Resize frame** ke 1/4 size untuk detection (lebih cepat)
2. **Process every 3rd frame** only (skip beberapa frame)
3. **Cache results** sebentar (pakai hasil recognition sebelumnya)

MediaPipe sudah cepat, tapi tricks ini bikin lebih smooth!

## Langkah Praktik

1. **Setup known faces** (sama seperti Lesson 1):
   - Pastikan ada folder `known_faces/alice/` dan `known_faces/bob/`
   - Isi dengan foto-foto mereka

2. **Run program:**
   ```bash
   python main.py
   ```

3. **Test recognition:**
   - Webcam akan terbuka
   - Tunjukkan wajah ke camera
   - Program akan show nama di atas wajah
   - Coba dengan orang known (Alice/Bob) dan unknown

4. **Check output:**
   - Snapshot tersimpan di folder `output/` (kalau tekan SPACE)

## Keyboard Controls
- ESC: Exit
- SPACE: Save snapshot
- R: Reset recognition

## Next: Minggu 4 - Dataset Collection
