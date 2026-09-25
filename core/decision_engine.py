class DecisionEngine:

    def decide(self, agent_results, verification):

        print("\n[DECISION ENGINE] Making final decision...")

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

        # Do not make a strong decision when verification fails
        if verification.status == "UNCERTAIN":
            return {
                "decision": "INSUFFICIENT EVIDENCE / REVIEW",
                "reason": verification.reason,
                "confidence": verification.confidence
            }

        # Multiple agents identify high risk
        if high_risk_count >= 2:
            return {
                "decision": "FRAUD / HIGH RISK",
                "reason": "Multiple independent agents identified high risk.",
                "confidence": 0.90
            }

        # One high-risk or multiple medium-risk results
        if high_risk_count == 1 or medium_risk_count >= 2:
            return {
                "decision": "REVIEW",
                "reason": "The transaction contains suspicious risk indicators.",
                "confidence": 0.70
            }

        # Mostly low-risk results
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