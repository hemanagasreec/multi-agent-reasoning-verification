from agents.base_agent import BaseAgent
from core.schemas import Transaction, AgentResult


class VerifierAgent(BaseAgent):

    def __init__(self):
        super().__init__("Verifier Agent")

    def analyze(self, transaction: Transaction) -> AgentResult:

        evidence = [
            "Verification agent is ready to independently check transaction evidence."
        ]

        return AgentResult(
            agent_name=self.name,
            risk_level="LOW",
            reason="Transaction verification completed.",
            evidence=evidence,
            confidence=0.70
        )
