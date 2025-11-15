# Lesson 2: Real-Time Face Recognition dari Webcam

## Tujuan
- Real-time face recognition dari webcam
- Display nama dan confidence score
- Optimize performance untuk smooth video
- Handle multiple faces simultaneously

## Perbedaan Lesson 1 vs 2
- Lesson 1: Static image → Slow OK
- Lesson 2: Video stream → Must be FAST!

## Optimization Tips
1. Resize frame ke 1/4 size untuk detection
2. Process every 3rd frame only
3. Use faster face_locations model: `model="hog"`

## Setup
Gunakan known_faces yang sama dari Lesson 1

## Langkah
1. Run: `python main.py`
2. Webcam akan show dengan rectangle & nama
3. Press ESC untuk exit

## Keyboard Controls
- ESC: Exit
- SPACE: Save snapshot
- R: Reset recognition

## Next: Minggu 4 - Dataset Collection
