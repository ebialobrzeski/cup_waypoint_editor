"""File I/O operations for CUP and CSV formats."""

import csv
import requests
from typing import List
from pathlib import Path

from .models import Waypoint
from .utils import ddmm_to_deg, deg_to_ddmm
from .config import STYLE_OPTIONS, ELEVATION_API_URL, ELEVATION_API_TIMEOUT


def get_elevation(lat: float, lon: float) -> float:
    """
    Fetch elevation data from open-elevation API.
    
    Args:
        lat: Latitude in decimal degrees
        lon: Longitude in decimal degrees
        
    Returns:
        Elevation in meters, or 0.0 if fetch fails
    """
    try:
        resp = requests.get(
            ELEVATION_API_URL,
            params={"locations": f"{lat},{lon}"},
            timeout=ELEVATION_API_TIMEOUT
        )
        return resp.json()['results'][0]['elevation']
    except Exception as e:
        print(f"Elevation fetch error for {lat}, {lon}: {e}")
        return 0.0


def parse_cup_file(filepath: str) -> List[Waypoint]:
    """
    Parse a CUP file and return list of Waypoint objects.
    
    Args:
        filepath: Path to the CUP file
        
    Returns:
        List of Waypoint objects
    """
    waypoints = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Skip header line
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        
        # Parse CSV line respecting quoted fields
        parts = []
        current = []
        in_quotes = False
        
        for char in line:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                parts.append(''.join(current).strip().strip('"'))
                current = []
            else:
                current.append(char)
        parts.append(''.join(current).strip().strip('"'))
        
        # Ensure we have enough fields
        while len(parts) < 12:
            parts.append('')
        
        name, code, country, lat_str, lon_str, elev_str, style_str, rwdir, rwlen, rwwidth, freq, desc = parts[:12]
        
        try:
            lat = ddmm_to_deg(lat_str)
            lon = ddmm_to_deg(lon_str)
            style = int(style_str) if style_str else 1
            
            # Parse elevation
            elev = None
            if elev_str:
                # Remove 'm' suffix if present
                elev_str = elev_str.rstrip('m')
                try:
                    elev = float(elev_str)
                except ValueError:
                    pass
            
            waypoint = Waypoint(
                name=name,
                latitude=lat,
                longitude=lon,
                style=style,
                code=code,
                country=country,
                elevation=elev,
                runway_direction=rwdir,
                runway_length=rwlen,
                runway_width=rwwidth,
                frequency=freq,
                description=desc
            )
            waypoints.append(waypoint)
        except Exception as e:
            print(f"Error parsing line: {line}\nError: {e}")
            continue
    
    return waypoints


def write_cup_file(filepath: str, waypoints: List[Waypoint], fetch_elevation: bool = True) -> None:
    """
    Write waypoints to CUP file format.
    
    Args:
        filepath: Path to save the CUP file
        waypoints: List of Waypoint objects to save
        fetch_elevation: Whether to fetch elevation from API if not present
    """
    rows = ["name,code,country,lat,lon,elev,style,rwdir,rwlen,rwwidth,freq,desc"]
    
    for waypoint in waypoints:
        # Get or fetch elevation
        if waypoint.elevation is not None:
            elev = waypoint.elevation
        elif fetch_elevation:
            elev = get_elevation(waypoint.latitude, waypoint.longitude)
        else:
            elev = 0.0
        
        # Generate description if not provided
        desc = waypoint.description
        if not desc:
            style_name = STYLE_OPTIONS.get(waypoint.style, 'Point')
            desc = f"{style_name}: {waypoint.name}"
        
        # Convert coordinates to DDMM format
        lat_str = deg_to_ddmm(waypoint.latitude, True)
        lon_str = deg_to_ddmm(waypoint.longitude, False)
        
        # Build row
        row = f'"{waypoint.name}",{waypoint.code},{waypoint.country},{lat_str},{lon_str},{elev:.1f}m,{waypoint.style},{waypoint.runway_direction},{waypoint.runway_length},{waypoint.runway_width},"{waypoint.frequency}","{desc}"'
        rows.append(row)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(rows))


def parse_csv_file(filepath: str) -> List[Waypoint]:
    """
    Parse a CSV file and return list of Waypoint objects.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        List of Waypoint objects
    """
    waypoints = []
    
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                waypoint = Waypoint(
                    name=row.get('name', ''),
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude']),
                    style=int(row.get('style', 1))
                )
                waypoints.append(waypoint)
            except (ValueError, KeyError) as e:
                print(f"Skipping invalid CSV row: {row}, Error: {e}")
                continue
    
    return waypoints


def write_csv_file(filepath: str, waypoints: List[Waypoint]) -> None:
    """
    Write waypoints to CSV file.
    
    Args:
        filepath: Path to save the CSV file
        waypoints: List of Waypoint objects to save
    """
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'latitude', 'longitude', 'style']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for waypoint in waypoints:
            writer.writerow({
                'name': waypoint.name,
                'latitude': waypoint.latitude,
                'longitude': waypoint.longitude,
                'style': waypoint.style
            })
