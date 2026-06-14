# AGENTS.md — Blockchain Agent Entry Point

This file is the **primary routing document** for AI coding agents working in this repository. Read it before loading any skill.

## Mission

Execute **deterministic multi-chain blockchain operations** across 18 supported chains without inventing RPC methods, bypassing guardrails, or broadcasting unsigned/unverified transactions. All write operations pass through **simulate-first** validation and **guardrail checks** before broadcast.

## Mandatory rules

1. **Load skills progressively** — use `using-blockchain-agent-skills` for routing; then load exactly one primary skill per operation thread.
2. **Never expose private keys** — use AWS KMS or HSM; never log, return, or reconstruct seed phrases.
3. **Simulate before broadcast** — block any mainnet write if simulation reverts.
4. **Apply guardrails** — transaction safety, security, and compliance rules in [guardrails/](guardrails/) are non-negotiable.
5. **Emit auditable artifacts** — tx payloads, simulation results, receipts, confidence scores.
6. **Respect lifecycle order**: `/plan` → `/simulate` → `/confirm` → `/broadcast` → `/confirm-depth`.

## Skill routing

| Signal in user request | Primary skill |
| --- | --- |
| Broad / unclear chain or action | `using-blockchain-agent-skills` |
| Multi-chain, chain selection, address format | `chain-abstraction` |
| Build, sign, send, retry, replace tx | `transaction-lifecycle` |
| Deploy, upgrade, verify, interact with contracts | `smart-contract-factory` |
| Read blocks, state, traces, storage slots | `block-state-queries` |
| Events, logs, subgraphs, indexers | `event-indexing` |
| Staking, validators, slashing, MEV-Boost | `consensus-validator-ops` |
| Merkle proofs, storage proofs, light clients | `storage-state-proofs` |
| ERC-20/721, SPL, NEP-141, CW-20, Jettons, etc. | `token-standards-engine` |
| ZK proofs, private txs, ZK-KYC | `privacy-zk` |
| Node health, mempool, forks, gas markets | `network-monitoring` |
| EIP-4844 blobs, Celestia, EigenDA, Avail | `data-availability` |
| L2 deposits/withdrawals, batch posting, fraud proofs | `rollup-operations` |

Full catalog: [skills-index.md](skills-index.md).

## Agent personas (supervisor-worker)

For multi-agent workflows, see `agents/`:

| Agent | Skills | Responsibility |
| --- | --- | --- |
| `blockchain-supervisor.md` | All | Orchestration, guardrail enforcement, result aggregation |
| `chain-interaction-agent.md` | 1, 2, 4 | RPC reads/writes, tx build/simulate/broadcast |
| `contract-agent.md` | 3, 8 | Contract deploy/upgrade/verify, token standards |
| `validator-da-agent.md` | 6, 7, 10, 11 | Validators, proofs, monitoring, DA posting |
| `rollup-zk-agent.md` | 9, 12 | ZK proofs, rollup ops, privacy txs |

## MCP servers

Configure from `mcp/` before chain operations. Eight chain-family servers:

| Server | Chains |
| --- | --- |
| `evm-rpc-server` | ETH, Polygon, Arbitrum, Base, OP, Avalanche C-Chain, BNB, zkSync, Starknet |
| `solana-rpc-server` | Solana mainnet/devnet |
| `near-rpc-server` | NEAR, Aurora |
| `cosmos-rpc-server` | Cosmos Hub, Osmosis, Celestia, Injective, dYdX, Neutron |
| `move-rpc-server` | Sui, Aptos |
| `bitcoin-rpc-server` | Bitcoin, Lightning, Stacks, Liquid |
| `ton-rpc-server` | TON mainnet/testnet |
| `substrate-rpc-server` | Polkadot, Kusama, Moonbeam, Astar |

See [mcp/README.md](mcp/README.md).

## Guardrails

| Category | File |
| --- | --- |
| Transaction safety | `guardrails/transaction-safety.yaml` |
| Security | `guardrails/security.yaml` |
| Compliance | `guardrails/compliance.yaml` |
| Denied topics | `guardrails/denied-topics.yaml` |

## Key files

| File | Role |
| --- | --- |
| `registry/assets.json` | Skills, MCP servers, chains index |
| `docs/TECHNICAL-REFERENCE.md` | Full chain coverage and architecture spec |
| `docs/coverage-roadmap.md` | Phase implementation roadmap |
| `templates/` | Bedrock action group, Lambda, OpenAPI scaffolds |

## Validation

Before committing skill or asset changes:

```bash
python scripts/validate-skills.py
```
