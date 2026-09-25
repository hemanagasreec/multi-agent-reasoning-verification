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


# ==========================================
# HIGH-RISK TEST TRANSACTION
# ==========================================

transaction = Transaction(
    transaction_id="TX004",
    amount=50000,
    location="Unknown Location",
    device="New Device",
    timestamp="2026-09-25 02:00"
)


# ==========================================
# ALL AGENTS
# ==========================================

agents = [
    PatternAgent(),
    RiskAgent(),
    HistoryAgent(),
    CriticAgent(),
    VerifierAgent(),
    AnalystAgent()
]


# ==========================================
# START ORCHESTRATOR
# ==========================================

orchestrator = Orchestrator()


final_result, agent_results, verification, evidence_records = orchestrator.run(
    transaction,
    agents
)


# ==========================================
# FINAL RESULT
# ==========================================

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


# ==========================================
# VERIFICATION RESULT
# ==========================================

print("\n========== VERIFICATION ==========")

print(
    "Status:",
    verification.status
)

print(
    "Reason:",
    verification.reason
)

print(
    "Confidence:",
    verification.confidence
)

print(
    "Revision:",
    verification.revision
)


# ==========================================
# AGENT RESULTS
# ==========================================

print("\n========== AGENT RESULTS ==========")

for result in agent_results:

    print("\n-----------------------------------")

    print(
        "Agent:",
        result.agent_name
    )

    print(
        "Risk:",
        result.risk_level
    )

    print(
        "Reason:",
        result.reason
    )

    print(
        "Evidence:"
    )

    for evidence in result.evidence:
        print(
            " -",
            evidence
        )

    print(
        "Confidence:",
        result.confidence
    )

    print(
        "Revision:",
        result.revision
    )


print("\n===================================")
print("HIGH-RISK TEST COMPLETED")
print("===================================")
