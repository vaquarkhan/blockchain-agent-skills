---
name: token-standards-engine
description: Deploy and manage tokens per chain-native standards — ERC-20/721/1155/4626/6551 (EVM), NEP-141/171 (NEAR), SPL/Token-2022 (Solana), CW-20/721 (Cosmos), Jettons (TON), Coin/Kiosk (Sui/Aptos). Automatic standard detection and unified interface. Trigger when minting, transferring, or deploying tokens.
---

# Token Standards Engine

## Overview

Unified fungible/NFT interface with chain-specific adapters:

| Chain | Fungible | NFT |
| --- | --- | --- |
| Ethereum | ERC-20 | ERC-721, ERC-1155 |
| NEAR | NEP-141 | NEP-171 |
| Solana | SPL, Token-2022 | Metaplex, cNFTs |
| Cosmos | CW-20, ICS-20 | CW-721 |
| TON | Jettons (TEP-74) | TON NFT (TEP-62) |
| Sui | Coin | Kiosk |
| Aptos | Fungible Asset v2 | Digital Asset |

## Core Process

### Step 1: Detect standard

From contract address or program ID, identify token standard and fetch metadata (name, symbol, decimals).

### Step 2: Security checks

Before interaction:

- Honeypot detection (simulate buy + sell)
- GoPlus token security API
- Top holder concentration >30% → warn
- Unlimited approval → warn (suggest bounded amount)

### Step 3: Execute operation

Mint, transfer, approve (EVM), or chain-native equivalent via `transaction-lifecycle`.

### Step 4: Verify receipt

Parse Transfer/Mint events from receipt logs; confirm balance change via `block-state-queries`.

## Verification

- [ ] Standard detected correctly
- [ ] Honeypot/security checks passed
- [ ] Transfer confirmed with event log match
