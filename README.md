# XCSoar CUP Waypoint Editor

A professional graphical editor for XCSoar CUP waypoint files with **full SeeYou CUP format support** and CSV import/export capabilities.

## Features

### Core Features
- **Complete CUP Format Support**: All 12 fields (name, code, country, coordinates, elevation, style, runway info, frequency, description)
- **Enhanced Dialog**: 3-tab interface for basic info, airfield data, and details
- **Extended Tree View**: 8 columns showing all important waypoint information
- **CSV Support**: Full import/export with all fields preserved
- **In-Memory Editing**: Changes only saved when you explicitly click Save
- **Unsaved Changes Protection**: Warns you before closing with unsaved changes

### Waypoint Management
- **Full CRUD Operations**: Create, Read, Update, Delete waypoints
- **All 21 Waypoint Types**: Complete style support (waypoints, airfields, mountains, etc.)
- **Airfield Support**: Runway direction, length, width, and radio frequency
- **Automatic Elevation**: Fetches elevation data from Open-Elevation API
- **Field Validation**: Comprehensive validation for all input fields
- **Precision Coordinates**: 5 decimal place precision in DDMM format

### Technical Features
- **Modern Architecture**: Modular package structure following Python best practices
- **Professional Structure**: Proper separation of concerns (models, file I/O, GUI, utilities)
- **Type Safety**: Type hints throughout the codebase
- **Comprehensive Documentation**: Detailed docstrings and user guides

## Project Structure

```
cup_waypoint_editor/
├── src/
│   └── xcsoar_editor/          # Main package
│       ├── __init__.py          # Package exports
│       ├── __main__.py          # Entry point
│       ├── config.py            # Configuration and constants
│       ├── models.py            # Waypoint data model
│       ├── utils.py             # Coordinate conversion utilities
│       ├── file_io.py           # CUP/CSV file operations
│       └── gui/                 # GUI components
│           ├── __init__.py
│           ├── main_window.py   # Main application window
│           └── dialogs.py       # Dialog windows
├── xcsoar_gui_editor.py         # Legacy launcher (for backwards compatibility)
├── requirements.txt             # Dependencies
├── setup.py                     # Package setup (setuptools)
├── pyproject.toml               # Modern package configuration
└── README.md                    # This file
```

## Installation

### For End Users (No Python Required!)

**Download the Windows Executable** (easiest option):
- Get `XCSoar-CUP-Editor.exe` from releases
- Double-click to run
- No Python installation needed!

**Or build it yourself:** See [QUICK_BUILD.md](QUICK_BUILD.md)

### For Developers

#### Requirements
- Python 3.8 or higher
- `requests` library

#### Option 1: Development Installation (Recommended)

```powershell
# Install in editable mode
pip install -e .

# Run from anywhere
xcsoar-editor
```

#### Option 2: Direct Installation

```powershell
# Install package
pip install .

# Run from anywhere
xcsoar-editor
```

#### Option 3: Run Without Installation

```powershell
# Install dependencies
pip install -r requirements.txt

# Run directly
python -m xcsoar_editor
# OR use the legacy launcher
python xcsoar_gui_editor.py
```

## Building Executable

Want to create a standalone .exe file? See these guides:

- **[QUICK_BUILD.md](QUICK_BUILD.md)** - Quick start guide for beginners
- **[BUILD_EXE.md](BUILD_EXE.md)** - Detailed build options and troubleshooting

**Quick build:**
```powershell
# Double-click build.bat, or run:
python build_exe.py
```

Your executable will be in `dist/XCSoar-CUP-Editor.exe`

## Usage

### Starting a New File
1. Click **"New"** to start with an empty waypoint list
2. You'll be prompted to save if you have unsaved changes
3. Start adding waypoints immediately

### Opening Files
1. Click **"Open CUP"** to load an existing .cup file
2. Waypoints will be displayed in the table

### Editing Waypoints
1. **Add**: Click "Add Point" to create a new waypoint
   - Enter name, latitude, and longitude in decimal degrees format
   - Example: 52.765234, 23.186700
   - Select waypoint style from dropdown
2. **Edit**: Select a waypoint and click "Edit Selected" (or double-click the row)
3. **Remove**: Select waypoint(s) and click "Remove Selected"
4. **Sort**: Click the "Name" column header to sort alphabetically

### Saving Changes
- Click **"Save"** to save to the current file
- Click **"Save As"** to save to a new file
- Changes are kept in memory until you save
- You'll be prompted if you try to close with unsaved changes

### CSV Operations
- **Import CSV**: Add waypoints from a CSV file to your current list
- **Export CSV**: Save current waypoints to a CSV file

### CSV Format
```csv
name,latitude,longitude,style
Waypoint Name,52.7652,23.18671667,1
```

## Waypoint Styles

| Code | Style                |
|------|----------------------|
| 0    | Unknown              |
| 1    | Waypoint             |
| 2    | Airfield (grass)     |
| 3    | Outlanding           |
| 4    | Gliding airfield     |
| 5    | Airfield (solid)     |
| 6    | Mountain Pass        |
| 7    | Mountain Top         |
| 8    | Transmitter Mast     |
| 9    | VOR                  |
| 10   | NDB                  |
| 11   | Cooling Tower        |
| 12   | Dam                  |
| 13   | Tunnel               |
| 14   | Bridge               |
| 15   | Power Plant          |
| 16   | Castle               |
| 17   | Intersection         |
| 18   | Marker               |
| 19   | Reporting Point      |
| 20   | PG Take Off          |
| 21   | PG Landing           |

## Keyboard Shortcuts

In Add/Edit dialogs:
- **Enter**: Save changes
- **Escape**: Cancel

## Technical Details

### Coordinate Format
- **Input**: Decimal degrees (e.g., 52.7652, 23.1867)
- **CUP Output**: DDMM.MMM format (e.g., 5245.912N, 02311.203E)

### Elevation Data
- Automatically fetched from Open-Elevation API
- Default to 0.0m if API unavailable

## Changelog

### Version 2.0 (Latest)
- ✅ Changed primary format from CSV to CUP
- ✅ Added CUP file parser for reading existing files
- ✅ Moved CSV to Import/Export functionality
- ✅ Implemented in-memory editing (no auto-save)
- ✅ Added explicit Save/Save As buttons
- ✅ Added unsaved changes warning on close
- ✅ Improved coordinate validation
- ✅ Better error handling and user feedback
- ✅ Enhanced UI with keyboard shortcuts

### Version 1.0
- Initial release with CSV-based workflow

## License

Open source - free to use and modify.
