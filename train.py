import mlflow
import mlflow.sklearn
import pandas as pd
import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from src.features.feature_engineering import vectorize

mlflow.set_experiment("College_Chatbot")

df = pd.read_csv("data/processed/train.csv")

X = vectorize(df["question"])
y = df["intent"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

with mlflow.start_run():
    model = LogisticRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "model")

    with open("artifacts/model.pkl", "wb") as f:
        pickle.dump(model, f)
