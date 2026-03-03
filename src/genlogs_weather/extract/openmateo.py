from __future__ import annotations
import datetime as dt
import json
from typing import Any, Dict, List
import requests
from genlogs_weather.config.locations import Location

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_hourly_weather_rows(location: Location) -> List[Dict[str, Any]]:
    """
    Fetch hourly weather data for a single location and return row-shaped records:
    one row per (location, forecast_hour).

    Requirements mapping:
    - Include: temperature, precipitation, precipitation_probability, is_day
    - Ingest: 24 hours of history + next 1 hour of forecast
    """
    params = {
        "latitude": location.lat,
        "longitude": location.lon,
        # Request the required hourly fields
        "hourly": "temperature_2m,precipitation,precipitation_probability,is_day",
        # Request a window that includes recent history + near-term forecast
        # Using relative days keeps it repeatable without hardcoding dates.
        "past_days": 1,
        "forecast_days": 1,
        # Keep output in a consistent timezone for storage; UTC is simplest for pipelines.
        "timezone": "UTC",
    }

    response = requests.get(OPEN_METEO_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    
    hourly = payload.get("hourly") or {}
    times = hourly.get("time") or []
    temps = hourly.get("temperature_2m") or []
    precip = hourly.get("precipitation") or []
    precip_prob = hourly.get("precipitation_probability") or []
    is_day = hourly.get("is_day") or []

    n = len(times) # num hourly values returned; should be same for all
    if not all(len(arr) == n for arr in [temps, precip, precip_prob, is_day]):
        raise ValueError(
            f"Hourly arrays length mismatch for {location.name}: "
            f"time={len(times)}, temp={len(temps)}, precip={len(precip)}, "
            f"precip_prob={len(precip_prob)}, is_day={len(is_day)}"
        )