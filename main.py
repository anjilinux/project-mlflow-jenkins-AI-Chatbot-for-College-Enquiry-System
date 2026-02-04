from fastapi import FastAPI
import pickle

app = FastAPI()

model = pickle.load(open("artifacts/model.pkl", "rb"))
vectorizer = pickle.load(open("artifacts/vectorizer.pkl", "rb"))

RESPONSES = {
    "courses": "We offer B.Tech, M.Tech, MBA.",
    "admission": "Admissions are through entrance exams.",
    "fees": "Hostel fees are ₹80,000 per year.",
    "placements": "We have 95% placement record."
}

@app.post("/chat")
def chat(query: str):
    X = vectorizer.transform([query])
    intent = model.predict(X)[0]
    return {"response": RESPONSES.get(intent, "Please contact admin.")}
