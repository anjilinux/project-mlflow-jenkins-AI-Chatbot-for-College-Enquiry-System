import pandas as pd
import joblib
from sklearn.metrics import classification_report

def evaluate():
    # ROOT files only
    df = pd.read_csv("clean_data.csv")

    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")

    X = vectorizer.transform(df["question"])
    y = df["intent"]

    preds = model.predict(X)

    print("✅ Model Evaluation Report:")
    print(classification_report(y, preds))

if __name__ == "__main__":
    evaluate()
