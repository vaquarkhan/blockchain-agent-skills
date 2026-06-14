# Templates

Operational templates for blockchain agent workflows.

| Template | Use |
| --- | --- |
| `skill-definition.yaml` | Bedrock / skill metadata |
| `tx-plan.yaml` | Pre-broadcast transaction plan |
| `simulate-evidence.yaml` | Simulation evidence bundle |
| `mainnet-readiness.yaml` | Mainnet deploy checklist |
| `release-gate-evidence.yaml` | Release signoff record |
| `incident-runbook.md` | Chain incident response |
| `contract-audit-checklist.yaml` | Pre-deploy contract review |
| `bridge-transfer-plan.yaml` | Cross-chain bridge planning |
| `validator-rotation-plan.yaml` | Validator key rotation |
| `compliance-screening.yaml` | Sanctions / travel-rule record |
| `ibc-transfer-plan.yaml` | Cosmos IBC transfer plan |

Validated by `python scripts/validate-template-schemas.py` (starter packs) and `python scripts/validate-assets.py` (registry paths).
