# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file for XCSoar CUP Editor
Usage: pyinstaller xcsoar_cup_editor.spec
"""

block_cipher = None

a = Analysis(
    ['xcsoar_gui_editor.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/xcsoar_editor', 'xcsoar_editor'),  # Include package modules
    ],
    hiddenimports=[
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'PyQt5',
        'PyQt6',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='XCSoar-CUP-Editor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Enable UPX compression if available
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add 'icon.ico' if you have an icon file
)
