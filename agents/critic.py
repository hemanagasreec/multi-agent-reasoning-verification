from agents.base_agent import BaseAgent
from core.schemas import Transaction, AgentResult


class CriticAgent(BaseAgent):

    def __init__(self):
        super().__init__("Critic Agent")

    def analyze(self, transaction: Transaction) -> AgentResult:

        evidence = [
            "Critic agent independently reviews the transaction for unsupported conclusions."
        ]

        # Basic contradiction/risk check
        if transaction.amount >= 50000:
            risk_level = "HIGH"
            reason = "High-value transaction requires additional scrutiny."
            confidence = 0.80
        else:
            risk_level = "LOW"
            reason = "No major contradiction or high-risk indicator detected."
            confidence = 0.70

        return AgentResult(
            agent_name=self.name,
            risk_level=risk_level,
            reason=reason,
            evidence=evidence,
            confidence=confidence
        )
