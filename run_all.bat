cd src
uv run -m genlogs_weather.run_pipeline
cd ..\dbt\genlogs_weather_dbt
dbt run