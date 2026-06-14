# Evaluation Runner

Compares baseline agent concern coverage against with-skills coverage for blockchain tasks.

## Purpose

Answer: **Do the skills cause agents to mention simulation, guardrails, confirmation depth, KMS signing, and compliance more often?**

This is a repeatable CI signal, not a full LLM eval harness.

## Run

```bash
python evals/run.py
python benchmarks/score_benchmarks.py
```

## Custom inputs

```bash
python evals/run.py \
  --tasks benchmarks/tasks.json \
  --baseline benchmarks/baseline-results.json \
  --with-skills benchmarks/with-skills-results.json \
  --report evals/report.json
```

## CI

`.github/workflows/validate-and-package.yml` runs the scorer on push/PR. **CI requires 40/40** concern coverage.

See [gaps.md](gaps.md) for historical gap analysis and out-of-scope areas.

## Updating results

When adding benchmark tasks in `benchmarks/tasks.json`, update both `baseline-results.json` and `with-skills-results.json` to reflect expected concern tags.
