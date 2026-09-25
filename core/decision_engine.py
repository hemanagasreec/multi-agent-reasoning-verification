class DecisionEngine:

    def decide(
        self,
        agent_results,
        verification,
        analyst_result=None
    ):

        print("\n[DECISION ENGINE] Making final decision...")

        # ---------------------------------------------------------
        # NO AGENT RESULTS
        # ---------------------------------------------------------

        if not agent_results:
            return {
                "decision": "INSUFFICIENT EVIDENCE / REVIEW",
                "reason": "No primary agent results are available.",
                "confidence": 0.0
            }

        # ---------------------------------------------------------
        # VERIFICATION FAILED
        # ---------------------------------------------------------

        if verification.status == "FAILED":
            return {
                "decision": "INSUFFICIENT EVIDENCE / REVIEW",
                "reason": verification.reason,
                "confidence": verification.confidence
            }

        # ---------------------------------------------------------
        # CONTRADICTION DETECTED
        # ---------------------------------------------------------

        if verification.status == "UNCERTAIN":
            return {
                "decision": "INSUFFICIENT EVIDENCE / REVIEW",
                "reason": (
                    "Agent conclusions remain contradictory after "
                    "verification and re-analysis."
                ),
                "confidence": verification.confidence
            }

        # ---------------------------------------------------------
        # VERIFICATION REQUIRES REVIEW
        # ---------------------------------------------------------

        if verification.status == "REVIEW":
            return {
                "decision": "REVIEW",
                "reason": verification.reason,
                "confidence": verification.confidence
            }

        # ---------------------------------------------------------
        # FINAL ANALYST RESULT
        # ---------------------------------------------------------

        if analyst_result:

            analyst_risk = analyst_result.risk_level.upper()

            analyst_confidence = analyst_result.confidence

            # HIGH RISK
            if analyst_risk == "HIGH":
                return {
                    "decision": "FRAUD / HIGH RISK",
                    "reason": analyst_result.reason,
                    "confidence": min(
                        analyst_confidence,
                        verification.confidence
                    )
                }

            # MEDIUM RISK
            if analyst_risk == "MEDIUM":
                return {
                    "decision": "REVIEW",
                    "reason": analyst_result.reason,
                    "confidence": min(
                        analyst_confidence,
                        verification.confidence
                    )
                }

            # LOW RISK
            if analyst_risk == "LOW":
                return {
                    "decision": "LEGITIMATE",
                    "reason": analyst_result.reason,
                    "confidence": min(
                        analyst_confidence,
                        verification.confidence
                    )
                }

        # ---------------------------------------------------------
        # FALLBACK
        # ---------------------------------------------------------

        high_risk_count = 0
        medium_risk_count = 0
        low_risk_count = 0

        for result in agent_results:

            risk = result.risk_level.upper()

            if risk == "HIGH":
                high_risk_count += 1

            elif risk == "MEDIUM":
                medium_risk_count += 1

            elif risk == "LOW":
                low_risk_count += 1

        # Multiple HIGH results
        if high_risk_count >= 2:
            return {
                "decision": "FRAUD / HIGH RISK",
                "reason": (
                    "Multiple primary agents independently "
                    "identified high risk."
                ),
                "confidence": 0.90
            }

        # One HIGH or multiple MEDIUM results
        if high_risk_count == 1 or medium_risk_count >= 2:
            return {
                "decision": "REVIEW",
                "reason": (
                    "The transaction contains suspicious "
                    "risk indicators."
                ),
                "confidence": 0.70
            }

        # Multiple LOW results
        if low_risk_count >= 2:
            return {
                "decision": "LEGITIMATE",
                "reason": (
                    "Most primary agents found no significant "
                    "fraud indicators."
                ),
                "confidence": 0.85
            }

        # ---------------------------------------------------------
        # INSUFFICIENT EVIDENCE
        # ---------------------------------------------------------

        return {
            "decision": "INSUFFICIENT EVIDENCE / REVIEW",
            "reason": (
                "There is not enough evidence for a "
                "reliable decision."
            ),
            "confidence": 0.50
        }
