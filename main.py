from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

class Question(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: Question):
    X = vectorizer.transform([data.question])
    intent = model.predict(X)[0]

    responses = {
        "courses": "We offer B.Tech MBA MCA",
        "admission": "Admission is based on entrance exam",
        "fees": "Fee is 1.2 LPA",
        "hostel": "Yes hostel is available",
        "timings": "College runs from 9AM to 4PM",
        "placements": "Yes 95 percent placement"
    }

    return {
        "intent": intent,
        "answer": responses.get(intent, "Sorry, I don't understand")
    }
