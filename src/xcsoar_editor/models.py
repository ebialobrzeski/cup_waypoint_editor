"""Data models for waypoints."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Waypoint:
    """Represents a waypoint with coordinates and metadata."""
    
    name: str
    latitude: float
    longitude: float
    style: int = 1
    code: str = ""
    country: str = "PL"
    elevation: Optional[float] = None
    runway_direction: str = ""
    runway_length: str = ""
    runway_width: str = ""
    frequency: str = ""
    description: str = ""
    
    def __post_init__(self):
        """Validate waypoint data after initialization."""
        if not self.name:
            raise ValueError("Waypoint name cannot be empty")
        if not (-90 <= self.latitude <= 90):
            raise ValueError(f"Latitude {self.latitude} must be between -90 and 90")
        if not (-180 <= self.longitude <= 180):
            raise ValueError(f"Longitude {self.longitude} must be between -180 and 180")
    
    def to_dict(self) -> dict:
        """Convert waypoint to dictionary format."""
        return {
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'style': self.style,
            'code': self.code,
            'country': self.country,
            'elevation': self.elevation,
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
            style=int(data.get('style', 1)),
            code=data.get('code', ''),
            country=data.get('country', 'PL'),
            elevation=float(data['elevation']) if data.get('elevation') else None,
            runway_direction=data.get('runway_direction', ''),
            runway_length=data.get('runway_length', ''),
            runway_width=data.get('runway_width', ''),
            frequency=data.get('frequency', ''),
            description=data.get('description', '')
        )
