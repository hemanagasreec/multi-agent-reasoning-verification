import streamlit as st

st.set_page_config(
    page_title="Financial Fraud Detection",
    page_icon="💳",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("💳 Financial Fraud Detection System")
st.caption("Multi-Agent AI Fraud Detection & Verification Dashboard")

st.divider()

# --------------------------------------------------
# TRANSACTION INPUT
# --------------------------------------------------

st.header("📋 Transaction Details")

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

# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if st.button("🔍 Analyze Transaction", use_container_width=True):

    if not transaction_id or not merchant or not location or not device_id:

        st.warning("⚠️ Please fill in all transaction details.")

    else:

        # --------------------------------------------------
        # DEMO ANALYSIS
        # This will later be replaced with Member 2's
        # actual AI-agent outputs.
        # --------------------------------------------------

        risk_score = 72

        agent_results = {
            "Transaction Pattern Agent": "Completed",
            "Risk Agent": "Completed",
            "History Agent": "Completed",
            "Fraud Analyst": "Completed",
            "Independent Verifier": "Completed",
            "Critic": "Completed"
        }

        evidence = [
            "Transaction requires additional verification.",
            "Transaction type and amount require risk assessment.",
            "Independent verification completed."
        ]

        # --------------------------------------------------
        # AGENT STATUS
        # --------------------------------------------------

        st.divider()

        st.header("🤖 Agent Analysis")

        for agent, status in agent_results.items():

            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(f"**{agent}**")

            with col2:
                st.success("✅ " + status)

        # --------------------------------------------------
        # RISK SCORE
        # --------------------------------------------------

        st.divider()

        st.header("📊 Risk Assessment")

        score_col1, score_col2 = st.columns(2)

        with score_col1:

            st.metric(
                "Fraud Risk Score",
                f"{risk_score}%"
            )

        with score_col2:

            if risk_score >= 70:
                st.error("🔴 HIGH RISK")
            elif risk_score >= 40:
                st.warning("🟠 MEDIUM RISK")
            else:
                st.success("🟢 LOW RISK")

        st.progress(risk_score / 100)

        # --------------------------------------------------
        # EVIDENCE
        # --------------------------------------------------

        st.divider()

        st.header("🔎 Evidence")

        for item in evidence:
            st.write("•", item)

        # --------------------------------------------------
        # TRANSACTION SUMMARY
        # --------------------------------------------------

        st.divider()

        st.header("📄 Transaction Summary")

        summary_col1, summary_col2 = st.columns(2)

        with summary_col1:
            st.write("**Transaction ID:**", transaction_id)
            st.write("**Merchant:**", merchant)
            st.write("**Amount:**", f"₹{amount:,.2f}")

        with summary_col2:
            st.write("**Location:**", location)
            st.write("**Device ID:**", device_id)
            st.write("**Transaction Type:**", transaction_type)

        # --------------------------------------------------
        # FINAL DECISION
        # --------------------------------------------------

        st.divider()

        st.header("🚨 Final Fraud Decision")

        if risk_score >= 70:

            st.error(
                "🔴 HIGH RISK — TRANSACTION REQUIRES VERIFICATION"
            )

            st.write(
                "⚠️ The transaction has been flagged for further review."
            )

        elif risk_score >= 40:

            st.warning(
                "🟠 MEDIUM RISK — REVIEW RECOMMENDED"
            )

        else:

            st.success(
                "🟢 LOW RISK — TRANSACTION APPEARS SAFE"
            )

        st.info(
            "ℹ️ Agent outputs shown here are currently demonstration "
            "results. They will be connected to the actual AI agents "
            "once the agent module is integrated."
        )

