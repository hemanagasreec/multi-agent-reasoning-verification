# agents/pattern_agent.py
from typing import Dict, Any
from agents.base_agent import BaseAgent
from schemas.transaction import AgentOutput

class PatternAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="PatternAgent")

    def analyze(self, transaction: Dict[str, Any]) -> AgentOutput:
        amount = transaction.get("amount", 0)
        typical_range = transaction.get("typical_range", [500, 2000])
        category = transaction.get("category", "General")
        
        evidence = []
        risk_score = 0.0
        max_expected = typical_range[1]

        # Anomaly checks
        if amount >= max_expected * 10:
            evidence.append(f"Amount ₹{amount:,} is over 10x the typical upper limit (₹{max_expected:,}) for {category}.")
            risk_score += 0.85
        elif amount > max_expected * 2:
            evidence.append(f"Amount ₹{amount:,} exceeds usual spending range (₹{typical_range[0]}-₹{max_expected}).")
            risk_score += 0.4

        # Sub-threshold structuring pattern
        if 45000 <= amount <= 49999:
            evidence.append("Transaction amount is structured just under the ₹50,000 regulatory reporting threshold.")
            risk_score += 0.3

        risk_level = "HIGH" if risk_score >= 0.7 else ("MEDIUM" if risk_score >= 0.3 else "LOW")
        if risk_level == "LOW":
            evidence.append("Transaction value conforms to normal distribution patterns.")

        return AgentOutput(
            agent_name=self.name,
            risk=risk_level,
            reason="High transaction amount anomaly detected" if risk_level != "LOW" else "Normal spending pattern",
            evidence=evidence,
            confidence=round(min(0.95, 0.60 + (risk_score * 0.35)), 2)
        )