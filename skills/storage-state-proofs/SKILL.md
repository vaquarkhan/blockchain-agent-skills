---
name: storage-state-proofs
description: Merkle and Patricia trie proofs, storage slot reading, and state verification across chains. Generates proofs for cross-chain verification, zkBridge, and light client protocols. Trigger when proving account balance, storage slot, or cross-chain state inclusion.
---

# Storage & State Proofs

## Overview

Proof generation per VM:

| Chain | Proof type |
| --- | --- |
| EVM | Merkle-Patricia trie proof (EIP-1186 eth_getProof) |
| Solana | Account proof via bank hash |
| Cosmos | ICS-23 proof via IBC |
| Bitcoin | Merkle proof of tx inclusion in block |

## Core Process

### Step 1: Identify proof requirement

- Light client verification
- Cross-chain bridge (zkBridge, IBC)
- Audit evidence of on-chain state at block N

### Step 2: Generate proof

**EVM:**

```
eth_getProof(address, [storageKeys], blockNumber)
→ accountProof[], storageProof[][]
```

Verify proof against known block header state root.

### Step 3: Cross-chain verification

Submit proof to verifier contract or light client on destination chain.

## Verification

- [ ] Proof generated at specific block height
- [ ] State root matches known block header
- [ ] Verifier accepts proof on destination (if cross-chain)
