# CUP Format Support - Full Field Implementation

## Overview

The XCSoar CUP Editor now supports **all fields** defined in the SeeYou CUP file format specification, making it a comprehensive waypoint management tool.

## Supported Fields

### Required Fields
- **Name** - Waypoint name (e.g., "Bielsk Podlaski")
- **Latitude** - Decimal degrees, -90 to 90
- **Longitude** - Decimal degrees, -180 to 180

### Optional Fields
- **Code** - Short identifier code (e.g., "EPBK" for airports)
- **Country** - 2-3 letter country code (e.g., "PL", "US", "UK")
- **Elevation** - Height in meters (auto-fetched if not provided)
- **Style** - Waypoint type (0-21, see style codes below)
- **Runway Direction** - Primary runway heading (e.g., "09/27", "36")
- **Runway Length** - Length in meters (e.g., "1200")
- **Runway Width** - Width in meters (e.g., "30")
- **Frequency** - Radio frequency in MHz (e.g., "122.500")
- **Description** - Free text description or notes

## Style Codes

The application supports all 21 waypoint styles defined in the CUP format:

| Code | Type | Description |
|------|------|-------------|
| 0 | Unknown | Unknown waypoint type |
| 1 | Waypoint | Generic waypoint |
| 2 | Airfield (grass) | Grass runway airfield |
| 3 | Outlanding | Emergency landing site |
| 4 | Gliding airfield | Glider-specific airfield |
| 5 | Airfield (solid) | Paved runway airfield |
| 6 | Mountain Pass | Geographic mountain pass |
| 7 | Mountain Top | Mountain summit |
| 8 | Transmitter Mast | Radio/TV transmission tower |
| 9 | VOR | VHF Omnidirectional Range |
| 10 | NDB | Non-Directional Beacon |
| 11 | Cooling Tower | Power plant cooling tower |
| 12 | Dam | Water dam structure |
| 13 | Tunnel | Road or rail tunnel |
| 14 | Bridge | Major bridge |
| 15 | Power Plant | Power generation facility |
| 16 | Castle | Historic castle or fortress |
| 17 | Intersection | Road or airway intersection |
| 18 | Marker | Location marker |
| 19 | Reporting Point | ATC reporting point |
| 20 | PG Take Off | Paragliding launch site |
| 21 | PG Landing | Paragliding landing zone |

## Enhanced Dialog Interface

The waypoint dialog now features a **3-tab interface**:

### Tab 1: Basic Info
- Name * (required)
- Code (optional identifier)
- Country (2-letter code)
- Latitude * (decimal degrees)
- Longitude * (decimal degrees)
- Elevation (meters, auto-fetched if empty)
- Style (waypoint type)

### Tab 2: Airfield Info
For airports and landing sites:
- Runway Direction (e.g., "09/27")
- Runway Length (meters)
- Runway Width (meters)
- Radio Frequency (MHz)

### Tab 3: Details
- Description (multi-line text field for notes)

## Field Validation

The application includes comprehensive validation:

### Coordinate Validation
- Latitude: -90 to 90 degrees
- Longitude: -180 to 180 degrees

### Style Validation
- Must be integer 0-21

### Country Code Validation
- 2-3 characters maximum
- Automatically converted to uppercase

### Runway Direction Validation
- Only digits and "/" allowed
- Common formats: "09", "27", "09/27", "180"

### Numeric Field Validation
- Runway length/width must be numeric
- Allows optional "m" suffix (e.g., "1200m")

### Frequency Validation
- Must be numeric
- Typical range: 100.0-150.0 MHz (aviation band)
- Format: "122.500"

## Enhanced Tree View

The main window now displays **8 columns**:

1. **Name** - Waypoint name
2. **Code** - Short identifier
3. **Country** - Country code
4. **Latitude** - Decimal degrees (6 decimals)
5. **Longitude** - Decimal degrees (6 decimals)
6. **Elevation** - Height in meters
7. **Type** - Human-readable style name
8. **Airfield** - ✓ marker if has runway/frequency data

## CSV Export/Import

CSV files now include **all 12 fields**:

