from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

@dataclass(frozen=True)
class Location:
    """Represents fixed locations for each location, 4 decimal places gives 10m precision, which should be more than enough.
    In the real world, this would probably come from a metadata table
    """
    name: str
    lat: float
    lon: float

# Source: known public coordinates for each location; got from google. treated as configuration inputs to Open-Meteo.
LOCATIONS: List[Location] = [
    Location("Atlanta, GA", 33.7490, -84.3880),
    Location("New York, NY", 40.7128, -74.0060),
    Location("Washington, DC", 38.9072, -77.0369),
    Location("San Francisco, CA", 37.7749, -122.4194),
    Location("Daniel Boone National Forest, KY", 37.5952, -83.5243),
]