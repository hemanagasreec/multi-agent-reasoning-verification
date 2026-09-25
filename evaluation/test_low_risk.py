from core.schemas import Transaction
from core.orchestrator import Orchestrator

from agents import (
    PatternAgent,
    RiskAgent,
    HistoryAgent,
    CriticAgent,
    VerifierAgent,
    AnalystAgent
)


transaction = Transaction(
    transaction_id="LOW001",
    amount=1000,
    location="Known Location",
    device="Known Device",
    timestamp="2026-09-25 14:00"
)


agents = [
    PatternAgent(),
    RiskAgent(),
    HistoryAgent(),
    CriticAgent(),
    VerifierAgent(),
    AnalystAgent()
]


orchestrator = Orchestrator()


final_result, agent_results, verification, evidence_records = orchestrator.run(
    transaction,
    agents
)


print("\n========== LOW-RISK TEST ==========")
print("Final Decision:", final_result.decision)
print("Confidence:", final_result.confidence)
print("Revision:", final_result.revision)

print("\n========== VERIFICATION ==========")
print("Status:", verification.status)
print("Reason:", verification.reason)
print("Confidence:", verification.confidence)
print("Revision:", verification.revision)

print("\n========== AGENTS ==========")

for result in agent_results:
    print(
        f"{result.agent_name}: "
        f"{result.risk_level} "
        f"({result.confidence:.0%})"
    )

print("\n=================================")
