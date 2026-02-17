"""
Build Script - Face Recognition Attendance System
Builds standalone .exe using PyInstaller

Cara pakai:
    1. Buka terminal di folder app-build/
    2. Jalankan: python build.py
    3. Tunggu selesai (~10-20 menit)
    4. Hasil di folder: dist/FaceAttendance/
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

# Paths
BUILD_DIR = Path(__file__).parent
PROJECT_DIR = BUILD_DIR.parent / "minggu-8-final-project" / "project"
DIST_DIR = BUILD_DIR / "dist"
OUTPUT_DIR = DIST_DIR / "FaceAttendance"

def check_pyinstaller():
    """Check if PyInstaller is installed, install if not"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed")

def create_data_folders():
    """Create necessary data folders in output directory"""
    folders = [
        OUTPUT_DIR / "models",
        OUTPUT_DIR / "logs",
        OUTPUT_DIR / "logs" / "photos",
        OUTPUT_DIR / "reports",
        OUTPUT_DIR / "dataset",
    ]
    
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        print(f"   📁 {folder.relative_to(DIST_DIR)}")

def copy_project_data():
    """Copy models, config, and existing data from project"""
    
    # Copy models (keras_model.h5 + labels.txt)
    src_models = PROJECT_DIR / "models"
    dst_models = OUTPUT_DIR / "models"
    
    if src_models.exists():
        for item in src_models.iterdir():
            if item.is_dir():
                dst = dst_models / item.name
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(item, dst)
                print(f"   📋 Model: {item.name}")
    
    # Copy config.json
    config_file = PROJECT_DIR / "config.json"
    if config_file.exists():
        shutil.copy2(config_file, OUTPUT_DIR / "config.json")
        print("   📋 config.json")
    
    # Copy existing attendance logs
    src_logs = PROJECT_DIR / "logs"
    if src_logs.exists():
        for f in src_logs.glob("*.csv"):
            shutil.copy2(f, OUTPUT_DIR / "logs" / f.name)
            print(f"   📋 logs/{f.name}")

def build_exe():
    """Build the .exe using PyInstaller"""
    
    main_script = str(PROJECT_DIR / "main_app.py")
    
    # Paths for --paths (so PyInstaller finds core/ and gui/ as importable)
    # and --add-data (for mediapipe model files, config, etc.)
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "FaceAttendance",
        "--onedir",
        "--console",                       # Console window (more compatible)
        "--noconfirm",
        "--clean",                         # Clean build cache
        "--distpath", str(DIST_DIR),
        "--workpath", str(BUILD_DIR / "build"),
        "--specpath", str(BUILD_DIR),
        
        # Add project directory to Python path so imports work
        "--paths", str(PROJECT_DIR),
        
        # Bundle config.py alongside the exe
        "--add-data", f"{PROJECT_DIR / 'config.py'}{os.pathsep}.",
        
        # Hidden imports PyInstaller might miss
        "--hidden-import", "mediapipe",
        "--hidden-import", "cv2",
        "--hidden-import", "PIL",
        "--hidden-import", "PIL.Image",
        "--hidden-import", "PIL.ImageTk",
        "--hidden-import", "numpy",
        "--hidden-import", "pandas",
        "--hidden-import", "tensorflow",
        "--hidden-import", "keras",
        "--hidden-import", "sklearn",
        "--hidden-import", "sklearn.metrics",
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.ttk",
        "--hidden-import", "tkinter.messagebox",
        "--hidden-import", "tkinter.simpledialog",
        "--hidden-import", "tkinter.filedialog",
        "--hidden-import", "csv",
        "--hidden-import", "json",
        "--hidden-import", "core",
        "--hidden-import", "core.recognition_service",
        "--hidden-import", "core.attendance_system",
        "--hidden-import", "core.dataset_manager",
        "--hidden-import", "core.teachable_recognizer",
        "--hidden-import", "core.model_manager",
        "--hidden-import", "gui",
        "--hidden-import", "gui.main_window",
        "--hidden-import", "gui.attendance_window",
        "--hidden-import", "gui.reports_window",
        "--hidden-import", "gui.register_window",
        "--hidden-import", "gui.settings_dialog",
        "--hidden-import", "config",
        
        # Collect mediapipe data files (model blobs etc.)
        "--collect-data", "mediapipe",
        
        main_script
    ]
    
    print("\n🔨 Building .exe (this may take 10-20 minutes)...\n")
    
    result = subprocess.run(cmd, cwd=str(BUILD_DIR))
    
    if result.returncode == 0:
        print("\n✅ PyInstaller build successful!")
        return True
    else:
        print("\n❌ Build failed! Check errors above.")
        return False

def create_launcher():
    """Create a .bat launcher for easy startup"""
    bat_content = (
        '@echo off\r\n'
        'echo ========================================\r\n'
        'echo   Face Recognition Attendance System\r\n'
        'echo ========================================\r\n'
        'echo.\r\n'
        'echo Starting application...\r\n'
        'start "" "%~dp0FaceAttendance\\FaceAttendance.exe"\r\n'
    )
    
    bat_path = DIST_DIR / "Jalankan_Aplikasi.bat"
    with open(bat_path, 'w') as f:
        f.write(bat_content)
    print(f"   📋 {bat_path.name}")

def main():
    print("=" * 60)
    print("   🔨 Face Recognition Attendance System - Builder")
    print("=" * 60)
    print()
    
    # Verify project exists
    if not PROJECT_DIR.exists():
        print(f"❌ Project not found: {PROJECT_DIR}")
        sys.exit(1)
    
    if not (PROJECT_DIR / "main_app.py").exists():
        print(f"❌ main_app.py not found in: {PROJECT_DIR}")
        sys.exit(1)
    
    print(f"📂 Project : {PROJECT_DIR}")
    print(f"📂 Output  : {OUTPUT_DIR}")
    print()
    
    # Step 1
    print("Step 1/5: Checking PyInstaller...")
    check_pyinstaller()
    
    # Step 2
    print("\nStep 2/5: Building .exe...")
    success = build_exe()
    
    if not success:
        print("\n❌ Build gagal. Fix error di atas lalu jalankan ulang.")
        sys.exit(1)
    
    # Step 3
    print("\nStep 3/5: Creating data folders...")
    create_data_folders()
    
    # Step 4
    print("\nStep 4/5: Copying project data...")
    copy_project_data()
    
    # Step 5
    print("\nStep 5/5: Creating launcher...")
    create_launcher()
    
    # Done!
    print()
    print("=" * 60)
    print("   ✅ BUILD COMPLETE!")
    print("=" * 60)
    print()
    print(f"📂 Output: {OUTPUT_DIR}")
    print()
    print("📦 Untuk distribusi ke student:")
    print("   1. Copy folder 'dist/' ke USB / Google Drive")
    print("   2. Pastikan models/ berisi keras_model.h5 + labels.txt")
    print("   3. Double-click 'Jalankan_Aplikasi.bat' untuk run")
    print()
    print("📊 Ukuran estimasi:")
    
    # Calculate size
    total_size = 0
    for f in OUTPUT_DIR.rglob('*'):
        if f.is_file():
            total_size += f.stat().st_size
    
    print(f"   Total: {total_size / (1024*1024):.0f} MB")

if __name__ == "__main__":
    main()
