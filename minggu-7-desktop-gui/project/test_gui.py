"""
Test GUI Application
Week 7 Project Module

Test script for GUI components
"""
import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path


def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    errors = []
    
    try:
        import cv2
        print("✅ OpenCV imported")
    except ImportError as e:
        errors.append(f"❌ OpenCV: {e}")
    
    try:
        from PIL import Image, ImageTk
        print("✅ Pillow imported")
    except ImportError as e:
        errors.append(f"❌ Pillow: {e}")
    
    try:
        import mediapipe
        print("✅ MediaPipe imported")
    except ImportError as e:
        errors.append(f"❌ MediaPipe: {e}")
    
    try:
        from gui import MainWindow, RegisterWindow, AttendanceWindow, ReportsWindow
        print("✅ GUI modules imported")
    except ImportError as e:
        errors.append(f"❌ GUI modules: {e}")
    
    try:
        from recognition_service import RecognitionService
        print("✅ RecognitionService imported")
    except ImportError as e:
        errors.append(f"❌ RecognitionService: {e}")
    
    try:
        from attendance_system import AttendanceSystem
        print("✅ AttendanceSystem imported")
    except ImportError as e:
        errors.append(f"❌ AttendanceSystem: {e}")
    
    return errors


def test_dataset():
    """Test if dataset is properly set up"""
    print("\nTesting dataset...")
    errors = []
    
    dataset_path = Path("dataset")
    if not dataset_path.exists():
        errors.append("❌ Dataset folder not found")
        return errors
    
    print("✅ Dataset folder exists")
    
    # Check for encodings
    encodings_file = dataset_path / "encodings.pkl"
    if not encodings_file.exists():
        errors.append("❌ encodings.pkl not found")
    else:
        print("✅ Face encodings file exists")
        
        # Try to load
        try:
            import pickle
            with open(encodings_file, 'rb') as f:
                data = pickle.load(f)
                encoding_count = len(data.get('encodings', []))
                name_count = len(set(data.get('names', [])))
                print(f"   - {encoding_count} encodings")
                print(f"   - {name_count} persons")
        except Exception as e:
            errors.append(f"❌ Failed to load encodings: {e}")
    
    # Check for person folders
    person_folders = [f for f in dataset_path.iterdir() if f.is_dir()]
    if person_folders:
        print(f"✅ {len(person_folders)} person folders found")
    else:
        print("⚠️  No person folders found (dataset is empty)")
    
    return errors


def test_webcam():
    """Test webcam access"""
    print("\nTesting webcam...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Webcam accessible")
            ret, frame = cap.read()
            if ret:
                print(f"✅ Frame captured: {frame.shape}")
            else:
                print("⚠️  Webcam opened but cannot read frame")
            cap.release()
        else:
            print("❌ Cannot open webcam")
            return ["❌ Webcam not accessible"]
    except Exception as e:
        return [f"❌ Webcam test failed: {e}"]
    
    return []


def test_gui_basic():
    """Test basic GUI functionality"""
    print("\nTesting basic GUI...")
    
    try:
        root = tk.Tk()
        root.title("GUI Test")
        root.geometry("400x300")
        
        tk.Label(
            root,
            text="✅ Tkinter GUI Test",
            font=("Arial", 16, "bold"),
            fg="#4CAF50"
        ).pack(pady=50)
        
        tk.Label(
            root,
            text="If you see this window, Tkinter is working!",
            font=("Arial", 12)
        ).pack(pady=20)
        
        tk.Button(
            root,
            text="Close Test",
            command=root.destroy,
            width=15,
            height=2,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10)
        ).pack(pady=20)
        
        print("✅ GUI window created")
        print("   Close the test window to continue...")
        
        root.mainloop()
        return []
    
    except Exception as e:
        return [f"❌ GUI test failed: {e}"]


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("GUI Application Test Suite")
    print("Week 7 - Desktop GUI")
    print("=" * 60)
    print()
    
    all_errors = []
    
    # Test 1: Imports
    errors = test_imports()
    all_errors.extend(errors)
    
    # Test 2: Dataset
    errors = test_dataset()
    all_errors.extend(errors)
    
    # Test 3: Webcam
    errors = test_webcam()
    all_errors.extend(errors)
    
    # Test 4: GUI Basic
    errors = test_gui_basic()
    all_errors.extend(errors)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if all_errors:
        print("\n❌ Tests completed with errors:\n")
        for error in all_errors:
            print(error)
        print("\n💡 Please fix the issues above before running the application.")
    else:
        print("\n✅ All tests passed!")
        print("\n🚀 You can now run the application:")
        print("   python main_app.py")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    run_all_tests()
    input("\nPress Enter to exit...")
