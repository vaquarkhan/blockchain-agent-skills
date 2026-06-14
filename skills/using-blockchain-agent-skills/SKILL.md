---
name: using-blockchain-agent-skills
description: Meta entry skill for the blockchain-agent-skills repository. Routes tasks to chain abstraction, transaction lifecycle, smart contracts, state queries, event indexing, validator ops, storage proofs, token standards, privacy/ZK, network monitoring, data availability, and rollup skills; configures MCP servers, guardrails, and the tx lifecycle (/plan, /simulate, /confirm, /broadcast, /confirm-depth). Trigger when starting any multi-chain operation, choosing which skill to load, onboarding, or orchestrating cross-chain workflows. Do not use when a specific skill already matches the task.
---

# Using Blockchain Agent Skills

## Overview

This skill is the **routing and orchestration layer** for the blockchain-agent-skills repository. It teaches the agent how to discover, load, and chain specialized skills without inventing RPC methods or bypassing guardrails.

All write operations enforce **simulate-first** validation and **guardrail checks** from `guardrails/` before mainnet broadcast. Private keys never enter LLM context — signing occurs via AWS KMS/HSM only (`guardrails/security.yaml` → `private_key_protection`, override: none).

**Implementation tiers:**

| Tier | Scope | Status |
| --- | --- | --- |
| Tier 1 | EVM chains via `lib/chain_providers/evm.py` | Implemented |
| Tier 2 | Solana, NEAR, Cosmos via `lib/chain_providers/` | Implemented |
| Tier 3 | Move (Sui/Aptos), ZK rollups, DA layers | `move-rpc-server` + EVM L2 routing |
| Tier 4 | Bitcoin, TON, Substrate | `bitcoin-rpc-server`, `ton-rpc-server`, `substrate-rpc-server` |

**Lifecycle commands:**

| Command | Purpose | Guardrail refs |
| --- | --- | --- |
| `/plan` | Identify chain, action, MCP tools, guardrail checks | All three YAML files |
| `/simulate` | Dry-run tx or call; decode revert reasons | `transaction-safety.yaml` → `simulate_before_broadcast` |
| `/confirm` | Human confirmation for high-value or LOW-confidence ops | `transaction-safety.yaml` → `max_value_without_confirmation` ($10k) |
| `/broadcast` | Sign (KMS) and submit to network | `security.yaml` → `blind_signing_block` |
| `/confirm-depth` | Wait for chain-specific finality depth | `transaction-safety.yaml` → `reorg_protection` |

## When to Use

Use this skill when:

- The user asks a **broad blockchain question** without naming a chain or skill
- You need to **select among the 12 core skills**
- Configuring **MCP servers** for a chain family
- Starting a **new operation** and defining plan before execution
- Chaining skills (e.g., chain-abstraction → transaction-lifecycle → block-state-queries)

Do **not** use when the task maps cleanly to one specialized skill (load it directly).

## Core Process

### Step 1: Intake and chain detection

1. Parse the user request for:
   - **Chain signals**: EVM (ETH, Arbitrum, Base), Solana (SVM, Anchor), NEAR (named accounts), Cosmos (IBC), Move (Sui/Aptos objects), Bitcoin (UTXO), etc.
   - **Action type**: read, write, deploy, stake, bridge, index
   - **Environment**: mainnet vs testnet, MCP availability, KMS signing
2. If multiple chains apply, propose a **sequenced plan** with cross-chain dependencies.
3. Record operation metadata: UTC timestamp, run ID, target chain(s), value estimate.

### Step 2: Plan (`/plan`)

1. Document **target chain** with chainId, RPC endpoint, confirmation depth from `registry/chains.json`.
2. Select **MCP server** from chain family (see `mcp/README.md`).
3. Load applicable **guardrails**: `guardrails/transaction-safety.yaml`, `guardrails/security.yaml`, `guardrails/compliance.yaml`.
4. Emit plan artifact: `plan-{run-id}.json` with skill route, guardrail refs, and confidence baseline.

### Step 3: Skill routing matrix

Load **exactly one primary skill** per operation thread:

