import streamlit as st
import pickle
import tweepy
from pycoingecko import CoinGeckoAPI

# Load bearer token
bearer_token = st.secrets["bearer_token"]
client = tweepy.Client(bearer_token=bearer_token)

st.title("Crypto AI Terminal")
st.write("Experimental AI models for crypto analytics")

# Define tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🐋 Whale Detector",
    "📰 Sentiment Analyzer",
    "💰 Portfolio Tracker",
    "🐦 Tweet Analyzer"
])

# ---------- Whale Detector ----------
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

with tab1:
    st.header("On-Chain Whale Detector")
    transaction = st.number_input("Enter transaction value ($)", min_value=0, step=1000)
    if st.button("Analyze Whale Activity"):
        result = whale_model.predict(transaction)
        st.success(f"Prediction: {result}")

# ---------- Sentiment Analyzer ----------
with tab2:
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

# ---------- Portfolio Tracker ----------
with tab3:
    st.header("💰 My Crypto Portfolio Tracker")
    cg = CoinGeckoAPI()

    btc_amount = st.number_input("Enter your BTC holdings:", min_value=0.0, format="%.6f")
    eth_amount = st.number_input("Enter your ETH holdings:", min_value=0.0, format="%.6f")

    prices = cg.get_price(ids=['bitcoin', 'ethereum'], vs_currencies='usd')
    btc_price = prices['bitcoin']['usd']
    eth_price = prices['ethereum']['usd']

    btc_value = btc_amount * btc_price
    eth_value = eth_amount * eth_price
    total_value = btc_value + eth_value

    st.subheader("📊 Portfolio Value")
    st.write(f"BTC Value: ${btc_value:,.2f}")
    st.write(f"ETH Value: ${eth_value:,.2f}")
    st.success(f"Total Portfolio Value: ${total_value:,.2f}")

# ---------- Tweet Analyzer ----------
with tab4:
    st.header("Tweet Sentiment Analyzer")
    keyword = st.text_input("Enter a keyword to search tweets (e.g., Bitcoin, Ethereum, NFT)")

    def tweet_sentiment(text):
        positive_words = ["bull", "pump", "moon", "buy", "great", "love", "good"]
        negative_words = ["dump", "sell", "bear", "crash", "bad", "hate", "poor"]

        score = 0
        for word in positive_words:
            if word in text.lower():
                score += 1
        for word in negative_words:
            if word in text.lower():
                score -= 1

        if score > 0:
            return "Bullish/Positive"
        elif score < 0:
            return "Bearish/Negative"
        else:
            return "Neutral"

    if st.button("Fetch & Analyze Tweets"):
        if keyword:
            tweets = client.search_recent_tweets(query=keyword, max_results=5)
            for tweet in tweets.data:
                sentiment = tweet_sentiment(tweet.text)
                st.write(f"Tweet: {tweet.text}")
                st.write(f"Sentiment: {sentiment}")
                st.write("---")
        else:
            st.warning("Please enter a keyword.")
