import os
from openai import OpenAI
from models.base import LLMModel

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OpenAIModel(LLMModel):
    def __init__(self, name="gpt-4o-mini"):
        super().__init__(name)

    def generate(self, prompt: str) -> str:
        response = client.chat.completions.create(
            model=self.name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content
