# src/genlogs_weather/app.py
from __future__ import annotations
import logging
import os
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import List, Tuple

# Load .env for secure configs
load_dotenv()