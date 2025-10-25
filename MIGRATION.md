# Migration Guide

## What Changed?

The XCSoar CUP Editor has been refactored from a single-file application into a professional Python package with proper structure and organization.

## For End Users

### Nothing breaks! 

You can continue using the application exactly as before:

```powershell
python xcsoar_gui_editor.py
```

### Better Way (Recommended)

After installing the package, you can now run it from anywhere:

```powershell
# Install once
python -m pip install -e .

# Run from anywhere
python -m xcsoar_editor
# OR (if Scripts folder is in PATH)
xcsoar-editor
```

## For Developers

### Old Structure
```
cup_waypoint_editor/
├── xcsoar_gui_editor.py  (all code in one file)
├── requirements.txt
└── README.md
```

### New Structure
```
cup_waypoint_editor/
├── src/
│   └── xcsoar_editor/
│       ├── __init__.py
│       ├── __main__.py
│       ├── config.py
│       ├── models.py
│       ├── utils.py
│       ├── file_io.py
│       └── gui/
│           ├── __init__.py
│           ├── main_window.py
│           └── dialogs.py
├── xcsoar_gui_editor.py  (now just a launcher)
├── setup.py
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── README.md
└── ARCHITECTURE.md
```

## Key Changes

### 1. Code Organization

**Before:**
- Everything in one 530-line file
- Hard to navigate
- Hard to test
- Hard to reuse

**After:**
- Separated into logical modules
- Each module < 200 lines
- Clear responsibilities
- Easy to test and reuse

### 2. Data Structures

**Before:**
```python
point = {
    'name': 'Home',
    'latitude': 52.765234,
    'longitude': 23.186700,
    'style': 1
}
```

**After:**
```python
from xcsoar_editor import Waypoint

waypoint = Waypoint(
    name='Home',
    latitude=52.765234,
    longitude=23.186700,
    style=1
)
```

**Benefits:**
- Type safety
- Validation
- Better IDE support
- Clear structure

### 3. Imports

**Before:**
```python
# Everything was in one file
from xcsoar_gui_editor import *  # (not recommended)
```

**After:**
```python
# Clean, specific imports
from xcsoar_editor import Waypoint
from xcsoar_editor import parse_cup_file, write_cup_file
from xcsoar_editor.utils import ddmm_to_deg, deg_to_ddmm
```

### 4. Installation

**Before:**
```powershell
pip install requests
python xcsoar_gui_editor.py
```

**After (Development):**
```powershell
pip install -e .
xcsoar-editor  # or: python -m xcsoar_editor
```

**After (Production):**
```powershell
pip install .
xcsoar-editor
```

## Using as a Library

The new structure allows you to use the editor components as a library:

```python
from xcsoar_editor import Waypoint, parse_cup_file, write_cup_file

# Read waypoints
waypoints = parse_cup_file("input.cup")

# Modify
for wp in waypoints:
    if wp.style == 1:  # Change all waypoints to airfields
        wp.style = 4

# Add new waypoint
new_wp = Waypoint(
    name="New Point",
    latitude=52.0,
    longitude=23.0,
    style=1
)
waypoints.append(new_wp)

# Save
write_cup_file("output.cup", waypoints)
```

## Testing

The new structure makes testing much easier:

```python
# Test coordinate conversion
from xcsoar_editor.utils import ddmm_to_deg, deg_to_ddmm

lat = 52.765234
lat_ddmm = deg_to_ddmm(lat, True)
assert lat_ddmm == "5245.91404N"
assert ddmm_to_deg(lat_ddmm) == lat

# Test waypoint validation
from xcsoar_editor import Waypoint

try:
    invalid = Waypoint(name="Bad", latitude=100, longitude=0)
except ValueError as e:
    print(f"Validation works: {e}")
```

## Configuration Changes

**Before:** Constants scattered throughout code

**After:** Centralized in `config.py`

```python
from xcsoar_editor.config import STYLE_OPTIONS, LATITUDE_MIN, LATITUDE_MAX

print(STYLE_OPTIONS[1])  # "Waypoint"
print(f"Valid latitude range: {LATITUDE_MIN} to {LATITUDE_MAX}")
```

## GUI Changes

The GUI code has been split:

- **main_window.py**: Main application window
- **dialogs.py**: Dialog windows (Add/Edit waypoint)

This separation makes it easier to:
- Modify the UI
- Add new dialogs
- Test components individually
- Create alternative UIs (e.g., web interface)

## Backward Compatibility

The original `xcsoar_gui_editor.py` file still works! It now:

1. Adds `src/` to the Python path
2. Imports from the new package
3. Calls the main entry point

This ensures existing scripts and workflows continue to work.

## Common Migration Patterns

### Pattern 1: Direct Script Usage
**Before:**
```powershell
python xcsoar_gui_editor.py
```

**After (Still Works):**
```powershell
python xcsoar_gui_editor.py
```

**After (Better):**
```powershell
python -m xcsoar_editor
```

### Pattern 2: Programmatic Usage
**Before:** Not possible (everything in GUI class)

**After:**
```python
from xcsoar_editor import parse_cup_file, write_cup_file

waypoints = parse_cup_file("input.cup")
# Process waypoints
write_cup_file("output.cup", waypoints)
```

### Pattern 3: Custom Scripts
**Before:**
```python
# Had to copy-paste functions
def ddmm_to_deg(coord_str):
    # ... lots of code ...
```

**After:**
```python
from xcsoar_editor.utils import ddmm_to_deg

result = ddmm_to_deg("5245.91404N")
```

## Benefits Summary

1. **Maintainability**: Easier to understand and modify
2. **Testability**: Can test individual components
3. **Reusability**: Use as library in other projects
4. **Professional**: Follows Python packaging standards
5. **Extensible**: Easy to add new features
6. **Documentation**: Clear structure with docstrings
7. **Type Safety**: Type hints throughout
8. **Validation**: Built-in data validation

## Questions?

See `ARCHITECTURE.md` for detailed design documentation.
