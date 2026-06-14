---
name: event-indexing
description: Subscribe to on-chain events, parse logs, and build real-time notification pipelines. Integrates with The Graph subgraphs, Goldsky, Envio, and Subsquid for historical and streaming event data. Trigger when monitoring contract events, building indexers, or querying subgraph data.
---

# Event Indexing

## Overview

Event pipeline layers for historical and real-time on-chain data:

1. **RPC subscription** — `eth_subscribe` logs, Solana Geyser/`logsSubscribe`
2. **Indexer platforms** — The Graph, Goldsky, Envio, Subsquid
3. **Parse & normalize** — ABI decode, topic filtering, block reorg handling

Read-heavy skill — no signing required. Apply `compliance.yaml` rate limits on RPC polling. For write-triggered monitoring (e.g., alert on Transfer then act), chain to `transaction-lifecycle` separately.

**Tier 1** EVM: `eth_getLogs`, `eth_subscribe`, The Graph. **Tier 2** Solana/NEAR/Cosmos: Geyser, receipt logs, Tendermint WS. **Tier 3–4**: partial indexer coverage — document gaps.

## When to Use

- Monitoring contract events (Transfer, Swap, Deposit, etc.)
- Building or querying indexers and subgraphs
- Real-time notification pipelines (webhooks, SNS, DynamoDB streams)
- Historical event backfill across block ranges
- IBC packet tracking (Cosmos)

Do **not** use for single balance reads (use `block-state-queries`) or storage proofs (use `storage-state-proofs`).

## Core Process

### Step 1: Define event filter

```
contractAddress, eventSignature (topic0), indexed params (topic1-3)
fromBlock, toBlock (or "latest" with reorg buffer)
chainId, MCP server
```

Topic0 = `keccak256("EventName(type1,type2,...)")` for EVM.

### Step 2: Query source selection

| Need | Source | MCP / platform |
| --- | --- | --- |
| Real-time stream | WebSocket `eth_subscribe` | evm-rpc-server |
| Real-time Solana | Geyser plugin / `logsSubscribe` | solana-rpc-server |
| Historical bulk (>10k blocks) | Subgraph / Goldsky / Subsquid | Indexer API |
| Single tx logs | `eth_getTransactionReceipt` | evm-rpc-server |
| Filtered range (RPC) | `eth_getLogs` | evm-rpc-server |

Use subgraph for bulk historical; RPC for recent blocks with reorg buffer (12+ blocks on Ethereum).

### Step 3: Parse logs

1. Decode via contract ABI (topic0 → event selector → indexed/non-indexed args).
2. Handle **reorgs**: track `blockHash`; on reorg, rewind and re-index affected blocks.
3. Apply reorg buffer: do not finalize events until `confirm-depth` reached (`transaction-safety.yaml` → reorg_protection).
4. Emit normalized events: `{ blockNumber, blockHash, txHash, logIndex, eventName, decodedArgs, timestamp }`.

### Step 4: Notification pipeline

Optional downstream: webhook, SNS, or DynamoDB stream. Log indexer cursor position for restart recovery.

### Step 5: Rate limiting and backoff

Per `compliance.yaml`: EVM 100 req/s for `eth_getLogs` pagination. Use exponential backoff with jitter on 429/5xx.

## Phase 2 — Alt-L1 event sources

### Solana — Tier 2

| Source | Method |
| --- | --- |
| Real-time | Geyser plugin / WebSocket `logsSubscribe` |
| Program logs | `getSignaturesForAddress` + tx meta log parsing |
| DAS events | Helius enhanced webhooks for NFT transfers |

Reorg handling: commitment levels — `confirmed` for indexing, 32 slots for finality.

### NEAR — Tier 2

- Index via `EXPERIMENTAL_tx_status` and receipt logs
- Cross-shard: track promise callbacks in receipt tree
- Event format: JSON logs emitted via `env::log`

### Cosmos / IBC — Tier 2

- Tendermint WS: `subscribe` to `tm.event='Tx'`
- IBC packets: index `send_packet`, `recv_packet`, `acknowledge_packet`, `timeout_packet`
- CosmWasm: `wasm-contract-event` attributes in tx result

## Decision framework

1. **Real-time vs historical?** → Real-time: WebSocket subscribe. Historical: subgraph if range >10k blocks.
2. **Single contract vs factory pattern?** → Factory: index `PairCreated` then track derived addresses.
3. **Reorg-sensitive action downstream?** → Wait 12 blocks (ETH) before triggering writes.
4. **Solana program vs account?** → Program logs via `getSignaturesForAddress(programId)`.
5. **Cross-chain events?** → IBC: Cosmos WS; L2: index L1 bridge events + L2 mint events separately.

| Scenario | Source | Reorg buffer |
| --- | --- | --- |
| Monitor Uniswap Swap | Subgraph or eth_subscribe | 12 blocks |
| Backfill 1M blocks | Goldsky/Subsquid | N/A (indexed) |
| Single tx receipt logs | eth_getTransactionReceipt | Confirm tx finalized |
| Solana NFT mint | Geyser / Helius DAS | 32 slots |

## Anti-patterns and rationalizations

| Rationalization | Risk | Required response |
| --- | --- | --- |
| "eth_getLogs from genesis in one call" | RPC timeout, rate ban | Paginate 2k–10k blocks per request |
| "Process events at head without reorg buffer" | Double credit, wrong state | Buffer 12 blocks ETH, 32 slots Solana |
| "Topic filter wrong — decode anyway" | Garbage data, missed events | Validate topic0 against ABI before pipeline |
| "Subgraph stale — trust anyway" | Missing recent events | Cross-check head with RPC; note sync lag |
| "Trigger trade on first event seen" | Reorg reverses event | Wait confirm-depth before downstream writes |
| "No cursor persistence" | Duplicate/missed events on restart | Persist block cursor in DynamoDB |
| "Index all chains with one schema" | Normalization errors | Chain-specific decode adapters |

## Verification

- [ ] Event filter matches expected ABI (topic0 verified against keccak256 signature)
- [ ] Query source selected appropriately (RPC vs subgraph vs WS)
- [ ] Reorg buffer applied for streaming (12 ETH blocks, 32 Solana slots)
- [ ] Decoded fields validated against schema/ABI types
- [ ] blockHash tracked for reorg detection and rewind logic
- [ ] Rate limits respected per `compliance.yaml`
- [ ] Indexer cursor persisted for restart recovery
- [ ] Confidence score reflects source freshness (subgraph sync lag noted)
- [ ] Normalized event schema includes blockNumber, txHash, logIndex
- [ ] Downstream write actions deferred until confirm-depth (if applicable)
- [ ] Chain and contract address validated via `chain-abstraction`
- [ ] Audit log for pipelines processing high-value or compliance-sensitive events
