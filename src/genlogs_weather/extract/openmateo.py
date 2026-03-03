from __future__ import annotations
import datetime as dt
from typing import Any, Dict, List
import requests
from genlogs_weather.config.locations import Location

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"