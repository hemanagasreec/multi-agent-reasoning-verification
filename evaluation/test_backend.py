from core.schemas import Transaction, AgentResult
from core.orchestrator import Orchestrator


class TestAgent:

    def __init__(self, name, risk, confidence):
        self.name = name
        self.risk = risk
        self.confidence = confidence

    def analyze(self, transaction):
        return AgentResult(
            agent_name=self.name,
            risk_level=self.risk,
            reason="Test analysis",
            evidence=["Test evidence"],
            confidence=self.confidence
        )


transaction = Transaction(
    transaction_id="TX001",
    amount=50000,
    location="Unknown",
    device="New Device",
    timestamp="2026-09-25 14:00"
)

agents = [
    TestAgent("Pattern Agent", "HIGH", 0.90),
    TestAgent("Risk Agent", "HIGH", 0.85),
    TestAgent("History Agent", "LOW", 0.80)
]

orchestrator = Orchestrator()

final_result, agent_results, verification = orchestrator.run(
    transaction,
    agents
)

print("\n===== TEST RESULT =====")
print("Decision:", final_result.decision)
print("Confidence:", final_result.confidence)
print("Verification:", verification.status)
print("Verification Reason:", verification.reason)