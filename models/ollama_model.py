import requests
from models.base import LLMModel

class OllamaModel(LLMModel):
    def __init__(self, name="llama3"):
        super().__init__(name)

    def generate(self, prompt: str) -> str:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.name,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]
