import sys
import pandas as pd

run_file = sys.argv[1]

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

print("\n=== MODEL EVALUATION SUMMARY ===\n")
print(summary.to_string(index=False))
