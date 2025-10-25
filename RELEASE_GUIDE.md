# GitHub Release Guide

This guide explains how to create a GitHub release and upload the Windows executable.

## Prerequisites

- GitHub account with access to the repository
- Built executable file: `dist/Soaring-CUP-Editor.exe`
- Repository pushed to GitHub

## Steps to Create a Release

### 1. Build the Executable

First, make sure you have a fresh build:

```powershell
# Clean previous builds
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

# Build the executable
python build_exe.py
# OR
build.bat

# Verify the executable exists
Test-Path dist\Soaring-CUP-Editor.exe
```

The executable will be in `dist/Soaring-CUP-Editor.exe` (approximately 15-20 MB).

### 2. Test the Executable

**Important:** Test the executable before releasing!

```powershell
# Run from dist folder
cd dist
.\Soaring-CUP-Editor.exe

# Test these features:
# - Opens without errors
# - Loads a CUP file
# - Adds/edits a waypoint
# - Saves a file
# - All tabs work in dialog
# - Unit dropdowns work
```

### 3. Create a Release on GitHub

#### Option A: Using GitHub Web Interface (Recommended)

1. **Go to your repository** on GitHub:
   ```
   https://github.com/ebialobrzeski/cup_waypoint_editor
   ```

2. **Click on "Releases"** (right sidebar)

3. **Click "Create a new release"** or **"Draft a new release"**

4. **Fill in the release information:**

   **Tag version:** (e.g., `v3.0.0`)
   ```
   v3.0.0
   ```
   
   **Release title:**
   ```
   Soaring CUP File Editor v3.0.0 - Complete CUP Specification Compliance
   ```
   
   **Description:** (copy/paste this template)
   ```markdown
   ## ✨ What's New in v3.0.0
   
   ### Complete CUP Specification Compliance
   - ✅ **Full Unit Support**: Elevation (m/ft), Runway dimensions (m/nm/ml) with dropdown selectors
   - ✅ **Runway Direction Validation**: Strict 3-digit (000-359) or PG format (100-359.xxx)
   - ✅ **Auto-Correction**: Converts invalid 360° to 000° automatically
   - ✅ **Extended Precision**: 5 decimal places in coordinates for maximum accuracy
   - ✅ **Google Maps Integration**: Paste coordinates directly from clipboard
   - ✅ **🌍 Auto-Elevation Fetch**: 💡 **IMPORTANT** - Zero-effort elevation! Just enter coordinates, elevation is automatically fetched from Open-Elevation API. No manual lookup needed!
   - ✅ **Smart UI**: Auto-sort, auto-refresh, selection tracking
   
   ### All Features
   - 🎯 100% SeeYou CUP format specification compliance
   - 🖥️ Modern 3-tab dialog interface
   - 🛫 Complete airfield data support
   - 💾 In-memory editing with explicit save
   - 📊 8-column tree view (1200x600 window)
   - 🌍 All 22 waypoint types (0-21)
   - 🔧 Mixed units support in same file
   
   ## 📥 Download
   
   **Windows Users:** Download `Soaring-CUP-Editor.exe` below
   - No Python installation required
   - Just download and run!
   - ~15-20 MB file size
   
   **Developers:** Clone the repository and run from source:
   ```bash
   git clone https://github.com/ebialobrzeski/cup_waypoint_editor.git
   cd cup_waypoint_editor
   pip install -r requirements.txt
   python soaring_cup_editor.py
   ```
   
   ## 📝 System Requirements
   - Windows 10/11 (64-bit)
   - No additional software needed
   
   ## 🐛 Known Issues
   - None currently known
   
   ## 📚 Documentation
   - See [README.md](README.md) for full usage guide
   - See [BUILD_EXE.md](BUILD_EXE.md) for building from source
   
   ---
   
   **Full Changelog:** See README.md in the repository
   
   **Happy Soaring! ⛅✈️**
   ```

