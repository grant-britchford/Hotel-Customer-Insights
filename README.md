# Hotel Customer & Insights Analysis

## Overview

This project analyses hotel behaviour using the public Hotel Booking Demand dataset.
It covers customer mix, cancellations, seasonality, and commercial/operational insight proxies, and ends with a Power BI dashboard.

## Data

- https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2020/2020-02-11/hotels.csv
- https://rfordatascience.github.io/tidytuesday/data/2020/2020-02-11/readme.html
- https://doaj.org/article/a8490350a5e74c5f94d7e3e531fbdf75

## Objectives

- Understand customer composition & booking behaviour
- Measure cancellation & no-show patterns
- Analyse seasonality & demand trends
- Build a business decision-making dashboard

## Technology Stack

- Python (Pandas/Numpy/Jupyter Notebook/Matplotlib/Seaborn/Plotly)
- Power BI Desktop
- GitHub

## Setup

1. python -m venv .venv
2. source .venv/bin/activate
3. pip freeze > requirements.txt

## Run Order

1. python scripts/01_download_data.py
2. python scripts/02_clean_data.py
3. python scripts/03_feature_engineering.py
4. python scripts/04_aggregate_outputs.py
5. python scripts/05_quality_checks.py
6. python scripts/06_run_sql_checks.py

## Dashboard Pages

1. Executive Overview
2. Customer Insights
3. Cancellation Insights
4. Demand & Seasonality
5. Operational Insights
