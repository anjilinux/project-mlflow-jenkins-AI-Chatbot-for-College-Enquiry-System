import pandas as pd
import joblib
from sklearn.metrics import classification_report

df = pd.read_csv("data/processed/clean_data.csv")

model = joblib.load("artifacts/model.pkl")
vectorizer = joblib.load("artifacts/vectorizer.pkl")

X = vectorizer.transform(df["question"])
y = df["intent"]

preds = model.predict(X)

print(classification_report(y, preds))
