"""
Build script for creating Windows executable of XCSoar CUP Editor.

Usage:
    python build_exe.py

This script will:
1. Check if PyInstaller is installed
2. Clean previous builds
3. Build the executable
4. Report the output location
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path


def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} is installed")
        return True
    except ImportError:
        print("✗ PyInstaller is not installed")
        print("\nInstalling PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install PyInstaller")
            return False


def clean_build_dirs():
    """Remove previous build directories."""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}/...")
            shutil.rmtree(dir_name)
    
    # Remove spec file if it exists (we have a custom one)
    if os.path.exists('XCSoar-CUP-Editor.spec'):
        os.remove('XCSoar-CUP-Editor.spec')
    
    print("✓ Cleaned previous build artifacts")


def build_executable():
    """Build the executable using PyInstaller."""
    print("\nBuilding executable...")
    print("This may take a few minutes...\n")
    
    # Check if custom spec file exists
    if os.path.exists('xcsoar_cup_editor.spec'):
        print("Using custom spec file: xcsoar_cup_editor.spec")
        cmd = [sys.executable, "-m", "PyInstaller", "xcsoar_cup_editor.spec"]
    else:
        print("Using default PyInstaller settings")
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", "XCSoar-CUP-Editor",
            "--hidden-import", "requests",
            "--hidden-import", "urllib3",
            "--hidden-import", "certifi",
            "xcsoar_gui_editor.py"
        ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print("✗ Build failed!")
        print("\nError output:")
        print(e.stderr)
        return False


def report_results():
    """Report the build results."""
    exe_path = Path("dist/XCSoar-CUP-Editor.exe")
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print("\n" + "="*60)
        print("BUILD SUCCESSFUL!")
        print("="*60)
        print(f"\nExecutable location: {exe_path.absolute()}")
        print(f"File size: {size_mb:.2f} MB")
        print("\nYou can now:")
        print("1. Test it: .\\dist\\XCSoar-CUP-Editor.exe")
        print("2. Share it: Send the .exe file to others")
        print("3. Move it: Copy to any location (no Python needed!)")
        print("\nNote: Windows Defender may scan it on first run.")
        print("="*60)
    else:
        print("\n✗ Executable not found. Build may have failed.")


def main():
    """Main build process."""
    print("="*60)
    print("XCSoar CUP Editor - Windows Executable Builder")
    print("="*60)
    print()
    
    # Step 1: Check PyInstaller
    if not check_pyinstaller():
        print("\nPlease install PyInstaller manually:")
        print("  pip install pyinstaller")
        return 1
    
    # Step 2: Clean previous builds
    clean_build_dirs()
    
    # Step 3: Build
    if not build_executable():
        return 1
    
    # Step 4: Report results
    report_results()
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nBuild cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)