| User intent | Primary skill | Common secondary |
| --- | --- | --- |
| Which chain / address format | `chain-abstraction` | — |
| Send / retry / cancel tx | `transaction-lifecycle` | `chain-abstraction` |
| Read balance / block / trace | `block-state-queries` | `chain-abstraction` |
| Deploy / upgrade contract | `smart-contract-factory` | `transaction-lifecycle` |
| Events / subgraphs | `event-indexing` | `block-state-queries` |
| Mint / transfer tokens | `token-standards-engine` | `transaction-lifecycle` |
| Stake / validator / MEV | `consensus-validator-ops` | `network-monitoring` |
| Merkle / storage proof | `storage-state-proofs` | `block-state-queries` |
| ZK proof / private tx | `privacy-zk` | `transaction-lifecycle` |
| Node health / fork / gas | `network-monitoring` | — |
| Blob / DA posting | `data-availability` | `transaction-lifecycle` |
| L2 bridge / withdrawal | `rollup-operations` | `transaction-lifecycle` |

### Step 4: MCP configuration

Confirm required MCP server before `/simulate`:

| MCP server | Chains | Key tools |
| --- | --- | --- |
| evm-rpc-server | ETH, Polygon, Arbitrum, Base, OP, Avalanche, BNB, zkSync, Starknet | `eth_call`, `eth_sendRawTransaction`, `eth_getProof` |
| solana-rpc-server | Solana | `simulateTransaction`, `getAccountInfo` |
| near-rpc-server | NEAR, Aurora | `view_function`, `send_tx` |
| cosmos-rpc-server | Cosmos Hub, Osmosis, Celestia, Injective | `abci_query`, `broadcast_tx` |
| move-rpc-server | Sui, Aptos | Implemented |
| bitcoin-rpc-server | Bitcoin, Lightning, Stacks | Implemented |
| ton-rpc-server | TON | Implemented |
| substrate-rpc-server | Polkadot, Moonbeam, Astar | Implemented |

If required MCP is unavailable, **stop** and document blocking status — do not invent RPC methods.

### Step 5: Simulate (`/simulate`)

1. Apply guardrails from `guardrails/transaction-safety.yaml` and `guardrails/security.yaml`.
2. Run chain-specific simulation (`eth_call`, `simulateTransaction`, NEAR dry-run, Cosmos `simulate`).
3. Decode revert reasons structurally — do not broadcast on failure.
4. Assign **confidence score**: HIGH (sim pass + fresh RPC), MEDIUM (sim pass + stale RPC or fallback endpoint), LOW (edge case, partial data, or Tier 3–4 chain).

### Step 6: Confirm (`/confirm`)

Require human confirmation when:

- Transaction value > **$10,000** equivalent (`transaction-safety.yaml`)
- Contract unaudited or **<7 days** old with high value (`security.yaml` → `contract_age_check`)
- Validator operations, rollup exit proofs, or fraud proof submission
- Confidence score is **LOW**
- Travel rule applies: VASP-to-VASP transfer > **$1,000** (`compliance.yaml`)

### Step 7: Broadcast (`/broadcast`)

1. Sign via KMS/HSM — never in LLM context.
2. Broadcast via MCP tool (`eth_sendRawTransaction`, `send_tx`, etc.).
3. Log payload hash, simulation result, and tx hash to audit trail (`compliance.yaml` → DynamoDB, 7-year retention).

### Step 8: Confirm depth (`/confirm-depth`)

Wait for chain-specific finality before marking complete:

| Chain | Blocks/slots |
| --- | --- |
| Ethereum | 12 blocks |
| BNB | 15 blocks |
| Bitcoin | 6 blocks |
| Solana | 32 slots |
| Arbitrum / Base | 20 blocks (L1 finality for high-value) |

## Decision framework

