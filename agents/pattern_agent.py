from agents.base_agent import BaseAgent
from core.schemas import Transaction, AgentResult
from agents.gemini_client import ask_gemini
import json


class PatternAgent(BaseAgent):

    def __init__(self):
        super().__init__("Pattern Agent")

    def analyze(
        self,
        transaction: Transaction,
        feedback: str = None
    ) -> AgentResult:

        correction_feedback = feedback or "No previous verification feedback."

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

If this is a re-analysis, specifically reconsider the issue mentioned
in the verifier feedback and check whether your previous conclusion
was properly supported by the transaction evidence.

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
- If there is not enough evidence, use LOW or MEDIUM with appropriate confidence.
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

        except RuntimeError as e:

            # ------------------------------------------------
            # RULE-BASED FALLBACK
            # ------------------------------------------------
            # Gemini may be temporarily unavailable or
            # rate-limited. The agent still performs analysis.

            evidence = []
            risk_score = 0.0

            if "new" in transaction.device.lower():

                evidence.append(
                    "Transaction was initiated from a new device."
                )

                risk_score += 0.4

            if "unknown" in transaction.location.lower():

                evidence.append(
                    "Transaction originated from an unknown location."
                )

                risk_score += 0.3

            try:

                hour = int(
                    transaction.timestamp.split()[1].split(":")[0]
                )

                if 1 <= hour <= 4:

                    evidence.append(
                        f"Transaction occurred during unusual hours: {hour}:00."
                    )

                    risk_score += 0.3

            except (IndexError, ValueError):

                evidence.append(
                    "Transaction timestamp could not be fully analyzed."
                )

                risk_score += 0.1

            if risk_score >= 0.7:

                risk_level = "HIGH"

            elif risk_score >= 0.3:

                risk_level = "MEDIUM"

            else:

                risk_level = "LOW"

            if not evidence:

                evidence.append(
                    "No major suspicious transaction patterns detected."
                )

            confidence = min(
                0.85,
                0.55 + risk_score * 0.30
            )

            return AgentResult(
                agent_name=self.name,
                risk_level=risk_level,
                reason=(
                    "Rule-based fallback analysis completed because "
                    "the Gemini API is temporarily unavailable."
                ),
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
