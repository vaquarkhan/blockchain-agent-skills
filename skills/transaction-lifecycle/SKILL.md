---
name: transaction-lifecycle
description: Build, sign, simulate, broadcast, confirm, retry, and replace transactions across all supported chains. Manages nonces, gas/fees, mempool monitoring, and stuck-transaction recovery. Trigger when sending tokens, calling contracts, canceling pending txs, or recovering stuck transactions. Requires simulate-first and guardrail compliance.
---

# Transaction Lifecycle

## Overview

End-to-end transaction management across all supported chains, enforcing the full lifecycle:

1. **Build** — encode calldata, set EIP-1559 fields (or chain equivalent)
2. **Simulate** — `eth_call` / `simulateTransaction` / NEAR dry-run / Cosmos `simulate` before broadcast
3. **Sign** — AWS KMS/HSM only; never in agent context (`security.yaml` → `private_key_protection`)
4. **Broadcast** — `eth_sendRawTransaction`, `send_tx`, `broadcast_tx` via MCP
5. **Monitor** — receipt polling + event subscription
6. **Retry** — higher gas replacement or cancel (0-value self-send)

**Tier 1** (EVM): full implementation via `evm-rpc-server`. **Tier 2** (Solana, NEAR, Cosmos): chain-specific encoding in `lib/chain_providers/`. **Tier 3–4**: roadmap — document gaps honestly.

Guardrails applied on every write: `guardrails/transaction-safety.yaml`, `guardrails/security.yaml`, `guardrails/compliance.yaml`.

## When to Use

- Sending native token or calling a contract
- Replacing stuck pending transactions (same nonce, higher fee)
- Canceling pending transactions via nonce replacement
- Estimating gas and building EIP-1559 or chain-native fee transactions
- Any mainnet write after `/plan` from `using-blockchain-agent-skills`

Do **not** use for read-only queries (use `block-state-queries`) or contract deployment orchestration (use `smart-contract-factory` as primary).

## Core Process

### Step 1: Build transaction

Resolve chain via `chain-abstraction` first.

**EVM (EIP-1559):**

```
maxFeePerGas = baseFee * 2 + maxPriorityFeePerGas
maxPriorityFeePerGas = eth_feeHistory percentile (50th–75th)
nonce = per-chain nonce registry (alert on gap per transaction-safety.yaml)
chainId = from resolve_chain()
gasLimit = eth_estimateGas * safety factor (max 10x per transaction-safety.yaml)
```

**Solana:** versioned transaction + priority fee (`getRecentPrioritizationFees`) + optional Jito tip  
**NEAR:** access key + gas (`300 TGas` default) + yoctoNEAR deposit for storage  
**Cosmos:** fee + gas limit + memo; simulate via `cosmos-rpc-server`

### Step 2: Simulate (mandatory)

Per `transaction-safety.yaml` → `simulate_before_broadcast` — **BLOCK** on skip:

| Chain | MCP tool | Method |
| --- | --- | --- |
| EVM | evm-rpc-server | `eth_call`, `eth_estimateGas` |
| Solana | solana-rpc-server | `simulateTransaction` |
| NEAR | near-rpc-server | dry-run via view |
| Cosmos | cosmos-rpc-server | `simulate` |

On revert: decode reason (custom error selector → ABI decode). **Block broadcast** if simulation fails.

### Step 3: Guardrail checks

Apply before sign:

| Check | Source | Action |
| --- | --- | --- |
| Destination validation | transaction-safety.yaml | BLOCK on malformed |
| Sanctions screening | compliance.yaml | BLOCK sanctioned addresses |
| Value threshold | transaction-safety.yaml | REQUIRE_HUMAN_CONFIRM >$10k |
| Unverified contract | transaction-safety.yaml | BLOCK on mainnet |
| Honeypot detection | security.yaml | BLOCK if sell fails |
| Blind signing | security.yaml | BLOCK opaque payloads |
| Unlimited approval | transaction-safety.yaml | WARN; suggest bounded amount |
| Gas limit | transaction-safety.yaml | BLOCK if >10x estimate |

### Step 4: Confirm (`/confirm`)

