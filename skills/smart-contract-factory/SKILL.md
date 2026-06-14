---
name: smart-contract-factory
description: Deploy, upgrade (UUPS/Transparent/Diamond), verify, and interact with smart contracts. Supports Solidity, Cairo, Rust (Anchor/Ink!/Move), and CosmWasm across all chains. Trigger when deploying contracts, proxy upgrades, Etherscan verification, or complex multi-sig/diamond interactions. Phase 2+ for non-EVM VMs.
---

# Smart Contract Factory

## Overview

Contract lifecycle management:

- **Deploy** — factory patterns, CREATE2 deterministic addresses
- **Upgrade** — UUPS, Transparent Proxy, Diamond (EIP-2535)
- **Verify** — Etherscan/Blockscout/Sourcify source verification
- **Interact** — ABI/IDL-driven encoding, Multicall3 batching

## Core Process

### Step 1: Compile and audit check

1. Identify language: Solidity, Cairo, Rust/Anchor, CosmWasm.
2. Warn if contract <30 days old with no audit; escalate if <7 days + high value.
3. Block interaction with unverified contracts on mainnet (guardrail).

### Step 2: Deploy

1. Estimate gas via `transaction-lifecycle`.
2. Simulate deploy transaction.
3. Sign and broadcast; capture deployed address from receipt logs.

### Step 3: Verify

Post-deploy verification on chain explorer:

- EVM: Etherscan/Blockscout API with standard-json-input
- Solana: Anchor IDL on-chain + verification
- NEAR: NEP-330 source metadata

### Step 4: Upgrade (proxies)

| Pattern | Upgrade function location |
| --- | --- |
| UUPS | Implementation contract |
| Transparent | ProxyAdmin |
| Diamond | facet cut on Diamond contract |

Always simulate upgrade tx; verify storage layout compatibility.

## Verification

- [ ] Simulation passed for deploy/upgrade/interact
- [ ] Contract verified on explorer
- [ ] Proxy pattern documented if applicable
- [ ] Audit trail logged
