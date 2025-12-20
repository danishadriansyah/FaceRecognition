"""
Main Application - Desktop GUI
Week 7 - Face Recognition Attendance System

Complete desktop application with Tkinter
"""
import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path

# Import GUI modules
from gui import MainWindow


def check_requirements():
    """Check if all requirements are met"""
    errors = []
    
    # Check dataset (use absolute path based on this file location)
    project_dir = Path(__file__).parent
    dataset_path = project_dir / "dataset"
    
    if not dataset_path.exists():
        errors.append("❌ Dataset folder not found")
        errors.append("   → Run: python ../setup_week7.py")
    else:
        encodings_file = dataset_path / "encodings.pkl"
        if not encodings_file.exists():
            errors.append("⚠️  Face encodings not found (no persons registered yet)")
            errors.append("   → Use 'Register Person' in app to add people")
    
    # Check required modules
    try:
        import cv2
    except ImportError:
        errors.append("❌ OpenCV not installed")
        errors.append("   → pip install opencv-python")
    
    try:
        import PIL
    except ImportError:
        errors.append("❌ Pillow not installed")
        errors.append("   → pip install pillow")
    
    try:
        import mediapipe
    except ImportError:
        errors.append("❌ MediaPipe not installed")
        errors.append("   → pip install mediapipe")
    
    return errors


def main():
    """Main application entry point"""
    print("=" * 60)
    print("Face Recognition Attendance System")
    print("Week 7 - Desktop GUI")
    print("=" * 60)
    print()
    
    # Check requirements
    print("🔍 Checking requirements...")
    errors = check_requirements()
    
    if errors:
        print("\n❌ Requirements not met:\n")
        for error in errors:
            print(error)
        print("\n💡 Please fix the issues above before running the application.")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("✅ All requirements met!\n")
    print("🚀 Starting application...\n")
    
    # Create root window
    root = tk.Tk()
    
    # Set window icon (optional)
    try:
        # root.iconbitmap('icon.ico')
        pass
    except:
        pass
    
    # Create main window
    try:
        app = MainWindow(root)
        print("✅ Application started successfully!")
        print("=" * 60)
        root.mainloop()
    except Exception as e:
        messagebox.showerror(
            "Application Error",
            f"Failed to start application:\n\n{str(e)}"
        )
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
