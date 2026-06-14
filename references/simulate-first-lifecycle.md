# Simulate-First Lifecycle

1. **Plan** — Document intent, chain, value at risk, and rollback.
2. **Simulate** — Run dry-run (`eth_call`, `simulateTransaction`, view call) and capture revert data.
3. **Confirm** — Human approval for mainnet, high value, or LOW confidence.
4. **Broadcast** — Sign via KMS; never paste private keys into agent context.
5. **Confirm depth** — Wait for chain-specific finality before downstream actions.

Block broadcast if simulation failed or guardrails are incomplete.
