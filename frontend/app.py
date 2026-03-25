import streamlit as st
import requests
import pandas as pd
import time
import random
import re

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(page_title="Sentinel-Text", layout="wide")

# ================= KEYWORDS =================
KEYWORDS = {
    "otp": "Sensitive credential request",
    "password": "Sensitive credential request",
    "urgent": "Urgency manipulation",
    "immediately": "Urgency manipulation",
    "transfer": "Financial request",
    "bank": "Financial context",
    "ceo": "Authority impersonation",
    "verify": "Phishing attempt",
    "login": "Credential access"
}

SUSPICIOUS_DOMAINS = ["bit.ly", "tinyurl", "grabify", "rebrand.ly"]

# ================= SESSION =================
if "text" not in st.session_state:
    st.session_state.text = ""

if "prev_score" not in st.session_state:
    st.session_state.prev_score = 0

if "last_input_time" not in st.session_state:
    st.session_state.last_input_time = time.time()

if "last_random" not in st.session_state:
    st.session_state.last_random = ""

# ================= HIGHLIGHT =================
def highlight_text(text):
    explanations = []

    for word, reason in KEYWORDS.items():
        if word in text.lower():
            explanations.append(f"{word.upper()} → {reason}")

            text = re.sub(
                rf"\b({word})\b",
                r"<span style='background:#ffd6d6;color:#b30000;padding:3px 6px;border-radius:6px;font-weight:600;'>\1</span>",
                text,
                flags=re.IGNORECASE
            )

    urls = re.findall(r'(https?://\S+)', text)
    for url in urls:
        if any(d in url for d in SUSPICIOUS_DOMAINS):
            explanations.append("Suspicious shortened link detected")

    return text, explanations

