from core.schemas import Transaction, FinalDecision
from core.verifier import Verifier
from core.decision_engine import DecisionEngine
from core.correction import CorrectionEngine

from database.database import (
    create_tables,
    save_task,
    save_agent_result,
    save_verification
)


class Orchestrator:

    def __init__(self):
        self.max_revisions = 2
        self.verifier = Verifier()
        self.decision_engine = DecisionEngine()
        self.correction_engine = CorrectionEngine()

        # Create database tables
        create_tables()

    def run(self, transaction: Transaction, agents):

        print("\n[ORCHESTRATOR] Starting fraud analysis...")

        # Step 1: Run specialized agents
        agent_results = []

        for agent in agents:
            result = agent.analyze(transaction)
            agent_results.append(result)

            # Save agent result to database
            save_agent_result(
                transaction.transaction_id,
                result
            )

            print(
                f"[ORCHESTRATOR] {result.agent_name}: "
                f"{result.risk_level} ({result.confidence})"
            )

        # Step 2: Verify results
        verification = self.verifier.verify(agent_results)

        # Save verification result
        save_verification(
            transaction.transaction_id,
            verification
        )

        print(
            f"[ORCHESTRATOR] Verification: "
            f"{verification.status}"
        )

        print(
            f"[ORCHESTRATOR] Verification reason: "
            f"{verification.reason}"
        )

        # Step 3: Self-correction loop
        revision = 0

        while (
            verification.status == "UNCERTAIN"
            and revision < self.max_revisions
        ):

            revision += 1

            print(
                f"\n[ORCHESTRATOR] Revision {revision} triggered."
            )

            agent_results = self.correction_engine.correct(
                transaction,
                agent_results
            )

            # Verify again after correction
            verification = self.verifier.verify(agent_results)

            # Save re-verification result
            save_verification(
                transaction.transaction_id,
                verification
            )

            print(
                f"[ORCHESTRATOR] Re-verification: "
                f"{verification.status}"
            )

        # Step 4: Decision Engine
        decision_data = self.decision_engine.decide(
            agent_results,
            verification
        )

        # Step 5: Create final result
        final_result = FinalDecision(
            decision=decision_data["decision"],
            reason=decision_data["reason"],
            confidence=decision_data["confidence"],
            revision=revision
        )

        print(
            f"[ORCHESTRATOR] Final Decision: "
            f"{final_result.decision}"
        )

        # Step 6: Save final decision to database
        save_task(
            transaction.transaction_id,
            transaction.transaction_id,
            final_result.decision,
            final_result.confidence,
            transaction.timestamp
        )

        return final_result, agent_results, verification