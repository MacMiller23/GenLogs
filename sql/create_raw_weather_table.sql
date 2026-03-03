CREATE TABLE if not exists raw.weather_hourly (
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