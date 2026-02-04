import pandas as pd

df = pd.read_csv("data/processed/clean_data.csv")

print("Dataset Shape:", df.shape)
print("\nIntent Distribution:\n", df["intent"].value_counts())
