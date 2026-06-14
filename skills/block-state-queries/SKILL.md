---
name: block-state-queries
description: Read chain state, trace calls, parse receipts, and retrieve historical block data. Wraps chain-specific RPC methods into a unified query API across EVM, SVM, NEAR, Cosmos, and Move VMs. Trigger when reading balances, storage slots, transaction receipts, or tracing contract execution.
---

# Block & State Queries

## Overview

Unified **read-only** API over chain-family MCP tools. No signing, no broadcast — reads do not require `/simulate` for writes but still need guardrails for sanctioned address lookups and audit logging for sensitive queries.

| Operation | EVM (evm-rpc-server) | Solana | NEAR | Cosmos |
| --- | --- | --- | --- | --- |
| Latest block | `eth_getBlockByNumber` | `getBlock` | `block` | `block` |
| Account balance | `eth_getBalance` | `getBalance` | `view_account` | bank balance |
| Contract call | `eth_call` | `simulateTransaction` | `view_function` | `abci_query` |
| Storage slot | `eth_getStorageAt` | `getAccountInfo` | `view_state` | smart query |
| Tx receipt | `eth_getTransactionReceipt` | `getTransaction` | `tx_status` | tx query |
| Trace | `debug_traceCall` | — | — | — |
| Storage proof | `eth_getProof` | bank hash proof | — | ICS-23 via IBC |

**Tier 1** EVM: full MCP tool coverage. **Tier 2** Solana/NEAR/Cosmos: implemented in respective MCP servers. **Tier 3–4**: partial — note gaps in response confidence.

Archive nodes required for historical state queries beyond ~128 blocks (EVM) or chain-specific pruning windows.

## When to Use

- Reading balances, nonces, or contract state at a block tag
- Fetching transaction receipts and parsing event logs
- Tracing contract execution (`debug_traceCall` on EVM)
- Reading storage slots; optionally generating Merkle proofs via `storage-state-proofs`
- Verifying post-tx state after `transaction-lifecycle` broadcast

Do **not** use for writes, event streaming pipelines (use `event-indexing`), or proof generation alone (use `storage-state-proofs` as primary).

## Core Process

### Step 1: Resolve chain and MCP

1. Use `chain-abstraction` → `resolve_chain()` for chainId and MCP server.
2. Select RPC tier: **full node** for `latest`; **archive node** for historical `blockTag`.
3. Apply read rate limits per `compliance.yaml`: EVM 100 req/s, Solana 50, NEAR/Cosmos 30.

### Step 2: Execute query

**EVM examples (evm-rpc-server):**

```
eth_getBlockByNumber("latest", false)
eth_getBalance(address, blockTag)
eth_call({to, data}, blockTag)
eth_getStorageAt(address, slot, blockTag)
eth_getTransactionReceipt(txHash)
eth_getLogs({address, topics, fromBlock, toBlock})
debug_traceCall({to, data}, blockTag, {tracer: "callTracer"})
eth_getProof(address, [storageKeys], blockNumber)
```

**Solana (solana-rpc-server):**

```
getAccountInfo(pubkey)
getTokenAccountsByOwner(owner, {mint})
simulateTransaction(tx)          # read-only simulation
getSignaturesForAddress(address)
getBlock(slot)
```

**NEAR (near-rpc-server):**

```
view_account(accountId)
view_function(contractId, methodName, argsBase64)
EXPERIMENTAL_tx_status(txHash)
```

**Cosmos (cosmos-rpc-server):**

```
abci_query(path, data, height)
block(height)
tx_search(query)
```

### Step 3: Parse and normalize

Return structured response with:

- Raw RPC result
- Decoded fields where ABI/IDL available
- Block number, hash, and timestamp
- **Confidence score**: HIGH (synced node, `latest`, primary RPC), MEDIUM (fallback RPC or `safe` block tag), LOW (archive unavailable, Tier 3 chain, partial trace)

### Step 4: Storage proofs (optional)

For cross-chain verification, delegate to `storage-state-proofs` skill → `eth_getProof` on EVM.

### Step 5: Post-write verification

After `transaction-lifecycle` broadcast, re-query balance/state at confirmed block to verify expected delta.

## Decision framework

1. **Need current state?** → `blockTag: "latest"` or `"safe"` on EVM; `confirmed` commitment on Solana.
2. **Need historical state at block N?** → Archive node required; if unavailable, BLOCK query and report.
3. **Need event history?** → Bulk: `event-indexing` + subgraph. Single tx: `eth_getTransactionReceipt`.
4. **Need execution trace?** → EVM only: `debug_traceCall`. Solana: limited via `simulateTransaction` logs.
5. **Need cryptographic proof?** → `storage-state-proofs` as primary skill.
6. **Query involves sanctioned address?** → Screen per `compliance.yaml`; block if sanctioned.

| Query type | Tool | Archive required? |
| --- | --- | --- |
| Current ETH balance | `eth_getBalance` | No |
| Balance at block 18M | `eth_getBalance` + blockTag | Yes |
| Contract view call | `eth_call` | Only if historical blockTag |
| All Transfer events 30 days | `event-indexing` / subgraph | N/A |
| Storage slot proof | `eth_getProof` | Yes at historical height |

## Anti-patterns and rationalizations

| Rationalization | Risk | Required response |
| --- | --- | --- |
| "Use full node for historical block 17M" | Wrong or null state returned | Require archive node; block query if unavailable |
| "eth_call without blockTag is fine" | Inconsistent reads during reorg | Specify blockTag; use `safe` for high-stakes reads |
| "Trace unavailable — guess from logs" | Incomplete execution analysis | Report trace unavailable; use `debug_traceCall` on archive |
| "Skip confidence score on reads" | Downstream decisions on stale data | Always assign HIGH/MEDIUM/LOW |
| "Query sanctioned address for research" | Compliance violation | Block per `compliance.yaml`; no override |
| "Poll every 100ms for receipt" | Rate limit ban | Respect `compliance.yaml` limits; exponential backoff |
| "Return raw hex without decode" | User misinterpretation | Decode with ABI/IDL when available |

## Verification

- [ ] Chain resolved via `chain-abstraction` with correct MCP server
- [ ] RPC tier selected: full vs archive based on blockTag
- [ ] Correct MCP tool invoked (no invented RPC methods)
- [ ] Response includes block context: number, hash, timestamp
- [ ] Archive node confirmed for historical queries beyond pruning window
- [ ] ABI/IDL decode attempted for contract calls and logs
- [ ] Rate limits respected per `compliance.yaml`
- [ ] Confidence score assigned based on RPC freshness and sync status
- [ ] Sanctions screening applied if query targets counterparty addresses
- [ ] Post-write verification re-query matches expected state delta (if applicable)
- [ ] Errors surfaced structurally (revert data decoded on EVM)
- [ ] Audit log entry for sensitive queries (high-value address lookups)
