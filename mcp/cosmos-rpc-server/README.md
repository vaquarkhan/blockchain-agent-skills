# Cosmos / IBC RPC MCP Server

MCP server for Cosmos SDK chains with IBC support. Phase 2 implementation.

## Tools

| Tool | Description |
| --- | --- |
| `broadcast_tx` | Broadcast signed Cosmos transaction |
| `abci_query` | Query application state (CosmWasm contracts) |
| `ibc_transfer` | ICS-20 fungible token transfer with memo |
| `query_client_state` | IBC client state query |
| `query_channel` | IBC channel state |
| `get_ibc_denom_trace` | Trace IBC denom origin |
| `query_interchain_account` | ICA controller/host account query |
| `icq_query` | Interchain Queries for remote state reads |

## IBC workflow

1. Verify client, connection, and channel are OPEN
2. Build ICS-20 transfer msg with timeout height/timestamp
3. Simulate via `simulate` endpoint
4. Broadcast and monitor packet ack/timeout via relayer events

## Token standards

CW-20 (CosmWasm fungible), CW-721 (NFT), ICS-20 (IBC transfer), ICS-721 (IBC NFT).

## Supported chains

Cosmos Hub, Osmosis, Celestia, Injective (+ extensible via config.yaml).

## Setup

```bash
export COSMOS_HUB_RPC=https://rpc.cosmos.network
export MCP_API_KEY=dev-local-key
python server.py
```
