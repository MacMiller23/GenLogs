from __future__ import annotations
import logging
import os
from dotenv import load_dotenv
import uuid # unique python run ID when loading into snowflake
from genlogs_weather.config.locations import LOCATIONS #config/locations.py
from genlogs_weather.extract.openmateo import fetch_hourly_weather_rows #extract/openmateo.py
from genlogs_weather.load.snowflake_loader import insert_weather_rows #load/snowflake_loader.py

# Load .env for secure configs
load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper() #Default to INFO if not set; allows override via environment variable

# Configure logging with a standard format and level set by LOG_LEVEL environment variable
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s", # Log format: timestamp, log level, logger name, and message
)
logger = logging.getLogger("genlogs_weather")

def main() -> None:
    """Orchestrates the job. Keeps API + Snowflake logic in helper modules."""
    pipeline_run_id = str(uuid.uuid4()) # Generate a unique ID for this pipeline run
    logger.info("Starting genlogs weather ingestion job")
    logger.debug("LOG_LEVEL=%s", LOG_LEVEL)
    logger.debug("pipeline_run_id=%s", pipeline_run_id)
    logger.info("Target locations:")
    for loc in LOCATIONS:
        logger.info(" - %s (lat=%s, lon=%s)", loc.name, loc.lat, loc.lon)

    # For initial skeleton, just test the Open-Meteo extraction for the first location and log the number of rows returned.
    all_rows = []

    for loc in LOCATIONS:
        rows = fetch_hourly_weather_rows(loc, pipeline_run_id)
        logger.info("Extracted %s rows for %s", len(rows), loc.name)
        all_rows.extend(rows)
    logger.info("Total rows extracted across all locations: %s", len(all_rows))

    insert_weather_rows(all_rows)

    logger.info("Loaded %s rows into Snowflake", len(all_rows))

if __name__ == "__main__":
    main()