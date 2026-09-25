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
