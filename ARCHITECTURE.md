# Architecture and Design Document

## Overview

The XCSoar CUP Editor has been refactored from a single monolithic file into a well-structured Python package following industry best practices.

## Design Principles

### 1. Separation of Concerns
Each module has a single, well-defined responsibility:
- **models.py**: Data structures and validation
- **file_io.py**: File parsing and writing operations
- **utils.py**: Utility functions for coordinate conversions
- **config.py**: Application constants and configuration
- **gui/**: User interface components

### 2. Modularity
The code is organized into logical modules that can be:
- Tested independently
- Reused in other projects
- Modified without affecting other components
- Imported as a library

### 3. Type Safety
- Uses dataclasses for structured data
- Type hints throughout the codebase
- Clear interfaces between modules

### 4. Error Handling
- Validation in the Waypoint model
- Graceful degradation for API failures
- User-friendly error messages

## Module Descriptions

### Core Modules

#### `models.py` - Data Models
- **Waypoint**: Dataclass representing a waypoint with validation
- **Benefits**:
  - Automatic `__init__`, `__repr__`, `__eq__` methods
  - Post-initialization validation
  - Clear data structure
  - Easy serialization/deserialization

#### `file_io.py` - File Operations
- **parse_cup_file()**: Read CUP format
- **write_cup_file()**: Write CUP format with optional elevation fetching
- **parse_csv_file()**: Import from CSV
- **write_csv_file()**: Export to CSV
- **get_elevation()**: Fetch elevation from API
- **Benefits**:
  - Centralized file handling
  - Consistent error handling
  - Easy to test
  - Can be used programmatically

#### `utils.py` - Utilities
- **ddmm_to_deg()**: Convert DDMM.MMMMM to decimal degrees
- **deg_to_ddmm()**: Convert decimal degrees to DDMM.MMMMM
- **Benefits**:
  - Pure functions (no side effects)
  - Easy to test
  - Reusable in other projects
  - Well-documented with examples

#### `config.py` - Configuration
- Style options mapping
- API configuration
- Coordinate validation ranges
- **Benefits**:
  - Single source of truth
  - Easy to modify settings
  - No magic numbers in code

### GUI Modules

#### `gui/main_window.py` - Main Window
- **MainWindow**: Main application class
- Handles file operations
- Manages waypoint list
- Tree view display
- **Benefits**:
  - Clean separation from business logic
  - Easy to modify UI without affecting data handling
  - Private methods prefixed with `_` for clarity

#### `gui/dialogs.py` - Dialog Windows
- **WaypointDialog**: Add/Edit waypoint dialog
- Input validation
- Keyboard shortcuts
- **Benefits**:
  - Reusable dialog component
  - Consistent validation
  - Modal dialog handling

## Key Improvements

### 1. From Dictionary to Dataclass
**Before:**
```python
point = {"name": name, "latitude": lat, "longitude": lon, "style": style}
```

**After:**
```python
waypoint = Waypoint(name=name, latitude=lat, longitude=lon, style=style)
```

**Benefits:**
- Type checking
- Automatic validation
- Better IDE support (autocomplete, type hints)
- Immutability options

### 2. Separation of GUI and Logic
**Before:** All logic in XCSoarGUI class

**After:** 
- Business logic in `file_io.py` and `models.py`
- GUI only handles display and user interaction

**Benefits:**
- Can test logic without GUI
- Can create CLI version easily
- Can use as a library

### 3. Proper Package Structure
**Before:** Single file `xcsoar_gui_editor.py`

**After:** Full package with:
```
src/xcsoar_editor/
├── __init__.py (exports public API)
├── __main__.py (entry point)
├── config.py
├── models.py
├── utils.py
├── file_io.py
└── gui/
```

**Benefits:**
- Installable via pip
- Importable as library
- Proper namespace
- Professional structure

### 4. Modern Python Packaging
**Added:**
- `pyproject.toml` (PEP 518)
- `setup.py` (for compatibility)
- Entry point console script
- Editable installation support

**Benefits:**
- `pip install -e .` for development
- `xcsoar-editor` command available globally
- Can publish to PyPI if desired

### 5. Documentation
**Added:**
- Docstrings for all functions and classes
- Type hints throughout
- Examples in docstrings
- Comprehensive README

## Usage Patterns

### As a Standalone Application
```powershell
# After installation
xcsoar-editor

# Or directly
python -m xcsoar_editor
```

### As a Library
```python
from xcsoar_editor import Waypoint, parse_cup_file, write_cup_file

# Read waypoints
waypoints = parse_cup_file("myfile.cup")

# Create new waypoint
new_wp = Waypoint(name="Home", latitude=52.765234, longitude=23.186700, style=1)
waypoints.append(new_wp)

# Save
write_cup_file("output.cup", waypoints)
```

### For Testing
```python
from xcsoar_editor.utils import ddmm_to_deg, deg_to_ddmm

# Test coordinate conversions
assert ddmm_to_deg("5245.91404N") == 52.765234
assert deg_to_ddmm(52.765234, True) == "5245.91404N"
```

## Testing Strategy

The modular structure enables easy testing:

1. **Unit Tests**: Test individual functions
   - `utils.py` functions (pure functions, easy to test)
   - `models.py` validation
   - File parsing logic

2. **Integration Tests**: Test module interactions
   - File I/O with models
   - GUI interactions with file operations

3. **End-to-End Tests**: Test full workflows
   - Load → Edit → Save
   - Import CSV → Export CUP

## Future Enhancements

The new structure makes it easy to add:

1. **Command-Line Interface**: Add `cli.py` module
2. **Unit Tests**: Add `tests/` directory
3. **Async Operations**: Make elevation fetching async
4. **Plugins**: Add plugin system for custom formats
5. **Batch Operations**: Process multiple files
6. **Configuration File**: User preferences and settings
7. **Undo/Redo**: Command pattern for operations

## Performance Considerations

- Lazy loading of elevation data
- Tree view updates only when needed
- File operations use generators for large files (future)
- Minimal imports for faster startup

## Backward Compatibility

The original `xcsoar_gui_editor.py` file has been converted to a simple launcher that imports from the new package structure, ensuring existing workflows continue to work.

## Conclusion

This refactoring transforms a quick script into a professional, maintainable Python package that:
- Follows Python best practices
- Is easy to extend and modify
- Can be used as both an application and a library
- Has clear separation of concerns
- Is ready for testing and CI/CD integration
