import os
from openai import OpenAI
from models.base import LLMModel


class OpenAIModel(LLMModel):
    def __init__(self, name="gpt-4o-mini"):
        super().__init__(name)
        # Created here (not at import time) so other adapters work without an OpenAI key.
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content
