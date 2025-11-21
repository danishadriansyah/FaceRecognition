# Lesson 2: Performance Optimization & Metrics

## Tujuan
Optimize recognition system untuk production

## Optimizations
1. Reduce frame size (1/4)
2. Skip frames (every 3rd)
3. Use HOG model
4. Cache results
5. Multi-threading

## Metrics Tracked
- FPS (frames per second)
- Recognition accuracy
- False positive rate
- Response time

## Langkah
1. Load encodings dari Lesson 1
2. Run: `python main.py`
3. Check performance metrics
4. Tune parameters for best results

## Target Performance
- FPS: 25-30
- Accuracy: 95%+
- False positive: <5%

## Next: Minggu 6 - Database & Attendance
