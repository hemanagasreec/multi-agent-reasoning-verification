from abc import ABC, abstractmethod

from core.schemas import Transaction, AgentResult


class BaseAgent(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def analyze(self, transaction: Transaction) -> AgentResult:
        pass
