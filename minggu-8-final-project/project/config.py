"""
Configuration Management for Face Recognition Attendance System
Week 8 - Final Project
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any
import json


@dataclass
class RecognitionConfig:
    """Recognition system configuration"""
    threshold: float = 0.6  # Face recognition threshold (0.5-0.7)
    detection_confidence: float = 0.5  # Face detection confidence
    model_name: str = "Facenet512"  # DeepFace model
    distance_metric: str = "euclidean"  # Distance calculation method
    
    # Teachable Machine settings
    use_teachable_machine: bool = True  # Use Teachable Machine model
    active_model_id: str = None  # Active model ID (auto-detect if None)
    teachable_confidence: float = 0.7  # Confidence threshold for TM model


@dataclass
class PerformanceConfig:
    """Performance optimization settings"""
    frame_skip: int = 2  # Process every N frames
    max_detection_size: int = 640  # Max frame size for detection
    cache_encodings: bool = True  # Cache face encodings in memory
    max_cache_size: int = 100  # Maximum cached encodings


@dataclass
class AttendanceConfig:
    """Attendance system settings"""
    cooldown_seconds: int = 5  # Prevent duplicate entries
    auto_checkout_hours: int = 12  # Auto check-out after N hours
    work_start_hour: int = 8  # Work day start (8 AM)
    work_end_hour: int = 17  # Work day end (5 PM)


@dataclass
class DatasetConfig:
    """Dataset management settings"""
    min_photos_per_person: int = 20  # Minimum required photos
    max_photos_per_person: int = 50  # Maximum stored photos
    photo_capture_interval: float = 0.5  # Seconds between captures
    min_face_size: int = 80  # Minimum face size in pixels


@dataclass
class BackupConfig:
    """Backup and maintenance settings"""
    auto_backup: bool = True  # Enable automatic backups
    backup_interval_days: int = 1  # Backup every N days
    backup_retention_days: int = 30  # Keep backups for N days
    max_log_size_mb: int = 50  # Max log file size


@dataclass
class GUIConfig:
    """GUI appearance settings"""
    window_width: int = 1200  # Main window width
    window_height: int = 700  # Main window height
    theme: str = "light"  # UI theme (light/dark)
    webcam_width: int = 640  # Webcam display width
    webcam_height: int = 480  # Webcam display height


class Config:
    """
    Central configuration manager for the application.
    
    Example:
        config = Config()
        print(config.recognition.threshold)  # 0.6
        config.recognition.threshold = 0.7
        config.save()
    """
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(__file__).parent / config_file
        
        # Initialize configuration objects
        self.recognition = RecognitionConfig()
        self.performance = PerformanceConfig()
        self.attendance = AttendanceConfig()
        self.dataset = DatasetConfig()
        self.backup = BackupConfig()
        self.gui = GUIConfig()
        
        # Load saved configuration
        self.load()
    
    def load(self) -> bool:
        """
        Load configuration from JSON file.
        
        Returns:
            bool: True if loaded successfully
        """
        if not self.config_file.exists():
            return False
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Update configuration objects
            if 'recognition' in data:
                for key, value in data['recognition'].items():
                    if hasattr(self.recognition, key):
                        setattr(self.recognition, key, value)
            
            if 'performance' in data:
                for key, value in data['performance'].items():
                    if hasattr(self.performance, key):
                        setattr(self.performance, key, value)
            
            if 'attendance' in data:
                for key, value in data['attendance'].items():
                    if hasattr(self.attendance, key):
                        setattr(self.attendance, key, value)
            
            if 'dataset' in data:
                for key, value in data['dataset'].items():
                    if hasattr(self.dataset, key):
                        setattr(self.dataset, key, value)
            
            if 'backup' in data:
                for key, value in data['backup'].items():
                    if hasattr(self.backup, key):
                        setattr(self.backup, key, value)
            
            if 'gui' in data:
                for key, value in data['gui'].items():
                    if hasattr(self.gui, key):
                        setattr(self.gui, key, value)
            
            return True
        except Exception as e:
            print(f"Error loading config: {e}")
            return False
    
    def save(self) -> bool:
        """
        Save configuration to JSON file.
        
        Returns:
            bool: True if saved successfully
        """
        try:
            data = {
                'recognition': self._dataclass_to_dict(self.recognition),
                'performance': self._dataclass_to_dict(self.performance),
                'attendance': self._dataclass_to_dict(self.attendance),
                'dataset': self._dataclass_to_dict(self.dataset),
                'backup': self._dataclass_to_dict(self.backup),
                'gui': self._dataclass_to_dict(self.gui),
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def reset_to_defaults(self):
        """Reset all configuration to default values"""
        self.recognition = RecognitionConfig()
        self.performance = PerformanceConfig()
        self.attendance = AttendanceConfig()
        self.dataset = DatasetConfig()
        self.backup = BackupConfig()
        self.gui = GUIConfig()
        self.save()
    
    def _dataclass_to_dict(self, obj) -> Dict[str, Any]:
        """Convert dataclass to dictionary"""
        return {
            key: getattr(obj, key) 
            for key in obj.__annotations__.keys()
        }
    
    def get_all_settings(self) -> Dict[str, Dict[str, Any]]:
        """Get all settings as nested dictionary"""
        return {
            'recognition': self._dataclass_to_dict(self.recognition),
            'performance': self._dataclass_to_dict(self.performance),
            'attendance': self._dataclass_to_dict(self.attendance),
            'dataset': self._dataclass_to_dict(self.dataset),
            'backup': self._dataclass_to_dict(self.backup),
            'gui': self._dataclass_to_dict(self.gui),
        }
    
    def update_setting(self, category: str, key: str, value: Any) -> bool:
        """
        Update a specific setting.
        
        Args:
            category: Configuration category (e.g., 'recognition')
            key: Setting key (e.g., 'threshold')
            value: New value
        
        Returns:
            bool: True if updated successfully
        """
        try:
            if category == 'recognition' and hasattr(self.recognition, key):
                setattr(self.recognition, key, value)
            elif category == 'performance' and hasattr(self.performance, key):
                setattr(self.performance, key, value)
            elif category == 'attendance' and hasattr(self.attendance, key):
                setattr(self.attendance, key, value)
            elif category == 'dataset' and hasattr(self.dataset, key):
                setattr(self.dataset, key, value)
            elif category == 'backup' and hasattr(self.backup, key):
                setattr(self.backup, key, value)
            elif category == 'gui' and hasattr(self.gui, key):
                setattr(self.gui, key, value)
            else:
                return False
            
            self.save()
            return True
        except Exception:
            return False


# Global configuration instance
_config_instance = None

def get_config() -> Config:
    """
    Get global configuration instance (singleton).
    
    Returns:
        Config: Global configuration object
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance


