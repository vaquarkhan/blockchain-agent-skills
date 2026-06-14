# Skills Index

Machine-readable registry: [registry/assets.json](registry/assets.json).  
Validation: `python scripts/validate-skills.py`  
Coverage gaps: [docs/coverage-roadmap.md](docs/coverage-roadmap.md)

---

## Meta / orchestration

| Skill | Path | Summary |
| --- | --- | --- |
| **using-blockchain-agent-skills** | [skills/using-blockchain-agent-skills/](skills/using-blockchain-agent-skills/) | Routes tasks to chain skills; configures MCP servers, guardrails, and tx lifecycle (`/plan` … `/confirm-depth`). |

---

## Phase 1 — EVM Core

| Skill | Path | Summary |
| --- | --- | --- |
| **chain-abstraction** | [skills/chain-abstraction/](skills/chain-abstraction/) | Unified multi-chain interface — EVM, Solana, Cosmos, Move, NEAR, UTXO. Resolves tx models, address formats, RPC endpoints. |
| **transaction-lifecycle** | [skills/transaction-lifecycle/](skills/transaction-lifecycle/) | Build, sign, simulate, broadcast, confirm, retry, replace txs. Nonce/gas management, stuck-tx recovery. |
| **block-state-queries** | [skills/block-state-queries/](skills/block-state-queries/) | Read chain state, trace calls, parse receipts, historical blocks. Unified query API across all VMs. |

**Phase 1 chains:** Ethereum, Arbitrum, Base, Polygon

---

## Phase 2 — Alt-L1s

| Skill | Path | Summary |
| --- | --- | --- |
| **smart-contract-factory** | [skills/smart-contract-factory/](skills/smart-contract-factory/) | Deploy, upgrade (UUPS/Transparent/Diamond), verify, interact. Solidity, Cairo, Rust/Anchor, CosmWasm. |
| **event-indexing** | [skills/event-indexing/](skills/event-indexing/) | Subscribe to events, parse logs, real-time pipelines. The Graph, Goldsky, Envio, Subsquid. |
| **token-standards-engine** | [skills/token-standards-engine/](skills/token-standards-engine/) | Deploy/manage tokens per chain-native standards: ERC-20/721, NEP-141, SPL, CW-20, Jettons, Coin/Kiosk. |

**Phase 2 chains:** Solana, NEAR, Cosmos

---

## Phase 3 — ZK & Move

| Skill | Path | Summary |
| --- | --- | --- |
| **rollup-operations** | [skills/rollup-operations/](skills/rollup-operations/) | L2 deposits/withdrawals, sequencer interaction, batch posting, fraud/validity proofs. OP Stack + ZK Stack. |
| **data-availability** | [skills/data-availability/](skills/data-availability/) | EIP-4844 blob posting, Celestia, EigenDA, Avail, Near DA. Blob fee calculation and routing. |
| **privacy-zk** | [skills/privacy-zk/](skills/privacy-zk/) | ZK proof generation/verification, private txs, ZK-KYC. STARK, SNARK, Groth16/PLONK, Aztec. |
| **storage-state-proofs** | [skills/storage-state-proofs/](skills/storage-state-proofs/) | Merkle/Patricia trie proofs, storage slot reading, cross-chain state verification. |

**Phase 3 chains:** Starknet, zkSync Era, Sui, Aptos

---

## Phase 4 — Legacy & Niche

| Skill | Path | Summary |
| --- | --- | --- |
| **consensus-validator-ops** | [skills/consensus-validator-ops/](skills/consensus-validator-ops/) | Staking, validator management, slashing protection, MEV-Boost. PoS, PoW, PoSA, Hashgraph, Snow. |
| **network-monitoring** | [skills/network-monitoring/](skills/network-monitoring/) | Node health, mempool analysis, fork detection, reorg handling, gas market tracking. |

**Phase 4 chains:** Bitcoin L2s, TON, Polkadot, Hedera

---

## Routing quick reference

```
User intent unclear           → using-blockchain-agent-skills
Which chain / address format  → chain-abstraction
Send / retry / cancel tx      → transaction-lifecycle
Read balance / block / trace  → block-state-queries
Deploy or upgrade contract    → smart-contract-factory
Listen to events / subgraph   → event-indexing
Mint ERC-20 / SPL / NEP-141   → token-standards-engine
Stake / validator / MEV       → consensus-validator-ops
Merkle / storage proof        → storage-state-proofs
ZK proof / private tx         → privacy-zk
Node down / fork / gas spike  → network-monitoring
Post blob / DA layer          → data-availability
L2 bridge / withdrawal        → rollup-operations
```
