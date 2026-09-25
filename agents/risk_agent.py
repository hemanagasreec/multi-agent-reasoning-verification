# agents/risk_agent.py
from typing import Dict, Any
from agents.base_agent import BaseAgent
from schemas.transaction import AgentOutput

class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="RiskAgent")

    def analyze(self, context: Dict[str, Any]) -> AgentOutput:
        evidence = []
        points = 0

        if context.get("is_new_device", False):
            evidence.append("Initiated from an unrecognized device hardware fingerprint.")
            points += 30

        if context.get("is_new_location", False):
            evidence.append(f"Originates from new location: {context.get('location', 'Unknown IP')}.")
            points += 20

        rapid_txs = context.get("rapid_succession_count", 0)
        if rapid_txs >= 3:
            evidence.append(f"High velocity: {rapid_txs} transactions within 5 minutes.")
            points += 40

        hour = context.get("hour_of_day", 12)
        if 1 <= hour <= 4:
            evidence.append(f"Executed during off-hours window ({hour}:00 AM).")
            points += 15

        risk_level = "HIGH" if points >= 50 else ("MEDIUM" if points >= 25 else "LOW")
        if risk_level == "LOW":
            evidence.append("Environmental contextual factors align with low-risk baseline.")

        return AgentOutput(
            agent_name=self.name,
            risk=risk_level,
            reason=f"Environmental risk score elevated ({points}/100 points)" if risk_level != "LOW" else "Low risk environment",
            evidence=evidence,
            confidence=round(min(0.98, 0.50 + (points / 120)), 2)
        )