# NEAR RPC MCP Server

MCP server for NEAR Protocol mainnet/testnet and Aurora (EVM on NEAR). Phase 2 implementation.

## Tools

| Tool | NEAR RPC method | Description |
| --- | --- | --- |
| `query` | query | Generic state query (view function, account) |
| `send_tx` | send_tx | Broadcast signed transaction |
| `view_access_key` | EXPERIMENTAL_view_access_key | Access key nonce and allowance |
| `view_account` | view_account | Account balance and storage usage |
| `view_contract_state` | EXPERIMENTAL_view_contract_state | Contract storage keys |
| `gas_price` | gas_price | Current gas price |
| `broadcast_tx_async` | broadcast_tx_async | Async tx broadcast |
| `broadcast_tx_commit` | broadcast_tx_commit | Sync tx broadcast with receipt |

## NEAR-specific features

- **Named accounts** — human-readable (e.g., `alice.near`)
- **Access keys** — full-access vs function-call with method whitelist
- **Storage staking** — 0.0001 NEAR/byte
- **Chain signatures** — multi-chain signing from NEAR account
- **Cross-shard calls** — async promise-based contract calls

## Token standards

NEP-141 (fungible), NEP-171 (NFT), NEP-177 (metadata), NEP-145 (storage management).

## Setup

```bash
export PAGODA_NEAR_URL=https://rpc.mainnet.pagoda.co
export MCP_API_KEY=dev-local-key
python server.py
```
