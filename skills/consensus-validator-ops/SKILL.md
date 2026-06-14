---
name: consensus-validator-ops
description: Staking, validator management, slashing protection, and MEV-Boost configuration. Covers PoS (ETH, NEAR, SOL), PoW (BTC), PoSA (BNB), Hashgraph (Hedera), and Avalanche Snow consensus. Trigger when staking, managing validators, configuring MEV, or monitoring slashing risk. Requires human confirmation for all validator operations.
---

# Consensus & Validator Ops

## Overview

Infrastructure-level consensus and validator operations — **not** DeFi staking UI flows. All validator writes require **mandatory human confirmation** (no threshold exception per operational risk profile).

| Chain | Consensus | Key operations | Tier |
| --- | --- | --- | --- |
| Ethereum | PoS / Casper | 32 ETH validator, MEV-Boost, PBS | 1 |
| Solana | PoH + Tower BFT | Vote accounts, commission | 2 |
| NEAR | PoS / Nightshade | Validator seat, staking pool | 2 |
| BNB | PoSA (21 validators) | Parlia validator set | 1 |
| Avalanche | Snow consensus | P-Chain validator, Subnet validation | 3 partial |
| Hedera | Hashgraph aBFT | Mirror reads via `hedera-rpc-server`; council ops human-only | 4 read-only |
| Bitcoin | PoW | UTXO + Lightning reads via `bitcoin-rpc-server` | 4 read-only |

Guardrails: `transaction-safety.yaml` (simulate, value thresholds), `security.yaml` (KMS for validator keys — never in LLM), `compliance.yaml` (audit trail). Slashing protection is **mandatory** for Ethereum PoS.

Cross-reference `network-monitoring` for validator performance, missed blocks, and slashing events.

## When to Use

- Staking or unstaking validator positions (ETH 32 ETH, NEAR seat, SOL vote account)
- Configuring MEV-Boost relays (Ethereum)
- Managing validator keys and withdrawal credentials (via KMS/HSM)
- Monitoring slashing risk and missed attestations
- Commission changes on Solana/NEAR validators

Do **not** use for liquid staking token swaps (DeFi — use `token-standards-engine`) or simple delegations under $10k without infra ops scope.

## Core Process

### Step 1: Operation classification

All validator operations require **human confirmation** before `/broadcast` — document in plan artifact:

- Operation type: stake, unstake, withdraw, key rotation, MEV config
- Value at risk (principal + slashing exposure)
- Chain and consensus mechanism
- Confidence score (typically MEDIUM for infra ops)

### Step 2: Staking workflow

1. Verify minimum stake requirements (ETH: 32 ETH; NEAR: seat auction; SOL: rent-exempt vote account).
2. **Simulate** staking transaction via chain MCP tool.
3. Configure **slashing protection** (double-sign prevention) — Ethereum: Doppelganger or equivalent; never disable.
4. Sign validator operations via KMS/HSM — withdrawal credentials and signing keys never in LLM.
5. Broadcast via `transaction-lifecycle`; monitor activation epoch.

### Step 3: MEV-Boost (Ethereum) — Tier 1

1. Configure relay endpoints (Flashbots, bloXroute, etc.) — verify relay reputation.
2. Verify builder block acceptance via `mev-boost` API.
3. Monitor missed slots and relay failures via `network-monitoring`.
4. Document relay selection in audit trail.

### Step 4: Unstaking and withdrawals

| Chain | Unbonding period | Human confirm |
| --- | --- | --- |
| Ethereum | Variable exit queue | Always |
| NEAR | ~52-65 hours | Always |
| Solana | Cooldown epoch | Always |

Track exit queue on Ethereum — do not mark funds available until withdrawal processed.

### Step 5: Monitoring

1. Cross-reference `network-monitoring` for missed blocks, attestation delays.
2. Alert on slashing events or double-sign detection.
3. Track validator effectiveness rate (ETH: >95% target).

## Decision framework

1. **Stake vs delegate vs liquid staking?** → Infra stake: this skill. LST swap: token-standards-engine.
2. **Ethereum validator new or existing?** → New: deposit contract 32 ETH. Existing: monitor + MEV config.
3. **Key rotation needed?** → Requires human confirm + slashing protection pause procedure.
4. **MEV-Boost enable?** → Verify relay trust; document endpoints; monitor missed slots.
5. **Slashing event detected?** → Stop operations; alert; do not auto-resubmit conflicting attestations.
6. **Tier 3–4 chain?** → State roadmap; block undocumented validator paths.

| Operation | Chain | Simulation tool | Confirm |
| --- | --- | --- | --- |
| 32 ETH deposit | Ethereum | eth_call deposit contract | Required |
| Vote account create | Solana | simulateTransaction | Required |
| Validator seat bid | NEAR | near dry-run | Required |
| MEV relay switch | Ethereum | Config only + monitor | Required |

## Anti-patterns and rationalizations

| Rationalization | Risk | Required response |
| --- | --- | --- |
| "Skip human confirm — routine stake" | Slashing, irreversible infra ops | Always require `/confirm` |
| "Disable slashing protection for maintenance" | Double-sign slash (ETH: 16 ETH+) | Never disable; use proper pause procedures |
| "Validator key in env for automation" | Key theft, slashing | KMS/HSM only per `security.yaml` |
| "Missed slots — increase aggressive MEV" | Relay trust issues, missed blocks | Diagnose via network-monitoring first |
| "Run two validators same keys for redundancy" | Guaranteed double-sign slash | One keypair per validator only |
| "Broadcast unstake without exit queue check" | Unexpected lock period | Query exit queue; disclose timeline |
| "Tier 4 Hedera council op — improvise" | Undefined infra path | State roadmap; block undocumented ops |

## Verification

- [ ] Operation classified and documented in plan artifact
- [ ] Human confirmation obtained before any validator write
- [ ] Minimum stake requirements verified for target chain
- [ ] Staking transaction simulated via chain MCP tool
- [ ] Slashing protection configured and active (Ethereum PoS)
- [ ] KMS/HSM signing used — no validator keys in LLM context
- [ ] Activation epoch or seat assignment monitored post-broadcast
- [ ] MEV-Boost relay endpoints documented (if applicable)
- [ ] Exit queue / unbonding period communicated for unstake ops
- [ ] network-monitoring alerts configured for missed blocks
- [ ] Audit trail logged per `compliance.yaml` (7-year retention)
- [ ] Confidence score included (typically MEDIUM for infra operations)
