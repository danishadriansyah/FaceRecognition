"""
GUI Module for Desktop Application
Week 7 - Desktop GUI Development
"""

from .main_window import MainWindow
from .register_window import RegisterWindow
from .attendance_window import AttendanceWindow
from .reports_window import ReportsWindow

__all__ = [
    'MainWindow',
    'RegisterWindow', 
    'AttendanceWindow',
    'ReportsWindow'
]
