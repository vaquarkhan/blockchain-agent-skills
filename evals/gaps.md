# Evaluation Gap Analysis

As of **v0.5.0**, benchmark concern coverage is **40/40 complete**.

## Method

`benchmarks/tasks.json` defines 8 tasks with 5 expected concern tags each (40 total).  
`benchmarks/with-skills-results.json` records concern tags that skills and references teach agents to surface.  
`evals/run.py` fails CI if any task is incomplete and writes per-task breakdown to `evals/report.json`.

## Historical gaps (v0.4.0 → closed in v0.5.0)

| Task | Previously missing | Closed by |
| --- | --- | --- |
| `solana_spl_mint` | `upgrade` | `references/solana-program-security.md` — upgrade authority section |
| `cosmos_ibc_transfer` | `reconciliation` | `references/cosmos-ibc-patterns.md` — post-transfer reconciliation |
| `contract_upgrade` | `evidence` | `references/evm-mainnet-guardrails.md` — `release-gate-evidence.yaml` |
| `validator_slashing` | `communication` | `references/substrate-validator-patterns.md` — incident comms |
| `compliance_screening` | `denied-topics` | `guardrails/denied-topics.yaml` + compliance references |
| `rollup_batch` | `cost` | `references/zk-rollup-operations.md` — batch cost analysis |

## Out of scope (not measured by current benchmark)

These are **not** scored in the 40-point harness; they are covered by chain providers, MCP servers, and reference guides instead:

| Area | Coverage | Notes |
| --- | --- | --- |
| Move (Sui/Aptos) | `move-rpc-server`, `references/move-object-patterns.md` | Read paths implemented; Cairo deploy deferred |
| Bitcoin / Lightning | `bitcoin-rpc-server`, `references/bitcoin-utxo-lightning-patterns.md` | UTXO + LND REST read tools |
| Substrate validators | `substrate-rpc-server`, `references/substrate-validator-patterns.md` | Rotation templates; no live validator write MCP |
| Hedera HTS | `hedera-rpc-server`, `references/hedera-hts-patterns.md` | Mirror node reads; council ops human-only |
| ZK prover integration | `skills/privacy-zk`, `references/zk-rollup-operations.md` | Workflow guidance; external prover required |

## Adding benchmark tasks

When adding tasks to `benchmarks/tasks.json`:

1. Update `baseline-results.json` and `with-skills-results.json`.
2. Extend skills/references so each expected concern is documented.
3. Re-run `python evals/run.py` — CI requires **40/40** for the current task set (or update `possible_score` if tasks are added).
