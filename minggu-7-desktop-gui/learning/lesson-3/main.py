"""
Lesson 3: System Testing & Validation

Tutorial: Comprehensive testing suite untuk desktop GUI application
"""

import sys
import os
from pathlib import Path

# Add project path
project_path = Path(__file__).parent.parent.parent / "project"
sys.path.insert(0, str(project_path))

print("="*70)
print("  LESSON 3: Desktop GUI System Testing")
print("="*70)
print()
print("This testing suite validates:")
print("  1. Package imports (all dependencies)")
print("  2. Project structure (folders & files)")
print("  3. Webcam detection (auto-detect cameras)")
print("  4. Face detection module")
print("  5. Dataset validation")
print("  6. GUI components (interactive test)")
print()
print("="*70)
print()


def print_section(title):
    """Print section header"""
    print()
    print("─" * 70)
    print(f"  {title}")
    print("─" * 70)


def test_imports():
    """Test 1: Package imports"""
    print_section("TEST 1: Package Imports")
    
    packages = [
        ('cv2', 'OpenCV'),
        ('PIL', 'Pillow'),
        ('numpy', 'NumPy'),
        ('tkinter', 'Tkinter'),
    ]
    
    results = {'passed': 0, 'failed': 0}
    
    for package, name in packages:
        try:
            __import__(package)
            print(f"   ✅ {name} ({package})")
            results['passed'] += 1
        except ImportError:
            print(f"   ❌ {name} ({package}) - NOT INSTALLED")
            results['failed'] += 1
    
    return results


def test_structure():
    """Test 2: Project structure"""
    print_section("TEST 2: Project Structure")
    
    project_root = Path(__file__).parent.parent.parent / "project"
    
    required_items = {
        'Folders': [
            'project/gui',
            'project/dataset',
            'project/logs',
        ],
        'Files': [
            'project/main_app.py',
            'project/face_detector.py',
            'project/recognition_service.py',
            'project/attendance_system.py',
            'project/gui/main_window.py',
            'project/gui/register_window.py',
        ]
    }
    
    results = {'passed': 0, 'failed': 0}
    
    for category, items in required_items.items():
        print(f"\n   {category}:")
        for item in items:
            path = Path(__file__).parent.parent.parent / item
            if path.exists():
                print(f"      ✅ {item}")
                results['passed'] += 1
            else:
                print(f"      ❌ {item} - MISSING")
                results['failed'] += 1
    
    return results


def test_webcam():
    """Test 3: Webcam detection"""
    print_section("TEST 3: Webcam Detection")
    
    results = {'passed': 0, 'failed': 0, 'cameras': []}
    
    try:
        import cv2
        
        print("   Detecting cameras...")
        camera_count = 0
        
        # Try to detect cameras (index 0-2)
        for i in range(3):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                # Get camera info
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                
                print(f"\n   ✅ Camera {i} found:")
                print(f"      Resolution: {width}x{height}")
                print(f"      FPS: {fps}")
                
                # Test frame capture
                ret, frame = cap.read()
                if ret:
                    print(f"      Frame shape: {frame.shape}")
                    results['passed'] += 1
                else:
                    print(f"      ⚠️  Cannot capture frame")
                
                results['cameras'].append({
                    'index': i,
                    'resolution': f"{width}x{height}",
                    'fps': fps
                })
                
                camera_count += 1
                cap.release()
        
        if camera_count == 0:
            print("   ❌ No cameras detected")
            print("   💡 Check camera permissions in Windows Settings")
            results['failed'] += 1
        else:
            print(f"\n   ✅ Total cameras found: {camera_count}")
            
    except Exception as e:
        print(f"   ❌ Webcam test error: {e}")
        results['failed'] += 1
    
    return results


def test_face_detection():
    """Test 4: Face detection module"""
    print_section("TEST 4: Face Detection Module")
    
    results = {'passed': 0, 'failed': 0}
    
    try:
        from face_detector import FaceDetector
        print("   ✅ FaceDetector imported")
        results['passed'] += 1
        
        # Initialize detector
        detector = FaceDetector()
        print("   ✅ FaceDetector initialized")
        results['passed'] += 1
        
        # Test with dummy image
        import numpy as np
        dummy_img = np.zeros((480, 640, 3), dtype=np.uint8)
        faces = detector.detect_faces(dummy_img)
        print(f"   ✅ detect_faces() works (detected {len(faces)} faces in dummy image)")
        results['passed'] += 1
        
    except ImportError as e:
        print(f"   ❌ Cannot import FaceDetector: {e}")
        results['failed'] += 3
    except Exception as e:
        print(f"   ❌ Face detection test error: {e}")
        results['failed'] += 1
    
    return results


