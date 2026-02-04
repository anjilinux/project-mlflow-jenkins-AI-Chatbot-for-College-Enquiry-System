from fastapi import FastAPI
import joblib

app = FastAPI(title="AI College Enquiry Chatbot")

# Load artifacts once at startup
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(payload: dict):
    question = payload.get("question")

    if not question:
        return {"error": "Question is required"}

    X = vectorizer.transform([question.lower().strip()])
    prediction = model.predict(X)[0]

    return {"intent": prediction}
