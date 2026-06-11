
from pathlib import Path
import pandas as pd
import numpy as np

RAW_PATH = Path("data/raw/hotels.csv")
INTERIM_DIR = Path("data/interim")
INTERIM_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_CSV = INTERIM_DIR / "hotels_cleaned.csv"
OUTPUT_PARQUET = INTERIM_DIR / "hotels_cleaned.parquet"

MONTH_ORDER = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

EXPECTED_COLUMNS = [
    "hotel",
    "is_canceled",
    "lead_time",
    "arrival_date_year",
    "arrival_date_month",
    "arrival_date_week_number",
    "arrival_date_day_of_month",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "adults",
    "children",
    "babies",
    "meal",
    "country",
    "market_segment",
    "distribution_channel",
    "is_repeated_guest",
    "previous_cancellations",
    "previous_bookings_not_canceled",
    "reserved_room_type",
    "assigned_room_type",
    "booking_changes",
    "deposit_type",
    "agent",
    "company",
    "days_in_waiting_list",
    "customer_type",
    "adr",
    "required_car_parking_spaces",
    "total_of_special_requests",
    "reservation_status",
    "reservation_status_date"
]

TEXT_COLUMNS = [
    "hotel",
    "meal",
    "country",
    "market_segment",
    "distribution_channel",
    "deposit_type",
    "agent",
    "company",
    "customer_type",
    "reserved_room_type",
    "assigned_room_type",
    "reservation_status"
]

NUMERIC_COLUMNS = [
    "is_canceled",
    "lead_time",
    "arrival_date_year",
    "arrival_date_week_number",
    "arrival_date_day_of_month",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "adults",
    "children",
    "babies",
    "is_repeated_guest",
    "previous_cancellations",
    "previous_bookings_not_canceled",
    "booking_changes",
    "days_in_waiting_list",
    "adr",
    "required_car_parking_spaces",
    "total_of_special_requests"
]

def clean_text_value(x):
    """
    Return:
    - None for missing/blank values
    - stripped Python str for everything else
    """
    if pd.isna(x):
        return None
    s = str(x).strip()
    if s == "" or s.lower() == "nan":
        return None
    return s

def main():
    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"Raw file not found: {RAW_PATH}. Run scripts/01_download_data.py first."
        )

    df = pd.read_csv(RAW_PATH)

    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    # Convert numeric columns safely
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Normalize text columns to pure Python strings / None
    for col in TEXT_COLUMNS:
        df[col] = df[col].apply(clean_text_value)

    # Fill children for guest counting logic
    df["children"] = df["children"].fillna(0)

    # Build arrival month number
    df["arrival_month_num"] = df["arrival_date_month"].map(MONTH_ORDER)
    df["arrival_month_num"] = pd.to_numeric(df["arrival_month_num"], errors="coerce")
    df["arrival_date_year"] = pd.to_numeric(df["arrival_date_year"], errors="coerce")
    df["arrival_date_day_of_month"] = pd.to_numeric(df["arrival_date_day_of_month"], errors="coerce")

    # Build safe date string
    year_str = df["arrival_date_year"].astype("Int64").astype(str)
    month_str = df["arrival_month_num"].astype("Int64").astype(str)
    day_str = df["arrival_date_day_of_month"].astype("Int64").astype(str)

    date_str = year_str + "-" + month_str + "-" + day_str
    invalid_mask = (
        df["arrival_date_year"].isna()
        | df["arrival_month_num"].isna()
        | df["arrival_date_day_of_month"].isna()
    )
    date_str = date_str.mask(invalid_mask, None)

    df["arrival_date"] = pd.to_datetime(date_str, errors="coerce")
    df["reservation_status_date"] = pd.to_datetime(df["reservation_status_date"], errors="coerce")

    # QA flags before filling text missing values
    df["flag_missing_country"] = df["country"].isna().astype(int)
    df["flag_missing_agent"] = df["agent"].isna().astype(int)
    df["flag_missing_company"] = df["company"].isna().astype(int)
    df["flag_bad_arrival_date"] = df["arrival_date"].isna().astype(int)

    # Standardize meal values and fill key missing text
    df["meal"] = df["meal"].replace({"Undefined": "SC"})
    df["country"] = df["country"].fillna("Unknown")
    df["agent"] = df["agent"].fillna("Unknown")
    df["company"] = df["company"].fillna("Unknown")

    # Exact duplicate removal only
    df = df.drop_duplicates()

    # FINAL text normalization again to guarantee plain strings
    for col in TEXT_COLUMNS:
        df[col] = df[col].apply(clean_text_value)

    # Save CSV as primary reliable output
    df.to_csv(OUTPUT_CSV, index=False)

    # Optional: try Parquet, but don't block the project if pyarrow still complains
    try:
        parquet_df = df.copy()
        for col in TEXT_COLUMNS:
            parquet_df[col] = parquet_df[col].astype("string")
        parquet_df.to_parquet(OUTPUT_PARQUET, index=False)
        print(f"Saved cleaned CSV to: {OUTPUT_CSV}")
        print(f"Saved cleaned Parquet to: {OUTPUT_PARQUET}")
    except Exception as e:
        print(f"Saved cleaned CSV to: {OUTPUT_CSV}")
        print("Parquet save skipped due to type conversion issue:")
        print(e)

    print(f"Shape: {df.shape}")

if __name__ == "__main__":
    main()
