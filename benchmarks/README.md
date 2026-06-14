# Agent Behavior Benchmarks

This folder contains a lightweight benchmark pack that compares baseline agent behavior against responses produced with the blockchain skills loaded.

Use it to answer one practical question: does the skill pack cause an agent to cover more blockchain concerns such as simulation, mainnet guardrails, confirmation depth, KMS signing, and compliance?

## Included Assets

- `tasks.json` — benchmark prompts for EVM, Solana, Cosmos, compliance, and rollup scenarios
- `baseline-results.json` — sample concern coverage without the skill pack
- `with-skills-results.json` — sample concern coverage with the skill pack loaded
- `score_benchmarks.py` — scores concern coverage and fails if the with-skills run does not improve over baseline

## Run

```bash
python benchmarks/score_benchmarks.py
```

## Good Outcome

The with-skills score should exceed the baseline score and demonstrate that the toolkit changes what the agent remembers to check before broadcast.
