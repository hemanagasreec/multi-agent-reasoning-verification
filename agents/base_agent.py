# agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Any, Dict
from schemas.transaction import AgentOutput

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def analyze(self, *args, **kwargs) -> AgentOutput:
        """Core execution method required for every agent."""
        pass