if __name__ == "__main__":
    # Test configuration
    print("=== Configuration Test ===\n")
    
    config = Config()
    
    print("Recognition Settings:")
    print(f"  Threshold: {config.recognition.threshold}")
    print(f"  Model: {config.recognition.model_name}")
    
    print("\nPerformance Settings:")
    print(f"  Frame Skip: {config.performance.frame_skip}")
    print(f"  Max Detection Size: {config.performance.max_detection_size}")
    
    print("\nAttendance Settings:")
    print(f"  Cooldown: {config.attendance.cooldown_seconds}s")
    print(f"  Work Hours: {config.attendance.work_start_hour}:00 - {config.attendance.work_end_hour}:00")
    
    print("\nDataset Settings:")
    print(f"  Min Photos: {config.dataset.min_photos_per_person}")
    print(f"  Max Photos: {config.dataset.max_photos_per_person}")
    
    print("\nBackup Settings:")
    print(f"  Auto Backup: {config.backup.auto_backup}")
    print(f"  Retention: {config.backup.backup_retention_days} days")
    
    print("\nGUI Settings:")
    print(f"  Window Size: {config.gui.window_width}x{config.gui.window_height}")
    print(f"  Theme: {config.gui.theme}")
    
    # Test save/load
    print("\n=== Testing Save/Load ===")
    config.recognition.threshold = 0.7
    config.save()
    print("✅ Configuration saved")
    
    config2 = Config()
    print(f"✅ Loaded threshold: {config2.recognition.threshold}")
    
    # Reset
    config2.reset_to_defaults()
    print("✅ Configuration reset to defaults")
