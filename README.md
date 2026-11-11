# Automated LLM Evaluation Pipeline

A lightweight, extensible framework for evaluating LLM reliability beyond accuracy. It runs a golden dataset against one or more LLM providers and scores every response for **accuracy, hallucination, refusal behavior and latency (p50/p95)**. Each run is saved as a CSV artifact so you can compare models and track regressions after a prompt or model change.

**Tech stack:** Python, OpenAI API, Ollama (local models), Pandas

## Why this matters

Most LLM demos only ask: *"Is the response correct?"*

Production systems also need to know:

- When the model **hallucinates**
- When the model **should refuse** (and whether it does)
- How **latency degrades** on harder prompts
- How behavior **changes across runs and models**

## Metrics

| Metric | Definition |
| --- | --- |
| Accuracy | Share of answerable prompts the model gets right (refusal-only prompts are excluded) |
| Refusal rate | Share of all responses that decline to help |
| Hallucination rate | Share of all responses where the model answered a prompt it should have refused |
| Latency p50 / p95 | Median and 95th-percentile response time in seconds |

## Golden dataset

`data/Golden_data.csv` contains **50 prompts** across five categories:

| Category | Prompts |
| --- | --- |
| Factual | 15 |
| Reasoning | 10 |
| Ambiguous | 10 |
| Safety | 10 |
| Extraction | 5 |

Each row has an `expected_answer`, an `allow_refusal` flag (20 prompts are ones the model should decline) and a `scoring` method: `exact_match`, `numeric`, `keyword`, `json_match` or `refusal_only`.

## How it works

```
data/Golden_data.csv
        |
        v
models/   (OpenAI, Ollama)   -->  response + measured latency
        |
        v
scoring/  (accuracy, refusal, hallucination)
        |
        v
runs/run_<id>.csv   -->   summarize_run.py   -->   per-model metrics table
```

## Project structure

```
Automated-LLM-Evaluation-Pipeline/
├── data/               # Golden dataset
├── models/             # LLM adapters (base class, OpenAI, Ollama)
├── scoring/            # Accuracy, refusal and hallucination logic
├── tests/              # Unit tests for the scoring logic
├── runs/               # Per-run CSV artifacts (git-ignored)
├── run_eval.py         # Runs the benchmark
├── summarize_run.py    # Summarizes a saved run
├── .env.example        # Template for your API key
└── requirements.txt
```

## Quickstart

```bash
# 1. Clone and install
git clone https://github.com/Arpithasp-22/Automated-LLM-Evaluation-Pipeline.git
cd Automated-LLM-Evaluation-Pipeline
pip install -r requirements.txt

# 2. Add your OpenAI key
cp .env.example .env        # then edit .env and set OPENAI_API_KEY

# 3. Run the evaluation (default model: gpt-4o-mini, temperature 0)
python run_eval.py

# 4. Summarize the latest run (or pass a specific file)
python summarize_run.py
python summarize_run.py runs/run_<id>.csv
```

To evaluate a local model, start [Ollama](https://ollama.com) (default model `llama3`, served at `localhost:11434`) and run:

```bash
python run_eval.py --models ollama          # local only
python run_eval.py --models openai ollama   # compare both in one run
```

Use `--data path/to/file.csv` to run your own golden dataset with the same columns.

## Adding a new model

1. Create an adapter in `models/` that subclasses `LLMModel` and implements `generate(prompt) -> str`.
2. Register it in the `AVAILABLE_MODELS` dictionary in `run_eval.py`.
3. Run `python run_eval.py --models <your-key>` and compare the new run against earlier ones in `runs/`.

## Tests

```bash
pip install pytest
python -m pytest
```

## Limitations

- Refusal detection matches a fixed list of phrases, so unusual refusal wording can be missed.
- `exact_match` and `keyword` accuracy check whether the expected text appears in the response, which can over-credit long answers.
- The dataset is small (50 prompts), so treat results as a regression signal rather than a benchmark.

## Roadmap

- [ ] Fail the run automatically when a metric regresses past a threshold
- [ ] Retry and error handling for API failures
- [ ] CI workflow (GitHub Actions)
- [ ] Charts comparing runs side by side
