import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Stock Trading Platform", layout="wide")

# ---------------- SESSION ----------------
if "balance" not in st.session_state:
    st.session_state.balance = 10000

if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}

# ---------------- HEADER ----------------
st.title("Stock Trading Dashboard")

st.markdown("Simulated trading platform built using Streamlit")

# ---------------- SIDEBAR ----------------
menu = st.sidebar.selectbox(
    "Menu",
    ["Market Overview", "Stock Analysis", "Buy Stock", "Sell Stock", "Portfolio"]
)

# ---------------- MARKET OVERVIEW ----------------
if menu == "Market Overview":

    st.subheader("Popular Stocks")

    stocks = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]

    data = []

    for stock in stocks:
        ticker = yf.Ticker(stock)
        price = ticker.history(period="1d")["Close"][0]

        data.append({
            "Stock": stock,
            "Price": round(price,2)
        })

    df = pd.DataFrame(data)

    st.dataframe(df, use_container_width=True)

# ---------------- STOCK ANALYSIS ----------------
elif menu == "Stock Analysis":

    st.subheader("Stock Analysis")

    symbol = st.text_input("Enter Stock Symbol", "AAPL")

    stock = yf.Ticker(symbol)

    data = stock.history(period="6mo")

    if not data.empty:

        st.metric("Current Price", f"${data['Close'][-1]:.2f}")

        # Candlestick Chart
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"]
        )])

        fig.update_layout(title=f"{symbol} Candlestick Chart")

        st.plotly_chart(fig, use_container_width=True)

# ---------------- BUY STOCK ----------------
elif menu == "Buy Stock":

    st.subheader("Buy Stock")

    symbol = st.text_input("Stock Symbol")

    quantity = st.number_input("Quantity", min_value=1)

    if st.button("Buy"):

        stock = yf.Ticker(symbol)

        price = stock.history(period="1d")["Close"][0]

        cost = price * quantity

        if cost <= st.session_state.balance:

            st.session_state.balance -= cost

            if symbol in st.session_state.portfolio:
                st.session_state.portfolio[symbol] += quantity
            else:
                st.session_state.portfolio[symbol] = quantity

            st.success(f"Bought {quantity} shares of {symbol}")

        else:
            st.error("Insufficient balance")

# ---------------- SELL STOCK ----------------
elif menu == "Sell Stock":

    st.subheader("Sell Stock")

    symbol = st.text_input("Stock Symbol")

    quantity = st.number_input("Quantity", min_value=1)

    if st.button("Sell"):

        if symbol in st.session_state.portfolio:

            if st.session_state.portfolio[symbol] >= quantity:

                stock = yf.Ticker(symbol)
                price = stock.history(period="1d")["Close"][0]

                revenue = price * quantity

                st.session_state.balance += revenue

                st.session_state.portfolio[symbol] -= quantity

                st.success("Stock sold successfully")

            else:
                st.error("Not enough shares")

        else:
            st.error("Stock not owned")

# ---------------- PORTFOLIO ----------------
elif menu == "Portfolio":

    st.subheader("Portfolio Dashboard")

    portfolio_data = []
    total_value = 0

    for symbol, qty in st.session_state.portfolio.items():

        stock = yf.Ticker(symbol)
        price = stock.history(period="1d")["Close"][0]

        value = price * qty
        total_value += value

        portfolio_data.append({
            "Stock": symbol,
            "Quantity": qty,
            "Price": price,
            "Value": value
        })

    if portfolio_data:

        df = pd.DataFrame(portfolio_data)

        st.dataframe(df, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Portfolio Value", f"${total_value:.2f}")

        with col2:
            st.metric("Cash Balance", f"${st.session_state.balance:.2f}")

        # Portfolio Pie Chart
        pie = px.pie(df, values="Value", names="Stock", title="Portfolio Distribution")

        st.plotly_chart(pie, use_container_width=True)

    else:
        st.info("Portfolio is empty")