def test_dataset():
    """Test 5: Dataset validation"""
    print_section("TEST 5: Dataset Validation")
    
    results = {'passed': 0, 'failed': 0}
    
    dataset_path = Path(__file__).parent.parent.parent / "project" / "dataset"
    
    # Check dataset folder
    if dataset_path.exists():
        print(f"   ✅ Dataset folder exists: {dataset_path}")
        results['passed'] += 1
        
        # Check encodings.pkl
        encodings_file = dataset_path / "encodings.pkl"
        if encodings_file.exists():
            print("   ✅ encodings.pkl found")
            results['passed'] += 1
            
            # Try to load
            try:
                import pickle
                with open(encodings_file, 'rb') as f:
                    data = pickle.load(f)
                    if 'encodings' in data and 'names' in data:
                        num_persons = len(set(data['names']))
                        print(f"   ✅ Encodings valid ({num_persons} persons)")
                        results['passed'] += 1
                    else:
                        print("   ⚠️  Encodings format invalid")
            except Exception as e:
                print(f"   ⚠️  Cannot load encodings: {e}")
        else:
            print("   ⚠️  encodings.pkl not found (no persons registered yet)")
        
        # Check persons.json
        persons_file = dataset_path / "persons.json"
        if persons_file.exists():
            print("   ✅ persons.json found")
            results['passed'] += 1
        else:
            print("   ⚠️  persons.json not found")
            
    else:
        print(f"   ❌ Dataset folder missing: {dataset_path}")
        results['failed'] += 1
    
    return results


def test_gui():
    """Test 6: GUI components (interactive)"""
    print_section("TEST 6: GUI Components (Interactive Test)")
    
    results = {'passed': 0, 'failed': 0}
    
    print("   Opening test GUI window...")
    print("   💡 Please click buttons to test interactions")
    
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        # Create test window
        root = tk.Tk()
        root.title("GUI Test Window")
        root.geometry("500x400")
        
        # Title
        tk.Label(
            root,
            text="GUI Components Test",
            font=("Arial", 16, "bold"),
            bg="#1976D2",
            fg="white",
            pady=20
        ).pack(fill=tk.X)
        
        # Status label
        status_label = tk.Label(
            root,
            text="Status: Ready",
            font=("Arial", 12),
            fg="green"
        )
        status_label.pack(pady=20)
        
        # Test buttons
        def test_button(name):
            status_label.config(text=f"Status: {name} clicked ✅")
            messagebox.showinfo("Test", f"{name} works!")
        
        buttons = [
            "Register Button",
            "Attendance Button",
            "Reports Button",
            "Settings Button"
        ]
        
        for btn_name in buttons:
            tk.Button(
                root,
                text=btn_name,
                command=lambda n=btn_name: test_button(n),
                width=25,
                height=2,
                font=("Arial", 10),
                bg="#4CAF50",
                fg="white"
            ).pack(pady=5)
        
        # Close button
        tk.Button(
            root,
            text="Close & Continue Tests",
            command=root.destroy,
            width=25,
            height=2,
            font=("Arial", 10),
            bg="#f44336",
            fg="white"
        ).pack(pady=20)
        
        print("   ✅ GUI window created")
        results['passed'] += 1
        
        root.mainloop()
        
        print("   ✅ GUI test completed")
        results['passed'] += 1
        
    except Exception as e:
        print(f"   ❌ GUI test error: {e}")
        results['failed'] += 1
    
    return results


def print_summary(all_results):
    """Print test summary"""
    print()
    print("="*70)
    print("  TEST SUMMARY")
    print("="*70)
    print()
    
    total_passed = sum(r['passed'] for r in all_results.values())
    total_failed = sum(r['failed'] for r in all_results.values())
    total_tests = total_passed + total_failed
    
    for test_name, results in all_results.items():
        passed = results['passed']
        failed = results['failed']
        status = "✅ PASS" if failed == 0 else "⚠️  PARTIAL" if passed > 0 else "❌ FAIL"
        print(f"   {test_name}: {status} ({passed}/{passed+failed} passed)")
    
    print()
    print("─"*70)
    print(f"   OVERALL: {total_passed}/{total_tests} tests passed")
    print("─"*70)
    print()
    
    if total_failed == 0:
        print("   🎉 VERDICT: READY FOR PRODUCTION ✅")
    elif total_passed > total_failed:
        print("   ⚠️  VERDICT: MOSTLY READY (some issues to fix)")
    else:
        print("   ❌ VERDICT: NOT READY (critical issues found)")
    
    print()
    print("="*70)


def main():
    """Run all tests"""
    
    all_results = {}
    
    # Run tests
    all_results['Test 1: Imports'] = test_imports()
    all_results['Test 2: Structure'] = test_structure()
    all_results['Test 3: Webcam'] = test_webcam()
    all_results['Test 4: Face Detection'] = test_face_detection()
    all_results['Test 5: Dataset'] = test_dataset()
    all_results['Test 6: GUI'] = test_gui()
    
    # Print summary
    print_summary(all_results)
    
    print()
    print("="*70)
    print("  ✅ LESSON 3 COMPLETED!")
    print("="*70)
    print()
    print("You learned:")
    print("  ✅ How to test package dependencies")
    print("  ✅ How to validate project structure")
    print("  ✅ How to detect and test webcams")
    print("  ✅ How to test face detection modules")
    print("  ✅ How to validate dataset integrity")
    print("  ✅ How to create interactive GUI tests")
    print()
    print("Next: Build the full project (run project/main_app.py)")
    print("="*70)
    print()


if __name__ == '__main__':
    main()
