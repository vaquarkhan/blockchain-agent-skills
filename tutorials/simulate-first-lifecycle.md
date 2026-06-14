# Simulate-First Lifecycle Tutorial

## Steps

1. **Plan** — Fill `templates/tx-plan.yaml` with chain, value, and rollback notes.
2. **Simulate** — Call MCP read tools (`eth_call`, `simulateTransaction`) and save `templates/simulate-evidence.yaml`.
3. **Confirm** — Obtain human approval when value exceeds guardrail thresholds.
4. **Broadcast** — Sign with KMS only; never paste private keys into chat.
5. **Confirm depth** — Wait for chain-specific finality before downstream actions.

## Hooks

Run `python scripts/hook_runner.py session-start` at session start and apply `hooks/tx-simulate-pre.sh` before broadcast.
