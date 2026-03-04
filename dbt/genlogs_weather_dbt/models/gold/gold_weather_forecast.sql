{{ config(
    materialized='incremental',
    unique_key=['location_name','forecast_hour'],
    incremental_strategy='merge'
) }}

select
    location_name,
    latitude,
    longitude,
    forecast_hour,
    temperature_2m as temperature,
    precipitation,
    precipitation_probability,
    is_day,
    ingested_at

from {{ ref('silver_weather_hourly') }}

{% if is_incremental() %}

where ingested_at >
(
    select coalesce(max(ingested_at), to_timestamp('1900-01-01'))
    from {{ this }}
)

{% endif %}