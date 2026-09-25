import json

from agents import (
    PatternAgent,
    RiskAgent,
    HistoryAgent,
    VerifierAgent,
    CriticAgent
)

def run_demo():
    # Initialize agents
    pattern_agent = PatternAgent()
    risk_agent = RiskAgent()
    history_agent = HistoryAgent()
    verifier = VerifierAgent()
    critic = CriticAgent()

    # Mock incoming transaction data
    current_tx = {
        "amount": 75000,
        "category": "Electronics",
        "typical_range": [500, 2000]
    }
    
    risk_context = {
        "is_new_device": True,
        "is_new_location": True,
        "rapid_succession_count": 3,
        "hour_of_day": 2,
        "location": "Mumbai"
    }
    
    user_history = [500.0, 700.0, 1200.0, 800.0, 600.0]
    
    tx_metadata = {
        "merchant_category": "electronics",
        "user_income_bracket": "MEDIUM",
        "is_holiday_season": True
    }

    # Step 1: Run individual evaluation agents
    out_pattern = pattern_agent.analyze(current_tx)
    out_risk = risk_agent.analyze(risk_context)
    out_history = history_agent.analyze(current_tx["amount"], user_history)

    # Step 2: Run Verifier to synthesize findings
    out_verifier = verifier.analyze([out_pattern, out_risk, out_history])

    # Step 3: Run Critic to test false positive counter-evidence
    out_critic = critic.analyze(out_verifier, tx_metadata)

    # Output results to verify structure
    print("\n=== 1. PATTERN AGENT OUTPUT ===")
    print(json.dumps(out_pattern.model_dump(), indent=2))

    print("\n=== 2. RISK AGENT OUTPUT ===")
    print(json.dumps(out_risk.model_dump(), indent=2))

    print("\n=== 3. HISTORY AGENT OUTPUT ===")
    print(json.dumps(out_history.model_dump(), indent=2))

    print("\n=== 4. VERIFIER AGENT OUTPUT ===")
    print(json.dumps(out_verifier.model_dump(), indent=2))

    print("\n=== 5. CRITIC AGENT FINAL DECISION ===")
    print(json.dumps(out_critic.model_dump(), indent=2))

if __name__ == "__main__":
    run_demo()