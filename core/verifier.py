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

        # --------------------------------------------------------
        # COLLECT RISK LEVELS
        # --------------------------------------------------------

        risk_levels = [
            result.risk_level.upper()
            for result in agent_results
        ]

        high_count = risk_levels.count("HIGH")
        medium_count = risk_levels.count("MEDIUM")
        low_count = risk_levels.count("LOW")

        # --------------------------------------------------------
        # ALL AGENTS AGREE
        # --------------------------------------------------------

        if high_count == len(agent_results):

            return VerificationResult(
                status="VERIFIED",
                reason=(
                    "All agents independently identified "
                    "the transaction as high risk."
                ),
                confidence=0.90
            )

        if low_count == len(agent_results):

            return VerificationResult(
                status="VERIFIED",
                reason=(
                    "All agents independently identified "
                    "the transaction as low risk."
                ),
                confidence=0.90
            )

        # --------------------------------------------------------
        # CONTRADICTION DETECTION
        # --------------------------------------------------------

        if high_count > 0 and low_count > 0:

            high_agents = [
                result
                for result in agent_results
                if result.risk_level.upper() == "HIGH"
            ]

            low_agents = [
                result
                for result in agent_results
                if result.risk_level.upper() == "LOW"
            ]

            high_names = ", ".join(
                result.agent_name
                for result in high_agents
            )

            low_names = ", ".join(
                result.agent_name
                for result in low_agents
            )

            high_evidence = []

            for result in high_agents:
                high_evidence.extend(result.evidence)

            low_evidence = []

            for result in low_agents:
                low_evidence.extend(result.evidence)

            reason = (
                f"Contradiction detected between agents. "
                f"{high_names} classified the transaction as HIGH risk, "
                f"while {low_names} classified it as LOW risk. "
                f"High-risk evidence: {high_evidence}. "
                f"Low-risk evidence: {low_evidence}. "
                f"Re-analysis is required to determine whether "
                f"the high-risk evidence is sufficient."
            )

            return VerificationResult(
                status="UNCERTAIN",
                reason=reason,
                confidence=0.50
            )

        # --------------------------------------------------------
        # MIXED MEDIUM / OTHER RESULTS
        # --------------------------------------------------------

        agent_summary = []

        for result in agent_results:

            agent_summary.append(
                f"{result.agent_name}: "
                f"{result.risk_level.upper()} "
                f"({result.confidence:.0%})"
            )

        reason = (
            "Agents produced mixed risk assessments. "
            + " | ".join(agent_summary)
            + ". Additional analysis is required."
        )

        return VerificationResult(
            status="REVIEW",
            reason=reason,
            confidence=0.65
        )
