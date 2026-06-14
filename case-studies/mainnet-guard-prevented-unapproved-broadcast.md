# Case Study: Mainnet Guard Prevented Unapproved Broadcast

## Situation

An agent attempted to broadcast a high-value mainnet transfer without human confirmation.

## Actions

1. `mainnet-guard` hook flagged the threshold breach.
2. Team re-ran simulation and attached `release-gate-evidence.yaml`.
3. Human approver signed off before KMS broadcast.

## Outcome

Funds moved only after simulate-first evidence and guardrail signoff.

## Lessons

- Keep mainnet thresholds in `guardrails/transaction-safety.yaml`.
- Never disable hooks for production workspaces.
