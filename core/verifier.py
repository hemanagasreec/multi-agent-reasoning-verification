from core.schemas import AgentResult, VerificationResult


class Verifier:

    def verify(self, agent_results):
        print("\n[VERIFIER] Checking agent results...")

        if not agent_results:
            return VerificationResult(
                status="FAILED",
                reason="No agent results available.",
                confidence=0.0
            )

        # Check for disagreement
        risk_levels = [
            result.risk_level.upper()
            for result in agent_results
        ]

        high_count = risk_levels.count("HIGH")
        low_count = risk_levels.count("LOW")

        # Strong disagreement
        if high_count > 0 and low_count > 0:
            return VerificationResult(
                status="UNCERTAIN",
                reason="Agents disagree about the transaction risk.",
                confidence=0.50
            )

        # All agents agree on HIGH
        if high_count == len(agent_results):
            return VerificationResult(
                status="VERIFIED",
                reason="All agents identified high risk.",
                confidence=0.90
            )

        # All agents agree on LOW
        if low_count == len(agent_results):
            return VerificationResult(
                status="VERIFIED",
                reason="All agents identified low risk.",
                confidence=0.90
            )

        # Otherwise
        return VerificationResult(
            status="REVIEW",
            reason="Agent results are mixed and require further analysis.",
            confidence=0.65
        )