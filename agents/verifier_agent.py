from agents.base_agent import BaseAgent
from core.schemas import Transaction, AgentResult


class VerifierAgent(BaseAgent):

    def __init__(self):
        super().__init__("Verifier Agent")

    def analyze(
        self,
        transaction: Transaction,
        feedback: str = None
    ) -> AgentResult:

        evidence = []
        risk_score = 0.0

        # --------------------------------------------------------
        # TRANSACTION ID CHECK
        # --------------------------------------------------------

        if not transaction.transaction_id.strip():

            evidence.append(
                "Transaction ID is missing."
            )

            risk_score += 0.3

        else:

            evidence.append(
                "Transaction ID is present."
            )

        # --------------------------------------------------------
        # AMOUNT CHECK
        # --------------------------------------------------------

        if transaction.amount <= 0:

            evidence.append(
                "Transaction amount is invalid."
            )

            risk_score += 0.5

        elif transaction.amount >= 100000:

            evidence.append(
                "Transaction amount is unusually high."
            )

            risk_score += 0.3

        else:

            evidence.append(
                "Transaction amount is within the expected positive range."
            )

        # --------------------------------------------------------
        # LOCATION CHECK
        # --------------------------------------------------------

        if not transaction.location.strip():

            evidence.append(
                "Transaction location is missing."
            )

            risk_score += 0.2

        else:

            evidence.append(
                "Transaction location is available for verification."
            )

        # --------------------------------------------------------
        # DEVICE CHECK
        # --------------------------------------------------------

        if not transaction.device.strip():

            evidence.append(
                "Transaction device information is missing."
            )

            risk_score += 0.2

        else:

            evidence.append(
                "Transaction device information is available."
            )

        # --------------------------------------------------------
        # TIMESTAMP CHECK
        # --------------------------------------------------------

        if not transaction.timestamp.strip():

            evidence.append(
                "Transaction timestamp is missing."
            )

            risk_score += 0.2

        else:

            evidence.append(
                "Transaction timestamp is available."
            )

        # --------------------------------------------------------
        # RISK CLASSIFICATION
        # --------------------------------------------------------

        if risk_score >= 0.7:

            risk_level = "HIGH"

        elif risk_score >= 0.3:

            risk_level = "MEDIUM"

        else:

            risk_level = "LOW"

        confidence = min(
            0.95,
            0.70 + risk_score * 0.25
        )

        if risk_level == "HIGH":

            reason = (
                "Independent verification detected "
                "multiple transaction consistency problems."
            )

        elif risk_level == "MEDIUM":

            reason = (
                "Independent verification detected "
                "transaction information requiring additional review."
            )

        else:

            reason = (
                "Independent verification found the "
                "transaction information internally consistent."
            )

        return AgentResult(
            agent_name=self.name,
            risk_level=risk_level,
            reason=reason,
            evidence=evidence,
            confidence=round(confidence, 2)
        )
