# Lesson 1: Capture Faces dengan Quality Check

## Tujuan
- Capture wajah dari webcam
- Quality check otomatis (lighting, sharpness, size)
- Reject foto yang buruk
- Organize captured faces per person

## Yang Dipelajari
1. Capture dari webcam dengan spacebar
2. Quality validation:
   - Brightness check
   - Blur detection (Laplacian variance)
   - Face size minimum
   - Frontal face only
3. Auto organize: `captured_faces/person_name/`
4. Rejected photos: `rejected/`

## Langkah
1. Run: `python main.py`
2. Input nama person
3. Press SPACE untuk capture (target: 20+ photos)
4. Gerakkan wajah (kiri, kanan, atas, bawah)
5. Check hasil di `captured_faces/`

## Quality Metrics
- Min face size: 100x100 px
- Min brightness: 40
- Max brightness: 220
- Min sharpness (Laplacian): 100

## Next: Lesson 2 - Dataset Management
