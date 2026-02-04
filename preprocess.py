import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def preprocess():
    df = pd.read_csv("college_faq.csv")

    required_cols = {"question", "intent"}
    if not required_cols.issubset(df.columns):
        raise ValueError("❌ Invalid schema")

    df["question"] = df["question"].str.lower().str.strip()
    df.dropna(inplace=True)

    df.to_csv("clean_data.csv", index=False)
    logging.info("✅ clean_data.csv created")

if __name__ == "__main__":
    preprocess()
