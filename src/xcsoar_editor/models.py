"""Data models for waypoints."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Waypoint:
    """
    Represents a waypoint with all SeeYou CUP format fields.
    
    CUP Format Fields:
    - name: Waypoint name (required)
    - code: Short code/identifier (optional, e.g., "EPBK" for airports)
    - country: 2-letter country code (optional, e.g., "PL", "US")
    - latitude: Decimal degrees, positive = North, negative = South (required)
    - longitude: Decimal degrees, positive = East, negative = West (required)
    - elevation: Elevation in meters (optional, can be fetched from API)
    - style: Waypoint style/type code 0-21 (default: 1 = Waypoint)
    - runway_direction: Primary runway direction in degrees (optional, e.g., "09/27")
    - runway_length: Runway length in meters (optional, e.g., "1200")
    - runway_width: Runway width in meters (optional, e.g., "30")
    - frequency: Radio frequency in MHz (optional, e.g., "122.500")
    - description: Free text description (optional)
    """
    
    # Required fields
    name: str
    latitude: float
    longitude: float
    
    # Optional fields with defaults
    code: str = ""
    country: str = ""
    elevation: Optional[float] = None
    style: int = 1
    runway_direction: str = ""
    runway_length: str = ""
    runway_width: str = ""
    frequency: str = ""
    description: str = ""
    
    def __post_init__(self):
        """Validate waypoint data after initialization."""
        if not self.name or not self.name.strip():
            raise ValueError("Waypoint name cannot be empty")
        
        # Validate coordinates
        if not (-90 <= self.latitude <= 90):
            raise ValueError(f"Latitude {self.latitude} must be between -90 and 90")
        if not (-180 <= self.longitude <= 180):
            raise ValueError(f"Longitude {self.longitude} must be between -180 and 180")
        
        # Validate style code
        if not (0 <= self.style <= 21):
            raise ValueError(f"Style {self.style} must be between 0 and 21")
        
        # Validate country code if provided
        if self.country and len(self.country) > 3:
            raise ValueError(f"Country code '{self.country}' should be 2-3 characters (e.g., 'PL', 'US')")
        
        # Validate runway direction format if provided
        if self.runway_direction:
            self.runway_direction = self.runway_direction.strip()
            # Common formats: "09", "09/27", "90", etc.
            if self.runway_direction and not all(c.isdigit() or c == '/' for c in self.runway_direction):
                raise ValueError(f"Runway direction '{self.runway_direction}' should contain only digits and '/'")
        
        # Validate numeric fields if provided
        if self.runway_length:
            self.runway_length = self.runway_length.strip()
            try:
                if self.runway_length:
                    float(self.runway_length.rstrip('m'))  # Allow "1200" or "1200m"
            except ValueError:
                raise ValueError(f"Runway length '{self.runway_length}' must be numeric")
        
        if self.runway_width:
            self.runway_width = self.runway_width.strip()
            try:
                if self.runway_width:
                    float(self.runway_width.rstrip('m'))
            except ValueError:
                raise ValueError(f"Runway width '{self.runway_width}' must be numeric")
        
        # Validate frequency format if provided
        if self.frequency:
            self.frequency = self.frequency.strip()
            # Only validate if it looks like a numeric frequency
            # Skip validation for text descriptions that might be in this field
            if self.frequency and self.frequency.replace('.', '').replace(',', '').isdigit():
                try:
                    freq_val = float(self.frequency.replace(',', '.'))
                    # Only warn if outside typical range, but don't fail
                    if not (100.0 <= freq_val <= 150.0):
                        print(f"Warning: Frequency {freq_val} outside typical aviation range (100-150 MHz)")
                except ValueError:
                    pass  # Not a valid number, but that's okay - might be descriptive text
    
    def to_dict(self) -> dict:
        """Convert waypoint to dictionary format."""
        return {
            'name': self.name,
            'code': self.code,
            'country': self.country,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'elevation': self.elevation,
            'style': self.style,
            'runway_direction': self.runway_direction,
            'runway_length': self.runway_length,
            'runway_width': self.runway_width,
            'frequency': self.frequency,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Waypoint':
        """Create waypoint from dictionary format."""
        return cls(
            name=data.get('name', ''),
            latitude=float(data.get('latitude', 0.0)),
            longitude=float(data.get('longitude', 0.0)),
            code=data.get('code', ''),
            country=data.get('country', ''),
            elevation=float(data['elevation']) if data.get('elevation') else None,
            style=int(data.get('style', 1)),
            runway_direction=data.get('runway_direction', ''),
            runway_length=data.get('runway_length', ''),
            runway_width=data.get('runway_width', ''),
            frequency=data.get('frequency', ''),
            description=data.get('description', '')
        )
    
    @property
    def is_airfield(self) -> bool:
        """Check if this waypoint is an airfield (has runway information)."""
        return bool(self.runway_direction or self.runway_length or self.frequency)
    
    @property
    def short_description(self) -> str:
        """Get a short description for display."""
        if self.description:
            return self.description[:50] + ('...' if len(self.description) > 50 else '')
        return ""
