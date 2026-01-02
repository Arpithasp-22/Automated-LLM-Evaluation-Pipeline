import time
import uuid
import pandas as pd

from scoring.accuracy import score_accuracy
from scoring.refusal import is_refusal
from scoring.hallucination import is_hallucination

from models.openai_model import OpenAIModel
# from models.ollama_model import OllamaModel

RUN_ID = str(uuid.uuid4())

df = pd.read_csv("C:\\Users\\Arpitha.s\\Desktop\\llm-eval-framework\\data\\Golden_data.csv")

models = [
    OpenAIModel(),
    # OllamaModel()
]

results = []

for model in models:
    for _, row in df.iterrows():
        start = time.time()

        response = model.generate(row["prompt"])

        latency = time.time() - start

        refusal = is_refusal(response)
        hallucination = is_hallucination(response, row["allow_refusal"])
        accuracy = score_accuracy(
            response,
            str(row["expected_answer"]),
            row["scoring"]
        )

        results.append({
            "run_id": RUN_ID,
            "model": model.name,
            "prompt_id": row["id"],
            "category": row["category"],
            "accuracy": accuracy,
            "refusal": refusal,
            "hallucination": hallucination,
            "latency": latency
        })

out = pd.DataFrame(results)
out.to_csv(f"runs/run_{RUN_ID}.csv", index=False)

print("Run complete:", RUN_ID)
