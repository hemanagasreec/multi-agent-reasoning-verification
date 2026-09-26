# Multi-Agent Financial Fraud Detection & Verification Engine

## Problem Statement

Financial fraud detection systems can produce incorrect or unsupported decisions when transaction information is incomplete, conflicting, or misleading. A reliable system needs independent analysis and verification before accepting a fraud decision.

## Solution

We developed a **multi-agent AI fraud detection and verification engine**. Multiple specialized agents independently analyze a transaction, generate evidence, detect suspicious patterns, and verify each other's conclusions. If conflicting evidence is detected, the system performs re-analysis before making a final decision.

## Key Features

* 🤖 Multi-agent transaction analysis
* 🔍 Independent verification
* 📊 Risk and fraud pattern detection
* 📚 Historical transaction baseline analysis
* ⚠️ Contradiction and unsupported-evidence detection
* 🔄 Self-correction and re-verification
* 🧾 Structured evidence and audit information
* 🎯 Final decision with confidence level
* 🖥️ Interactive Streamlit dashboard

## Agent Architecture

**Pattern Agent → Risk Agent → History Agent → Verifier → Critic → Analyst → Decision Engine**

The system separates **generation, verification, criticism, and final decision-making**.

## Tech Stack

* **Python**
* **Streamlit**
* **Google Gemini API**
* **Pydantic**
* **SQLite**
* **Git & GitHub**

## Team Members

* **Nandhini A** — Frontend & Evaluation
* **Meghana p** — AI Agents & Prompt Engineering
* **Hemanagasree C** — Backend & Multi-Agent Orchestration

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/hemanagasreec/multi-agent-reasoning-verification.git
cd multi-agent-reasoning-verification
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API key

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

### 5. Run the application

```bash
streamlit run app.py
```

## Deployment

**Live Demo:** `[Add deployed URL here]`

## Repository

**GitHub:** https://github.com/hemanagasreec/multi-agent-reasoning-verification

> Built for **HackFusion 2026 – IEEE Robotics & Automation Society**.
