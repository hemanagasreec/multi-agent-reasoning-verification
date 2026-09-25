from agents.base_agent import BaseAgent
from core.schemas import Transaction, AgentResult


class CriticAgent(BaseAgent):

    def __init__(self):
        super().__init__("Critic Agent")

    def analyze(self, transaction: Transaction) -> AgentResult:

        evidence = [
            "Critic agent independently reviews the transaction for unsupported conclusions."
        ]

        # Basic contradiction/risk check
        if transaction.amount >= 50000:
            risk_level = "HIGH"
            reason = "High-value transaction requires additional scrutiny."
            confidence = 0.80
        else:
            risk_level = "LOW"
            reason = "No major contradiction or high-risk indicator detected."
            confidence = 0.70

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
