LLM Evaluation & Monitoring Framework

A lightweight framework for evaluating LLM reliability beyond accuracy.

This project evaluates large language models using a golden dataset and measures:
accuracy, hallucination, refusal behavior, and latency (p50/p95) — producing per-run artifacts for comparison and regression tracking.

Why this matters

Most LLM demos answer:
“Is the response correct?”
Production systems also need to know:
When models hallucinate
When models should refuse
How latency degrades on harder prompts
How behavior changes across runs or models


METRICS TRACKED
Accuracy	How often the model answers correctly
Refusal rate	How often the model safely declines
Hallucination rate	How often the model answers when it shouldn’t
Latency p50	Typical response time
Latency p95	Worst-case response time

PROJECT STRUCTURE
llm-eval-framework/
├── data/        # Golden dataset
├── models/      # LLM adapters (OpenAI, local)
├── scoring/     # Accuracy, refusal, hallucination logic
├── runs/        # Per-run artifacts
├── run_eval.py
├── summarize_run.py

How to run
pip install -r requirements.txt
python run_eval.py
python summarize_run.py runs/run_<id>.csv
