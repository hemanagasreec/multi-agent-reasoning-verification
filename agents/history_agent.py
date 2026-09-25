from agents.base_agent import BaseAgent
from core.schemas import Transaction, AgentResult
from database.database import get_transaction_history


class HistoryAgent(BaseAgent):

    def __init__(self):
        super().__init__("History Agent")

    def analyze(
        self,
        transaction: Transaction,
        feedback: str = None
    ) -> AgentResult:

        history = get_transaction_history(
            transaction.transaction_id
        )

        if not history:

            return AgentResult(
                agent_name=self.name,
                risk_level="LOW",
                reason=(
                    "No previous transaction history is available "
                    "for comparison."
                ),
                evidence=[
                    "No historical transactions found "
                    "in the database."
                ],
                confidence=0.50
            )

        average_amount = sum(history) / len(history)

        current_amount = transaction.amount

        evidence = []

        ratio = current_amount / average_amount

        evidence.append(
            f"Historical transaction count: {len(history)}."
        )

        evidence.append(
            f"Historical transaction baseline average: "
            f"₹{average_amount:,.2f}."
        )

        evidence.append(
            f"Current transaction amount: "
            f"₹{current_amount:,.2f}."
        )

        # Extremely large deviation
        if ratio >= 10:

            risk_level = "HIGH"

            reason = (
                "The current transaction amount is extremely "
                "higher than the historical transaction baseline."
            )

            confidence = 0.90

            evidence.append(
                f"Current amount is {ratio:.1f}x the "
                "historical transaction baseline."
            )

        # Significant deviation
        elif ratio >= 3:

            risk_level = "MEDIUM"

            reason = (
                "The current transaction amount is significantly "
                "higher than the historical transaction baseline."
            )

            confidence = 0.75

            evidence.append(
                f"Current amount is {ratio:.1f}x the "
                "historical transaction baseline."
            )

        # Noticeable deviation
        elif ratio >= 2:

            risk_level = "MEDIUM"

            reason = (
                "The current transaction amount is noticeably "
                "higher than the historical transaction baseline."
            )

            confidence = 0.65

            evidence.append(
                f"Current amount is {ratio:.1f}x the "
                "historical transaction baseline."
            )

        # Normal range
        else:

            risk_level = "LOW"

            reason = (
                "The current transaction amount is reasonably "
                "consistent with the historical transaction baseline."
            )

            confidence = 0.80

            evidence.append(
                f"Current amount is {ratio:.1f}x the "
                "historical transaction baseline."
            )

        if feedback:

            evidence.append(
                "Previous verifier feedback was considered "
                "during re-analysis."
            )

        return AgentResult(
            agent_name=self.name,
            risk_level=risk_level,
            reason=reason,
            evidence=evidence,
            confidence=confidence
        )
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
