import pandas as pd
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z ]", "", text)
    return text

df = pd.read_csv("data/raw/college_faq.csv")
df["question"] = df["question"].apply(clean_text)

df.to_csv("data/processed/train.csv", index=False)
