
from pathlib import Path
import pandas as pd

RAW_URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2020/2020-02-11/hotels.csv"
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = RAW_DIR / "hotels.csv"

def main():
    df = pd.read_csv(RAW_URL)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved raw dataset to: {OUTPUT_PATH}")
    print(f"Shape: {df.shape}")

if __name__ == "__main__":
    main()
