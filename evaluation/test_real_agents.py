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
    transaction_id="TX003",
    amount=50000,
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


final_result, agent_results, verification = orchestrator.run(
    transaction,
    agents
)


print("\n========== FINAL RESULT ==========")

print(
    "Decision:",
    final_result.decision
)

print(
    "Confidence:",
    final_result.confidence
)

print(
    "Revision:",
    final_result.revision
)


print("\n========== VERIFICATION ==========")

print(
    "Status:",
    verification.status
)

print(
    "Reason:",
    verification.reason
)


print("\n========== AGENT RESULTS ==========")

for result in agent_results:

    print("\nAgent:", result.agent_name)

    print(
        "Risk:",
        result.risk_level
    )

    print(
        "Reason:",
        result.reason
    )

    print(
        "Evidence:",
        result.evidence
    )

    print(
        "Confidence:",
        result.confidence
    )
