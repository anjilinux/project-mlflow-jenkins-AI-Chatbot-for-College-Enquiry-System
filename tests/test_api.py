from fastapi.testclient import TestClient
from main import app   # ✅ FIXED (was app.py earlier)

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict():
    response = client.post(
        "/predict",
        json={"question": "What courses are available?"}
    )

    assert response.status_code == 200
    assert "intent" in response.json()
