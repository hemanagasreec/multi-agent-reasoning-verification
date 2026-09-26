from core.schemas import Transaction, AgentResult
from core.orchestrator import Orchestrator
from agents.base_agent import BaseAgent


# ==========================================
# MOCK AGENTS FOR INCOMPLETE-DATA TEST
# ==========================================

class IncompleteDataAgent(BaseAgent):

    def __init__(self):
        super().__init__("Pattern Agent")

    def analyze(
        self,
        transaction,
        feedback=None
    ):

        evidence = []

        if not transaction.location.strip():
            evidence.append(
                "Transaction location is missing."
            )

        if not transaction.device.strip():
            evidence.append(
                "Transaction device information is missing."
            )

        if not transaction.timestamp.strip():
            evidence.append(
                "Transaction timestamp is missing."
            )

        if evidence:
            return AgentResult(
                agent_name=self.name,
                risk_level="MEDIUM",
                reason=(
                    "Important transaction information is "
                    "missing and reliable risk analysis is limited."
                ),
                evidence=evidence,
                confidence=0.60
            )

        return AgentResult(
            agent_name=self.name,
            risk_level="LOW",
            reason="Transaction information is available.",
            evidence=[
                "Required transaction information is available."
            ],
            confidence=0.80
        )


class MissingDataRiskAgent(BaseAgent):

    def __init__(self):
        super().__init__("Risk Agent")

    def analyze(
        self,
        transaction,
        feedback=None
    ):

        evidence = []

        if not transaction.location.strip():
            evidence.append(
                "Location cannot be verified."
            )

        if not transaction.device.strip():
            evidence.append(
                "Device cannot be verified."
            )

        if not transaction.timestamp.strip():
            evidence.append(
                "Timestamp cannot be verified."
            )

        if evidence:
            return AgentResult(
                agent_name=self.name,
                risk_level="MEDIUM",
                reason=(
                    "Missing transaction fields prevent "
                    "complete risk verification."
                ),
                evidence=evidence,
                confidence=0.65
            )

        return AgentResult(
            agent_name=self.name,
            risk_level="LOW",
            reason="No missing transaction information detected.",
            evidence=[
                "Transaction information is complete."
            ],
            confidence=0.80
        )


# ==========================================
# INCOMPLETE TRANSACTION
# ==========================================

transaction = Transaction(
    transaction_id="INCOMPLETE001",
    amount=5000,
    location="",
    device="",
    timestamp=""
)


# ==========================================
# AGENTS
# ==========================================

agents = [
    IncompleteDataAgent(),
    MissingDataRiskAgent()
]


# ==========================================
# RUN ORCHESTRATOR
# ==========================================

orchestrator = Orchestrator()

final_result, agent_results, verification, evidence_records = orchestrator.run(
    transaction,
    agents
)


# ==========================================
# OUTPUT
# ==========================================

print("\n========== INCOMPLETE DATA TEST ==========")

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

print("\n===================================")
print("INCOMPLETE DATA TEST COMPLETED")
print("===================================")
