from agents.base_agent import BaseAgent
from core.schemas import Transaction, AgentResult


class HistoryAgent(BaseAgent):

    def __init__(self):
        super().__init__("History Agent")

    def analyze(
    self,
    transaction: Transaction,
    feedback: str = None
) -> AgentResult:

        evidence = []

        # Demo historical transaction data
        history = [800, 1200, 1500, 1000, 1800]

        average = sum(history) / len(history)

        if transaction.amount >= average * 10:
            risk_level = "HIGH"
            reason = "Transaction is extremely higher than historical spending."
            evidence.append(
                f"Current amount ₹{transaction.amount:,.2f} is more than 10x "
                f"historical average ₹{average:,.2f}."
            )
            confidence = 0.90

        elif transaction.amount >= average * 3:
            risk_level = "MEDIUM"
            reason = "Transaction is significantly higher than historical spending."
            evidence.append(
                f"Current amount ₹{transaction.amount:,.2f} is significantly "
                f"higher than historical average ₹{average:,.2f}."
            )
            confidence = 0.75

        else:
            risk_level = "LOW"
            reason = "Transaction is consistent with historical spending."
            evidence.append(
                f"Historical average spending is ₹{average:,.2f}."
            )
            confidence = 0.80

        return AgentResult(
            agent_name=self.name,
            risk_level=risk_level,
            reason=reason,
            evidence=evidence,
            confidence=confidence
        )
