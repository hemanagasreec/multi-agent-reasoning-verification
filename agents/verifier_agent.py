# agents/verifier.py
from typing import List
from agents.base_agent import BaseAgent
from schemas.transaction import AgentOutput

class VerifierAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="VerifierAgent")

    def analyze(self, agent_outputs: List[AgentOutput]) -> AgentOutput:
        high_risk_agents = [a for a in agent_outputs if a.risk == "HIGH"]
        med_risk_agents = [a for a in agent_outputs if a.risk == "MEDIUM"]

        combined_evidence = []
        for agent in agent_outputs:
            for item in agent.evidence:
                combined_evidence.append(f"[{agent.agent_name}] {item}")

        total_weight = sum(a.confidence * 1.5 for a in high_risk_agents) + sum(a.confidence * 0.7 for a in med_risk_agents)

        if len(high_risk_agents) >= 2 or total_weight >= 2.0:
            final_risk = "HIGH"
            reason = "Corroborated fraud evidence found across multiple specialized agents."
        elif len(high_risk_agents) == 1 or len(med_risk_agents) >= 2:
            final_risk = "MEDIUM"
            reason = "Partial risk agreement across agents. Step-up authentication advised."
        else:
            final_risk = "LOW"
            reason = "Insufficient evidence across agents to confirm fraudulent activity."

        return AgentOutput(
            agent_name=self.name,
            risk=final_risk,
            reason=reason,
            evidence=combined_evidence,
            confidence=round(min(0.99, max(0.50, total_weight / 2.5)), 2)
        )