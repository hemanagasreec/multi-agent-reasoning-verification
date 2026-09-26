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
import json

from agents.base_agent import BaseAgent
from core.schemas import Transaction, AgentResult
from agents.gemini_client import ask_gemini
from database.database import get_transaction_history
import json


class PatternAgent(BaseAgent):

    def __init__(self):
        super().__init__("Pattern Agent")

    def analyze(
        self,
        transaction: Transaction,
        feedback: str = None
    ) -> AgentResult:

        correction_feedback = feedback or "No previous verifier feedback."

        prompt = f"""
You are a financial fraud pattern analysis agent.

Analyze this transaction ONLY for suspicious transaction patterns.

Transaction:
- ID: {transaction.transaction_id}
- Amount: ₹{transaction.amount}
- Location: {transaction.location}
- Device: {transaction.device}
- Timestamp: {transaction.timestamp}

Previous verifier feedback:
{correction_feedback}

Return ONLY valid JSON in exactly this format:

{{
    "risk_level": "LOW",
    "reason": "short explanation",
    "evidence": ["evidence 1", "evidence 2"],
    "confidence": 0.80
}}

Rules:
- risk_level must be exactly LOW, MEDIUM, or HIGH.
- confidence must be between 0.0 and 1.0.
- Evidence must contain concrete observations from the transaction.
- Do not invent transaction information.
- Do not automatically call an unusual transaction fraud.
"""

        try:

            response = ask_gemini(prompt)

            response = response.strip()

            if response.startswith("```"):
                response = response.replace("```json", "", 1)
                response = response.replace("```", "", 1)
                response = response.strip()

            data = json.loads(response)

            return AgentResult(
                agent_name=self.name,
                risk_level=data["risk_level"].upper(),
                reason=data["reason"],
                evidence=data["evidence"],
                confidence=float(data["confidence"])
            )

        except RuntimeError:

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
            # 2. Device anomaly
            # --------------------------------------------------

            if "new" in transaction.device.lower():

                evidence.append(
                    "Transaction was initiated from a new device."
                )

                risk_score += 0.2

            # --------------------------------------------------
            # 3. Location anomaly
            # --------------------------------------------------

            if "unknown" in transaction.location.lower():

                evidence.append(
                    "Transaction originated from an unknown location."
                )

                risk_score += 0.2

            # --------------------------------------------------
            # 4. Time anomaly
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
                    "Multiple suspicious transaction patterns "
                    "were detected."
                )

            elif risk_level == "MEDIUM":

                reason = (
                    "One or more suspicious transaction patterns "
                    "were detected."
                )

            else:

                reason = (
                    "No major suspicious transaction patterns "
                    "were detected."
                )

            if not evidence:

                evidence.append(
                    "No major suspicious transaction patterns detected."
                )

            confidence = min(
                0.90,
                0.55 + risk_score * 0.35
            )

            return AgentResult(
                agent_name=self.name,
                risk_level=risk_level,
                reason=reason,
                evidence=evidence,
                confidence=round(confidence, 2)
            )

        except (
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError
        ):

            return AgentResult(
                agent_name=self.name,
                risk_level="MEDIUM",
                reason=(
                    "Pattern Agent could not reliably parse "
                    "the AI response."
                ),
                evidence=[
                    "Invalid or unexpected Gemini response."
                ],
                confidence=0.30
            )
