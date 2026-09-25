from core.schemas import Transaction


class CorrectionEngine:

    def correct(self, transaction: Transaction, agents, verification):
        print("\n[CORRECTION ENGINE] Re-analysis started...")
        print(f"[CORRECTION ENGINE] Feedback: {verification.reason}")

        corrected_results = []

        for agent in agents:
            print(f"[CORRECTION ENGINE] Re-running {agent.name}...")
            result = agent.analyze(transaction)
            corrected_results.append(result)

        print("[CORRECTION ENGINE] Re-analysis completed.")

        return corrected_results
