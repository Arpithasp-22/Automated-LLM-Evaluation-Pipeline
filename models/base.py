from abc import ABC, abstractmethod

class LLMModel(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
