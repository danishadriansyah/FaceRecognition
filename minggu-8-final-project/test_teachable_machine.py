"""
Quick Test Script for Teachable Machine Integration
Tests if the Teachable Machine model is working correctly
"""

import sys
from pathlib import Path

# Add project to path
project_dir = Path(__file__).parent / "project"
sys.path.insert(0, str(project_dir))

print("="*60)
print("TEACHABLE MACHINE INTEGRATION TEST")
print("="*60)

# Test 1: Import modules
print("\n[Test 1] Importing modules...")
try:
    from core.teachable_recognizer import TeachableMachineRecognizer
    print("✅ Teachable Machine module imported")
except Exception as e:
    print(f"❌ Failed to import: {e}")
    sys.exit(1)

# Test 2: Check model files
print("\n[Test 2] Checking model files...")
model_path = project_dir / "models" / "keras_model.h5"
labels_path = project_dir / "models" / "labels.txt"

if not model_path.exists():
    print(f"❌ Model not found: {model_path}")
    sys.exit(1)
print(f"✅ Model found: {model_path}")

if not labels_path.exists():
    print(f"❌ Labels not found: {labels_path}")
    sys.exit(1)
print(f"✅ Labels found: {labels_path}")

# Test 3: Load model
print("\n[Test 3] Loading Teachable Machine model...")
try:
    recognizer = TeachableMachineRecognizer(
        model_path=str(model_path),
        labels_path=str(labels_path),
        confidence_threshold=0.7
    )
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    sys.exit(1)

# Test 4: Check model info
print("\n[Test 4] Model information:")
info = recognizer.get_model_info()
for key, value in info.items():
    print(f"  {key}: {value}")

# Test 5: Test with recognition service
print("\n[Test 5] Testing RecognitionService integration...")
try:
    from core.recognition_service import RecognitionService
    
    service = RecognitionService(
        dataset_path=str(project_dir / "dataset"),
        use_teachable_machine=True,
        teachable_model_path=str(model_path),
        teachable_labels_path=str(labels_path),
        teachable_confidence=0.7
    )
    print("✅ RecognitionService initialized with Teachable Machine")
except Exception as e:
    print(f"❌ Failed to initialize RecognitionService: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Check configuration
print("\n[Test 6] Checking configuration...")
try:
    from config import Config
    config = Config()
    print(f"  use_teachable_machine: {config.recognition.use_teachable_machine}")
    print(f"  model_path: {config.recognition.teachable_model_path}")
    print(f"  labels_path: {config.recognition.teachable_labels_path}")
    print(f"  confidence: {config.recognition.teachable_confidence}")
    print("✅ Configuration loaded")
except Exception as e:
    print(f"⚠️  Config not available (non-critical): {e}")

print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
print("\n📝 Next Steps:")
print("1. Run the main application:")
print("   cd minggu-8-final-project/project")
print("   python main_app.py")
print("\n2. Or test with webcam:")
print("   cd minggu-8-final-project/project/core")
print("   python teachable_recognizer.py")
print("\n3. To train new model:")
print("   Visit: https://teachablemachine.withgoogle.com/")
print("   Export as Tensorflow → Keras")
print("   Replace files in project/models/")
