# Snowflake Native Python ETL Pipeline

Demonstrates an end-to-end data pipeline that ingests raw CSV datasets, cleans and transforms fields using native Python, and efficiently loads records into Snowflake staging tables using `snowflake-connector-python`.

## Features
* Ingestion of raw source data via standard Python (`csv` module)
* Data transformation and schema standardization (capitalization, data cleaning)
* Batch parameter insertion into Snowflake staging tables

## Tech Stack
* **Language:** Python 3.9+
* **Database / Warehouse:** Snowflake
* **Library:** `snowflake-connector-python`
