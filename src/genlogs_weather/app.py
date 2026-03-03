# src/genlogs_weather/app.py
from __future__ import annotations
import logging
import os
from dotenv import load_dotenv
from genlogs_weather.config.locations import LOCATIONS #config/locations.py
from genlogs_weather.extract.openmateo import fetch_hourly_weather_rows #extract/openmateo.py

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
    logger.info("Starting genlogs weather ingestion job")
    logger.debug("LOG_LEVEL=%s", LOG_LEVEL)

    logger.info("Target locations (defined in config/locations.py):")
    for loc in LOCATIONS:
        logger.info(" - %s (lat=%s, lon=%s)", loc.name, loc.lat, loc.lon)

    logger.info("Skeleton run complete — extraction not yet implemented")


if __name__ == "__main__":
    rows = fetch_hourly_weather_rows(LOCATIONS[0])
    logger.info(f"Rows returned: {len(rows)}")
    main()