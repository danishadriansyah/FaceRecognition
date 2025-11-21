# Progressive Module Duplication

## Konsep

Setiap minggu memiliki **copy dari semua module minggu sebelumnya** sehingga student bisa langsung jalankan tanpa dependency issues.

## Struktur Per Week

### Week 1: Foundation
```
minggu-1-python-basics/project/
├── image_utils.py        ← New: Image preprocessing
└── test_utils.py
```

### Week 2: + Face Detection
```
minggu-2-face-detection/project/
├── image_utils.py        ← Copy from Week 1
├── face_detector.py      ← New: Face detection
└── test_detector.py
```

### Week 3: + Face Recognition
```
minggu-3-face-recognition/project/
├── image_utils.py        ← Copy from Week 1
├── face_detector.py      ← Copy from Week 2
├── face_recognizer.py    ← New: Face recognition
└── test_recognizer.py
```

### Week 4: + Dataset Management
```
minggu-4-dataset-collection/project/
├── image_utils.py        ← Copy from Week 1
├── face_detector.py      ← Copy from Week 2
├── face_recognizer.py    ← Copy from Week 3
├── dataset_manager.py    ← New: Dataset management
└── test_dataset.py
```

### Week 5: + Recognition Service
```
minggu-5-recognition-system/project/
├── image_utils.py        ← Copy from Week 1
├── face_detector.py      ← Copy from Week 2
├── face_recognizer.py    ← Copy from Week 3
├── dataset_manager.py    ← Copy from Week 4
├── recognition_service.py ← New: Complete integration
└── test_recognition.py
```

### Week 6: + Database & Attendance
```
minggu-6-database-attendance/project/
├── image_utils.py         ← Copy from Week 1
├── face_detector.py       ← Copy from Week 2
├── face_recognizer.py     ← Copy from Week 3
├── dataset_manager.py     ← Copy from Week 4
├── recognition_service.py ← Copy from Week 5
├── attendance_system.py   ← New: Database + attendance
└── test_attendance.py
```

### Week 7: + Flask REST API
```
minggu-7-web-api/project/
├── image_utils.py         ← Copy from Week 1
├── face_detector.py       ← Copy from Week 2
├── face_recognizer.py     ← Copy from Week 3
├── dataset_manager.py     ← Copy from Week 4
├── recognition_service.py ← Copy from Week 5
├── attendance_system.py   ← Copy from Week 6
├── app.py                 ← New: Flask application
├── test_app.py
└── api/                   ← API endpoints
    ├── auth.py
    ├── persons.py
    ├── attendance.py
    └── recognition.py
```

### Week 8: Testing & Deployment
```
minggu-8-testing-deployment/project/
├── tests/                 ← Integration tests
│   ├── test_models.py
│   ├── test_services.py
│   ├── test_api.py
│   └── test_integration.py
└── deploy/                ← Deployment guides
    ├── production_config.py
    ├── deploy_railway.md
    ├── deploy_render.md
    └── deploy_heroku.md
```

## Benefits

✅ **Self-contained**: Setiap minggu bisa standalone  
✅ **No import errors**: Semua dependencies sudah ada di folder  
✅ **Easy testing**: Student bisa test langsung tanpa setup kompleks  
✅ **Clear progression**: Lihat bertambahnya file setiap minggu  
✅ **Learning focused**: Student fokus ke konsep baru, bukan troubleshooting imports  

## How to Use

### Run Week 2 (Example)
```bash
cd minggu-2-face-detection/project
python test_detector.py
```

Tidak perlu:
- ❌ Setup PYTHONPATH
- ❌ Install package sebagai module
- ❌ Bingung import dari folder lain

Semua module sudah ada di folder yang sama! ✅

## Integration Flow

```
Week 1: image_utils
         ↓ (used by)
Week 2: face_detector
         ↓ (used by)
Week 3: face_recognizer
         ↓ (used by)
Week 4: dataset_manager
         ↓ (used by)
Week 5: recognition_service
         ↓ (used by)
Week 6: attendance_system
         ↓ (used by)
Week 7: app.py (Flask API)
         ↓ (validated by)
Week 8: tests & deployment
```

## File Count Per Week

| Week | Total Modules | New Module | Test File |
|------|--------------|------------|-----------|
| 1 | 1 | image_utils | test_utils |
| 2 | 2 | face_detector | test_detector |
| 3 | 3 | face_recognizer | test_recognizer |
| 4 | 4 | dataset_manager | test_dataset |
| 5 | 5 | recognition_service | test_recognition |
| 6 | 6 | attendance_system | test_attendance |
| 7 | 7 | app.py | test_app |
| 8 | - | (tests only) | 4 test files |

**Total progression: 1 → 2 → 3 → 4 → 5 → 6 → 7 modules**

Student bisa lihat project berkembang step by step! 🚀
