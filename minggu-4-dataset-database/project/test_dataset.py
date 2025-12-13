"""
Test Dataset Manager
Week 4 Project Module - Progressive Web Application (File-Based Mode)

Tests for dataset management functionality with local file storage
"""

import sys
import os
import numpy as np
import cv2
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from dataset_manager import DatasetManager


def test_initialization():
    """Test dataset manager initialization"""
    print("Test 1: Initialization")
    
    try:
        manager = DatasetManager(dataset_path="test_output/test_dataset")
        print("✓ Dataset manager initialized (File-based mode)")
        print(f"  Dataset path: {manager.dataset_path.absolute()}")
        print(f"  Metadata file: {manager.metadata_file.name}")
        print(f"  Encodings file: {manager.encodings_file.name}")
        return True
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        return False


def test_add_person():
    """Test adding person to dataset"""
    print("\nTest 2: Add Person to Dataset")
    
    try:
        manager = DatasetManager("test_output/test_dataset")
        
        person_id = manager.add_person(
            name="Test User Alice",
            employee_id="TEST001",
            department="IT"
        )
        
        assert person_id is not None
        print(f"✓ Person added with ID: {person_id}")
        
        # Check folder created
        person_folder = manager.dataset_path / person_id
        assert person_folder.exists()
        print(f"✓ Person folder created: {person_folder}")
        
        # Check metadata
        people = manager.get_person_list()
        print(f"✓ Total people in dataset: {len(people)}")
        
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_save_face_image():
    """Test saving face image to person folder"""
    print("\nTest 3: Save Face Image")
    
    try:
        manager = DatasetManager("test_output/test_dataset")
        
        # Add person first
        person_id = manager.add_person("Test User Bob", "TEST002", "HR")
        
        # Create test face image
        test_face = np.ones((200, 200, 3), dtype=np.uint8) * 180
        cv2.rectangle(test_face, (50, 50), (150, 150), (100, 150, 200), -1)
        
        # Save to person folder
        person_folder = manager.dataset_path / person_id
        image_path = person_folder / f"{person_id}_001.jpg"
        cv2.imwrite(str(image_path), test_face)
        
        assert image_path.exists()
        print(f"✓ Image saved: {image_path.name}")
        
        # Verify can load
        loaded = cv2.imread(str(image_path))
        assert loaded is not None
        print(f"✓ Image verified: {loaded.shape}")
        
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_generate_encodings():
    """Test generating encodings from images"""
    print("\nTest 4: Generate Face Encodings")
    
    try:
        manager = DatasetManager("test_output/test_dataset")
        
        # Check if we have persons with images
        stats = manager.get_statistics()
        
        if stats["total_persons"] == 0:
            print("⚠️  No persons in dataset, skipping encoding test")
            return True
        
        print(f"  Found {stats['total_persons']} persons")
        print(f"  Total images: {stats['total_images']}")
        
        # Generate encodings
        print("  Generating encodings (this may take a moment)...")
        count = manager.generate_encodings(model_name='Facenet512')
        
        assert count > 0
        print(f"✓ Generated {count} encodings")
        
        # Check encodings file
        assert manager.encodings_file.exists()
        print(f"✓ Encodings saved to: {manager.encodings_file.name}")
        
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_load_encodings():
    """Test loading encodings from file"""
    print("\nTest 5: Load Face Encodings")
    
    try:
        manager = DatasetManager("test_output/test_dataset")
        
        if not manager.encodings_file.exists():
            print("⚠️  No encodings file found, skipping load test")
            return True
        
        encodings, names, metadata = manager.load_encodings()
        
        assert len(encodings) > 0
        assert len(encodings) == len(names)
        assert len(encodings) == len(metadata)
        
        print(f"✓ Loaded {len(encodings)} encodings")
        print(f"  Unique persons: {len(set(names))}")
        print(f"  Encoding shape: {np.array(encodings[0]).shape}")
        
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_get_statistics():
    """Test getting dataset statistics"""
    print("\nTest 6: Get Dataset Statistics")
    
    try:
        manager = DatasetManager("test_output/test_dataset")
        
        stats = manager.get_statistics()
        
        print(f"✓ Dataset statistics:")
        print(f"  Total persons: {stats['total_persons']}")
        print(f"  Total images: {stats['total_images']}")
        print(f"  Total encodings: {stats['total_encodings']}")
        print(f"  Has encodings file: {stats['has_encodings']}")
        print(f"  Dataset path: {stats['dataset_path']}")
        
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_export_metadata():
    """Test exporting metadata to JSON"""
    print("\nTest 7: Export Metadata")
    
    try:
        manager = DatasetManager("test_output/test_dataset")
        
        export_file = manager.export_metadata("test_output/dataset_export.json")
        
        assert Path(export_file).exists()
        print(f"✓ Metadata exported to: {export_file}")
        
        # Verify can read
        import json
        with open(export_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert "dataset_path" in data
        assert "statistics" in data
        assert "persons" in data
        
        print(f"✓ Export file verified")
        
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("DATASET MANAGER TESTS (File-Based Mode)")
    print("="*60)
    
    tests = [
        test_initialization,
        test_add_person,
        test_save_face_image,
        test_generate_encodings,
        test_load_encodings,
        test_get_statistics,
        test_export_metadata
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ Test crashed: {e}")
            results.append(False)
        print()
    
    # Summary
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")
    
    print("="*60)


if __name__ == "__main__":
    # Create test output directory
    Path("test_output/test_dataset").mkdir(parents=True, exist_ok=True)
    
    run_all_tests()
