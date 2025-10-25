# XCSoar CUP Waypoint Editor

A graphical editor for XCSoar CUP waypoint files with CSV import/export capabilities.

## Features

- **Primary Format**: CUP files (.cup)
- **CSV Support**: Import/Export CSV files as secondary format
- **In-Memory Editing**: Changes only saved when you explicitly click Save
- **Unsaved Changes Protection**: Warns you before closing with unsaved changes
- **Full CRUD Operations**: Create, Read, Update, Delete waypoints
- **Automatic Elevation**: Fetches elevation data from Open-Elevation API
- **Multiple Waypoint Types**: Supports all 21 XCSoar waypoint styles

## Installation

### Requirements
- Python 3.7 or higher
- `requests` library

### Setup

```powershell
# Install dependencies
python -m pip install requests

# Run the application
python xcsoar_gui_editor.py
```

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
   - Enter name, latitude, and longitude in separate fields
   - Select waypoint style from dropdown
2. **Edit**: Select a waypoint and click "Edit Selected"
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
