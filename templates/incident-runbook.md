# Blockchain Incident Runbook

Use this template when a chain interaction, contract deployment, or validator operation fails in production.

## Summary

- **Incident ID:**
- **Chain / network:**
- **Severity:**
- **Owner:**

## Impact

- Affected addresses, contracts, or validators
- Funds at risk (if any)
- Downstream systems blocked

## Timeline

| Time (UTC) | Event |
| --- | --- |
| | Detection |
| | Containment |
| | Recovery |

## Immediate Actions

1. Halt further broadcasts until simulation is repeated.
2. Capture tx hash, block height, and RPC responses.
3. Escalate if mainnet guardrails were bypassed.

## Recovery

- Rollback or compensating transaction plan
- Confirmation depth reached
- Post-incident guardrail review

## Follow-up

- Root cause
- Guardrail or skill update
- Evidence attached (`templates/release-gate-evidence.yaml`)
