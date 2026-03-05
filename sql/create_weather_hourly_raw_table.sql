CREATE TABLE GENLOGS.RAW.WEATHER_HOURLY_RAW (
	pipeline_run_id STRING,
    location_name STRING,
    latitude FLOAT,
    longitude FLOAT,
    forecast_hour TIMESTAMP_NTZ,
    temperature_2m FLOAT,
    precipitation FLOAT,
    precipitation_probability FLOAT,
    is_day BOOLEAN,
    ingested_at TIMESTAMP_NTZ,
    source STRING
);