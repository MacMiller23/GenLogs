from __future__ import annotations
import datetime as dt
import time
from typing import Any, Dict, List
import requests
import csv
from pathlib import Path
from genlogs_weather.config.locations import Location #pass to use the Location class defined in config/locations.py for type hinting

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_hourly_weather_rows(location: Location, pipeline_run_id: str) -> List[Dict[str, Any]]: 
    """
        Fetch hourly weather data for a single location and return row-shaped records:
        one row per (location, forecast_hour).

        Requirements mapping per prompt:
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
        # Keep output in a consistent timezone for storage; UTC is simplest for pipelines becuase 
        "timezone": "UTC",
    }

    last_err: Exception | None = None
    for attempt in range(3):
        try:
            resp = requests.get(OPEN_METEO_URL, params=params, timeout=30)
            resp.raise_for_status()
            payload = resp.json()
            break
        except requests.RequestException as e:
            last_err = e
            time.sleep(1)  # simple backoff for transient network/HTTP issues
    else:
        raise RuntimeError(f"Open-Meteo request failed for {location.name}") from last_err
    hourly = payload.get("hourly") or {}
    times = hourly.get("time") or []
    temps = hourly.get("temperature_2m") or []
    precip = hourly.get("precipitation") or []
    precip_prob = hourly.get("precipitation_probability") or []
    is_day = hourly.get("is_day") or []

    n = len(times) # num hourly values returned; should be same for all
    if not all(len(arr) == n for arr in [temps, precip, precip_prob, is_day]): # account for potential API changes or issues where some fields might be missing values
        raise ValueError(
            f"Hourly arrays length mismatch for {location.name}: "
            f"time={len(times)}, temp={len(temps)}, precip={len(precip)}, "
            f"precip_prob={len(precip_prob)}, is_day={len(is_day)}"
        )

    # define time window for filtering: last 24 hours + next 1 hour from now, per prompt requirements
    now_utc = dt.datetime.now(dt.timezone.utc) # define current time
    window_start = now_utc - dt.timedelta(hours=24) # 24 hours ago
    window_end = now_utc + dt.timedelta(hours=1) # 1 hour from now

    rows: List[Dict[str, Any]] = [] # will hold the final row-shaped records
    ingested_at = now_utc.isoformat() # timestamp for when data was ingested

    for i, t in enumerate(times):
        ts = dt.datetime.fromisoformat(t).replace(tzinfo=dt.timezone.utc)
        if window_start <= ts <= window_end:
            rows.append(
                {
                    "pipeline_run_id": pipeline_run_id,
                    "location_name": location.name,
                    "latitude": location.lat,
                    "longitude": location.lon,
                    "forecast_hour": ts.isoformat(),
                    "temperature_2m": temps[i],
                    "precipitation": precip[i],
                    "precipitation_probability": precip_prob[i],
                    "is_day": is_day[i],
                    "ingested_at": ingested_at,
                    "source": "open-meteo",
                }
            )

    return rows
def export_rows_to_csv(rows: List[Dict[str, Any]], filepath: str) -> None:
    """
    Export extracted weather rows to a CSV file.
    Useful for testing Snowflake COPY INTO loading.
    """
    if not rows:
        print("No rows to export.")
        return

    # Ensure directory exists
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exported {len(rows)} rows to {filepath}")