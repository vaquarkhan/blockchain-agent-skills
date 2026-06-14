# Simulate-First Lifecycle

Mandatory write path for all chain families in this repository. No mainnet broadcast without a successful simulation artifact and guardrail env vars.

## Lifecycle phases

| Phase | Command | Purpose | Blocking gate |
| --- | --- | --- | --- |
| Plan | `/plan` | Intent, chain, value at risk, rollback | `templates/tx-plan.yaml` |
| Simulate | `/simulate` | Dry-run state change | Revert → stop |
| Confirm | `/confirm` | Human approval | Mainnet, >$10k, LOW confidence |
| Broadcast | `/broadcast` | KMS-signed send | `SIMULATE_PASSED` + `HUMAN_CONFIRMED` on mainnet |
| Confirm depth | `/confirm-depth` | Finality before downstream actions | `reorg_protection` depths |

## Simulation methods by VM

| VM family | RPC / tool | MCP server |
| --- | --- | --- |
| EVM | `eth_call`, `debug_trace_call` | `evm-rpc-server` → `eth_call` |
| Solana | `simulateTransaction` | `solana-rpc-server` → `simulate_transaction` |
| NEAR | `query` view + dry-run | `near-rpc-server` → `query`, `view_account` |
| Cosmos | `/simulate` REST | Pre-broadcast via signed tx simulation |
| Move (Sui/Aptos) | dry-run / view | `move-rpc-server` → `sui_get_object`, `aptos_view` |
| Bitcoin | `testmempoolaccept` (node) | Read-only planning via `getblockchaininfo` |
| Substrate | `state_call` / dry-run | `substrate-rpc-server` → `chain_get_block` for context |

## Environment variables (write gate)

Broadcast MCP tools call `mcp/_shared/guardrails.py`:

```bash
# After verified simulation (required for all writes)
export SIMULATE_PASSED=true
# OR attach a run ID from your CI simulate job
export SIMULATION_RUN_ID=sim-20260613-abc123

# Mainnet / production only (required in addition to simulation)
export HUMAN_CONFIRMED=true
export NETWORK=mainnet   # or CHAIN_ENV=mainnet

# Emergency override — use only in controlled test harnesses
export BLOCKCHAIN_ALLOW_WRITE=true
```

Failure mode: calling `eth_send_raw_transaction`, `send_transaction`, `send_tx`, or `broadcast_tx` without evidence raises `GuardrailError` and returns a non-broadcast result.

## Hooks and pre-flight scripts

Run from repository root before agent sessions or broadcasts:

```bash
python scripts/hook_runner.py session-start
python scripts/hook_runner.py tx-simulate-pre
python scripts/hook_runner.py mainnet-guard
```

| Hook | When | Output |
| --- | --- | --- |
| `session-start` | Session open | Routes to `using-blockchain-agent-skills` |
| `tx-simulate-pre` | Before `/broadcast` | Reminds: attach `templates/simulate-evidence.yaml` |
| `mainnet-guard` | Mainnet writes | Requires `templates/mainnet-readiness.yaml` |

Shell wrappers: `hooks/session-start.sh`, `hooks/release-guard.sh` (advisory; non-zero on risky state).

## Worked example (EVM ERC-20 transfer)

1. **Plan** — Document recipient, amount, token contract; confidence HIGH if verified on Etherscan.
2. **Simulate** — MCP `eth_call` with `from`, `to`, `data` (encoded `transfer(address,uint256)`).
3. **Confirm** — If `value_usd > 10000`, operator sets `HUMAN_CONFIRMED=true` after review.
4. **Broadcast** — Sign offline via AWS KMS; pass raw hex to `eth_send_raw_transaction` with `SIMULATE_PASSED=true`.
5. **Confirm depth** — Poll `eth_get_transaction_receipt`; wait 12 Ethereum blocks before marking complete.

## Failure modes

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `execution reverted` on `eth_call` | Allowance, pause, wrong selector | Decode revert; do not broadcast |
| `GuardrailError: SIMULATE_PASSED` | Env not set post-simulate | Re-run simulate; export env |
| `GuardrailError: HUMAN_CONFIRMED` | Mainnet without approval | Escalate to human reviewer |
| Receipt OK but balance wrong | Reorg | Wait `/confirm-depth`; reconcile |
| Simulation OK, broadcast fails | Nonce gap, underpriced gas | `transaction-lifecycle` retry rules |

## Audit artifacts

Emit and retain:

- Unsigned tx payload (no keys)
- Simulation trace or `eth_call` return / revert data
- Guardrail env snapshot (redact secrets)
- Signed tx hash, receipt, block number at confirm-depth

## Authoritative sources

- [AGENTS.md — lifecycle order](../AGENTS.md)
- [transaction-lifecycle SKILL](../skills/transaction-lifecycle/SKILL.md)
- [using-blockchain-agent-skills SKILL](../skills/using-blockchain-agent-skills/SKILL.md)
- [MCP write guardrails](../mcp/_shared/guardrails.py)
- [transaction-safety.yaml](../guardrails/transaction-safety.yaml)
- [hook_runner.py](../scripts/hook_runner.py)
- [release-gate-evidence template](../templates/release-gate-evidence.yaml)

## Provenance

| Field | Value |
| --- | --- |
| Source document | `references/simulate-first-lifecycle.md` |
| Version / effective | 1.0 / 2026-06-13 |
| Last reviewed | 2026-06-13 |
| Reviewer | blockchain-agent-skills maintainers |
| Next review due | 2026-09-13 |
| Notes | Aligns with `/plan` → `/confirm-depth` and MCP env gates |
