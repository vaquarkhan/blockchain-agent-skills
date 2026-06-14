---
name: event-indexing
description: Subscribe to on-chain events, parse logs, and build real-time notification pipelines. Integrates with The Graph subgraphs, Goldsky, Envio, and Subsquid for historical and streaming event data. Trigger when monitoring contract events, building indexers, or querying subgraph data.
---

# Event Indexing

## Overview

Event pipeline layers:

1. **RPC subscription** — `eth_subscribe` logs, Solana program logs
2. **Indexer platforms** — The Graph, Goldsky, Envio, Subsquid
3. **Parse & normalize** — ABI decode, topic filtering, block reorg handling

## Core Process

### Step 1: Define event filter

```
contractAddress, eventSignature (topic0), indexed params (topic1-3)
fromBlock, toBlock (or "latest" with reorg buffer)
```

### Step 2: Query source selection

| Need | Source |
| --- | --- |
| Real-time stream | WebSocket eth_subscribe / Geyser (Solana) |
| Historical bulk | Subgraph / Goldsky / Subsquid |
| Single tx logs | eth_getTransactionReceipt |

### Step 3: Parse logs

1. Decode via contract ABI (topic0 → event selector).
2. Handle reorgs: track `blockHash`; on reorg, rewind and re-index affected blocks.
3. Emit normalized events with block number, tx hash, log index.

### Step 4: Notification pipeline

Optional: webhook, SNS, or DynamoDB stream for downstream consumers.

## Phase 2 — Alt-L1 event sources

### Solana

| Source | Method |
| --- | --- |
| Real-time | Geyser plugin / WebSocket `logsSubscribe` |
| Program logs | `getSignaturesForAddress` + tx meta log parsing |
| DAS events | Helius enhanced webhooks for NFT transfers |

Reorg handling: Solana uses commitment levels (`confirmed` → 32 slots for finality).

### NEAR

- Index via `EXPERIMENTAL_tx_status` and receipt logs
- Cross-shard: track promise callbacks in receipt tree
- Event format: JSON logs emitted via `env::log`

### Cosmos / IBC

- Tendermint WS: `subscribe` to `tm.event='Tx'`
- IBC packets: index `send_packet`, `recv_packet`, `acknowledge_packet`, `timeout_packet`
- CosmWasm: `wasm-contract-event` attributes in tx result

## Verification

- [ ] Event filter matches expected ABI
- [ ] Reorg buffer applied for streaming
- [ ] Decoded fields validated against schema
