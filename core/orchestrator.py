from core.schemas import Transaction, FinalDecision
from core.verifier import Verifier
from core.decision_engine import DecisionEngine
from core.correction import CorrectionEngine

from database.database import (
    create_tables,
    save_transaction,
    save_task,
    save_agent_result,
    save_verification
)

from agents import (
    CriticAgent,
    VerifierAgent,
    AnalystAgent
)


class Orchestrator:

    def __init__(self):

        self.max_revisions = 2

        self.verifier = Verifier()
        self.decision_engine = DecisionEngine()
        self.correction_engine = CorrectionEngine()

        create_tables()

    def run(
        self,
        transaction: Transaction,
        agents
    ):

        print(
            "\n[ORCHESTRATOR] Starting fraud analysis..."
        )

        # ---------------------------------------------------------
        # STEP 0: SAVE TRANSACTION
        # ---------------------------------------------------------

        save_transaction(transaction)

        # ---------------------------------------------------------
        # SEPARATE AGENT ROLES
        # ---------------------------------------------------------

        primary_agents = [
            agent
            for agent in agents
            if agent.name in [
                "Pattern Agent",
                "Risk Agent",
                "History Agent"
            ]
        ]

        critic_agent = next(
            (
                agent
                for agent in agents
                if agent.name == "Critic Agent"
            ),
            None
        )

        independent_verifier = next(
            (
                agent
                for agent in agents
                if agent.name == "Verifier Agent"
            ),
            None
        )

        analyst_agent = next(
            (
                agent
                for agent in agents
                if agent.name == "Analyst Agent"
            ),
            None
        )

        # ---------------------------------------------------------
        # STEP 1: PRIMARY AGENTS
        # ---------------------------------------------------------

        print(
            "\n[ORCHESTRATOR] "
            "Running primary analysis agents..."
        )

        agent_results = []

        for agent in primary_agents:

            print(
                f"\n[ORCHESTRATOR] Running {agent.name}..."
            )

            result = agent.analyze(transaction)

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
                f"({result.confidence:.0%})"
            )

        # ---------------------------------------------------------
        # STEP 2: CORE VERIFICATION
        # ---------------------------------------------------------

        verification = self.verifier.verify(
            agent_results
        )

        verification.revision = 0

        save_verification(
            transaction.transaction_id,
            verification
        )

        print(
            f"\n[ORCHESTRATOR] "
            f"Core Verification: "
            f"{verification.status}"
        )

        print(
            f"[ORCHESTRATOR] "
            f"Verification reason: "
            f"{verification.reason}"
        )

        # ---------------------------------------------------------
        # STEP 3: CRITIC
        # ---------------------------------------------------------

        critic_result = None

        if critic_agent:

            print(
                "\n[ORCHESTRATOR] "
                "Running Critic Agent..."
            )

            critic_result = critic_agent.analyze(
                transaction,
                agent_results=agent_results,
                verification=verification
            )

            critic_result.revision = 0

            save_agent_result(
                transaction.transaction_id,
                critic_result
            )

            print(
                f"[ORCHESTRATOR] "
                f"Critic: "
                f"{critic_result.risk_level} "
                f"({critic_result.confidence:.0%})"
            )

            print(
                f"[ORCHESTRATOR] "
                f"Critic reason: "
                f"{critic_result.reason}"
            )

        # ---------------------------------------------------------
        # STEP 4: INDEPENDENT VERIFIER
        # ---------------------------------------------------------

        independent_result = None

        if independent_verifier:

            print(
                "\n[ORCHESTRATOR] "
                "Running independent Verifier Agent..."
            )

            independent_result = (
                independent_verifier.analyze(
                    transaction
                )
            )

            independent_result.revision = 0

            save_agent_result(
                transaction.transaction_id,
                independent_result
            )

            print(
                f"[ORCHESTRATOR] "
                f"Independent Verifier: "
                f"{independent_result.risk_level} "
                f"({independent_result.confidence:.0%})"
            )

            print(
                f"[ORCHESTRATOR] "
                f"Verifier reason: "
                f"{independent_result.reason}"
            )

        # ---------------------------------------------------------
        # STEP 5: ANALYST
        # ---------------------------------------------------------

        analyst_result = None

        if analyst_agent:

            print(
                "\n[ORCHESTRATOR] "
                "Running Final Analyst..."
            )

            analyst_result = analyst_agent.analyze(
                transaction,
                agent_results=agent_results,
                verification=verification,
                independent_verification=independent_result
            )

            analyst_result.revision = 0

            save_agent_result(
                transaction.transaction_id,
                analyst_result
            )

            print(
                f"[ORCHESTRATOR] "
                f"Analyst: "
                f"{analyst_result.risk_level} "
                f"({analyst_result.confidence:.0%})"
            )

            print(
                f"[ORCHESTRATOR] "
                f"Analyst reason: "
                f"{analyst_result.reason}"
            )

        # ---------------------------------------------------------
        # STEP 6: SELF-CORRECTION LOOP
        # ---------------------------------------------------------

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

            # Re-run primary agents with feedback

            corrected_results = (
                self.correction_engine.correct(
                    transaction,
                    primary_agents,
                    verification
                )
            )

            agent_results = []

            for result in corrected_results:

                result.revision = revision

                agent_results.append(result)

                save_agent_result(
                    transaction.transaction_id,
                    result
                )

            # Re-verify corrected results

            verification = self.verifier.verify(
                agent_results
            )

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

            # Re-run Critic

            if critic_agent:

                print(
                    "\n[ORCHESTRATOR] "
                    "Re-running Critic Agent..."
                )

                critic_result = critic_agent.analyze(
                    transaction,
                    feedback=verification.reason,
                    agent_results=agent_results,
                    verification=verification
                )

                critic_result.revision = revision

                save_agent_result(
                    transaction.transaction_id,
                    critic_result
                )

            # Re-run Independent Verifier

            if independent_verifier:

                print(
                    "\n[ORCHESTRATOR] "
                    "Re-running Independent Verifier..."
                )

                independent_result = (
                    independent_verifier.analyze(
                        transaction,
                        feedback=verification.reason
                    )
                )

                independent_result.revision = revision

                save_agent_result(
                    transaction.transaction_id,
                    independent_result
                )

            # Re-run Analyst

            if analyst_agent:

                print(
                    "\n[ORCHESTRATOR] "
                    "Re-running Final Analyst..."
                )

                analyst_result = analyst_agent.analyze(
                    transaction,
                    feedback=verification.reason,
                    agent_results=agent_results,
                    verification=verification,
                    independent_verification=independent_result
                )

                analyst_result.revision = revision

                save_agent_result(
                    transaction.transaction_id,
                    analyst_result
                )

        # ---------------------------------------------------------
        # STEP 7: FINAL DECISION
        # ---------------------------------------------------------

        print(
            "\n[ORCHESTRATOR] "
            "Sending verified results to Decision Engine..."
        )

        decision_data = self.decision_engine.decide(
            agent_results,
            verification,
            analyst_result=analyst_result
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

        # ---------------------------------------------------------
        # STEP 8: SAVE FINAL AUDIT RECORD
        # ---------------------------------------------------------

        save_task(
            transaction.transaction_id,
            transaction.transaction_id,
            final_result.decision,
            final_result.confidence,
            transaction.timestamp
        )

        # ---------------------------------------------------------
        # RETURN RESULTS
        # ---------------------------------------------------------

        display_results = list(agent_results)

        if critic_result:
            display_results.append(critic_result)

        if independent_result:
            display_results.append(independent_result)

        if analyst_result:
            display_results.append(analyst_result)

        return (
            final_result,
            display_results,
            verification
        )
