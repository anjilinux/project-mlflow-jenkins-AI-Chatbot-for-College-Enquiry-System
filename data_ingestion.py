import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)

RAW_PATH = "data/raw/college_faq.csv"
PROCESSED_PATH = "data/processed/clean_data.csv"

def ingest_data():
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError("Raw data not found")

    df = pd.read_csv(RAW_PATH)

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    logging.info("Data ingestion successful")

if __name__ == "__main__":
    ingest_data()
