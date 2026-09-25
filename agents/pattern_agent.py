import json

from agents.base_agent import BaseAgent
from agents.gemini_client import ask_gemini
from core.schemas import Transaction, AgentResult


class PatternAgent(BaseAgent):

    def __init__(self):
        super().__init__("Pattern Agent")

    def analyze(self, transaction: Transaction) -> AgentResult:

        prompt = f"""
You are a financial fraud pattern detection agent.

Analyze the following transaction for suspicious patterns.

Transaction:
- ID: {transaction.transaction_id}
- Amount: ₹{transaction.amount}
- Location: {transaction.location}
- Device: {transaction.device}
- Timestamp: {transaction.timestamp}

Look for indicators such as:
- Unusually high transaction amount
- Unusual location
- New or unfamiliar device
- Unusual transaction time
- Combination of multiple suspicious indicators

IMPORTANT:
Do not automatically call an unusual transaction fraud.
If evidence is insufficient, use MEDIUM or LOW risk.

Return ONLY valid JSON in exactly this format:

{{
    "risk_level": "LOW",
    "reason": "short explanation",
    "evidence": ["evidence 1", "evidence 2"],
    "confidence": 0.80
}}

risk_level must be exactly one of:
LOW, MEDIUM, HIGH

confidence must be a number between 0 and 1.
"""

        response = ask_gemini(prompt)

        try:
            data = json.loads(response)

            return AgentResult(
                agent_name=self.name,
                risk_level=data["risk_level"],
                reason=data["reason"],
                evidence=data["evidence"],
                confidence=float(data["confidence"])
            )

        except Exception as e:
            return AgentResult(
                agent_name=self.name,
                risk_level="MEDIUM",
                reason="Pattern analysis could not be reliably parsed.",
                evidence=[f"Parser error: {str(e)}"],
                confidence=0.40
            )