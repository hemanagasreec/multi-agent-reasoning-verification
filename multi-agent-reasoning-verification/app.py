import streamlit as st
import math
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="SENTINEL // AI SECURITY",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 80% 10%, rgba(0, 229, 255, 0.08), transparent 25%),
        radial-gradient(circle at 10% 90%, rgba(99, 102, 241, 0.07), transparent 25%),
        #05070c;
}

/* Hide default Streamlit decoration */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Main width */
.block-container {
    padding: 2rem 3rem 4rem 3rem;
    max-width: 1600px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #070a10;
    border-right: 1px solid #17202e;
}

section[data-testid="stSidebar"] > div {
    padding: 2rem 1rem;
}

/* Sidebar buttons */
div[role="radiogroup"] label {
    background: transparent;
    border-radius: 10px;
    padding: 12px 14px;
    margin: 4px 0;
    transition: 0.2s;
}

div[role="radiogroup"] label:hover {
    background: #101722;
}

/* Headers */
h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Buttons */
.stButton > button {
    border-radius: 9px;
    min-height: 46px;
    font-weight: 700;
    border: 1px solid #1d3548;
    background: linear-gradient(135deg, #07141d, #0a1b26);
    color: #8beaff;
    transition: 0.2s;
}

.stButton > button:hover {
    border-color: #00e5ff;
    box-shadow: 0 0 20px rgba(0,229,255,0.18);
}

/* Inputs */
.stTextInput input,
.stNumberInput input {
    background: #090e16 !important;
    border: 1px solid #1b2a3a !important;
    color: #e7faff !important;
    border-radius: 8px !important;
}

div[data-baseweb="select"] > div {
    background: #090e16 !important;
    border-color: #1b2a3a !important;
}

/* ============================================================
   CUSTOM COMPONENTS
   ============================================================ */

.logo-box {
    padding: 10px 4px 25px 4px;
}

.logo-main {
    font-family: 'Space Grotesk';
    font-size: 25px;
    font-weight: 800;
    color: #e9fbff;
    letter-spacing: 2px;
}

.logo-sub {
    color: #4b6b7b;
    font-size: 9px;
    letter-spacing: 2px;
    margin-top: 3px;
}

.system-status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    border: 1px solid rgba(0,255,170,0.25);
    background: rgba(0,255,170,0.06);
    color: #55ffc4;
    padding: 7px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

.status-dot {
    width: 7px;
    height: 7px;
    background: #00ffa6;
    border-radius: 50%;
    box-shadow: 0 0 12px #00ffa6;
}

.hero {
    padding: 20px 0 5px 0;
}

.hero-kicker {
    color: #00d9ff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    margin-bottom: 8px;
}

.hero-title {
    font-family: 'Space Grotesk';
    font-size: 42px;
    font-weight: 800;
    color: #effcff;
    line-height: 1.05;
}

.hero-description {
    color: #66808d;
    font-size: 14px;
    margin-top: 8px;
}

.stat {
    background: linear-gradient(145deg, #0b111a, #080c13);
    border: 1px solid #172536;
    border-radius: 14px;
    padding: 18px;
    min-height: 110px;
    position: relative;
    overflow: hidden;
}

.stat:after {
    content: "";
    position: absolute;
    width: 80px;
    height: 80px;
    right: -35px;
    top: -35px;
    border-radius: 50%;
    background: rgba(0,229,255,0.06);
}

.stat-label {
    color: #526b78;
    font-size: 9px;
    letter-spacing: 2px;
    font-weight: 700;
}

.stat-value {
    font-family: 'Space Grotesk';
    color: #ecfbff;
    font-size: 30px;
    font-weight: 700;
    margin-top: 10px;
}

.stat-change {
    color: #38e8ae;
    font-size: 10px;
    margin-top: 4px;
}

/* Investigation card */

.investigation {
    background:
        linear-gradient(135deg, rgba(0,229,255,0.035), transparent 45%),
        #080d14;
    border: 1px solid #1a3344;
    border-radius: 18px;
    padding: 25px;
    position: relative;
    overflow: hidden;
}

.investigation:before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 2px;
    background: #00e5ff;
    box-shadow: 0 0 20px #00e5ff;
}

.mini-label {
    color: #526b78;
    font-size: 9px;
    letter-spacing: 2px;
    font-weight: 700;
}

.txn-id {
    color: #e9fbff;
    font-family: 'Space Grotesk';
    font-size: 23px;
    font-weight: 700;
    margin-top: 6px;
}

.txn-amount {
    color: #00e5ff;
    font-family: 'Space Grotesk';
    font-size: 32px;
    font-weight: 700;
}

.txn-meta {
    color: #6b8592;
    font-size: 11px;
}

/* Risk */

.risk-panel {
    background: #080d14;
    border: 1px solid #2b1d23;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
}

.risk-number {
    font-family: 'Space Grotesk';
    font-size: 70px;
    font-weight: 800;
    color: #ff4d67;
    line-height: 1;
    text-shadow: 0 0 25px rgba(255,77,103,0.25);
}

.risk-small {
    color: #6f7885;
    font-size: 10px;
    letter-spacing: 2px;
}

.risk-high {
    display: inline-block;
    color: #ff5c73;
    border: 1px solid rgba(255,77,103,0.3);
    background: rgba(255,77,103,0.07);
    padding: 7px 14px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-top: 12px;
}

/* Agent pipeline */

.pipeline {
    background: #080d14;
    border: 1px solid #172536;
    border-radius: 18px;
    padding: 25px;
}

.pipeline-title {
    color: #526b78;
    font-size: 9px;
    letter-spacing: 2px;
    font-weight: 700;
    margin-bottom: 20px;
}

.agent-node {
    background: #0b131c;
    border: 1px solid #1c3443;
    border-radius: 11px;
    padding: 14px 10px;
    text-align: center;
    min-height: 80px;
}

.agent-icon {
    color: #00e5ff;
    font-size: 17px;
}

.agent-name {
    color: #dcecf1;
    font-size: 10px;
    font-weight: 600;
    margin-top: 5px;
}

.agent-state {
    color: #42e8a7;
    font-size: 8px;
    letter-spacing: 1px;
    margin-top: 4px;
}

.connector {
    text-align: center;
    color: #294858;
    font-size: 18px;
    padding-top: 27px;
}

/* Evidence */

.evidence-card {
    background: #090f17;
    border: 1px solid #182837;
    border-radius: 11px;
    padding: 14px;
    margin-bottom: 9px;
}

.evidence-number {
    color: #00d9ff;
    font-size: 10px;
    font-weight: 700;
}

.evidence-title {
    color: #dcecf1;
    font-size: 12px;
    font-weight: 600;
}

.evidence-text {
    color: #607784;
    font-size: 10px;
    margin-top: 4px;
}

/* Activity */

.activity {
    background: #080d14;
    border: 1px solid #172536;
    border-radius: 18px;
    padding: 22px;
}

.activity-row {
    display: flex;
    gap: 12px;
    padding: 11px 0;
    border-bottom: 1px solid #111c27;
}

.activity-time {
    color: #405966;
    font-size: 9px;
    min-width: 50px;
}

.activity-dot {
    color: #00e5ff;
}

.activity-text {
    color: #9eb1ba;
    font-size: 10px;
}

/* Decision */

.decision {
    background:
        radial-gradient(circle at 50% 0%, rgba(255,55,80,0.08), transparent 55%),
        #0a0d13;
    border: 1px solid rgba(255,70,90,0.25);
    border-radius: 18px;
    padding: 28px;
    text-align: center;
}

.decision-icon {
    font-size: 35px;
}

.decision-title {
    color: #ff536b;
    font-family: 'Space Grotesk';
    font-size: 23px;
    font-weight: 800;
    margin-top: 8px;
}

.decision-sub {
    color: #687985;
    font-size: 11px;
    margin-top: 6px;
}

/* Timeline */

.timeline {
    background: #080d14;
    border: 1px solid #172536;
    border-radius: 18px;
    padding: 22px;
}

.timeline-row {
    display: flex;
    gap: 15px;
    padding: 9px 0;
}

.timeline-time {
    color: #3f5c69;
    font-size: 9px;
    width: 55px;
}

.timeline-dot {
    color: #42e8a7;
}

.timeline-text {
    color: #9bb0ba;
    font-size: 10px;
}

/* Section heading */

.section-head {
    font-family: 'Space Grotesk';
    font-size: 18px;
    color: #dff8ff;
    font-weight: 700;
    margin: 25px 0 13px 0;
}

.section-kicker {
    color: #405d6a;
    font-size: 9px;
    letter-spacing: 2px;
    margin-bottom: 5px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DEMO DATA
# ============================================================

risk_score = 72

agents = [
    ("01", "PATTERN", "✓"),
    ("02", "RISK", "✓"),
    ("03", "HISTORY", "✓"),
    ("04", "ANALYST", "✓"),
    ("05", "VERIFIER", "✓"),
    ("06", "CRITIC", "✓"),
]


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""
    <div class="logo-box">
        <div class="logo-main">◈ SENTINEL</div>
        <div class="logo-sub">AI FINANCIAL SECURITY // v1.0</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="system-status"><span class="status-dot"></span> SYSTEM ONLINE</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.caption("COMMAND CENTER")

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Transaction Lab",
            "Agent Network",
            "Evaluation"
        ],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption("SECURITY")

    st.markdown("""
    <div style="
        color:#58717d;
        font-size:10px;
        line-height:1.8;
        padding:10px;
        border:1px solid #13202c;
        border-radius:10px;
        background:#080c12;
    ">
    ● ORCHESTRATOR <span style="float:right;color:#42e8a7;">READY</span><br>
    ● AGENT NETWORK <span style="float:right;color:#42e8a7;">6/6</span><br>
    ● VERIFICATION <span style="float:right;color:#42e8a7;">ACTIVE</span><br>
    ● AUDIT LOG <span style="float:right;color:#42e8a7;">SYNCED</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption("HACKFUSION 2026")


# ============================================================
# TOP HEADER
# ============================================================

top1, top2 = st.columns([5, 1])

with top1:
    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">MULTI-AGENT INTELLIGENCE // FRAUD DEFENSE</div>
        <div class="hero-title">Financial Security<br>Command Center</div>
        <div class="hero-description">
            Autonomous transaction analysis, multi-agent reasoning
            and independent verification.
        </div>
    </div>
    """, unsafe_allow_html=True)

with top2:
    st.markdown(
        """
        <div style="text-align:right;color:#405965;font-size:10px;margin-top:15px;">
            NODE STATUS<br>
            <span style="color:#42e8a7;font-size:13px;">● OPERATIONAL</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.markdown("<br>", unsafe_allow_html=True)

    # Stats

    cols = st.columns(4)

    stats = [
        ("TRANSACTIONS ANALYZED", "1,284", "+12.4%"),
        ("THREATS DETECTED", "137", "+8.7%"),
        ("VERIFICATION RATE", "98.2%", "+2.1%"),
        ("ACTIVE AGENTS", "06 / 06", "ONLINE")
    ]

    for col, (label, value, change) in zip(cols, stats):

        with col:
            st.markdown(
                f"""
                <div class="stat">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value">{value}</div>
                    <div class="stat-change">↗ {change}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Investigation

    st.markdown(
        '<div class="section-kicker">LIVE INVESTIGATION</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-head">Transaction Under Analysis</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1.35, 0.75])

    with left:

        st.markdown("""
        <div class="investigation">

            <div class="mini-label">TRANSACTION IDENTIFIER</div>
            <div class="txn-id">TXN-10492</div>

            <br>

            <div class="mini-label">MERCHANT</div>
            <div style="color:#dcecf1;font-size:15px;font-weight:600;">
                Amazon
            </div>

            <br>

            <div class="mini-label">TRANSACTION VALUE</div>
            <div class="txn-amount">₹75,000</div>

            <br>

            <div style="display:flex;gap:35px;">
                <div>
                    <div class="mini-label">LOCATION</div>
                    <div class="txn-meta">Hyderabad, IN</div>
                </div>

                <div>
                    <div class="mini-label">CHANNEL</div>
                    <div class="txn-meta">Online</div>
                </div>

                <div>
                    <div class="mini-label">DEVICE</div>
                    <div class="txn-meta">DEV-88421</div>
                </div>
            </div>

        </div>
        """, unsafe_allow_html=True)

    with right:

        st.markdown(f"""
        <div class="risk-panel">
            <div class="mini-label">AGGREGATED RISK SCORE</div>

            <div style="margin-top:15px;">
                <span class="risk-number">{risk_score}</span>
                <span class="risk-small"> / 100</span>
            </div>

            <div class="risk-high">HIGH RISK</div>

            <div style="
                margin-top:20px;
                height:5px;
                background:#20232b;
                border-radius:5px;
                overflow:hidden;
            ">
                <div style="
                    width:{risk_score}%;
                    height:100%;
                    background:#ff4d67;
                    box-shadow:0 0 12px #ff4d67;
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Agent pipeline

    st.markdown(
        '<div class="section-kicker">ORCHESTRATION LAYER</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-head">Multi-Agent Reasoning Pipeline</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="pipeline">', unsafe_allow_html=True)

    pipeline_cols = st.columns(11)

    for i, (num, name, status) in enumerate(agents):

        with pipeline_cols[i * 2]:

            st.markdown(
                f"""
                <div class="agent-node">
                    <div class="agent-icon">◉</div>
                    <div class="agent-name">{name}</div>
                    <div class="agent-state">ONLINE</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        if i < len(agents) - 1:

            with pipeline_cols[i * 2 + 1]:
                st.markdown(
                    '<div class="connector">›</div>',
                    unsafe_allow_html=True
                )

    st.markdown('</div>', unsafe_allow_html=True)

    # Evidence + activity

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1, 1])

    with left:

        st.markdown(
            '<div class="section-head">Evidence & Reasoning</div>',
            unsafe_allow_html=True
        )

        evidence_data = [
            ("01", "AMOUNT ANOMALY", "Transaction value exceeds normal threshold."),
            ("02", "CHANNEL SIGNAL", "Online transaction requires additional verification."),
            ("03", "VERIFICATION", "Independent verifier confirmed elevated indicators.")
        ]

        for number, title, text in evidence_data:

            st.markdown(
                f"""
                <div class="evidence-card">
                    <div class="evidence-number">{number}</div>
                    <div class="evidence-title">{title}</div>
                    <div class="evidence-text">{text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with right:

        st.markdown(
            '<div class="section-head">Activity Stream</div>',
            unsafe_allow_html=True
        )

        activity_data = [
            ("20:04:01", "Pattern Agent completed analysis"),
            ("20:04:02", "Risk Agent generated risk indicators"),
            ("20:04:03", "History Agent completed verification"),
            ("20:04:04", "Fraud Analyst consolidated findings"),
            ("20:04:05", "Independent Verifier confirmed risk"),
            ("20:04:06", "Critic completed final review")
        ]

        st.markdown('<div class="activity">', unsafe_allow_html=True)

        for time, text in activity_data:

            st.markdown(
                f"""
                <div class="activity-row">
                    <div class="activity-time">{time}</div>
                    <div class="activity-dot">●</div>
                    <div class="activity-text">{text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # Final decision

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="decision">

        <div class="decision-icon">⚠</div>

        <div class="decision-title">
            TRANSACTION REQUIRES VERIFICATION
        </div>

        <div class="decision-sub">
            Multi-agent assessment produced a high-risk classification.
            Additional verification is recommended before approval.
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# TRANSACTION LAB
# ============================================================

elif page == "Transaction Lab":

    st.markdown("## Transaction Investigation Lab")

    st.caption(
        "Submit a transaction and initiate the multi-agent reasoning pipeline."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 0.8])

    with col1:

        st.markdown(
            '<div class="section-kicker">INPUT CHANNEL</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-head">Transaction Parameters</div>',
            unsafe_allow_html=True
        )

        transaction_id = st.text_input(
            "Transaction ID",
            placeholder="TXN-XXXXX"
        )

        merchant = st.text_input(
            "Merchant",
            placeholder="Merchant name"
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=100.0
        )

        location = st.text_input(
            "Location",
            placeholder="City / Region"
        )

        device_id = st.text_input(
            "Device ID",
            placeholder="DEV-XXXXX"
        )

        transaction_type = st.selectbox(
            "Transaction Channel",
            ["Online", "ATM", "POS", "Bank Transfer"]
        )

        st.markdown("<br>", unsafe_allow_html=True)

        analyze = st.button(
            "◈ INITIATE MULTI-AGENT ANALYSIS",
            use_container_width=True
        )

    with col2:

        st.markdown(
            '<div class="section-kicker">ENGINE STATUS</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-head">Agent Readiness</div>',
            unsafe_allow_html=True
        )

        for num, name, status in agents:

            st.markdown(
                f"""
                <div class="evidence-card">
                    <span style="color:#00d9ff;font-size:10px;">
                        {num}
                    </span>
                    <span style="color:#dcecf1;font-size:11px;font-weight:600;">
                        &nbsp; {name} AGENT
                    </span>
                    <span style="float:right;color:#42e8a7;font-size:9px;">
                        READY
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

    if analyze:

        if not transaction_id or not merchant or not location or not device_id:

            st.warning(
                "Complete all transaction fields before initiating analysis."

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
                "Transaction accepted. Analysis pipeline initiated."
            )

            st.markdown("### Analysis Result")

            r1, r2 = st.columns(2)

            with r1:

                st.markdown(
                    f"""
                    <div class="investigation">
                        <div class="mini-label">TRANSACTION</div>
                        <div class="txn-id">{transaction_id}</div>
                        <br>
                        <div class="mini-label">MERCHANT</div>
                        <div style="color:#dcecf1;">{merchant}</div>
                        <br>
                        <div class="mini-label">VALUE</div>
                        <div class="txn-amount">₹{amount:,.2f}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with r2:

                st.markdown(
                    f"""
                    <div class="risk-panel">
                        <div class="mini-label">AI RISK ASSESSMENT</div>
                        <div style="margin-top:15px;">
                            <span class="risk-number">{risk_score}</span>
                            <span class="risk-small"> / 100</span>
                        </div>
                        <div class="risk-high">HIGH RISK</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("### Agent Pipeline")

            for num, name, status in agents:

                st.markdown(
                    f"""
                    <div class="evidence-card">
                        <span style="color:#00e5ff;">◉</span>
                        <span style="color:#dcecf1;font-weight:600;">
                            &nbsp; {name} AGENT
                        </span>
                        <span style="float:right;color:#42e8a7;">
                            ✓ COMPLETE
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("### Final Decision")

            st.markdown("""
            <div class="decision">
                <div class="decision-icon">⚠</div>
                <div class="decision-title">
                    HIGH RISK
                </div>
                <div class="decision-sub">
                    Transaction requires additional verification.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.info(
                "DEMO MODE — risk score and agent responses are currently "
                "mock values. They will be replaced with the actual "
                "backend outputs during integration."
            )


# ============================================================
# AGENT NETWORK
# ============================================================

elif page == "Agent Network":

    st.markdown("## Agent Network")

    st.caption(
        "Six specialized AI components working together through the reasoning pipeline."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    agent_descriptions = [
        ("01", "Transaction Pattern Agent",
         "Analyzes transaction patterns and identifies unusual behavior."),

        ("02", "Risk Agent",
         "Evaluates transaction-level risk indicators."),

        ("03", "History Agent",
         "Checks historical transaction behavior."),

        ("04", "Fraud Analyst",
         "Combines findings from specialized agents."),

        ("05", "Independent Verifier",
         "Performs independent verification of the proposed assessment."),

        ("06", "Critic",
         "Reviews the reasoning and identifies inconsistencies.")
    ]

    for i in range(0, len(agent_descriptions), 2):

        cols = st.columns(2)

        for j, col in enumerate(cols):

            if i + j >= len(agent_descriptions):
                continue

            num, name, description = agent_descriptions[i + j]

            with col:

                st.markdown(
                    f"""
                    <div class="investigation" style="margin-bottom:15px;">

                        <div style="
                            color:#00e5ff;
                            font-size:10px;
                            letter-spacing:2px;
                        ">
                            AGENT {num}
                        </div>

                        <div style="
                            font-family:'Space Grotesk';
                            color:#e9fbff;
                            font-size:20px;
                            font-weight:700;
                            margin-top:7px;
                        ">
                            {name}
                        </div>

                        <div style="
                            color:#637b87;
                            font-size:11px;
                            margin-top:10px;
                            line-height:1.6;
                        ">
                            {description}
                        </div>

                        <div style="
                            margin-top:18px;
                            color:#42e8a7;
                            font-size:9px;
                            letter-spacing:1px;
                        ">
                            ● READY FOR INTEGRATION
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# EVALUATION
# ============================================================

elif page == "Evaluation":

    st.markdown("## Evaluation & Validation")

    st.caption(
        "Benchmark the fraud detection engine against predefined transaction scenarios."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Metrics

    cols = st.columns(4)

    metrics = [
        ("TEST CASES", "20"),
        ("PASSED", "18"),
        ("FAILED", "02"),
        ("ACCURACY", "90%")
    ]

    for col, (label, value) in zip(cols, metrics):

        with col:

            st.markdown(
                f"""
                <div class="stat">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Test Case Matrix")

    test_cases = [
        ["TC-001", "Normal POS", "₹500", "LOW", "LOW", "✓ PASS"],
        ["TC-002", "Large Online", "₹75,000", "HIGH", "HIGH", "✓ PASS"],
        ["TC-003", "ATM Withdrawal", "₹25,000", "MEDIUM", "MEDIUM", "✓ PASS"],
        ["TC-004", "Large Transfer", "₹1,50,000", "HIGH", "HIGH", "✓ PASS"],
        ["TC-005", "Small Online", "₹1,500", "LOW", "LOW", "✓ PASS"],
    ]

    st.dataframe(
        test_cases,
        column_config={
            0: "ID",
            1: "Scenario",
            2: "Amount",
            3: "Expected",
            4: "Actual",
            5: "Status"
        },
        hide_index=True,
        use_container_width=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Validation Timeline")

    timeline = [
        ("T+00", "Transaction dataset loaded"),
        ("T+01", "Pattern analysis executed"),
        ("T+02", "Risk assessment executed"),
        ("T+03", "Historical verification executed"),
        ("T+04", "Fraud analysis executed"),
        ("T+05", "Independent verification executed"),
        ("T+06", "Critic review completed")
    ]

    st.markdown('<div class="timeline">', unsafe_allow_html=True)

    for time, event in timeline:

        st.markdown(
            f"""
            <div class="timeline-row">
                <div class="timeline-time">{time}</div>
                <div class="timeline-dot">●</div>
                <div class="timeline-text">{event}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.warning(
        "DEMO EVALUATION — current values are placeholders for frontend "
        "testing. Final evaluation will use the integrated agent outputs."
    )
                "🟢 LOW RISK — TRANSACTION APPEARS SAFE"
            )

        st.info(
            "ℹ️ Agent outputs shown here are currently demonstration "
            "results. They will be connected to the actual AI agents "
            "once the agent module is integrated."
        )