# ================= NEUMORPHIC CSS =================
st.markdown("""
<style>

/* ===== BASE ===== */
[data-testid="stAppViewContainer"] {
    background: #e0e5ec;
    color: #333;
}

/* ===== COLUMNS AS CARDS ===== */
div[data-testid="column"] {
    background: #e0e5ec;
    border-radius: 20px;
    padding: 25px;
    margin-top: 15px;

    box-shadow: 
        10px 10px 20px #a3b1c6,
        -10px -10px 20px #ffffff;
}

/* ===== TEXTAREA ===== */
textarea {
    background: #e0e5ec !important;
    border-radius: 15px !important;
    border: none !important;

    box-shadow: 
        inset 4px 4px 8px #a3b1c6,
        inset -4px -4px 8px #ffffff;
}

/* ===== BUTTONS ===== */
button {
    background: #e0e5ec !important;
    border-radius: 12px !important;
    border: none !important;

    box-shadow: 
        5px 5px 10px #a3b1c6,
        -5px -5px 10px #ffffff;

    transition: all 0.2s ease;
}

button:active {
    box-shadow: 
        inset 4px 4px 8px #a3b1c6,
        inset -4px -4px 8px #ffffff;
}

/* ===== FILE UPLOADER ===== */
[data-testid="stFileUploader"] section {
    background: #e0e5ec !important;
    border-radius: 15px;
    box-shadow: 
        inset 4px 4px 8px #a3b1c6,
        inset -4px -4px 8px #ffffff;
}

/* ===== PROGRESS ===== */
.progress-container {
    background:#e0e5ec;
    padding:6px;
    border-radius:20px;
    box-shadow: inset 4px 4px 8px #a3b1c6,
                inset -4px -4px 8px #ffffff;
}

.progress-bar {
    height:26px;
    border-radius:20px;
    box-shadow: 
        4px 4px 10px rgba(0,0,0,0.2),
        -4px -4px 10px rgba(255,255,255,0.9);
}

</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown("""
<h1 style='
text-align: center;
font-size: 48px;
font-weight: 900;
background: linear-gradient(90deg, 
#ff4d4d, 
#ff9933,  
#ff66b2);
background-size: 300%;
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
animation: gradientShift 6s ease infinite;
margin-bottom: 10px;
'>
SENTINEL-TEXT PRO
</h1>

<style>
@keyframes gradientShift {
    0% {background-position: 0%;}
    50% {background-position: 100%;}
    100% {background-position: 0%;}
}
</style>
""", unsafe_allow_html=True)
col1, col2 = st.columns(2)

# ================= LEFT =================
with col1:
    st.subheader("📥 Input")

    user_text = st.text_area("Enter Message", value=st.session_state.text)

    now = time.time()
    if user_text != st.session_state.text:
        st.session_state.text = user_text
        st.session_state.last_input_time = now

    # Buttons
    c1, c2, c3 = st.columns(3)

    with c1:
        analyze_btn = st.button("Analyze")

    with c2:
        if st.button("🎲 Test Case"):
            SAMPLES = [
                "I am the CEO. Send me your password and OTP immediately.",
                "Transfer money now or your account will be blocked.",
                "Click http://bit.ly/secure-login to verify your account",
                "Your bank account needs urgent verification.",
                "Please share your OTP to complete verification.",
                "This is IT support, send your login details ASAP.",
                "Let's catch up later for coffee.",
                "Are you available for a meeting tomorrow?",
                "Happy birthday! Hope you have a great day!"
            ]

            sample = random.choice(SAMPLES)
            while sample == st.session_state.last_random:
                sample = random.choice(SAMPLES)

            st.session_state.text = sample
            st.session_state.last_random = sample
            st.rerun()

    with c3:
        if st.button("🔄 Reset"):
            st.session_state.text = ""
            st.session_state.prev_score = 0
            st.rerun()

    uploaded_file = st.file_uploader("Upload .txt file")

    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        st.session_state.text = content

    if st.session_state.text:
        highlighted, explanations = highlight_text(st.session_state.text)

        st.markdown("### 🔍 Highlighted")
        st.markdown(highlighted, unsafe_allow_html=True)

        st.markdown("### 🧠 Why flagged")
        if explanations:
            for e in explanations:
                st.write(f"- {e}")
        else:
            st.write("No suspicious patterns")

# ================= DETECTION =================
res = None

if time.time() - st.session_state.last_input_time > 0.7:
    if st.session_state.text:
        try:
            res = requests.post(API_URL, json={"text": st.session_state.text}).json()
        except:
            pass

if analyze_btn and st.session_state.text:
    res = requests.post(API_URL, json={"text": st.session_state.text}).json()

# ================= RIGHT =================
with col2:
    st.subheader("📊 Output")

    if res:
        st.write(f"### Risk Score: {res['risk_score']}%")

        placeholder = st.empty()

        prev = int(st.session_state.prev_score)
        target = int(res["risk_score"])
        step = 1 if target > prev else -1

        for i in range(prev, target + step, step):

            if i < 40:
                color1 = "#4CAF50"
                color2 = "#66bb6a"
            elif i < 70:
                color1 = "#ff9800"
                color2 = "#ffb74d"
            else:
                color1 = "#f44336"
                color2 = "#e57373"

            placeholder.markdown(f"""
            <div class="progress-container">
                <div class="progress-bar" style="
                    width:{i}%;
                    background: linear-gradient(90deg, {color1}, {color2});
                    color:white;
                    text-align:right;
                    padding-right:10px;
                    font-weight:600;
                ">
                {i}%
                </div>
            </div>
            """, unsafe_allow_html=True)

            time.sleep(0.01)

        st.session_state.prev_score = target

        st.write(f"**Attack Type:** {res['attack_type']}")
        st.write(f"**Confidence:** {res['confidence']}%")

        st.subheader("📊 Model Comparison")
        df = pd.DataFrame({
            "Model": ["ML", "Rule", "BERT"],
            "Score": [
                res["ml_score"],
                res["rule_score"],
                res["bert_score"]
            ]
        })

        st.bar_chart(df.set_index("Model"))

    else:
        st.info("Start typing to analyze")