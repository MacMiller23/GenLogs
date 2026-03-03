import os
import snowflake.connector
from typing import Any, Dict, List


def get_snowflake_connection():
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )

def insert_weather_rows(rows: List[Dict[str, Any]]) -> None:
    """Insert a list of RAW weather data rows into Snowflake."""
    if not rows:
        return  

    conn = get_snowflake_connection()
    cursor = conn.cursor()

    try:
        # Assuming a table structure that matches the row keys; adjust as needed
        insert_query = """
            INSERT INTO WEATHER_HOURLY_RAW (
                location_name, latitude, longitude, forecast_hour,
                temperature_2m, precipitation, precipitation_probability,
                is_day, ingested_at, source
            ) VALUES (%(location_name)s, %(latitude)s, %(longitude)s, %(forecast_hour)s,
                      %(temperature_2m)s, %(precipitation)s, %(precipitation_probability)s,
                      %(is_day)s, %(ingested_at)s, %(source)s)
        """
        cursor.executemany(insert_query, rows)
        conn.commit()
    finally:
        cursor.close()
        conn.close()