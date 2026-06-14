# EVM Mainnet Guardrails

- Require `templates/mainnet-readiness.yaml` before deploy.
- Simulate every state-changing call on a fork or `eth_call`.
- Set confirmation depth per chain (Ethereum 12+, L2s 20+).
- Escalate when USD value exceeds guardrail threshold.
- Attach `templates/release-gate-evidence.yaml` to release PRs.
