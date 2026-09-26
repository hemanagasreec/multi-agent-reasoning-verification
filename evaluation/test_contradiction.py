from core.schemas import Transaction, AgentResult
from core.orchestrator import Orchestrator
from agents.base_agent import BaseAgent


# ==========================================
# MOCK HIGH-RISK AGENT
# ==========================================

class HighRiskMockAgent(BaseAgent):

    def __init__(self):
        # Must use a name recognized by the orchestrator
        super().__init__("Pattern Agent")

    def analyze(
        self,
        transaction,
        feedback=None
    ):

        if feedback:
            print(
                "[MOCK HIGH-RISK AGENT] "
                "Received correction feedback."
            )

        return AgentResult(
            agent_name=self.name,
            risk_level="HIGH",
            reason=(
                "Mock agent detected suspicious "
                "transaction activity."
            ),
            evidence=[
                "Transaction amount is unusually high."
            ],
            confidence=0.90
        )


# ==========================================
# MOCK LOW-RISK AGENT
# ==========================================

class LowRiskMockAgent(BaseAgent):

    def __init__(self):
        # Must use a name recognized by the orchestrator
        super().__init__("Risk Agent")

    def analyze(
        self,
        transaction,
        feedback=None
    ):

        if feedback:
            print(
                "[MOCK LOW-RISK AGENT] "
                "Received correction feedback."
            )

        return AgentResult(
            agent_name=self.name,
            risk_level="LOW",
            reason=(
                "Mock agent found no major "
                "risk indicators."
            ),
            evidence=[
                "Transaction data appears normal."
            ],
            confidence=0.80
        )


# ==========================================
# TEST TRANSACTION
# ==========================================

transaction = Transaction(
    transaction_id="CONFLICT001",
    amount=5000,
    location="Known Location",
    device="Known Device",
    timestamp="2026-09-25 14:00"
)


# ==========================================
# MOCK AGENTS
# ==========================================

agents = [
    HighRiskMockAgent(),
    LowRiskMockAgent()
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

print("\n========== CONTRADICTION TEST ==========")

print(
    "Final Decision:",
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
print("CONTRADICTION TEST COMPLETED")
print("===================================")
