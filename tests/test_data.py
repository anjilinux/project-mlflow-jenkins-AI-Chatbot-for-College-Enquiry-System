import os
import pandas as pd

DATA_FILE = "clean_data.csv"

def test_clean_data_exists():
    assert os.path.exists(DATA_FILE), "❌ clean_data.csv file is missing"

def test_clean_data_not_empty():
    df = pd.read_csv(DATA_FILE)
    assert not df.empty, "❌ clean_data.csv is empty"

def test_required_columns_present():
    df = pd.read_csv(DATA_FILE)
    required_columns = {"question", "intent"}

    assert required_columns.issubset(df.columns), (
        f"❌ Missing required columns: {required_columns - set(df.columns)}"
    )
