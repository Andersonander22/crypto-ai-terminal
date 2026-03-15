import streamlit as st
from pycoingecko import CoinGeckoAPI

st.title("Crypto AI Terminal")

# Create tabs
tab1, tab2 = st.tabs(["📈 Portfolio Tracker", "📰 Sentiment Analyzer"])

# ---------- Portfolio Tracker ----------
with tab1:
    st.header("My Crypto Portfolio Tracker")

    # Initialize CoinGecko client
    cg = CoinGeckoAPI()

    # User inputs
    btc_amount = st.number_input("Enter your BTC holdings:", min_value=0.0, format="%.6f")
    eth_amount = st.number_input("Enter your ETH holdings:", min_value=0.0, format="%.6f")

    # Fetch live prices
    prices = cg.get_price(ids=['bitcoin', 'ethereum'], vs_currencies='usd')
    btc_price = prices['bitcoin']['usd']
    eth_price = prices['ethereum']['usd']

    # Calculate values
    btc_value = btc_amount * btc_price
    eth_value = eth_amount * eth_price
    total_value = btc_value + eth_value

    # Display results
    st.subheader("📊 Portfolio Value")
    st.write(f"BTC Value: ${btc_value:,.2f}")
    st.write(f"ETH Value: ${eth_value:,.2f}")
    st.success(f"Total Portfolio Value: ${total_value:,.2f}")

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
# ---------- Info ----------
st.write("---")
st.write("Built as part of Crypto AI Lab using OpenGradient models.")
