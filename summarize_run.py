import sys
from pathlib import Path

import pandas as pd

RUNS_DIR = Path(__file__).resolve().parent / "runs"


def latest_run():
    runs = sorted(RUNS_DIR.glob("run_*.csv"), key=lambda p: p.stat().st_mtime)
    if not runs:
        sys.exit("No run files found in runs/. Run `python run_eval.py` first.")
    return runs[-1]


# Use the file given on the command line, otherwise the most recent run.
run_file = Path(sys.argv[1]) if len(sys.argv) > 1 else latest_run()

df = pd.read_csv(run_file)

summary = (
    df.groupby("model")
      .agg(
          accuracy_rate=("accuracy", lambda x: x.dropna().mean()),
          refusal_rate=("refusal", "mean"),
          hallucination_rate=("hallucination", "mean"),
          latency_p50=("latency", "median"),
          latency_p95=("latency", lambda x: x.quantile(0.95)),
          total_prompts=("prompt_id", "count")
      )
      .reset_index()
)

print(f"\n=== MODEL EVALUATION SUMMARY ({run_file.name}) ===\n")
print(summary.to_string(index=False))
