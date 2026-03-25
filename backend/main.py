from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

from backend.utils import preprocess, rule_engine
from backend.model import load_model, ml_score
from backend.bert_model import semantic_score

app = FastAPI(title="Sentinel-Text API", version="4.0")

# Load ML model
model, vectorizer = load_model()

# Input schema
class InputText(BaseModel):
    text: str


# ================= MAIN ANALYSIS =================
@app.post("/analyze")
def analyze(data: InputText):
    text = preprocess(data.text)

    # ================= SCORES =================
    ml = ml_score(text, model, vectorizer)
    rule_score, indicators = rule_engine(text)
    bert = semantic_score(text)

    # ================= IMPROVED WEIGHTING =================
    final = (0.4 * ml) + (0.2 * rule_score) + (0.4 * bert)

    # ================= SAFE OVERRIDE (VERY IMPORTANT) =================
    if rule_score == 0 and bert < 40 and ml < 50:
        level = "SAFE"

    else:
        # ================= THRESHOLDS =================
        if final < 40:
            level = "SAFE"
        elif final < 70:
            level = "SUSPICIOUS"
        else:
            level = "HIGH RISK"

    # ================= ATTACK TYPE =================
    attack_type = "General"

    if "otp" in text or "password" in text:
        attack_type = "Credential Phishing"
    elif "ceo" in text or "manager" in text:
        attack_type = "Authority Impersonation"
    elif "bank" in text or "transfer" in text:
        attack_type = "Financial Fraud"

    # ================= CONFIDENCE =================
    confidence = max(ml, bert)

    # ================= INDICATOR FALLBACK =================
    if not indicators:
        indicators.append("No strong rule-based indicators detected.")

    # ================= RESPONSE =================
    return {
        "threat_level": level,
        "risk_score": round(final, 2),
        "ml_score": round(ml, 2),
        "rule_score": rule_score,
        "bert_score": round(bert, 2),
        "confidence": round(confidence, 2),
        "attack_type": attack_type,
        "indicators": indicators
    }


# ================= FILE ANALYSIS =================
@app.post("/analyze-file")
async def analyze_file(file: UploadFile):
    content = await file.read()
    text = content.decode("utf-8")

    return analyze(InputText(text=text))