from agents.base_agent import BaseAgent
from core.schemas import Transaction, AgentResult


class CriticAgent(BaseAgent):

    def __init__(self):
        super().__init__("Critic Agent")

    def analyze(
        self,
        transaction: Transaction,
        feedback: str = None,
        agent_results=None,
        verification=None
    ) -> AgentResult:

        evidence = []

        if not agent_results:

            return AgentResult(
                agent_name=self.name,
                risk_level="MEDIUM",
                reason=(
                    "Critic analysis cannot be completed because "
                    "no agent results are available."
                ),
                evidence=[
                    "No agent evidence was provided for criticism."
                ],
                confidence=0.30
            )

        # Count primary-agent conclusions
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
            f"Reviewed {len(agent_results)} primary agent results."
        )

        evidence.append(
            f"Risk distribution: HIGH={high_count}, "
            f"MEDIUM={medium_count}, LOW={low_count}."
        )

        # Check for disagreement
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

            evidence.append(
                "Strong disagreement exists between the agents."
            )

            evidence.append(
                f"High-risk agents: {', '.join(high_agents)}."
            )

            evidence.append(
                f"Low-risk agents: {', '.join(low_agents)}."
            )

            # Inspect the evidence behind the disagreement
            for result in agent_results:

                evidence.append(
                    f"{result.agent_name} evidence: "
                    + " | ".join(result.evidence)
                )

            risk_level = "MEDIUM"

            reason = (
                "The agent conclusions are contradictory. "
                "The strongest risk evidence should be examined "
                "before accepting a fraud conclusion."
            )

            confidence = 0.85

        elif high_count >= 2:

            evidence.append(
                "Multiple agents independently reported high risk."
            )

            risk_level = "LOW"

            reason = (
                "The high-risk conclusion is supported by multiple "
                "agents, but the Critic does not independently "
                "classify the transaction as fraud."
            )

            confidence = 0.80

        elif medium_count >= 2:

            evidence.append(
                "Multiple agents reported moderate risk."
            )

            risk_level = "LOW"

            reason = (
                "Moderate risk indicators are present, but they "
                "do not independently establish fraud."
            )

            confidence = 0.75

        elif low_count >= 2:

            evidence.append(
                "Most primary agents reported low risk."
            )

            risk_level = "LOW"

            reason = (
                "The available evidence generally supports the "
                "primary agents' low-risk conclusions."
            )

            confidence = 0.80

        else:

            evidence.append(
                "The available agent conclusions are not sufficiently "
                "consistent for a strong conclusion."
            )

            risk_level = "MEDIUM"

            reason = (
                "The Critic found insufficient agreement between "
                "the available agent conclusions."
            )

            confidence = 0.60

        if verification:

            evidence.append(
                f"Core verification status: "
                f"{verification.status.upper()}."
            )

        if feedback:

            evidence.append(
                "Previous verifier feedback was reviewed "
                "during critical re-analysis."
            )

        return AgentResult(
            agent_name=self.name,
            risk_level=risk_level,
            reason=reason,
            evidence=evidence,
            confidence=confidence
        )
# agents/critic.py
from typing import Dict, Any
from agents.base_agent import BaseAgent
from schemas.transaction import AgentOutput

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="CriticAgent")

    def analyze(self, verifier_output: AgentOutput, metadata: Dict[str, Any]) -> AgentOutput:
        counter_evidence = []
        fp_mitigation_score = 0.0

        category = metadata.get("merchant_category", "").lower()
        if category in ["travel", "electronics", "jewelry", "home_improvement"]:
            counter_evidence.append(f"High-value amount aligns with high-ticket merchant category: '{category.capitalize()}'.")
            fp_mitigation_score += 0.35

        if metadata.get("is_holiday_season", False):
            counter_evidence.append("Transaction occurred during festive/holiday spending season.")
            fp_mitigation_score += 0.25

        if metadata.get("user_income_bracket") in ["HIGH", "HNI"]:
            counter_evidence.append("User account is in High Net Worth tier; large purchases are common.")
            fp_mitigation_score += 0.30

        # Decide whether to overturn or downgrade high risk flags
        if fp_mitigation_score >= 0.50 and verifier_output.risk == "HIGH":
            final_risk = "MEDIUM"
            reason = "Critic Challenge: Flagged risk downgraded due to strong legitimate context (False Positive Prevention)."
        elif fp_mitigation_score >= 0.70:
            final_risk = "LOW"
            reason = "Critic Challenge: High probability transaction is legitimate."
        else:
            final_risk = verifier_output.risk
            reason = "Critic Challenge Passed: Fraud indicators remain dominant over false-positive context."
            if not counter_evidence:
                counter_evidence.append("No viable benign explanations found for the observed flags.")

        return AgentOutput(
            agent_name=self.name,
            risk=final_risk,
            reason=reason,
            evidence=counter_evidence,
            confidence=0.88
        )
