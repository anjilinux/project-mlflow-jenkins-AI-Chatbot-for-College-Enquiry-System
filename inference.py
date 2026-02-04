import joblib
import logging

logging.basicConfig(level=logging.INFO)

model = joblib.load("artifacts/model.pkl")
vectorizer = joblib.load("artifacts/vectorizer.pkl")

def predict_intent(text: str):
    logging.info("Inference request received")
    X = vectorizer.transform([text.lower()])
    return model.predict(X)[0]
