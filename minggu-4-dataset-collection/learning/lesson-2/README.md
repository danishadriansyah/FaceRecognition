# Lesson 2: Dataset Management & Organization

## Tujuan
- Organize dataset dengan struktur proper
- Generate metadata per person
- Create backups
- Validate dataset quality

## Struktur Dataset
```
dataset/
├── person_001_alice/
│   ├── metadata.json
│   ├── photo_001.jpg
│   └── photo_002.jpg
└── person_002_bob/
    └── ...
```

## Yang Dipelajari
1. Reorganize captured faces
2. Generate person ID
3. Create metadata (name, photo count, date)
4. Backup dataset to ZIP
5. Validation report

## Langkah
1. Capture faces di Lesson 1 dulu
2. Run: `python main.py`
3. Dataset akan di-organize ke `dataset/`
4. Backup auto created di `backups/`

## Next: Minggu 5 - Recognition System
