# Quick Start Guide: Building Your Executable

## For Complete Beginners

### Step 1: Open PowerShell in your project folder
1. Open the `cup_waypoint_editor` folder in File Explorer
2. Hold Shift and right-click in the folder
3. Select "Open PowerShell window here"

### Step 2: Run the build
Choose ONE of these methods:

#### Method A: Double-click (Easiest!)
Just double-click `build.bat` - it will:
- Check Python
- Install PyInstaller
- Build your .exe
- Show you where it is

#### Method B: Use the build script
```powershell
python build_exe.py
```

#### Method C: Manual PyInstaller
```powershell
# Install PyInstaller (first time only)
pip install pyinstaller

# Build the executable
pyinstaller xcsoar_cup_editor.spec
```

### Step 3: Find your executable
After building, you'll find your executable here:
```
dist/XCSoar-CUP-Editor.exe
```

### Step 4: Test it
```powershell
.\dist\XCSoar-CUP-Editor.exe
```

### Step 5: Share it
Just copy `XCSoar-CUP-Editor.exe` and share it!
- No Python installation needed on target computer
- No dependencies needed
- Just double-click and it works!

## Expected Results

### Build Time
- First build: 2-5 minutes (downloads dependencies)
- Subsequent builds: 30-60 seconds

### File Size
- Executable: ~15-25 MB (includes Python runtime)
- This is normal for Python executables!

### Startup Time
- First run: 3-5 seconds (unpacks to temp folder)
- Subsequent runs: 2-3 seconds

## Common Issues and Solutions

### Issue: "Python is not recognized"
**Solution:** Python is not in your PATH
```powershell
# Use full path to Python
C:\Users\YourName\AppData\Local\Programs\Python\Python3XX\python.exe build_exe.py
```

### Issue: "Permission denied"
**Solution:** Run as Administrator or move project to your user folder

### Issue: Antivirus flags the .exe
**Solution:** This is normal! 
- Add exception in Windows Defender
- Or use `--onedir` mode (see BUILD_EXE.md)

### Issue: "Failed to execute script"
**Solution:** Try building with console mode first:
```powershell
pyinstaller --onefile --console xcsoar_gui_editor.py
.\dist\xcsoar_gui_editor.exe
# Check error messages in console
```

### Issue: Large file size
**Solutions:**
1. Use UPX compression (reduces by ~30%):
   - Download UPX from https://upx.github.io/
   - Place upx.exe in project folder
   - Edit `xcsoar_cup_editor.spec`: change `upx=False` to `upx=True`

2. Use --onedir mode (creates folder with .exe + DLLs):
   ```powershell
   pyinstaller --onedir --windowed xcsoar_gui_editor.py
   ```

## Customization

### Add an Icon
1. Get a `.ico` file (256x256 recommended)
2. Save it as `icon.ico` in project folder
3. Edit `xcsoar_cup_editor.spec`:
   ```python
   icon='icon.ico',  # Change None to 'icon.ico'
   ```

### Change the Name
Edit `xcsoar_cup_editor.spec`:
```python
name='YourCustomName',  # Change 'XCSoar-CUP-Editor'
```

### Reduce Size
Edit `xcsoar_cup_editor.spec` and add more exclusions:
```python
excludes=[
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'PIL',
    'PyQt5',
    'PyQt6',
    'tkinter.test',  # Add this
    'test',           # Add this
    'unittest',       # Add this
],
```

## Distribution Checklist

Before sharing your .exe:

- [ ] Test on your computer
- [ ] Test on another Windows computer (if possible)
- [ ] Make sure all features work (open, edit, save)
- [ ] Test with actual CUP files
- [ ] Check that API calls work (elevation)
- [ ] Include a README.txt explaining how to use
- [ ] Mention that Windows Defender might scan it first time

## Professional Distribution (Optional)

For a more professional look:

### Option 1: Create an Installer
Use Inno Setup to create `XCSoar_CUP_Editor_Setup.exe`:
1. Download from: https://jrsoftware.org/isdl.php
2. Create installer script
3. Users get a proper Windows installer

### Option 2: Code Signing
- Prevents antivirus warnings
- Requires a code signing certificate (~$100/year)
- Recommended for commercial distribution

### Option 3: Microsoft Store
- Ultimate legitimacy
- Requires developer account
- Can monetize if desired

## Build Variants

### Development Build (with console for debugging)
```powershell
pyinstaller --onefile --console --name "XCSoar-Debug" xcsoar_gui_editor.py
```

### Production Build (no console, optimized)
```powershell
pyinstaller xcsoar_cup_editor.spec
```

### Portable Build (folder with .exe + DLLs)
```powershell
pyinstaller --onedir --windowed xcsoar_gui_editor.py
# Creates dist/xcsoar_gui_editor/ folder
# Can run from USB stick
```

## Troubleshooting Build Errors

If build fails, try these steps:

1. **Clean and rebuild:**
   ```powershell
   Remove-Item -Recurse -Force build, dist
   pyinstaller xcsoar_cup_editor.spec
   ```

2. **Check for missing imports:**
   ```powershell
   python -c "import xcsoar_editor; print('OK')"
   ```

3. **Use verbose mode:**
   ```powershell
   pyinstaller --log-level DEBUG xcsoar_cup_editor.spec
   ```

4. **Test the script first:**
   ```powershell
   python xcsoar_gui_editor.py
   # Make sure it works before building
   ```

## Need Help?

Check these files in the project:
- `BUILD_EXE.md` - Detailed building guide
- `ARCHITECTURE.md` - Project structure
- `README.md` - General information

## Success!

Once built, you can:
✓ Run `XCSoar-CUP-Editor.exe` on any Windows computer
✓ No Python installation required
✓ No dependencies required  
✓ Share the single .exe file
✓ It just works!

**File location:** `dist/XCSoar-CUP-Editor.exe`

**Size:** ~15-25 MB (this is normal!)

**Compatibility:** Windows 7, 8, 10, 11 (64-bit)
