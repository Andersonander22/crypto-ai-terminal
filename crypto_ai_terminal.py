import streamlit as st
import pickle

st.title("Crypto AI Terminal")
st.write("Experimental AI models for crypto analytics")

# ---------- Load Whale Model ----------
class WhaleMovementDetector:
    def __init__(self):
        self.threshold_medium = 100000
        self.threshold_high = 1000000

    def predict(self, transaction_value):
        if transaction_value >= self.threshold_high:
            return "High Whale Activity"
        elif transaction_value >= self.threshold_medium:
            return "Medium Whale Activity"
        else:
            return "Low Whale Activity"

try:
    with open("whale_movement_detector.pkl", "rb") as f:
        whale_model = pickle.load(f)
except:
    whale_model = WhaleMovementDetector()

# ---------- Whale Detector UI ----------
st.header("On-Chain Whale Detector")

transaction = st.number_input(
    "Enter transaction value ($)",
    min_value=0,
    step=1000
)

if st.button("Analyze Whale Activity"):
    result = whale_model.predict(transaction)
    st.success(f"Prediction: {result}")

# ---------- Sentiment Analyzer ----------
st.header("Crypto Sentiment Analyzer")

text = st.text_area("Enter crypto related text")

def simple_sentiment(text):
    positive_words = ["bull", "pump", "moon", "buy"]
    negative_words = ["dump", "sell", "bear", "crash"]

    score = 0

    for word in positive_words:
        if word in text.lower():
            score += 1

    for word in negative_words:
        if word in text.lower():
            score -= 1

    if score > 0:
        return "Bullish Sentiment"
    elif score < 0:
        return "Bearish Sentiment"
    else:
        return "Neutral Sentiment"

if st.button("Analyze Sentiment"):
    sentiment = simple_sentiment(text)
    st.success(f"Market Sentiment: {sentiment}")

# ---------- Info ----------
st.write("---")
st.write("Built as part of Crypto AI Lab using OpenGradient models.")