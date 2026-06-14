---
name: block-state-queries
description: Read chain state, trace calls, parse receipts, and retrieve historical block data. Wraps chain-specific RPC methods into a unified query API across EVM, SVM, NEAR, Cosmos, and Move VMs. Trigger when reading balances, storage slots, transaction receipts, or tracing contract execution.
---

# Block & State Queries

## Overview

Unified read API over chain-family MCP tools:

| Operation | EVM | Solana | NEAR | Cosmos |
| --- | --- | --- | --- | --- |
| Latest block | eth_getBlockByNumber | getBlock | block | block |
| Account balance | eth_getBalance | getBalance | view_account | bank balance |
| Contract call | eth_call | simulateTransaction | view_function | abci_query |
| Storage slot | eth_getStorageAt | getAccountInfo | view_state | query |
| Tx receipt | eth_getTransactionReceipt | getTransaction | tx_status | tx query |
| Trace | debug_traceCall | — | — | — |

Archive nodes required for historical state queries.

## When to Use

- Reading balances, nonces, or contract state
- Fetching transaction receipts and parsing logs
- Tracing contract execution (EVM debug_traceCall)
- Reading storage slots with Merkle proofs

## Core Process

### Step 1: Resolve chain and MCP

Use `chain-abstraction` to select MCP server and RPC tier (full vs archive).

### Step 2: Execute query

**EVM examples:**

```
eth_getBlockByNumber("latest", false)
eth_getBalance(address, blockTag)
eth_call({to, data}, blockTag)
eth_getStorageAt(address, slot, blockTag)
eth_getTransactionReceipt(txHash)
debug_traceCall({to, data}, blockTag, {tracer: "callTracer"})
```

**Solana:**

```
getAccountInfo(pubkey)
getTokenAccountsByOwner(owner, {mint})
simulateTransaction(tx)
getSignaturesForAddress(address)
```

### Step 3: Parse and normalize

Return structured response with:

- Raw RPC result
- Decoded fields where ABI/IDL available
- Block number and timestamp
- **Confidence score** based on RPC freshness and node sync status

### Step 4: Storage proofs (optional)

For cross-chain verification, generate Merkle/Patricia proofs via `storage-state-proofs` skill.

## Verification

- [ ] Correct MCP server and RPC tier selected
- [ ] Response includes block context (number, hash, timestamp)
- [ ] Archive node used for historical queries
- [ ] Confidence score assigned
