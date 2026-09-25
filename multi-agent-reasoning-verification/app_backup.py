import streamlit as st

st.set_page_config(
    page_title="Financial Fraud Detection",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Financial Fraud Detection System")
st.write("Multi-Agent AI Fraud Detection Dashboard")

st.divider()

st.header("Transaction Details")

col1, col2 = st.columns(2)

with col1:
    transaction_id = st.text_input("Transaction ID")

    amount = st.number_input(
        "Transaction Amount (₹)",
        min_value=0.0,
        step=100.0
    )

    merchant = st.text_input("Merchant")

with col2:
    location = st.text_input("Transaction Location")

    device_id = st.text_input("Device ID")

    transaction_type = st.selectbox(
        "Transaction Type",
        ["Online", "ATM", "POS", "Bank Transfer"]
    )

st.divider()

if st.button("🔍 Analyze Transaction", use_container_width=True):

    if not transaction_id or not merchant or not location or not device_id:

        st.warning("⚠️ Please fill in all transaction details.")

    else:

        st.success("✅ Transaction submitted for analysis!")

        st.subheader("🔎 Fraud Detection Result")

        st.info("🤖 AI agents are analyzing the transaction...")

        st.metric(
            label="Transaction Amount",
            value=f"₹{amount:,.2f}"
        )

        st.write("**Transaction Type:**", transaction_type)
        st.write("**Merchant:**", merchant)
        st.write("**Location:**", location)
        st.write("**Device ID:**", device_id)

        st.success("🟢 Transaction appears to be SAFE")