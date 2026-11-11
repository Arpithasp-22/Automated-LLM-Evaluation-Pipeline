import argparse
import time
import uuid
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from scoring.accuracy import score_accuracy
from scoring.refusal import is_refusal
from scoring.hallucination import is_hallucination

from models.openai_model import OpenAIModel
from models.ollama_model import OllamaModel

load_dotenv()

ROOT = Path(__file__).resolve().parent
DEFAULT_DATA = ROOT / "data" / "Golden_data.csv"
RUNS_DIR = ROOT / "runs"

# Register new model adapters here.
AVAILABLE_MODELS = {
    "openai": OpenAIModel,
    "ollama": OllamaModel,
}


def run(model_keys, data_path):
    run_id = str(uuid.uuid4())
    df = pd.read_csv(data_path)
    models = [AVAILABLE_MODELS[key]() for key in model_keys]

    results = []
    for model in models:
        for _, row in df.iterrows():
            start = time.time()
            response = model.generate(row["prompt"])
            latency = time.time() - start

            results.append({
                "run_id": run_id,
                "model": model.name,
                "prompt_id": row["id"],
                "category": row["category"],
                "accuracy": score_accuracy(
                    response, str(row["expected_answer"]), row["scoring"]
                ),
                "refusal": is_refusal(response),
                "hallucination": is_hallucination(response, row["allow_refusal"]),
                "latency": latency,
            })

    RUNS_DIR.mkdir(exist_ok=True)
    out_path = RUNS_DIR / f"run_{run_id}.csv"
    pd.DataFrame(results).to_csv(out_path, index=False)
    return run_id, out_path


def main():
    parser = argparse.ArgumentParser(
        description="Run the golden dataset against one or more LLMs."
    )
    parser.add_argument(
        "--models",
        nargs="+",
        choices=sorted(AVAILABLE_MODELS),
        default=["openai"],
        help="Model adapters to evaluate (default: openai).",
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA,
        help="Path to the golden dataset CSV.",
    )
    args = parser.parse_args()

    run_id, out_path = run(args.models, args.data)
    print("Run complete:", run_id)
    print("Saved to:", out_path)
    print(f"Summarize with: python summarize_run.py {out_path}")


if __name__ == "__main__":
    main()
