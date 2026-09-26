from core.schemas import VerificationResult


class Verifier:

    def verify(self, agent_results):

        print("\n[VERIFIER] Checking agent results...")

        if not agent_results:

            return VerificationResult(
                status="FAILED",
                reason="No agent results available.",
                confidence=0.0
            )

        risk_levels = [
            result.risk_level.upper()
            for result in agent_results
        ]

        high_count = risk_levels.count("HIGH")
        medium_count = risk_levels.count("MEDIUM")
        low_count = risk_levels.count("LOW")

        # --------------------------------------------------
        # 1. Check whether agents have common evidence
        # --------------------------------------------------

        evidence_map = {}

        for result in agent_results:

            for evidence in result.evidence:

                normalized = evidence.lower()

                # Historical amount anomaly
                if (
                    "historical transaction baseline" in normalized
                    or "historical average" in normalized
                    or "x the historical" in normalized
                ):

                    evidence_map.setdefault(
                        "amount_anomaly",
                        []
                    ).append(result.agent_name)

                # New device
                if "new device" in normalized:

                    evidence_map.setdefault(
                        "new_device",
                        []
                    ).append(result.agent_name)

                # Unknown location
                if "unknown location" in normalized:

                    evidence_map.setdefault(
                        "unknown_location",
                        []
                    ).append(result.agent_name)

                # Unusual transaction time
                if "unusual hours" in normalized:

                    evidence_map.setdefault(
                        "unusual_time",
                        []
                    ).append(result.agent_name)

        common_evidence = []

        for evidence_type, agents in evidence_map.items():

            unique_agents = list(dict.fromkeys(agents))

            if len(unique_agents) >= 2:

                common_evidence.append(
                    f"{evidence_type} identified by "
                    f"{', '.join(unique_agents)}."
                )

        # --------------------------------------------------
        # 2. Strong agreement on underlying evidence
        # --------------------------------------------------

        if common_evidence:

            # Different risk levels do not automatically mean
            # contradiction when agents identify the same evidence.

            if high_count >= 1 and medium_count >= 1:

                return VerificationResult(
                    status="VERIFIED",
                    reason=(
                        "Agents assigned different risk levels, "
                        "but independently identified consistent "
                        "underlying evidence. "
                        + " ".join(common_evidence)
                    ),
                    confidence=0.85
                )

            if high_count >= 2:

                return VerificationResult(
                    status="VERIFIED",
                    reason=(
                        "Multiple agents independently identified "
                        "consistent high-risk evidence. "
                        + " ".join(common_evidence)
                    ),
                    confidence=0.90
                )

            if medium_count >= 2:

                return VerificationResult(
                    status="VERIFIED",
                    reason=(
                        "Multiple agents independently identified "
                        "consistent moderate-risk evidence. "
                        + " ".join(common_evidence)
                    ),
                    confidence=0.85
                )

        # --------------------------------------------------
        # 3. All agents agree on LOW
        # --------------------------------------------------

        if low_count == len(agent_results):

            return VerificationResult(
                status="VERIFIED",
                reason=(
                    "All primary agents independently reported "
                    "low risk with no conflicting evidence."
                ),
                confidence=0.90
            )

        # --------------------------------------------------
        # 4. Genuine HIGH vs LOW contradiction
        # --------------------------------------------------

        if high_count > 0 and low_count > 0:

            high_agents = [
                result.agent_name
                for result in agent_results
                if result.risk_level.upper() == "HIGH"
            ]

            low_agents = [
                result.agent_name
                for result in agent_results
                if result.risk_level.upper() == "LOW"
            ]

            return VerificationResult(
                status="UNCERTAIN",
                reason=(
                    "Contradictory risk conclusions detected. "
                    f"HIGH-risk agents: {', '.join(high_agents)}. "
                    f"LOW-risk agents: {', '.join(low_agents)}. "
                    "The evidence must be re-analyzed before "
                    "accepting the conclusion."
                ),
                confidence=0.50
            )

        # --------------------------------------------------
        # 5. Other mixed or uncertain cases
        # --------------------------------------------------

        agent_summary = []

        for result in agent_results:

            agent_summary.append(
                f"{result.agent_name}: "
                f"{result.risk_level.upper()} "
                f"({result.confidence:.0%})"
            )

        return VerificationResult(
            status="REVIEW",
            reason=(
                "Agents produced mixed risk assessments. "
                + " | ".join(agent_summary)
                + ". Additional analysis is required."
            ),
            confidence=0.65
        )
