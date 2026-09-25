from agents.base_agent import BaseAgent
from core.schemas import Transaction, AgentResult
from agents.gemini_client import ask_gemini
import json


class PatternAgent(BaseAgent):

    def __init__(self):
        super().__init__("Pattern Agent")

    def analyze(self, transaction: Transaction) -> AgentResult:

        prompt = f"""
You are a financial fraud pattern analysis agent.

Analyze this transaction ONLY for suspicious transaction patterns.

Transaction:
- ID: {transaction.transaction_id}
- Amount: ₹{transaction.amount}
- Location: {transaction.location}
- Device: {transaction.device}
- Timestamp: {transaction.timestamp}

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

        response = ask_gemini(prompt)

        try:
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

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):

            return AgentResult(
                agent_name=self.name,
                risk_level="MEDIUM",
                reason="Pattern Agent could not reliably parse the AI response.",
                evidence=["Invalid or unexpected Gemini response."],
                confidence=0.30
            )
