# Minggu 4: Dataset Collection & Management

## Tujuan Pembelajaran
- Systematic face data collection
- Multiple angles dan lighting conditions
- Dataset organization
- Data quality validation

## Struktur Folder

```
minggu-4-dataset-collection/
├── README.md
├── learning/          # Tutorial dan latihan
│   ├── 01_capture_faces.py
│   ├── 02_multi_angle_capture.py
│   ├── 03_batch_processing.py
│   ├── 04_data_validation.py
│   └── latihan.py
└── project/           # Module untuk progressive build
    ├── dataset_manager.py
    ├── test_dataset.py
    └── README.md
```

## Learning Goals

### Tutorial Materials (learning/)
1. **01_capture_faces.py** - Basic face capture dari webcam
2. **02_multi_angle_capture.py** - Capture multiple angles
3. **03_batch_processing.py** - Process multiple images
4. **04_data_validation.py** - Validate dataset quality
5. **latihan.py** - Build complete dataset collector

### Konsep Utama
- Face capture dengan validation
- Multiple angles (frontal, left, right)
- Lighting variation
- Dataset folder structure
- Image preprocessing
- Quality metrics

## Project Development

### Module: `dataset_manager.py`
Production-ready dataset management module dengan fungsi:
- `DatasetManager` class - Manage face datasets
- `capture_face()` - Capture with validation
- `add_person()` - Add new person to dataset
- `remove_person()` - Remove person from dataset
- `get_person_images()` - Get all images for person
- `validate_dataset()` - Check dataset quality
- `export_encodings()` - Generate encodings for dataset

### Integration
Uses Week 2 `face_detector.py` and Week 3 `face_recognizer.py`.  
Module ini akan digunakan oleh:
- Week 5: Recognition system training
- Week 6: Attendance database seeding
- Week 7-8: Desktop GUI for person registration

## Cara Penggunaan

### Learning (Tutorial)
```bash
cd minggu-4-dataset-collection/learning
python 01_capture_faces.py
python 02_multi_angle_capture.py
python 03_batch_processing.py
python 04_data_validation.py
python latihan.py
```

### Project Development
```bash
cd minggu-4-dataset-collection/project
python test_dataset.py

# Integrate to main project
# Copy dataset_manager.py to ../../core/
```

## Dataset Structure

```
dataset/
├── person_1/
│   ├── frontal_1.jpg
│   ├── frontal_2.jpg
│   ├── left_angle.jpg
│   ├── right_angle.jpg
│   └── encodings.pkl
├── person_2/
│   └── ...
└── metadata.json
```

## Deliverables

### Learning
- Face capture application
- Multi-angle dataset
- Quality validation

### Project
- `dataset_manager.py` - Dataset management module
- `test_dataset.py` - Unit tests
- Sample dataset dengan 5+ people

## Next Week Preview

**Minggu 5: Complete Recognition System**
- Integrate all modules
- Recognition pipeline
- Performance optimization
- Error handling

---

**Time Estimate:** 5-6 hours  
**Difficulty:** Intermediate
