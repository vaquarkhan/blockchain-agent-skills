# Hooks

Safety hooks for blockchain agent workflows. Run manually or wire into Cursor hooks (`hooks/hooks.json`).

| Hook | Purpose |
| --- | --- |
| `session-start` | Load guardrails and remind simulate-first policy |
| `tx-simulate-pre` | Block mainnet write without simulation artifact |
| `mainnet-guard` | Require explicit confirmation for mainnet operations |
| `sanctions-check-pre` | Remind OFAC screening before counterparty txs |

```bash
bash hooks/session-start.sh
python scripts/hook_runner.py session-start
```
