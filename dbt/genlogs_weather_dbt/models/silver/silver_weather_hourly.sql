with raw_weather as (

    select pipeline_run_id,
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
    from {{ source('bronze', 'WEATHER_HOURLY_RAW') }}

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

    from raw_weather

)

select
        pipeline_run_id,
        --location
        location_name,
        latitude,
        longitude,

        --weather
        temperature_2m as temperature_c,
        {{ c_to_f('temperature_2m') }} as temperature_f, -- 2m temp in farenheir using macro
        case when temperature_2m < 0 then 'freezing'
            when temperature_2m between 0 and 10 then 'cold'
            when temperature_2m between 10 and 20 then 'cool'
            when temperature_2m between 20 and 30 then 'warm'
            else 'hot'
        end as temperature_band, -- temp bands for easier analysis   
        precipitation,
        precipitation_probability,
        case
            when precipitation_probability < 20 then 'low'
            when precipitation_probability < 50 then 'moderate'
            else 'high'
        end as precip_risk, -- precip risk bands for easier analysis    
        --time
        {# is_day, #}                
        forecast_hour,
        date_trunc('day', forecast_hour) as forecast_date, --individual date for easier analysis
        extract(hour from forecast_hour) as forecast_hour_of_day, -- separate individual hour for easier analysis
        case when is_day then 'day' 
            else 'night' 
        end as day_period, -- slightly more interpretable than boolean

        --metadata
        ingested_at,
        source

from deduplicated
where row_rank = 1