Require human confirmation when value >$10k, LOW confidence, unaudited contract <7 days, or validator-adjacent ops.

### Step 5: Sign and broadcast (`/broadcast`)

1. Sign via KMS — log audit entry with payload hash only (not private key).
2. Broadcast via MCP: `eth_sendRawTransaction`, `send_tx`, `broadcast_tx`.
3. Return tx hash immediately; **do not** treat as final.
4. Write audit trail per `compliance.yaml` → DynamoDB, 7-year retention.

### Step 6: Monitor and confirm depth (`/confirm-depth`)

1. Poll for receipt via `eth_getTransactionReceipt` or chain equivalent.
2. Wait for chain-specific confirmation depth (Ethereum 12, BNB 15, Solana 32 slots).
3. Handle reorgs: if receipt disappears, alert and re-evaluate; never mark complete early.

### Step 7: Retry / replace (stuck tx)

1. Detect pending tx exceeding timeout (EVM: >5 blocks without inclusion).
2. Require **explicit user override** per `transaction-safety.yaml` → `nonce_management`.
3. Replace with same nonce, higher `maxFeePerGas` (+10–20%).
4. Cancel: send 0-value tx to self with same nonce.

## Nonce management

- Maintain per-chain, per-address nonce registry.
- Detect gaps; **alert** before broadcast — never auto-increment on gap.
- Replace pending txs only with explicit override.

## Decision framework

1. **Is this a read?** → Redirect to `block-state-queries`; no signing.
2. **Chain unresolved?** → Load `chain-abstraction` first.
3. **Token transfer/mint?** → Primary `token-standards-engine`; this skill handles tx encoding.
4. **Contract deploy/upgrade?** → Primary `smart-contract-factory`; this skill handles broadcast.
5. **Stuck pending tx?** → Check nonce registry → require override → replace (+10–20% fee) or cancel (0-value self-send).
6. **Simulation reverts?** → Decode reason → block broadcast → report to user.
7. **Value >$10k?** → `/confirm` before `/broadcast`.
8. **L2 operation?** → Coordinate with `rollup-operations` for bridge-specific contracts.

| Chain family | Fee model | Stuck tx recovery |
| --- | --- | --- |
| EVM | EIP-1559 | Same-nonce replacement |
| Solana | Priority fee + blockhash | Rebuild with fresh blockhash |
| NEAR | Gas + deposit | Resubmit with higher gas |
| Cosmos | Fixed fee denom | Resubmit with higher fee |

## Anti-patterns and rationalizations

| Rationalization | Risk | Required response |
| --- | --- | --- |
| "Simulation passed on fork — broadcast now" | Stale state, wrong nonce | Verify latest block; re-simulate if >12 blocks stale |
| "User provided private key for speed" | Key exposure, audit violation | Refuse; KMS/HSM only |
| "Gas limit 50x estimate for safety" | Blocked by guardrail (>10x) | Cap at 10x estimate; investigate contract complexity |
| "Skip sanctions check — known good address" | Compliance violation, no override | Screen every counterparty per `compliance.yaml` |
| "Receipt received — done" | Reorg loss | Wait for `/confirm-depth` |
| "Auto-replace stuck tx without asking" | Unintended cancellation, double spend intent | Require explicit override per nonce_management |
| "Sign opaque calldata user pasted" | Blind signing, drain attack | Decode and display all params; reject opaque payloads |

## Verification

- [ ] Chain resolved via `chain-abstraction` with correct chainId
- [ ] Simulation passed via chain-specific MCP tool before broadcast
- [ ] All guardrails applied: transaction-safety, security, compliance
- [ ] Destination address validated (EIP-55, bech32, base58 as applicable)
- [ ] Sanctions screening passed for all counterparties
- [ ] Gas limit within 10x estimate; EIP-1559 fields set from fresh fee history
- [ ] Nonce verified against registry; gaps alerted
- [ ] Human confirmation obtained for >$10k or LOW confidence
- [ ] KMS signing used — no key material in logs or LLM context
- [ ] Tx hash returned; receipt polled
- [ ] Confirmation depth reached per chain before marking complete
- [ ] Audit trail entry in DynamoDB with payload hash, simulation result, confidence score
