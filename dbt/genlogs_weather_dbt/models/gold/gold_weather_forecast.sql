{{ config(
    materialized='incremental',
    unique_key=['location_name','forecast_hour'],
    incremental_strategy='merge'
) }}

select
    location_name,
    latitude,
    longitude,
    day_period,
    temperature_c,
    temperature_f,
    temperature_band,
    precipitation,
    precipitation_probability,
    precip_risk,
    forecast_hour_of_day,
    forecast_hour,
    forecast_date,
    ingested_at

from {{ ref('silver_weather_hourly') }}

{% if is_incremental() %}

where forecast_hour >
(
    select coalesce(max(forecast_hour), to_timestamp('1900-01-01'))
    from {{ this }}
)

{% endif %}