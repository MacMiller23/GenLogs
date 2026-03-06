# OpenMateo -> Snowflake -> DBT pipeline

_GenLogs Sr. Data Engineering Technical Takehome Assessment  (3.6.2026)_

<h1> Project Summary</h1>

This project implements an ELT data pipeline that retrieves hourly weather forecast data from the Open-Meteo API, loads the raw data into Snowflake via a python loader, and transforms it into an analytics-ready model using dbt.

<h2>Data Ingestion</h2>

Weather data is collected using a Python pipeline that calls the Open-Meteo API.
The pipeline includes retry logic for reliability and uses batch inserts (executemany) to efficiently load records into Snowflake.

<h2>Data Storage</h2>

Raw API responses are stored in a Snowflake raw table, preserving the source data while adding metadata such as pipeline run identifiers and ingestion timestamps.

<h2>Data Transformation</h2>

Transformations are handled with dbt using a medallion architecture:

<h3><u>Bronze</h3></u> Defines the raw Snowflake table as a dbt source and enforces data freshness checks.

<h3><u>Silver</h3></u>Cleans and standardizes the data, deduplicates records, and adds derived fields such as temperature conversions and day/night indicators.

<h3><u>Gold</h3></u> Produces the final analytics-ready weather forecast model.

<h2>Incremental Modeling</h2>

The Gold model is implemented as an incremental table with a merge strategy, allowing new forecast data to be inserted while updating existing rows if forecasts change.

<h2>Data Quality</h2>

dbt tests enforce the dataset grain of 1 row per location per forecast hour.
This ensures the final dataset remains clean, consistent, and ready for analysis.
