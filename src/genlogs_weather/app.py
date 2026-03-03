# src/genlogs_weather/app.py
from __future__ import annotations
import logging
import os
from dotenv import load_dotenv
from genlogs_weather.config.locations import LOCATIONS #config/locations.py 

# Load .env for secure configs
load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper() #Default to INFO if not set; allows override via environment variable

# Configure logging with a standard format and level set by LOG_LEVEL environment variable
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s", # Log format: timestamp, log level, logger name, and message
)
logger = logging.getLogger("genlogs_weather")