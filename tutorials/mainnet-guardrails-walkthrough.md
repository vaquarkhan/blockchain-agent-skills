# Mainnet Guardrails Walkthrough

1. Review `guardrails/transaction-safety.yaml` thresholds ($10k human confirm).
2. Complete `templates/mainnet-readiness.yaml` before mainnet deploy.
3. Attach `templates/release-gate-evidence.yaml` to the change record.
4. Run `hooks/mainnet-guard.sh` before approving broadcast.
