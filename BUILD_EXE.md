# Building Windows Executable

This guide explains how to compile the XCSoar CUP Editor into a standalone Windows executable (.exe) file.

## Option 1: PyInstaller (Recommended)

PyInstaller is the most popular tool for creating Python executables.

### Installation

```powershell
pip install pyinstaller
```

### Basic Build

```powershell
# Navigate to project directory
cd c:\Work\cup_waypoint_editor

# Create executable (one-file bundle)
pyinstaller --onefile --windowed --name "XCSoar-CUP-Editor" xcsoar_gui_editor.py

# Or use the provided spec file (see below)
pyinstaller xcsoar_cup_editor.spec
```

### Build Options Explained

- `--onefile`: Creates a single .exe file (easier to distribute)
- `--windowed` or `-w`: No console window appears (for GUI apps)
- `--name`: Custom name for the executable
- `--icon=icon.ico`: Add a custom icon (if you have one)
- `--add-data`: Include additional files

### Output

After building, you'll find:
- `dist/XCSoar-CUP-Editor.exe` - Your standalone executable!
- `build/` - Temporary build files (can be deleted)
- `XCSoar-CUP-Editor.spec` - Build configuration (can be reused)

## Option 2: Auto PY to EXE (GUI Tool)

If you prefer a graphical interface:

```powershell
pip install auto-py-to-exe
auto-py-to-exe
```

Then:
1. Select `xcsoar_gui_editor.py` as the script
2. Choose "One File"
3. Choose "Window Based (hide console)"
4. Click "Convert .py to .exe"

## Option 3: cx_Freeze

Alternative tool with similar features:

```powershell
pip install cx_Freeze
cxfreeze xcsoar_gui_editor.py --target-dir dist
```

## Optimized Build Script

For convenience, I've created a build script and spec file for you.

### Using the Build Script

```powershell
python build_exe.py
```

This will create an optimized executable with:
- Single file output
- No console window
- Proper name and version
- Minimal size

## Troubleshooting

### Issue: "Failed to execute script"

**Solution:** Try `--onedir` instead of `--onefile`:
```powershell
pyinstaller --onedir --windowed --name "XCSoar-CUP-Editor" xcsoar_gui_editor.py
```

### Issue: Large file size

**Solution:** Use UPX compression:
```powershell
# Download UPX from https://upx.github.io/
# Place upx.exe in your PATH or project directory
pyinstaller --onefile --windowed --upx-dir=. xcsoar_gui_editor.py
```

### Issue: Antivirus flags the .exe

This is common with PyInstaller. Solutions:
1. Use code signing certificate (professional)
2. Submit false positive to antivirus vendor
3. Distribute as Python package instead
4. Use `--onedir` mode (less likely to trigger)

### Issue: Missing modules

Add them explicitly:
```powershell
pyinstaller --hidden-import=requests --hidden-import=tkinter xcsoar_gui_editor.py
```

## File Size Comparison

- **--onefile**: ~15-25 MB (everything bundled)
- **--onedir**: Folder with .exe + DLLs (~30-40 MB total, but faster startup)
- **With UPX**: Can reduce by 30-50%

## Distribution

### Single File Distribution
1. Build with `--onefile`
2. Share `dist/XCSoar-CUP-Editor.exe`
3. Users just double-click to run!

### Installer Distribution
For professional distribution, consider:
- **Inno Setup**: Create a Windows installer
- **NSIS**: Another installer creator
- **WiX Toolset**: MSI installer creator

## Advanced: Creating an Installer with Inno Setup

1. Download Inno Setup: https://jrsoftware.org/isdl.php
2. Use the provided `.iss` script (see `installer.iss`)
3. Compile to create `XCSoar_CUP_Editor_Setup.exe`

## Testing Your Executable

```powershell
# Test in a clean directory
cd C:\Temp
C:\Work\cup_waypoint_editor\dist\XCSoar-CUP-Editor.exe
```

Make sure to test:
- Opening CUP files
- Saving CUP files
- CSV import/export
- All editing features
- Elevation API calls

## Performance Notes

- **Startup time**: ~2-5 seconds (loads Python runtime)
- **--onefile**: Slower startup (unpacks to temp folder)
- **--onedir**: Faster startup (no unpacking)

## Recommendations

**For personal use:**
- Use `--onefile` for simplicity
- Accept the slightly slower startup

**For distribution:**
- Consider `--onedir` with installer
- Or use code signing with `--onefile`
- Include README.txt with instructions

**For maximum compatibility:**
- Build on the oldest Windows version you want to support
- Test on multiple Windows versions (10, 11)
- 32-bit build works on 32 and 64-bit systems
