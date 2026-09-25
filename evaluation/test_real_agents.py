from core.schemas import Transaction
from core.orchestrator import Orchestrator

from agents import PatternAgent, RiskAgent, HistoryAgent


# Test transaction
transaction = Transaction(
    transaction_id="TX003",
    amount=50000,
    location="Known Location",
    device="Known Device",
    timestamp="2026-09-25 14:00"
)


# Create specialized agents
agents = [
    PatternAgent(),
    RiskAgent(),
    HistoryAgent()
]


# Create orchestrator
orchestrator = Orchestrator()


# Run complete analysis
final_result, agent_results, verification = orchestrator.run(
    transaction,
    agents
)


# Display results
print("\n========== FINAL RESULT ==========")
print("Decision:", final_result.decision)
print("Confidence:", final_result.confidence)
print("Revision:", final_result.revision)

print("\n========== VERIFICATION ==========")
print("Status:", verification.status)
print("Reason:", verification.reason)

print("\n========== AGENT RESULTS ==========")

for result in agent_results:
    print("\nAgent:", result.agent_name)
    print("Risk:", result.risk_level)
    print("Reason:", result.reason)
    print("Evidence:", result.evidence)
    print("Confidence:", result.confidence)
