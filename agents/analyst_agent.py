from agents.base_agent import BaseAgent
from core.schemas import Transaction, AgentResult


class AnalystAgent(BaseAgent):

    def __init__(self):
        super().__init__("Analyst Agent")

    def analyze(
        self,
        transaction: Transaction,
        feedback: str = None,
        agent_results=None,
        verification=None,
        independent_verification=None
    ) -> AgentResult:

        evidence = []

        if not agent_results:

            return AgentResult(
                agent_name=self.name,
                risk_level="MEDIUM",
                reason=(
                    "Final analysis cannot be completed because "
                    "no supporting agent results are available."
                ),
                evidence=[
                    "No agent evidence was provided."
                ],
                confidence=0.30
            )

        # ========================================================
        # COLLECT AGENT RESULTS
        # ========================================================

        high_count = 0
        medium_count = 0
        low_count = 0

        for result in agent_results:

            risk = result.risk_level.upper()

            if risk == "HIGH":
                high_count += 1

            elif risk == "MEDIUM":
                medium_count += 1

            elif risk == "LOW":
                low_count += 1

            evidence.append(
                f"{result.agent_name}: "
                f"{risk} risk "
                f"({result.confidence:.0%} confidence)."
            )

        # ========================================================
        # COLLECT IMPORTANT EVIDENCE
        # ========================================================

        for result in agent_results:

            for item in result.evidence:

                evidence.append(
                    f"{result.agent_name} evidence: {item}"
                )

        # ========================================================
        # CHECK VERIFICATION
        # ========================================================

        verification_status = "UNKNOWN"

        if verification:

            verification_status = verification.status.upper()

            evidence.append(
                f"Core verification status: "
                f"{verification_status}."
            )

        # ========================================================
        # CHECK INDEPENDENT VERIFIER
        # ========================================================

        independent_status = "UNKNOWN"

        if independent_verification:

            independent_status = (
                independent_verification.risk_level.upper()
            )

            evidence.append(
                f"Independent verifier assessment: "
                f"{independent_status}."
            )

        # ========================================================
        # FINAL ANALYSIS LOGIC
        # ========================================================

        # Strong contradiction means evidence is not sufficient
        # for a definitive fraud conclusion.

        if verification_status in ["UNCERTAIN", "REVIEW"]:

            risk_level = "MEDIUM"

            reason = (
                "Agent conclusions contain conflicting evidence. "
                "The transaction requires review rather than an "
                "automatic fraud classification."
            )

            confidence = 0.60

        # Multiple high-risk agents with successful verification

        elif high_count >= 2 and verification_status == "VERIFIED":

            risk_level = "HIGH"

            reason = (
                "Multiple independent analysis agents identified "
                "high-risk indicators and the evidence passed "
                "verification."
            )

            confidence = 0.90

        # One high-risk result is not enough by itself

        elif high_count == 1:

            risk_level = "MEDIUM"

            reason = (
                "A high-risk indicator was identified, but there "
                "is not enough independent evidence to confirm fraud."
            )

            confidence = 0.70

        # Multiple medium results

        elif medium_count >= 2:

            risk_level = "MEDIUM"

            reason = (
                "Multiple agents identified moderate risk indicators. "
                "Additional review is recommended."
            )

            confidence = 0.75

        # Mostly low risk

        elif low_count >= 2:

            risk_level = "LOW"

            reason = (
                "The available evidence is generally consistent "
                "with a low-risk transaction."
            )

            confidence = 0.85

        else:

            risk_level = "MEDIUM"

            reason = (
                "The available evidence is insufficient for a "
                "reliable high- or low-risk conclusion."
            )

            confidence = 0.50

        # ========================================================
        # FEEDBACK
        # ========================================================

        if feedback:

            evidence.append(
                "Previous verification feedback was considered "
                "during final re-analysis."
            )

        # ========================================================
        # RETURN FINAL ANALYST RESULT
        # ========================================================

        return AgentResult(
            agent_name=self.name,
            risk_level=risk_level,
            reason=reason,
            evidence=evidence,
            confidence=confidence
        )
