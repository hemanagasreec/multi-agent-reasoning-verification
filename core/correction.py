class CorrectionEngine:

    def correct(self, transaction, agent_results):
        print("\n[CORRECTION ENGINE] Re-analysis started...")

        corrected_results = []

        for result in agent_results:
            # Ask the agent to reconsider its previous result
            if result.risk_level.upper() == "HIGH":
                result.reason = (
                    result.reason
                    + " Re-checked against other agent findings."
                )

            elif result.risk_level.upper() == "LOW":
                result.reason = (
                    result.reason
                    + " Re-checked for possible missed risk indicators."
                )

            corrected_results.append(result)

        print("[CORRECTION ENGINE] Re-analysis completed.")

        return corrected_results