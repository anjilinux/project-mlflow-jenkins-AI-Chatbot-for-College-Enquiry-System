from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def vectorize(corpus):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)

    with open("artifacts/vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    return X