5. **Upload the executable:**
   - Scroll down to **"Attach binaries by dropping them here or selecting them"**
   - Click or drag `dist/Soaring-CUP-Editor.exe` into the box
   - Wait for upload to complete (shows green checkmark)

6. **Set as latest release:**
   - Check ✅ **"Set as the latest release"**
   - Leave **"Create a discussion for this release"** unchecked (optional)

7. **Publish:**
   - Click **"Publish release"** (green button)

#### Option B: Using GitHub CLI (`gh`)

If you have GitHub CLI installed:

```powershell
# Install GitHub CLI if needed
# winget install --id GitHub.cli

# Authenticate (first time only)
gh auth login

# Create release and upload executable
gh release create v3.0.0 `
  dist\Soaring-CUP-Editor.exe `
  --title "Soaring CUP File Editor v3.0.0 - Complete CUP Specification Compliance" `
  --notes-file RELEASE_NOTES.md
```

Create `RELEASE_NOTES.md` first with the description from above.

### 4. Verify the Release

1. **Go to releases page:**
   ```
   https://github.com/ebialobrzeski/cup_waypoint_editor/releases
   ```

2. **Check that:**
   - ✅ Release is marked as "Latest"
   - ✅ Version tag is correct (v3.0.0)
   - ✅ Executable is attached as an asset
   - ✅ Description displays correctly
   - ✅ Download link works

3. **Test download:**
   - Click on the executable asset
   - Download to a test location
   - Run to verify it works

## Version Numbering

Use [Semantic Versioning](https://semver.org/):

- **Major version** (v3.0.0): Breaking changes, major new features
- **Minor version** (v3.1.0): New features, backward compatible
- **Patch version** (v3.0.1): Bug fixes only

Examples:
- `v3.0.0` - Complete CUP specification compliance (current)
- `v3.1.0` - Future: Add map integration feature
- `v3.0.1` - Future: Fix a bug in elevation fetching

## Release Checklist

Before creating a release:

- [ ] All tests pass
- [ ] Documentation updated (README.md)
- [ ] Changelog updated
- [ ] Version number bumped in `__init__.py`
- [ ] Clean build created
- [ ] Executable tested on clean Windows system
- [ ] Git committed and pushed to main branch
- [ ] Git tag created locally: `git tag v3.0.0`
- [ ] Git tag pushed: `git push origin v3.0.0`

## Updating an Existing Release

If you need to fix a release:

1. **Edit the release:**
   - Go to releases page
   - Click "Edit" button (pencil icon)
   - Update description or title

2. **Replace executable:**
   - Delete old asset (click X)
   - Upload new executable
   - Click "Update release"

## Best Practices

### File Naming
- ✅ Good: `Soaring-CUP-Editor.exe`
- ❌ Bad: `editor.exe`, `setup.exe`, `app_v3.exe`

### Release Notes
- Always include what's new
- List breaking changes prominently
- Include system requirements
- Add screenshots if UI changed
- Link to documentation

### Frequency
- Don't release too often (confuses users)
- Group related fixes into one release
- Major features deserve their own release

### Pre-releases
For testing before official release:
- Create release as usual
- Check ☑️ **"Set as a pre-release"**
- Tag as `v3.0.0-beta.1` or `v3.0.0-rc.1`

## Troubleshooting

### Upload Failed
- Check file size (must be < 2 GB)
- Check internet connection
- Try again in a few minutes

### Can't Create Tag
```powershell
# Check existing tags
git tag -l

# Delete tag if it exists
git tag -d v3.0.0
git push origin :refs/tags/v3.0.0

# Create new tag
git tag v3.0.0
git push origin v3.0.0
```

### Wrong Version Number
- Edit the release
- Change the tag version
- Or delete release and recreate

## Additional Resources

- [GitHub Releases Documentation](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Semantic Versioning](https://semver.org/)
- [GitHub CLI Documentation](https://cli.github.com/manual/)

---

**Questions?** Open an issue on GitHub!
