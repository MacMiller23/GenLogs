from __future__ import annotations # allows for using the class name 'Location' in type hints within the class definition itself
from dataclasses import dataclass  # auto generates  __init__() and __repr__() for classes.  use here to define a simple class for locations, makes code cleaner
from typing import List, Tuple     # not strictly needed, but can be helpful for type hinting lists of tuples, which is what we use for locations in this project

@dataclass(frozen=True) # Data shouldn't change after creation
class Location:
    """Represents fixed locations for each location, 4 decimal places gives 10m precision, which should be more than enough.
    In the real world, this would probably come from a metadata table
    """
    name: str
    lat: float
    lon: float

# Known public coordinates for each location; got from google
# in a PROD scenario, these would likely come from a metadata table instead of being hardcoded in the codebase
LOCATIONS: List[Location] = [
    Location("Atlanta, GA", 33.7490, -84.3880),
    Location("New York, NY", 40.7128, -74.0060),
    Location("Washington, DC", 38.9072, -77.0369),
    Location("San Francisco, CA", 37.7749, -122.4194),
    Location("Daniel Boone National Forest, KY", 37.0210, -84.2873), # went to google maps, clicked on Daniel Boone National Forest, and got the coordinates from the URL
]