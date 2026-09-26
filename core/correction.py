from core.schemas import Transaction


class CorrectionEngine:

    def correct(
        self,
        transaction: Transaction,
        agents,
        verification
    ):

        print("\n[CORRECTION ENGINE] Re-analysis started...")

        print(
            f"[CORRECTION ENGINE] Feedback: "
            f"{verification.reason}"
        )

        corrected_results = []

        for agent in agents:

            print(
                f"[CORRECTION ENGINE] "
                f"Re-running {agent.name} with verifier feedback..."
            )

            result = agent.analyze(
                transaction,
                feedback=verification.reason
            )

            corrected_results.append(result)

        print(
            "[CORRECTION ENGINE] "
            "Feedback-aware re-analysis completed."
        )

        return corrected_results

