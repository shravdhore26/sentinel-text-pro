import joblib

def load_model():
    model = joblib.load("model/model.pkl")
    vectorizer = joblib.load("model/vectorizer.pkl")
    return model, vectorizer

def ml_score(text, model, vectorizer):
    X = vectorizer.transform([text])
    return model.predict_proba(X)[0][1] * 100