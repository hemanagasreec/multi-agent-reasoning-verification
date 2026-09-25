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

        create_tables()

    def run(self, transaction: Transaction, agents):

        print("\n[ORCHESTRATOR] Starting fraud analysis...")

        # -------------------------
        # INITIAL AGENT ANALYSIS
        # -------------------------

        agent_results = []

        for agent in agents:

            result = agent.analyze(transaction)

            # Initial analysis = Revision 0
            result.revision = 0

            agent_results.append(result)

            save_agent_result(
                transaction.transaction_id,
                result
            )

            print(
                f"[ORCHESTRATOR] "
                f"{result.agent_name}: "
                f"{result.risk_level} "
                f"({result.confidence})"
            )

        # -------------------------
        # INITIAL VERIFICATION
        # -------------------------

        verification = self.verifier.verify(agent_results)

        # Initial verification = Revision 0
        verification.revision = 0

        save_verification(
            transaction.transaction_id,
            verification
        )

        print(
            f"[ORCHESTRATOR] "
            f"Verification: {verification.status}"
        )

        print(
            f"[ORCHESTRATOR] "
            f"Verification reason: {verification.reason}"
        )

        # -------------------------
        # SELF-CORRECTION LOOP
        # -------------------------

        revision = 0

        while (
            verification.status == "UNCERTAIN"
            and revision < self.max_revisions
        ):

            revision += 1

            print(
                f"\n[ORCHESTRATOR] "
                f"Revision {revision} triggered."
            )

            # Re-run all agents
            agent_results = self.correction_engine.correct(
                transaction,
                agents,
                verification
            )

            # Store revision number for every agent result
            for result in agent_results:

                result.revision = revision

                save_agent_result(
                    transaction.transaction_id,
                    result
                )

            # Re-verify the new results
            verification = self.verifier.verify(
                agent_results
            )

            # Store revision number for verification
            verification.revision = revision

            save_verification(
                transaction.transaction_id,
                verification
            )

            print(
                f"[ORCHESTRATOR] "
                f"Re-verification: "
                f"{verification.status}"
            )

        # -------------------------
        # FINAL DECISION
        # -------------------------

        print("\n[DECISION ENGINE] Making final decision...")

        decision_data = self.decision_engine.decide(
            agent_results,
            verification
        )

        final_result = FinalDecision(
            decision=decision_data["decision"],
            reason=decision_data["reason"],
            confidence=decision_data["confidence"],
            revision=revision
        )

        print(
            f"[ORCHESTRATOR] "
            f"Final Decision: "
            f"{final_result.decision}"
        )

        # -------------------------
        # SAVE FINAL TASK
        # -------------------------

        save_task(
            transaction.transaction_id,
            transaction.transaction_id,
            final_result.decision,
            final_result.confidence,
            transaction.timestamp
        )

        return (
            final_result,
            agent_results,
            verification
        )
