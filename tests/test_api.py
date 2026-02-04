import os
import pickle
import pytest
from fastapi.testclient import TestClient

# Import FastAPI app (all files are in root)
from app import app  

client = TestClient(app)

MODEL_PATH = "artifacts/model.pkl"
VECTORIZER_PATH = "artifacts/vectorizer.pkl"


# -------------------------
# BASIC API HEALTH CHECK
# -------------------------
def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# -------------------------
# MODEL & VECTORIZER EXIST
# -------------------------
def test_model_artifacts_exist():
    assert os.path.exists(MODEL_PATH), "❌ model.pkl not found"
    assert os.path.exists(VECTORIZER_PATH), "❌ vectorizer.pkl not found"


# -------------------------
# LOAD MODEL SUCCESSFULLY
# -------------------------
def test_model_loadable():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)

    assert model is not None
    assert vectorizer is not None


# -------------------------
# CHATBOT PREDICTION TEST
# -------------------------
def test_chatbot_prediction():
    payload = {
        "question": "What courses are available?"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "intent" in data
    assert isinstance(data["intent"], str)
    assert len(data["intent"]) > 0


# -------------------------
# INVALID INPUT TEST
# -------------------------
def test_invalid_payload():
    response = client.post("/predict", json={})
    assert response.status_code in [400, 422]
