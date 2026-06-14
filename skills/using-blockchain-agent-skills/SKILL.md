---
name: using-blockchain-agent-skills
description: Meta entry skill for the blockchain-agent-skills repository. Routes tasks to chain abstraction, transaction lifecycle, smart contracts, state queries, event indexing, validator ops, storage proofs, token standards, privacy/ZK, network monitoring, data availability, and rollup skills; configures MCP servers, guardrails, and the tx lifecycle (/plan, /simulate, /confirm, /broadcast, /confirm-depth). Trigger when starting any multi-chain operation, choosing which skill to load, onboarding, or orchestrating cross-chain workflows. Do not use when a specific skill already matches the task.
---

# Using Blockchain Agent Skills

## Overview

This skill is the **routing and orchestration layer** for the blockchain-agent-skills repository. It teaches the agent how to discover, load, and chain specialized skills without inventing RPC methods or bypassing guardrails.

All write operations enforce **simulate-first** validation and **guardrail checks** from `guardrails/` before mainnet broadcast. Private keys never enter LLM context — signing occurs via AWS KMS/HSM only.

**Lifecycle commands:**

| Command | Purpose |
| --- | --- |
| `/plan` | Identify chain, action, required MCP tools, and guardrail checks |
| `/simulate` | Dry-run transaction or call; decode revert reasons |
| `/confirm` | Human confirmation for high-value or LOW-confidence operations |
| `/broadcast` | Sign (KMS) and submit to network |
| `/confirm-depth` | Wait for chain-specific finality depth |

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

1. Document **target chain** with chainId, RPC endpoint, confirmation depth.
2. Select **MCP server** from chain family (see `mcp/README.md`).
3. Load applicable **guardrails**: transaction-safety, security, compliance.
4. Emit plan artifact: `plan-{run-id}.json` with skill route and guardrail refs.

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

| MCP server | Chains |
| --- | --- |
| evm-rpc-server | ETH, Polygon, Arbitrum, Base, OP, Avalanche, BNB, zkSync, Starknet |
| solana-rpc-server | Solana |
| near-rpc-server | NEAR, Aurora |
| cosmos-rpc-server | Cosmos Hub, Osmosis, Celestia, Injective |
| move-rpc-server | Sui, Aptos |
| bitcoin-rpc-server | Bitcoin, Lightning, Stacks |
| ton-rpc-server | TON |
| substrate-rpc-server | Polkadot, Moonbeam, Astar |

If required MCP is unavailable, **stop** and document blocking status.

### Step 5: Simulate (`/simulate`)

1. Apply guardrails from `guardrails/transaction-safety.yaml` and `security.yaml`.
2. Run chain-specific simulation; decode revert reasons structurally.
3. Assign **confidence score**: HIGH (sim pass + fresh RPC), MEDIUM (sim pass + stale RPC), LOW (edge case or partial data).

### Step 6: Confirm (`/confirm`)

Require human confirmation when:

- Transaction value > $10,000 equivalent
- Contract unaudited or <7 days old with high value
- Validator operations or rollup exit proofs
- Confidence score is LOW

### Step 7: Broadcast (`/broadcast`)

1. Sign via KMS/HSM — never in LLM context.
2. Broadcast via MCP tool.
3. Log payload, simulation result, and tx hash to audit trail (DynamoDB, 7-year retention).

### Step 8: Confirm depth (`/confirm-depth`)

Wait for chain-specific finality before marking complete:

| Chain | Blocks/slots |
| --- | --- |
| Ethereum | 12 blocks |
| BNB | 15 blocks |
| Bitcoin | 6 blocks |
| Solana | 32 slots |

## Red Flags

- Mainnet broadcast without simulation
- Private key or seed phrase in logs or LLM context
- Sanctioned address not blocked
- Unverified contract interaction without override
- Treating unconfirmed tx as final

## Verification

- [ ] Chain and skill identified in plan artifact
- [ ] Guardrails loaded and applied
- [ ] MCP server confirmed available
- [ ] Simulation passed (or broadcast blocked)
- [ ] Human confirmation obtained where required
- [ ] Audit log entry with tx hash and confidence score
- [ ] Finality depth reached before marking complete
