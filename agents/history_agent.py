# agents/history_agent.py
import numpy as np
from typing import List
from agents.base_agent import BaseAgent
from schemas.transaction import AgentOutput

class HistoryAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="HistoryAgent")

    def analyze(self, current_amount: float, history: List[float]) -> AgentOutput:
        evidence = []
        
        if not history or len(history) < 2:
            return AgentOutput(
                agent_name=self.name,
                risk="MEDIUM",
                reason="Insufficient account history to build a statistical baseline",
                evidence=["Fewer than 2 historical transactions available."],
                confidence=0.5
            )

        mean_val = float(np.mean(history))
        std_val = float(np.std(history)) if np.std(history) > 0 else 1.0
        z_score = (current_amount - mean_val) / std_val
        multiplier = current_amount / mean_val if mean_val > 0 else 0.0

        if z_score > 3.0 or multiplier >= 10:
            risk_level = "HIGH"
            reason = f"Extreme deviation from history (Z-score: {z_score:.2f})"
            evidence.append(f"Current amount (₹{current_amount:,}) is {multiplier:.1f}x higher than historical mean (₹{mean_val:,.2f}).")
        elif z_score > 1.8 or multiplier >= 3:
            risk_level = "MEDIUM"
            reason = f"Moderate baseline shift (Z-score: {z_score:.2f})"
            evidence.append(f"Current amount is {multiplier:.1f}x historical average.")
        else:
            risk_level = "LOW"
            reason = "Matches user transaction history"
            evidence.append(f"Amount falls within standard historical bounds (Avg: ₹{mean_val:,.2f}).")

        return AgentOutput(
            agent_name=self.name,
            risk=risk_level,
            reason=reason,
            evidence=evidence,
            confidence=round(min(0.95, 0.65 + (abs(z_score) * 0.08)), 2)
        )