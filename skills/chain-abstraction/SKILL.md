---
name: chain-abstraction
description: Unified multi-chain interaction across EVM, Solana, Cosmos, Move (Sui/Aptos), NEAR, and UTXO (Bitcoin). Resolves chain-specific tx models, address formats, and RPC endpoints via ChainProvider adapters. Trigger when selecting chains, normalizing addresses, routing RPC calls, or building cross-chain operations. Phase 1 EVM + Phase 2 Solana, NEAR, Cosmos implemented in lib/chain_providers/.
---

# Chain Abstraction

## Overview

Provides a **ChainProvider** interface that normalizes chain-specific differences across 18 supported chains:

- `chainId`, `nativeCurrency`, `blockTime`, `confirmationDepth`
- Address validation (EIP-55, base58, bech32, NEAR named accounts)
- RPC endpoint selection with automatic fallback
- Transaction model mapping (account vs UTXO vs object-centric)

**Tier status:**

| Tier | Chains | Implementation |
| --- | --- | --- |
| Tier 1 | Ethereum, Arbitrum, Base, Polygon | `lib/chain_providers/evm.py` — full `resolve_chain()`, `validate_address()` |
| Tier 2 | Solana, NEAR, Aurora, Cosmos Hub, Osmosis, Celestia, Injective | `lib/chain_providers/solana.py`, `near.py`, `cosmos.py` |
| Tier 3 | Sui, Aptos, Starknet, zkSync | `lib/chain_providers/move.py` + `move-rpc-server`; EVM L2 via `evm-rpc-server` |
| Tier 4 | Bitcoin, TON, Polkadot, Kusama, Moonbeam | `lib/chain_providers/bitcoin.py`, `ton.py`, `substrate.py` + matching MCP servers |

All write operations downstream must follow simulate-first lifecycle and apply guardrails from `guardrails/transaction-safety.yaml`, `security.yaml`, and `compliance.yaml`.

## When to Use

- User asks "which chain should I use?" or provides an ambiguous address
- Normalizing addresses across chain families before RPC calls
- Resolving RPC endpoints and chain metadata from `registry/chains.json`
- Building operations that may span multiple chains (bridge, IBC, L2)
- Selecting MCP server before loading `transaction-lifecycle` or `block-state-queries`

Do **not** use when chain is already resolved and you only need to send a tx (use `transaction-lifecycle` directly).

## Core Process

### Step 1: Resolve chain

1. Accept `chainName` or `chainId` parameter.
2. Lookup in chain registry (`registry/chains.json`) or call `lib.chain_providers.resolve_chain(name)`.
3. Return normalized metadata: VM type, consensus, token standards, MCP server, confirmation depth.
4. If chain is Tier 3–4, emit LOW confidence and note roadmap status.

### Step 2: Validate address

Apply format rules from `guardrails/transaction-safety.yaml` → `destination_validation`:

| Family | Format | Example |
| --- | --- | --- |
| EVM | EIP-55 checksum | `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb` |
| Solana | base58, 32-byte pubkey | `7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU` |
| Cosmos | bech32 with chain prefix | `cosmos1...`, `osmo1...` |
| NEAR | `.near` named or implicit hex | `alice.near`, `abc123...` |
| Bitcoin | bech32 (SegWit) or legacy base58 | `bc1q...`, `1A1zP1...` |

Reject malformed addresses **before** any RPC call — block per guardrail.

### Step 3: Select MCP adapter

Route to chain-family MCP server:

```
EVM chains     → evm-rpc-server      (eth_call, eth_getBalance, eth_sendRawTransaction)
Solana         → solana-rpc-server   (getAccountInfo, simulateTransaction)
NEAR/Aurora    → near-rpc-server     (view_function, send_tx)
Cosmos/IBC     → cosmos-rpc-server   (abci_query, broadcast_tx)
Sui/Aptos      → move-rpc-server
Bitcoin        → bitcoin-rpc-server
TON            → ton-rpc-server
Substrate      → substrate-rpc-server
```

### Step 4: RPC fallback and health

1. Try primary RPC from chain config.
2. On failure (timeout >5s, HTTP 429, 5xx), rotate to fallback endpoints.
3. Apply rate limits per `compliance.yaml`: EVM 100 req/s, Solana 50, NEAR/Cosmos 30 — exponential backoff with jitter.
4. Log RPC health; downgrade confidence to MEDIUM if fallback used, LOW if all endpoints fail.

### Step 5: Map transaction model

| VM family | Model | Nonce/key concept |
| --- | --- | --- |
| EVM | Account-based | nonce, EIP-1559 gas |
| Solana | Account-based | blockhash, priority fee |
| NEAR | Account-based | access keys, yoctoNEAR deposit |
| Cosmos | Account-based | sequence, fee + gas limit |
| Bitcoin | UTXO | inputs/outputs, fee rate sat/vB |
| Move (Sui/Aptos) | Object-centric | object IDs, shared vs owned |