1. **Is the task read-only?** → Yes: route to `block-state-queries` or `event-indexing`; skip `/broadcast`. No: continue.
2. **Is chain ambiguous or multi-chain?** → Yes: load `chain-abstraction` first. No: resolve chain via `lib.chain_providers.resolve_chain()`.
3. **Does task involve token mint/transfer/approve?** → Yes: `token-standards-engine` + `transaction-lifecycle`. No: continue.
4. **Does task involve contract deploy/upgrade?** → Yes: `smart-contract-factory`. No: continue.
5. **Is it L2 bridge / withdrawal / batch?** → Yes: `rollup-operations`. No: continue.
6. **Is it validator / staking / MEV?** → Yes: `consensus-validator-ops` (always requires `/confirm`). No: continue.
7. **Is it ZK proof or privacy tx?** → Yes: `privacy-zk`; check `guardrails/denied-topics.yaml` for sanctions evasion. No: continue.
8. **Default write path:** `transaction-lifecycle` with full lifecycle `/plan` → `/simulate` → `/confirm` → `/broadcast` → `/confirm-depth`.

| Signal | Primary skill | MCP server |
| --- | --- | --- |
| "Which chain?" | chain-abstraction | Resolve first |
| "Send 1 ETH" | transaction-lifecycle | evm-rpc-server |
| "Deploy ERC-20" | smart-contract-factory | evm-rpc-server |
| "Index Transfer events" | event-indexing | evm-rpc-server + subgraph |
| "Prove storage slot" | storage-state-proofs | evm-rpc-server → `eth_getProof` |
| "Withdraw from Arbitrum" | rollup-operations | evm-rpc-server (L1 + L2) |

## Anti-patterns and rationalizations

| Rationalization | Risk | Required response |
| --- | --- | --- |
| "User is in a hurry — skip simulation" | Mainnet revert, fund loss, unaudited contract exposure | Block broadcast; run `/simulate` per `transaction-safety.yaml` |
| "I'll load two primary skills in parallel" | Conflicting nonce/gas assumptions, duplicate broadcasts | One primary skill per operation thread; secondaries only for reads |
| "Private key in env var is fine for this test" | Key exposure in logs, LLM context, audit trail | KMS/HSM only; never accept key material |
| "Sanctioned address is probably a false positive" | Regulatory violation; no override per `compliance.yaml` | Block immediately; document screening result |
| "MCP server down — I'll call RPC directly" | Undocumented methods, no rate limiting, no audit | Stop; document blocking status; use configured MCP |
| "Tx is in mempool — mark as complete" | Reorg, replacement, or drop loses finality | Wait for `/confirm-depth` before completion |
| "Low confidence but user said go" | Wrong chain, stale state, incorrect encoding | Require explicit `/confirm` with LOW-confidence disclosure |
| "Tier 3 chain — I'll guess the RPC method" | Invalid calls, security bypass | State Tier 3 limitation; use documented MCP scaffold only |

## Red Flags

- Mainnet broadcast without simulation
- Private key or seed phrase in logs or LLM context
- Sanctioned address not blocked (OFAC SDN, EU, UN, UK HMT)
- Unverified contract interaction without override
- Treating unconfirmed tx as final
- Mixer/tumbler interaction (Tornado Cash, etc.) — block per `compliance.yaml`
- Unlimited ERC-20 approval without bounded alternative suggested

## Verification

- [ ] Chain and primary skill identified in `plan-{run-id}.json` artifact
- [ ] All three guardrail files loaded: `transaction-safety.yaml`, `security.yaml`, `compliance.yaml`
- [ ] MCP server confirmed available via health check before `/simulate`
- [ ] Chain resolved via `lib.chain_providers.resolve_chain()` or registry (Tier 1–2)
- [ ] Simulation passed or broadcast explicitly blocked with decoded revert reason
- [ ] Destination addresses validated per chain format (`transaction-safety.yaml` → `destination_validation`)
- [ ] Sanctions screening applied to all counterparties (`compliance.yaml` → `sanctions_screening`)
- [ ] Human confirmation obtained for >$10k, LOW confidence, or validator/rollup ops
- [ ] KMS signing used — no private key material in logs or agent context
- [ ] Audit log entry created with tx hash, simulation result, confidence score (DynamoDB)
- [ ] Confirmation depth reached per chain before marking operation complete
- [ ] Confidence score (HIGH/MEDIUM/LOW) included in every operation response
