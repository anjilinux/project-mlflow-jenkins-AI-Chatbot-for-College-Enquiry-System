import joblib

def test_artifacts_exist():
    assert joblib.load("artifacts/model.pkl")
    assert joblib.load("artifacts/vectorizer.pkl")
