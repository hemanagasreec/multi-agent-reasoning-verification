class DecisionEngine:

    def decide(self, agent_results, verification):

        print("\n[DECISION ENGINE] Making final decision...")

        # No results means there is not enough evidence.
        if not agent_results:
            return {
                "decision": "INSUFFICIENT EVIDENCE / REVIEW",
                "reason": "No agent results are available.",
                "confidence": 0.0
            }

        high_risk_count = sum(
            1
            for result in agent_results
            if result.risk_level.upper() == "HIGH"
        )

        medium_risk_count = sum(
            1
            for result in agent_results
            if result.risk_level.upper() == "MEDIUM"
        )

        low_risk_count = sum(
            1
            for result in agent_results
            if result.risk_level.upper() == "LOW"
        )

        # --------------------------------------------------------
        # VERIFICATION MUST BE RESPECTED
        # --------------------------------------------------------

        if verification.status == "UNCERTAIN":
            return {
                "decision": "INSUFFICIENT EVIDENCE / REVIEW",
                "reason": verification.reason,
                "confidence": verification.confidence
            }

        if verification.status == "REVIEW":
            return {
                "decision": "REVIEW",
                "reason": verification.reason,
                "confidence": verification.confidence
            }

        if verification.status == "FAILED":
            return {
                "decision": "INSUFFICIENT EVIDENCE / REVIEW",
                "reason": verification.reason,
                "confidence": verification.confidence
            }

        # --------------------------------------------------------
        # VERIFIED RESULTS
        # --------------------------------------------------------

        if high_risk_count >= 2:
            return {
                "decision": "FRAUD / HIGH RISK",
                "reason": "Multiple independent agents identified high risk.",
                "confidence": 0.90
            }

        if high_risk_count == 1 or medium_risk_count >= 2:
            return {
                "decision": "REVIEW",
                "reason": "The transaction contains suspicious risk indicators.",
                "confidence": 0.70
            }

        if low_risk_count >= 2:
            return {
                "decision": "LEGITIMATE",
                "reason": "Most agents found no significant fraud indicators.",
                "confidence": 0.85
            }

        return {
            "decision": "INSUFFICIENT EVIDENCE / REVIEW",
            "reason": "There is not enough evidence for a reliable decision.",
            "confidence": 0.50
        }
