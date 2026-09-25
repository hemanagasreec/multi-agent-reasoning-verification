class DecisionEngine:

    def decide(
        self,
        agent_results,
        verification,
        analyst_result=None,
        critic_result=None,
        independent_result=None
    ):

        print("\n[DECISION ENGINE] Making final decision...")

        # ==========================================
        # NO PRIMARY RESULTS
        # ==========================================

        if not agent_results:
            return {
                "decision": "INSUFFICIENT EVIDENCE / REVIEW",
                "reason": (
                    "No primary agent results are available."
                ),
                "confidence": 0.0
            }

        # ==========================================
        # VERIFICATION FAILED
        # ==========================================

        if verification.status == "FAILED":
            return {
                "decision": "INSUFFICIENT EVIDENCE / REVIEW",
                "reason": verification.reason,
                "confidence": verification.confidence
            }

        # ==========================================
        # GET FINAL AGENT RISK LEVELS
        # ==========================================

        analyst_risk = None

        if analyst_result:
            analyst_risk = (
                analyst_result.risk_level.upper()
            )

        critic_risk = None

        if critic_result:
            critic_risk = (
                critic_result.risk_level.upper()
            )

        independent_risk = None

        if independent_result:
            independent_risk = (
                independent_result.risk_level.upper()
            )

        # ==========================================
        # INDEPENDENT VERIFIER SAFETY CHECK
        # ==========================================

        if (
            independent_result
            and independent_risk == "HIGH"
        ):

            return {
                "decision": "REVIEW",
                "reason": (
                    "The independent verifier detected "
                    "multiple transaction consistency problems. "
                    "The system will not automatically accept "
                    "the primary analysis."
                ),
                "confidence": min(
                    independent_result.confidence,
                    verification.confidence
                )
            }

        if (
            independent_result
            and independent_risk == "MEDIUM"
            and analyst_risk == "LOW"
        ):

            return {
                "decision": "REVIEW",
                "reason": (
                    "The independent verifier identified "
                    "transaction information requiring additional "
                    "review, so the low-risk conclusion was not "
                    "automatically accepted."
                ),
                "confidence": min(
                    independent_result.confidence,
                    verification.confidence
                )
            }

        # ==========================================
        # UNRESOLVED CONTRADICTION
        # ==========================================

        if verification.status == "UNCERTAIN":

            analyst_confidence = (
                analyst_result.confidence
                if analyst_result
                else verification.confidence
            )

            return {
                "decision": "INSUFFICIENT EVIDENCE / REVIEW",
                "reason": (
                    "The verification layer detected unresolved "
                    "conflicting evidence. The system cannot "
                    "reliably classify the transaction without "
                    "stronger supporting evidence."
                ),
                "confidence": min(
                    verification.confidence,
                    analyst_confidence
                )
            }

        # ==========================================
        # VERIFICATION REQUIRES REVIEW
        # ==========================================

        if verification.status == "REVIEW":

            return {
                "decision": "REVIEW",
                "reason": (
                    "The verification layer requires additional "
                    "review before accepting the transaction analysis."
                ),
                "confidence": verification.confidence
            }

        # ==========================================
        # VERIFIED + ANALYST HIGH
        # ==========================================

        if (
            verification.status == "VERIFIED"
            and analyst_risk == "HIGH"
        ):

            return {
                "decision": "FRAUD / HIGH RISK",
                "reason": analyst_result.reason,
                "confidence": min(
                    analyst_result.confidence,
                    verification.confidence
                )
            }

        # ==========================================
        # VERIFIED + ANALYST MEDIUM
        # ==========================================

        if (
            verification.status == "VERIFIED"
            and analyst_risk == "MEDIUM"
        ):

            return {
                "decision": "REVIEW",
                "reason": analyst_result.reason,
                "confidence": min(
                    analyst_result.confidence,
                    verification.confidence
                )
            }

        # ==========================================
        # VERIFIED + ANALYST LOW
        # ==========================================

        if (
            verification.status == "VERIFIED"
            and analyst_risk == "LOW"
        ):

            return {
                "decision": "LEGITIMATE",
                "reason": analyst_result.reason,
                "confidence": min(
                    analyst_result.confidence,
                    verification.confidence
                )
            }

        # ==========================================
        # FALLBACK
        # ==========================================

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

        if high_risk_count >= 2:

            return {
                "decision": "FRAUD / HIGH RISK",
                "reason": (
                    "Multiple primary agents independently "
                    "identified high risk."
                ),
                "confidence": 0.90
            }

        if (
            high_risk_count == 1
            or medium_risk_count >= 2
        ):

            return {
                "decision": "REVIEW",
                "reason": (
                    "The transaction contains suspicious "
                    "risk indicators."
                ),
                "confidence": 0.70
            }

        if low_risk_count >= 2:

            return {
                "decision": "LEGITIMATE",
                "reason": (
                    "Most primary agents found no significant "
                    "fraud indicators."
                ),
                "confidence": 0.85
            }

        return {
            "decision": "INSUFFICIENT EVIDENCE / REVIEW",
            "reason": (
                "There is not enough evidence for a "
                "reliable decision."
            ),
            "confidence": 0.50
        }
