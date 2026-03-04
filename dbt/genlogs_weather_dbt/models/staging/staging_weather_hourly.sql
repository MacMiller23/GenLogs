with source as (

    select *
    from {{ source('raw', 'WEATHER_HOURLY_RAW') }}

),

deduplicated as (

    select
        pipeline_run_id,
        location_name,
        latitude,
        longitude,
        forecast_hour,
        temperature_2m,
        precipitation,
        precipitation_probability,
        is_day,
        ingested_at,
        source,

        row_number() over (
            partition by location_name, forecast_hour
            order by ingested_at desc
        ) as row_rank

    from source

)

select
    pipeline_run_id,
    location_name,
    latitude,
    longitude,
    forecast_hour,
    temperature_2m,
    precipitation,
    precipitation_probability,
    is_day,
    ingested_at,
    source

from deduplicated
where row_rank = 1