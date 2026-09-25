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

        # --------------------------------------------------------
        # GET PREVIOUS TRANSACTIONS FROM DATABASE
        # --------------------------------------------------------

        history = get_transaction_history(
            transaction.transaction_id
        )

        # --------------------------------------------------------
        # NO HISTORY AVAILABLE
        # --------------------------------------------------------

        if not history:

            return AgentResult(
                agent_name=self.name,
                risk_level="LOW",
                reason=(
                    "No previous transaction history is available "
                    "for comparison."
                ),
                evidence=[
                    "No historical transactions found in the database."
                ],
                confidence=0.50
            )

        # --------------------------------------------------------
        # CALCULATE HISTORICAL AVERAGE
        # --------------------------------------------------------

        average_amount = sum(history) / len(history)

        current_amount = transaction.amount

        # --------------------------------------------------------
        # COMPARE CURRENT TRANSACTION WITH HISTORY
        # --------------------------------------------------------

        evidence = []

        ratio = current_amount / average_amount

        evidence.append(
            f"Historical transaction count: {len(history)}."
        )

        evidence.append(
            f"Historical average amount: ₹{average_amount:,.2f}."
        )

        evidence.append(
            f"Current transaction amount: ₹{current_amount:,.2f}."
        )

        # --------------------------------------------------------
        # RISK CLASSIFICATION
        # --------------------------------------------------------

        if ratio >= 10:

            risk_level = "HIGH"

            reason = (
                "Current transaction amount is extremely higher "
                "than the user's historical average."
            )

            confidence = 0.90

            evidence.append(
                f"Current amount is {ratio:.1f}x the historical average."
            )

        elif ratio >= 3:

            risk_level = "MEDIUM"

            reason = (
                "Current transaction amount is significantly higher "
                "than the user's historical average."
            )

            confidence = 0.75

            evidence.append(
                f"Current amount is {ratio:.1f}x the historical average."
            )

        elif ratio >= 2:

            risk_level = "MEDIUM"

            reason = (
                "Current transaction amount is noticeably higher "
                "than the user's historical average."
            )

            confidence = 0.65

            evidence.append(
                f"Current amount is {ratio:.1f}x the historical average."
            )

        else:

            risk_level = "LOW"

            reason = (
                "Current transaction amount is reasonably "
                "consistent with historical spending."
            )

            confidence = 0.80

            evidence.append(
                f"Current amount is {ratio:.1f}x the historical average."
            )

        # --------------------------------------------------------
        # FEEDBACK INFORMATION
        # --------------------------------------------------------

        if feedback:

            evidence.append(
                "Previous verifier feedback was considered "
                "during re-analysis."
            )

        # --------------------------------------------------------
        # RETURN RESULT
        # --------------------------------------------------------

        return AgentResult(
            agent_name=self.name,
            risk_level=risk_level,
            reason=reason,
            evidence=evidence,
            confidence=confidence
        )
