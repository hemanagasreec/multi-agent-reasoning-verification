from agents.base_agent import BaseAgent
from core.schemas import Transaction, AgentResult
from database.database import get_transaction_history


class RiskAgent(BaseAgent):

    def __init__(self):
        super().__init__("Risk Agent")

    def analyze(
        self,
        transaction: Transaction,
        feedback: str = None
    ) -> AgentResult:

        evidence = []
        risk_score = 0.0

        # --------------------------------------------------
        # 1. Historical amount anomaly
        # --------------------------------------------------

        history = get_transaction_history(
            transaction.transaction_id
        )

        if history:

            average_amount = sum(history) / len(history)

            if average_amount > 0:

                ratio = transaction.amount / average_amount

                if ratio >= 10:

                    evidence.append(
                        f"Transaction amount is {ratio:.1f}x "
                        "the historical transaction baseline."
                    )

                    risk_score += 0.6

                elif ratio >= 3:

                    evidence.append(
                        f"Transaction amount is {ratio:.1f}x "
                        "the historical transaction baseline."
                    )

                    risk_score += 0.4

                elif ratio >= 2:

                    evidence.append(
                        f"Transaction amount is {ratio:.1f}x "
                        "the historical transaction baseline."
                    )

                    risk_score += 0.2

        # --------------------------------------------------
        # 2. New device
        # --------------------------------------------------

        if "new" in transaction.device.lower():

            evidence.append(
                "Transaction was initiated from a new device."
            )

            risk_score += 0.2

        # --------------------------------------------------
        # 3. Unknown location
        # --------------------------------------------------

        if "unknown" in transaction.location.lower():

            evidence.append(
                "Transaction originated from an unknown location."
            )

            risk_score += 0.2

        # --------------------------------------------------
        # 4. Unusual transaction time
        # --------------------------------------------------

        try:

            hour = int(
                transaction.timestamp.split()[1].split(":")[0]
            )

            if 1 <= hour <= 4:

                evidence.append(
                    f"Transaction occurred during unusual hours: {hour}:00."
                )

                risk_score += 0.2

        except (IndexError, ValueError):

            evidence.append(
                "Transaction timestamp could not be fully analyzed."
            )

            risk_score += 0.1

        # --------------------------------------------------
        # 5. Risk classification
        # --------------------------------------------------

        if risk_score >= 0.7:

            risk_level = "HIGH"

        elif risk_score >= 0.3:

            risk_level = "MEDIUM"

        else:

            risk_level = "LOW"

        # --------------------------------------------------
        # 6. Reason
        # --------------------------------------------------

        if risk_level == "HIGH":

            reason = (
                "Multiple independent risk indicators "
                "were detected."
            )

        elif risk_level == "MEDIUM":

            reason = (
                "One or more transaction risk indicators "
                "were detected."
            )

        else:

            reason = (
                "No major transaction risk indicators "
                "were detected."
            )

        if not evidence:

            evidence.append(
                "No major transaction risk indicators detected."
            )

        confidence = min(
            0.90,
            0.60 + risk_score * 0.30
        )

        return AgentResult(
            agent_name=self.name,
            risk_level=risk_level,
            reason=reason,
            evidence=evidence,
            confidence=round(confidence, 2)
        )
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