Pass mapped model to `transaction-lifecycle` for encoding.

## Phase 1 EVM chains

| Chain | chainId | Block time | Confirm depth | MCP tool |
| --- | --- | --- | --- | --- |
| Ethereum | 1 | ~12s | 12 | evm-rpc-server |
| Arbitrum One | 42161 | ~0.25s | 20 | evm-rpc-server |
| Base | 8453 | ~2s | 20 | evm-rpc-server |
| Polygon PoS | 137 | ~2s | 128 | evm-rpc-server |

## Phase 2 Alt-L1 chains

| Chain | chainId | MCP server | Token standards |
| --- | --- | --- | --- |
| Solana | mainnet-beta | solana-rpc-server | SPL, Token-2022, Metaplex |
| NEAR | mainnet | near-rpc-server | NEP-141, NEP-171 |
| Aurora | 1313161554 | near-rpc-server | ERC-20 (EVM on NEAR) |
| Cosmos Hub | cosmoshub-4 | cosmos-rpc-server | CW-20, ICS-20 |
| Osmosis | osmosis-1 | cosmos-rpc-server | CW-20, ICS-20 |
| Celestia | celestia | cosmos-rpc-server | ICS-20 |
| Injective | injective-1 | cosmos-rpc-server | CW-20, ICS-20 |

Implementation: `lib/chain_providers/` — use `resolve_chain(name)` and `validate_address(name, addr)`.

## Decision framework

1. **Address provided without chain?** → Detect format: `0x` + 40 hex → EVM; base58 32–44 chars → likely Solana; bech32 prefix → Cosmos family; `.near` suffix → NEAR.
2. **Multiple chains possible?** → Ask user or check registry for canonical deployment; never guess mainnet.
3. **Cross-chain operation?** → Sequence: resolve source chain → resolve dest chain → check bridge/IBC skill (`rollup-operations` or Cosmos IBC).
4. **Read vs write?** → Read: pass MCP + address to `block-state-queries`. Write: pass to `transaction-lifecycle` after validation.
5. **Tier 3–4 chain requested?** → State roadmap limitation; use MCP scaffold if available; assign LOW confidence.

| Scenario | Action | Downstream skill |
| --- | --- | --- |
| Ambiguous `0x` address on unknown chain | Resolve via registry or user confirm | chain-abstraction only |
| IBC transfer Osmosis → Cosmos Hub | Validate bech32 prefixes, channel OPEN | token-standards-engine + cosmos-rpc-server |
| L2 address same as L1 (EOA) | Resolve L2 chainId separately | rollup-operations |
| Archive historical query | Select archive RPC tier | block-state-queries |

## Anti-patterns and rationalizations

| Rationalization | Risk | Required response |
| --- | --- | --- |
| "Address looks valid — skip checksum" | Funds sent to wrong address, irrecoverable loss | Enforce EIP-55/bech32 validation per `transaction-safety.yaml` |
| "Use Ethereum RPC for all EVM chains" | Wrong chainId, replay risk, wrong state | Resolve exact chainId; never assume chainId 1 |
| "Fallback RPC is fine without logging" | Audit gap, stale state, hidden failures | Log fallback use; downgrade confidence to MEDIUM |
| "Tier 3 chain — implement adapter inline" | Undocumented behavior, no tests | State roadmap gap; use documented MCP only |
| "Same address works on all EVM L2s" | Wrong balance, wrong contract | Resolve per-chain; L2 contracts differ |
| "Skip rate limiting for one quick call" | RPC ban, cascading failures | Apply `compliance.yaml` rate limits |
| "Implicit NEAR account — no validation needed" | Invalid implicit format | Validate 64-char hex implicit accounts |

## Verification

- [ ] Chain resolved with correct chainId, VM type, and MCP server via `resolve_chain()`
- [ ] Address validated per chain format before any RPC call
- [ ] Tier 1–2 implementation confirmed; Tier 3–4 limitations documented if applicable
- [ ] Primary RPC reachable; fallback documented with confidence downgrade if used
- [ ] Confirmation depth recorded for downstream `/confirm-depth`
- [ ] Transaction model (account/UTXO/object) mapped for write operations
- [ ] Rate limiting applied per `compliance.yaml` limits
- [ ] Sanctions screening delegated to downstream write skills for counterparties
- [ ] Confidence score assigned: HIGH (primary RPC, Tier 1–2), MEDIUM (fallback), LOW (Tier 3–4)
- [ ] Cross-chain dependencies sequenced in plan artifact if multi-chain
