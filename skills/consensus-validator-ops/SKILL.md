---
name: consensus-validator-ops
description: Staking, validator management, slashing protection, and MEV-Boost configuration. Covers PoS (ETH, NEAR, SOL), PoW (BTC), PoSA (BNB), Hashgraph (Hedera), and Avalanche Snow consensus. Trigger when staking, managing validators, configuring MEV, or monitoring slashing risk. Requires human confirmation for all validator operations.
---

# Consensus & Validator Ops

## Overview

Infrastructure-level consensus operations — **not** DeFi staking UI flows.

| Chain | Consensus | Key operations |
| --- | --- | --- |
| Ethereum | PoS / Casper | 32 ETH validator, MEV-Boost, PBS |
| Solana | PoH + Tower BFT | Vote accounts, commission |
| NEAR | PoS / Nightshade | Validator seat, staking pool |
| BNB | PoSA (21 validators) | Parlia validator set |
| Avalanche | Snow consensus | P-Chain validator, Subnet validation |
| Hedera | Hashgraph aBFT | Governing council nodes |

## Core Process

### Step 1: Operation classification

All validator operations require **human confirmation** (guardrail).

### Step 2: Staking workflow

1. Verify minimum stake requirements.
2. Simulate staking transaction.
3. Configure slashing protection (double-sign prevention).
4. Broadcast and monitor activation epoch.

### Step 3: MEV-Boost (Ethereum)

1. Configure relay endpoints.
2. Verify builder block acceptance.
3. Monitor missed slots and relay failures.

### Step 4: Monitoring

Cross-reference `network-monitoring` for validator performance, missed blocks, and slashing events.

## Verification

- [ ] Human confirmation obtained
- [ ] Slashing protection configured
- [ ] Staking tx simulated and confirmed
- [ ] Validator status monitored post-activation
