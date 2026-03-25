import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Sample dataset
data = {
    "text": [
        "send otp immediately",
        "i am ceo transfer money",
        "hello how are you",
        "meeting tomorrow",
        "urgent password needed",
    ],
    "label": [1, 1, 0, 0, 1]
}

df = pd.DataFrame(data)

X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2
)

vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)

model = LogisticRegression()
model.fit(X_train_vec, y_train)

joblib.dump(model, "model/model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("Model trained and saved!")