# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('c:\\Ngoding\\Kerja\\ExtraQueensya\\minggu-8-final-project\\project\\config.py', '.')]
datas += collect_data_files('mediapipe')


a = Analysis(
    ['c:\\Ngoding\\Kerja\\ExtraQueensya\\minggu-8-final-project\\project\\main_app.py'],
    pathex=['c:\\Ngoding\\Kerja\\ExtraQueensya\\minggu-8-final-project\\project'],
    binaries=[],
    datas=datas,
    hiddenimports=['mediapipe', 'cv2', 'PIL', 'PIL.Image', 'PIL.ImageTk', 'numpy', 'pandas', 'tensorflow', 'keras', 'sklearn', 'sklearn.metrics', 'tkinter', 'tkinter.ttk', 'tkinter.messagebox', 'tkinter.simpledialog', 'tkinter.filedialog', 'csv', 'json', 'core', 'core.recognition_service', 'core.attendance_system', 'core.dataset_manager', 'core.teachable_recognizer', 'core.model_manager', 'gui', 'gui.main_window', 'gui.attendance_window', 'gui.reports_window', 'gui.register_window', 'gui.settings_dialog', 'config'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FaceAttendance',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FaceAttendance',
)
