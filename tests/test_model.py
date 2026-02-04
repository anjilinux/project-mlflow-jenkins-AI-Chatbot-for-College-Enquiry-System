import joblib

def test_artifacts_exist():
    assert joblib.load("model.pkl")
    assert joblib.load("vectorizer.pkl")
