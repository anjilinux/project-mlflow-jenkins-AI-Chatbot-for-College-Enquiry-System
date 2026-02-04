import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import mlflow
import mlflow.sklearn

def train():
    df = pd.read_csv("clean_data.csv")

    X = df["question"]
    y = df["intent"]

    vectorizer = TfidfVectorizer()
    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_vec, y)

    joblib.dump(model, "model.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")

    mlflow.log_artifact("model.pkl")
    mlflow.log_artifact("vectorizer.pkl")

    print("✅ Model trained successfully")

if __name__ == "__main__":
    train()
