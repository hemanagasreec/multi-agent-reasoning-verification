from pydantic import BaseModel
from typing import List


class Transaction(BaseModel):
    transaction_id: str
    amount: float
    location: str
    device: str
    timestamp: str


class AgentResult(BaseModel):
    agent_name: str
    risk_level: str
    reason: str
    evidence: List[str]
    confidence: float
    revision: int = 0


class VerificationResult(BaseModel):
    status: str
    reason: str
    confidence: float
    revision: int = 0


class FinalDecision(BaseModel):
    decision: str
    reason: str
    confidence: float
    revision: int = 0
