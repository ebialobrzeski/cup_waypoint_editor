@echo off
REM Quick build script for XCSoar CUP Editor
REM Double-click this file to build the executable

echo ========================================
echo XCSoar CUP Editor - Build to EXE
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
echo Done! Check the dist folder for XCSoar-CUP-Editor.exe
echo.
pause
