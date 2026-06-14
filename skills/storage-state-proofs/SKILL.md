---
name: storage-state-proofs
description: Merkle and Patricia trie proofs, storage slot reading, and state verification across chains. Generates proofs for cross-chain verification, zkBridge, and light client protocols. Trigger when proving account balance, storage slot, or cross-chain state inclusion.
---

# Storage & State Proofs

## Overview

Cryptographic proof generation and verification for on-chain state inclusion across VM families. Read-heavy with optional on-chain verifier submission via `transaction-lifecycle`.

| Chain | Proof type | MCP tool | Tier |
| --- | --- | --- | --- |
| EVM | Merkle-Patricia trie (EIP-1186) | `eth_getProof` | 1 |
| Solana | Account proof via bank hash | bank hash + account data | 2 |
| Cosmos | ICS-23 proof via IBC | IBC client query | 2 |
| Bitcoin | Merkle tx inclusion | block Merkle branch | 4 read via `bitcoin-rpc-server` |

Proofs enable light client verification, cross-chain bridges (zkBridge, IBC), and audit evidence of state at block N.

## When to Use

- Proving account balance or storage slot at historical block height
- Cross-chain state verification (submit proof to destination verifier)
- Light client protocols and zkBridge workflows
- Audit evidence: cryptographic proof of on-chain state
- Complementing `block-state-queries` with verifiable inclusion

Do **not** use for simple reads without proof requirement (use `block-state-queries`).

## Core Process

### Step 1: Identify proof requirement

| Requirement | Proof elements | Verifier |
| --- | --- | --- |
| Account balance | accountProof against state root | L1 header stateRoot |
| Storage slot | storageProof[] for key | Same account trie |
| Cross-chain | accountProof + header proof | Destination chain verifier contract |
| IBC (Cosmos) | ICS-23 proof packet | Counterparty light client |

Record target block height — **archive node required** for historical proofs.

### Step 2: Generate proof (EVM)

Via `evm-rpc-server` → `eth_getProof`:

```
eth_getProof(address, [storageKeys], blockNumber)
→ { accountProof[], storageProof[][], balance, codeHash, storageHash }
```

1. Resolve chain via `chain-abstraction`.
2. Fetch block header at `blockNumber` → extract `stateRoot`.
3. Verify proof path hashes reconstruct to `stateRoot`.
4. Return proof bundle with block header for independent verification.

### Step 3: Verify proof locally

1. RLP-decode proof nodes; walk Patricia trie path.
2. Confirm `keccak256(rlp(node))` links match state root.
3. For storage proofs: verify storage trie root matches `storageHash` in account.
4. Assign confidence: HIGH (archive node, verified root), LOW (incomplete proof path).

### Step 4: Cross-chain verification (optional)

1. Submit proof + header to verifier contract on destination chain.
2. Simulate `verifyProof()` via `eth_call` before broadcast.
3. Broadcast via `transaction-lifecycle` if on-chain submission required.

### Step 5: Non-EVM proofs

**Solana (Tier 2):** Account data + bank hash at slot; verify against cluster confirmed block.  
**Cosmos (Tier 2):** ICS-23 proof via `abci_query` with proof enabled; verify against IBC client state.

## Decision framework

1. **Proof for current or historical block?** → Historical: archive node mandatory.
2. **Account only or storage slot?** → Storage requires storage key in `eth_getProof` array.
3. **Local verification or on-chain submission?** → Local first; on-chain for trustless third party.
4. **EVM or IBC path?** → EVM: EIP-1186. Cosmos cross-chain: ICS-23 via IBC client.
5. **Block header source?** → Must match proof blockNumber; fetch via `eth_getBlockByNumber`.
6. **Tier 4 (Bitcoin Merkle)?** → State roadmap; document limitation.

| Scenario | Tool | Archive? |
| --- | --- | --- |
| Prove USDC balance block 18M | eth_getProof | Yes |
| Prove mapping slot | eth_getProof + storageKey | Yes |
| zkBridge submit | eth_getProof + header → dest verifier | Yes |
| IBC token balance | ICS-23 abci_query | Client state height |

## Anti-patterns and rationalizations

| Rationalization | Risk | Required response |
| --- | --- | --- |
| "Proof at latest — full node OK" | Stale root if reorg | Pin blockNumber; use finalized block |
| "Skip local verification — submit on-chain" | Failed verify tx, wasted gas | Verify locally before submit |
| "State root from different block" | Invalid proof | Header blockNumber must match proof |
| "eth_getProof without storage key" | Incomplete storage proof | Include keccak256(slot) for mappings |
| "Trust RPC proof without walk" | Tampered proof from bad RPC | Independently verify trie path |
| "Historical proof on pruned node" | Empty or error response | Require archive; block if unavailable |
| "Cross-chain without simulate" | Verifier revert | eth_call verifyProof before broadcast |

## Verification

- [ ] Target block height and chain resolved via `chain-abstraction`
- [ ] Archive node confirmed for historical proof generation
- [ ] `eth_getProof` (or chain equivalent) returned complete proof path
- [ ] Block header fetched at matching blockNumber
- [ ] stateRoot from header matches locally recomputed root from proof
- [ ] Storage proof verified against account storageHash (if applicable)
- [ ] Local verification passed before any on-chain submission
- [ ] On-chain verifier simulated via `eth_call` (if cross-chain submit)
- [ ] Confidence score assigned based on node tier and verification result
- [ ] Proof bundle documented for audit (blockNumber, address, storageKeys)
- [ ] KMS signing for on-chain submit txs only via `transaction-lifecycle`
- [ ] Audit trail logged per `compliance.yaml`
