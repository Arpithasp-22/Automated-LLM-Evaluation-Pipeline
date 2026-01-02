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

This framework makes those behaviors measurable.

What it does (at a glance)

Runs the same prompt set across one or more LLMs

Scores each response on:

Accuracy

Refusal behavior

Hallucination

Latency

Writes per-run CSV artifacts

Aggregates results into model-level summaries

Metrics tracked
Metric	What it tells you
Accuracy	How often the model answers correctly
Refusal rate	How often the model safely declines
Hallucination rate	How often the model answers when it shouldn’t
Latency p50	Typical response time
Latency p95	Worst-case response time
Golden dataset

50 prompts across:

Factual

Extraction

Reasoning

Ambiguous

Safety-sensitive tasks

Each prompt defines:

Expected behavior

Whether refusal is allowed

Scoring strategy

This enables repeatable and comparable evaluations.

Example results (single run)
model        accuracy  refusal  hallucination  p50_latency  p95_latency
gpt-4o-mini     0.63      0.04           0.36        1.43s        3.83s


Key insight:
The model performs well on factual prompts but frequently hallucinates on ambiguous inputs.

Project structure
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

Why this is different

Treats hallucination as a first-class failure

Models refusal as correct behavior

Measures latency percentiles, not just averages

Produces audit-friendly run artifacts

Designed for regression tracking

