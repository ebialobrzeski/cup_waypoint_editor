@echo off
REM Quick build script for Soaring CUP File Editor
REM Double-click this file to build the executable

echo ========================================
echo Soaring CUP File Editor - Build to EXE
echo ========================================
echo.

echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Installing/Checking PyInstaller...
python -m pip install pyinstaller

echo.
echo Building executable...
python build_exe.py

echo.
echo Done! Check the dist folder for Soaring-CUP-Editor.exe
echo.
pause
