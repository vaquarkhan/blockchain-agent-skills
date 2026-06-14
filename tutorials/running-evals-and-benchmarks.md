# Running Evals and Benchmarks

```bash
python benchmarks/score_benchmarks.py
python evals/run.py
```

Benchmarks compare baseline vs with-skills concern coverage using `benchmarks/tasks.json`. CI runs these via `.github/workflows/agent-benchmarks.yml`.
