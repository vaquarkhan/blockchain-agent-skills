---
name: transaction-lifecycle
description: Build, sign, simulate, broadcast, confirm, retry, and replace transactions across all supported chains. Manages nonces, gas/fees, mempool monitoring, and stuck-transaction recovery. Trigger when sending tokens, calling contracts, canceling pending txs, or recovering stuck transactions. Requires simulate-first and guardrail compliance.
---

# Transaction Lifecycle

## Overview

End-to-end transaction management:

1. **Build** — encode calldata, set EIP-1559 fields (or chain equivalent)
2. **Simulate** — `eth_call` / `simulateTransaction` before broadcast
3. **Sign** — AWS KMS/HSM only; never in agent context
4. **Broadcast** — `eth_sendRawTransaction` or chain equivalent
5. **Monitor** — receipt polling + event subscription
6. **Retry** — higher gas replacement or cancel (0-value self-send)

## When to Use

- Sending native token or calling a contract
- Replacing stuck pending transactions
- Canceling pending transactions via nonce replacement
- Estimating gas and building EIP-1559 transactions

## Core Process

### Step 1: Build transaction

**EVM (EIP-1559):**

```
maxFeePerGas = baseFee * 2 + maxPriorityFeePerGas
maxPriorityFeePerGas = mempool percentile estimate
nonce = per-chain nonce registry
chainId = from chain-abstraction
```

**Solana:** versioned transaction + priority fee + optional Jito tip  
**NEAR:** access key + gas + deposit  
**Cosmos:** fee + gas limit + memo

### Step 2: Simulate (mandatory)

1. Run simulation via MCP tool.
2. On revert: decode reason (custom error selector → ABI decode).
3. **Block broadcast** if simulation fails.

### Step 3: Guardrail checks

Apply before sign:

- Destination address validation
- Sanctions screening (`guardrails/compliance.yaml`)
- Value threshold ($10k → human confirm)
- Unverified contract block
- Honeypot detection for token interactions

### Step 4: Sign and broadcast

1. Sign via KMS — log audit entry with payload hash (not private key).
2. Broadcast via MCP.
3. Return tx hash immediately; do not treat as final.

### Step 5: Monitor and confirm

1. Poll for receipt.
2. Wait for chain-specific confirmation depth (see chain-abstraction).
3. Handle reorgs: if receipt disappears, alert and re-evaluate.

### Step 6: Retry / replace (stuck tx)

1. Detect pending tx exceeding timeout.
2. Require explicit user override for replacement.
3. Replace with same nonce, higher `maxFeePerGas` (+10-20%).
4. Cancel: send 0-value tx to self with same nonce.

## Nonce management

- Maintain per-chain, per-address nonce registry.
- Detect gaps; alert before broadcast.
- Never auto-increment on gap without user acknowledgment.

## Verification

- [ ] Simulation passed before broadcast
- [ ] All guardrails applied and logged
- [ ] KMS signing (no key material in logs)
- [ ] Receipt received and confirmation depth reached
- [ ] Audit trail entry in DynamoDB