```csv
name,code,country,latitude,longitude,elevation,style,runway_direction,runway_length,runway_width,frequency,description
"EPBK",,PL,52.765234,23.186700,140.0,5,"09/27","1200","30","122.500","Bielsk Podlaski Airfield"
```

Benefits:
- Complete data preservation
- Easy spreadsheet editing
- Bulk waypoint management
- Data analysis capabilities

## CUP File Format

Output CUP files follow the standard format:

```
name,code,country,lat,lon,elev,style,rwdir,rwlen,rwwidth,freq,desc
"Bielsk Podlaski",,PL,5245.91404N,02311.20404E,140.0m,1,,,,"","Waypoint: Bielsk Podlaski"
```

### Coordinate Format
- Latitude: DDMM.MMMMMN/S (5 decimal places for minutes)
- Longitude: DDDMM.MMMMMN/S (5 decimal places for minutes)
- High precision preserves accuracy

### Field Formatting
- Names and descriptions are quoted
- Code and country are unquoted
- Elevation includes "m" suffix
- Empty fields are preserved as empty

## Usage Examples

### Adding a Simple Waypoint
```
Name: Home
Latitude: 52.765234
Longitude: 23.186700
Style: Waypoint
```

### Adding an Airfield
```
Basic Info:
  Name: Bielsk Podlaski
  Code: EPBK
  Country: PL
  Latitude: 52.765234
  Longitude: 23.186700
  Elevation: 140
  Style: Airfield (solid)

Airfield Info:
  Runway Direction: 09/27
  Runway Length: 1200
  Runway Width: 30
  Frequency: 122.500

Details:
  Description: Main airfield for the region
```

### Adding a Mountain Top
```
Name: Mount Example
Latitude: 52.5
Longitude: 23.5
Elevation: 1250
Style: Mountain Top
Description: Popular gliding thermal spot
```

## Data Preservation

When opening existing CUP files:
- ✓ All fields are preserved
- ✓ Descriptions maintained
- ✓ Runway information retained
- ✓ Frequency data kept
- ✓ Country codes preserved
- ✓ Elevation values retained

## API Integration

### Elevation Data
If elevation is not provided:
- Automatically fetched from Open-Elevation API
- Happens during save operation
- Can be disabled in code if needed

## Best Practices

### For Airfields
Always include:
- Code (ICAO/local identifier)
- Country
- Runway direction
- Runway length
- Frequency (if applicable)
- Accurate elevation

### For Waypoints
Minimum required:
- Name
- Latitude
- Longitude
- Appropriate style

Optional but recommended:
- Country
- Elevation
- Description

### Data Entry Tips
1. **Coordinates**: Use decimal degrees (e.g., 52.765234, not 52° 45' 54.84")
2. **Country Codes**: Use ISO 3166-1 alpha-2 (PL, US, GB, DE, etc.)
3. **Runway Direction**: Use magnetic heading (e.g., "09/27" not "090/270")
4. **Frequencies**: Use standard format with 3 decimals (e.g., "122.500")
5. **Descriptions**: Keep concise but informative

## Compatibility

- ✓ Fully compatible with SeeYou CUP format
- ✓ Backward compatible with older CUP files
- ✓ Forward compatible with extended fields
- ✓ Compatible with XCSoar
- ✓ Compatible with LK8000
- ✓ Compatible with other CUP-supporting software

## Migration from Previous Version

### Existing Files
Old CUP files with limited fields will:
- Load correctly
- Show empty fields as blank
- Preserve existing data
- Allow adding new field data

### Backward Compatibility
Files saved with new fields:
- Work with old software (ignores extra fields)
- Maintain CUP format standard
- Preserve all data for future use

## Performance

- Fast loading of large waypoint databases
- Efficient parsing of all fields
- Quick save operations
- Responsive UI even with 1000+ waypoints

## Known Limitations

- Elevation fetch requires internet connection
- API has rate limits (usually not an issue)
- Very large descriptions may be truncated in display
- Some legacy CUP variants may have slight format differences

## Future Enhancements

Potential additions:
- Custom fields support
- Waypoint photos/attachments
- GPS coordinate import from file
- Batch elevation fetch
- Advanced filtering by field values
- Export to other formats (GPX, KML)
