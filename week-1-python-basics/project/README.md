# Week 1 Project Module: Image Utilities

## Overview
This module contains core image processing functions that will be used throughout the face recognition web application.

## Files

### `image_utils.py`
Main module containing reusable image processing functions:

**Functions:**
- `load_image()` - Load image from file with format options
- `resize_image()` - Resize with dimensions or scale factor
- `preprocess_image()` - Prepare images for face recognition
- `convert_to_grayscale()` - BGR to grayscale conversion
- `save_image()` - Save with quality control
- `validate_image_quality()` - Check image meets requirements

### `test_utils.py`
Comprehensive test suite for all utility functions.

## Running Tests

```bash
cd project
python test_utils.py
```

Expected output: All tests should pass, confirming module works correctly.

## Integration to Main Project

In Week 2, this module will be copied to the main project structure:

```
ExtraQueensya/
└── core/
    └── image_utils.py   # This file
```

It will be imported and used by:
- Week 2: Face detection API
- Week 3: Face recognition system
- Week 4: Database storage (preprocessing before saving)
- Week 5-8: REST API endpoints

## Usage Example

```python
from core.image_utils import load_image, preprocess_image, validate_image_quality

# Load and validate
image = load_image("photo.jpg")
is_valid, msg = validate_image_quality(image)

if is_valid:
    # Preprocess for face detection
    processed = preprocess_image(image, target_size=(640, 480))
    
    # Continue with face detection...
```

## Development Notes

- All functions include type hints for clarity
- Error handling with informative messages
- Supports both color and grayscale images
- Maintains aspect ratio by default when resizing
- Quality validation prevents poor images from processing

## Next Week

Week 2 will build on this module by adding:
- `face_detector.py` - Uses `image_utils` for preprocessing
- Detection API endpoint that validates images before processing
