import re

URGENCY = ["urgent", "immediately", "now", "asap", "fast"]
AUTHORITY = ["ceo", "manager", "admin", "it support"]
SENSITIVE = ["password", "otp", "transfer", "bank"]

def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text

def rule_engine(text):
    score = 0
    indicators = []

    if any(w in text for w in URGENCY):
        score += 20
        indicators.append("Urgency manipulation detected (e.g., 'fast', 'immediately')")

    if any(w in text for w in AUTHORITY):
        score += 25
        indicators.append("Authority impersonation detected (e.g., 'CEO', 'manager')")

    if any(w in text for w in SENSITIVE):
        score += 30
        indicators.append("Sensitive credential request detected (e.g., 'OTP', 'password')")

    return score, indicators