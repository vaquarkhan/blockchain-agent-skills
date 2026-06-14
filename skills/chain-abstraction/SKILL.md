---
name: chain-abstraction
description: Unified multi-chain interaction across EVM, Solana, Cosmos, Move (Sui/Aptos), NEAR, and UTXO (Bitcoin). Resolves chain-specific tx models, address formats, and RPC endpoints via ChainProvider adapters. Trigger when selecting chains, normalizing addresses, routing RPC calls, or building cross-chain operations. Phase 1 implements EVM adapters (Ethereum, Arbitrum, Base, Polygon).
---

# Chain Abstraction

## Overview

Provides a **ChainProvider** interface that normalizes chain-specific differences:

- `chainId`, `nativeCurrency`, `blockTime`, `confirmationDepth`
- Address validation (EIP-55, base58, bech32, NEAR named accounts)
- RPC endpoint selection with automatic fallback
- Transaction model mapping (account vs UTXO vs object-centric)

## When to Use

- User asks "which chain should I use?" or provides an ambiguous address
- Normalizing addresses across chain families
- Resolving RPC endpoints and chain metadata
- Building operations that may span multiple chains

## Core Process

### Step 1: Resolve chain

1. Accept `chainName` or `chainId` parameter.
2. Lookup in chain registry (`registry/assets.json` → `chains`).
3. Return normalized metadata: VM type, consensus, token standards, MCP server.

### Step 2: Validate address

Apply format rules from `guardrails/transaction-safety.yaml`:

| Family | Format |
| --- | --- |
| EVM | EIP-55 checksum |
| Solana | base58, 32-byte pubkey |
| Cosmos | bech32 with chain prefix |
| NEAR | `.near` named or implicit hex |
| Bitcoin | bech32 (SegWit) or legacy base58 |

Reject malformed addresses before any RPC call.

### Step 3: Select MCP adapter

Route to chain-family MCP server:

```
EVM chains     → evm-rpc-server
Solana         → solana-rpc-server
NEAR/Aurora    → near-rpc-server
Cosmos/IBC     → cosmos-rpc-server
Sui/Aptos      → move-rpc-server
Bitcoin        → bitcoin-rpc-server
TON            → ton-rpc-server
Substrate      → substrate-rpc-server
```

### Step 4: RPC fallback

1. Try primary RPC from `config.yaml`.
2. On failure (timeout, 429, 5xx), rotate to fallback endpoints.
3. Log RPC health; downgrade confidence if fallback used.

## Phase 1 EVM chains

| Chain | chainId | Block time | Confirm depth |
| --- | --- | --- | --- |
| Ethereum | 1 | ~12s | 12 |
| Arbitrum One | 42161 | ~0.25s | 20 |
| Base | 8453 | ~2s | 20 |
| Polygon PoS | 137 | ~2s | 128 |

## Verification

- [ ] Chain resolved with correct chainId and MCP server
- [ ] Address validated per chain format
- [ ] RPC endpoint reachable or fallback documented
- [ ] Confidence score assigned based on RPC health
