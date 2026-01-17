"""
Face Recognition Attendance System - Main Application
Week 8 - Final Capstone Project

Complete integration of all modules from Week 1-7.
"""

import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import logging
from datetime import datetime

# Add core modules to path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Configure logging
log_dir = project_dir / "logs"
log_dir.mkdir(exist_ok=True)

# Configure logging with UTF-8 encoding for Windows compatibility
import sys
import io

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'app.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def check_requirements():
    """
    Check if all required dependencies are installed.
    
    Returns:
        list: List of missing dependencies (empty if all OK)
    """
    missing = []
    required = {
        'cv2': 'opencv-python',
        'mediapipe': 'mediapipe',
        'PIL': 'Pillow',
        'numpy': 'numpy',
        'deepface': 'deepface',
    }
    
    for module_name, package_name in required.items():
        try:
            __import__(module_name)
        except ImportError:
            missing.append(package_name)
    
    return missing


def check_directory_structure():
    """
    Ensure all required directories exist.
    
    Returns:
        bool: True if all directories OK
    """
    required_dirs = [
        project_dir / "core",
        project_dir / "gui",
        project_dir / "dataset",
        project_dir / "logs",
        project_dir / "backups",
        project_dir / "tests",
        project_dir / "docs",
    ]
    
    for directory in required_dirs:
        directory.mkdir(exist_ok=True)
    
    return True


def check_core_modules():
    """
    Verify that all core modules are available.
    
    Returns:
        tuple: (success: bool, missing: list)
    """
    required_modules = [
        'core.image_utils',
        'core.face_detector',
        'core.face_recognizer',
        'core.dataset_manager',
        'core.recognition_service',
        'core.attendance_system',
    ]
    
    missing = []
    for module_name in required_modules:
        try:
            __import__(module_name)
        except ImportError:
            missing.append(module_name)
    
    return len(missing) == 0, missing


def check_gui_modules():
    """
    Verify that all GUI modules are available.
    
    Returns:
        tuple: (success: bool, missing: list)
    """
    required_modules = [
        'gui.main_window',
        'gui.register_window',
        'gui.attendance_window',
        'gui.reports_window',
    ]
    
    missing = []
    for module_name in required_modules:
        try:
            __import__(module_name)
        except ImportError:
            missing.append(module_name)
    
    return len(missing) == 0, missing


def create_requirements_txt():
    """Check if requirements.txt exists in root workspace"""
    root_dir = project_dir.parent.parent
    req_file = root_dir / "requirements.txt"
    
    if req_file.exists():
        logger.info(f"✅ Using requirements.txt from: {req_file}")
        return True
    else:
        logger.warning(f"⚠️  requirements.txt not found at: {req_file}")
        logger.warning("   Please ensure requirements.txt exists in root workspace")
        return False


def initialize_application():
    """
    Initialize application with all necessary checks.
    
    Returns:
        bool: True if initialization successful
    """
    logger.info("="*60)
    logger.info("Face Recognition Attendance System - Starting...")
    logger.info("Week 8 - Final Capstone Project")
    logger.info("="*60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        logger.error("Python 3.8+ required")
        return False
    logger.info(f"✅ Python version: {sys.version}")
    
    # Check dependencies
    missing_deps = check_requirements()
    if missing_deps:
        logger.error(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        logger.error("Install with: pip install " + " ".join(missing_deps))
        
        # Show error dialog
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Missing Dependencies",
            f"Please install missing packages:\n\n" +
            "\n".join(missing_deps) +
            "\n\nRun: pip install -r requirements.txt"
        )
        return False
    logger.info("✅ All dependencies installed")
    
    # Check directory structure
    check_directory_structure()
    logger.info("✅ Directory structure OK")
    
    # Check requirements.txt exists in root
    if not create_requirements_txt():
        logger.warning("⚠️  requirements.txt check failed (non-critical)")
    
    # Check core modules
    core_ok, missing_core = check_core_modules()
    if not core_ok:
        logger.error(f"❌ Missing core modules: {', '.join(missing_core)}")
        logger.error("Please ensure all Week 1-6 modules are in core/ folder")
        return False
    logger.info("✅ Core modules available")
    
    # Check GUI modules
    gui_ok, missing_gui = check_gui_modules()
    if not gui_ok:
        logger.error(f"❌ Missing GUI modules: {', '.join(missing_gui)}")
        logger.error("Please ensure all Week 7 modules are in gui/ folder")
        return False
    logger.info("✅ GUI modules available")
    
    logger.info("="*60)
    logger.info("🚀 Application initialized successfully!")
    logger.info("="*60)
    
    return True


def main():
    """Main application entry point"""
    
    # Initialize application
    if not initialize_application():
        logger.error("Application initialization failed")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    try:
        # Import main window (after all checks pass)
        from gui.main_window import MainWindow
        
        # Create Tkinter root
        root = tk.Tk()
        
        # Set window icon and title
        root.title("Face Recognition Attendance System - Final Project")
        
        # Center window on screen
        window_width = 1200
        window_height = 700
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Prevent resizing
        root.resizable(False, False)
        
        # Create main window
        app = MainWindow(root)
        
        logger.info("Application window created")
        logger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Start event loop
        root.mainloop()
        
        logger.info("Application closed")
        
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        
        # Show error dialog
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Application Error",
            f"An error occurred:\n\n{str(e)}\n\nCheck logs/app.log for details"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
