# schemas/transaction.py
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

RiskLevel = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]

class AgentOutput(BaseModel):
    agent_name: str = Field(..., description="Name of the agent generating the evaluation")
    risk: RiskLevel = Field(..., description="Assessed risk level")
    reason: str = Field(..., description="Short summary explaining the risk score")
    evidence: List[str] = Field(default_factory=list, description="List of specific fraud indicators found")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")