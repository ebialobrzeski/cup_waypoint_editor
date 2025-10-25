# Quick Release Checklist

Use this checklist when creating a new release.

## Pre-Release
- [ ] All code changes committed
- [ ] Tests pass (load file, add waypoint, edit waypoint, save)
- [ ] README.md updated
- [ ] Version bumped in `src/soaring_cup_file_editor/__init__.py`
- [ ] Changelog section added to README.md

## Build
```powershell
# Clean previous builds
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

# Build executable
python build_exe.py

# Verify file exists and size is reasonable
Get-Item dist\Soaring-CUP-Editor.exe | Select-Object Name, Length
```

## Test Executable
- [ ] Opens without errors
- [ ] Loads waypoints_epbk.cup
- [ ] Adds new waypoint with units
- [ ] Edits existing waypoint
- [ ] All 3 tabs work in dialog
- [ ] Unit dropdowns function
- [ ] Saves file correctly
- [ ] Clipboard paste works

## Git Operations
```powershell
# Commit all changes
git add .
git commit -m "Release v3.0.0 - Complete CUP specification compliance"

# Create and push tag
git tag v3.0.0
git push origin main
git push origin v3.0.0
```

## GitHub Release
1. [ ] Go to https://github.com/ebialobrzeski/cup_waypoint_editor/releases
2. [ ] Click "Create a new release"
3. [ ] Choose tag: v3.0.0
4. [ ] Set title: "Soaring CUP File Editor v3.0.0 - Complete CUP Specification Compliance"
5. [ ] Paste release notes from RELEASE_GUIDE.md
6. [ ] Upload `dist/Soaring-CUP-Editor.exe`
7. [ ] Check "Set as the latest release"
8. [ ] Click "Publish release"

## Verify
- [ ] Release appears on releases page
- [ ] Marked as "Latest"
- [ ] Executable download link works
- [ ] Download and test executable from release page
- [ ] Description displays correctly

## Post-Release
- [ ] Announce on social media (optional)
- [ ] Update any external documentation
- [ ] Close resolved issues on GitHub

---

**Current Version:** v3.0.0
**Next Version:** v3.1.0 or v3.0.1 (TBD)
