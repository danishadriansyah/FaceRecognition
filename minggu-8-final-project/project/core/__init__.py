"""
Core modules package for Face Recognition Attendance System.
Week 8 - Final Project

This package contains all core modules from Week 1-6:
- image_utils (Week 1): Image processing utilities
- face_detector (Week 2): MediaPipe face detection
- face_recognizer (Week 3): DeepFace face recognition
- dataset_manager (Week 4): Dataset management
- recognition_service (Week 5): Recognition pipeline
- attendance_system (Week 6): Attendance logging
- teachable_recognizer (Week 8): Teachable Machine integration
"""

__version__ = "1.0.0"
__author__ = "Face Recognition Team"

# Import core modules for easy access (with error handling)
try:
    from .teachable_recognizer import TeachableMachineRecognizer
except ImportError:
    TeachableMachineRecognizer = None

__all__ = [
    'TeachableMachineRecognizer',
]
