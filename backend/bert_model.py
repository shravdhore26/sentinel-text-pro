from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

PHISHING_PATTERNS = [
    "send otp immediately",
    "transfer money now",
    "i am ceo send password",
    "verify your account urgently",
]

def semantic_score(text):
    emb1 = model.encode([text])[0]
    emb2 = model.encode(PHISHING_PATTERNS)

    sims = [
        np.dot(emb1, e) / (np.linalg.norm(emb1) * np.linalg.norm(e))
        for e in emb2
    ]

    return max(sims) * 100