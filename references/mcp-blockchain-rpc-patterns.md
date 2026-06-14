# MCP Blockchain RPC Patterns

Nine chain-family MCP stdio servers under `mcp/`. Install via flat templates `mcp/*.mcp.json` in Cursor, Claude, or Bedrock MCP clients.

## Server catalog

| Server | Tools | Chains | Config template |
| --- | ---: | --- | --- |
| `evm-rpc-server` | 11 | ETH, Arbitrum, Base, Polygon | `mcp/evm-rpc.mcp.json` |
| `solana-rpc-server` | 4 | Solana mainnet/devnet | `mcp/solana-rpc.mcp.json` |
| `near-rpc-server` | 4 | NEAR, Aurora | `mcp/near-rpc.mcp.json` |
| `cosmos-rpc-server` | 4 | Cosmos Hub, Osmosis, Celestia, Injective | `mcp/cosmos-rpc.mcp.json` |
| `move-rpc-server` | 2 | Sui, Aptos | `mcp/move-rpc.mcp.json` |
| `bitcoin-rpc-server` | 4 | Bitcoin, Lightning (LND) | `mcp/bitcoin-rpc.mcp.json` |
| `ton-rpc-server` | 1 | TON | `mcp/ton-rpc.mcp.json` |
| `substrate-rpc-server` | 2 | Polkadot, Kusama, Moonbeam | `mcp/substrate-rpc.mcp.json` |
| `hedera-rpc-server` | 2 | Hedera | `mcp/hedera-rpc.mcp.json` |

Validate locally:

```bash
python scripts/validate-mcp-servers.py
python tests/test_mcp_servers.py
```

## Environment variables

| Server | Required env | Optional |
| --- | --- | --- |
| evm-rpc | `ALCHEMY_ETH_URL`, `ALCHEMY_ARB_URL`, `ALCHEMY_BASE_URL`, `ALCHEMY_POLYGON_URL` | `NETWORK`, `CHAIN_ENV` |
| solana-rpc | `SOLANA_RPC_URL` | `SOLANA_CLUSTER` (default `mainnet-beta`) |
| near-rpc | `NEAR_RPC_URL` | `NEAR_NETWORK` (default `mainnet`) |
| cosmos-rpc | `COSMOS_RPC_URL` | `COSMOS_CHAIN_ID` (default `cosmoshub-4`) |
| move-rpc | `SUI_RPC_URL`, `APTOS_RPC_URL` | — |
| bitcoin-rpc | `BITCOIN_RPC_URL` | `LND_REST_URL`, `LND_MACAROON` |
| ton-rpc | `TON_API_URL` | — |
| substrate-rpc | `SUBSTRATE_RPC_URL` | — |
| hedera-rpc | `HEDERA_MIRROR_URL` | — |

Write gates (all broadcast tools):

```bash
export SIMULATE_PASSED=true          # or SIMULATION_RUN_ID=...
export HUMAN_CONFIRMED=true            # mainnet / production
export BLOCKCHAIN_ALLOW_WRITE=true     # test harness only
```

## Read vs write tools

### evm-rpc-server

| Tool | Type | Underlying RPC |
| --- | --- | --- |
| `eth_block_number` | read | `eth_blockNumber` |
| `eth_get_block_by_number` | read | `eth_getBlockByNumber` |
| `eth_get_balance` | read | `eth_getBalance` |
| `eth_call` | read (simulate) | `eth_call` |
| `eth_estimate_gas` | read | `eth_estimateGas` |
| `eth_get_logs` | read | `eth_getLogs` |
| `eth_get_storage_at` | read | `eth_getStorageAt` |
| `eth_get_transaction_receipt` | read | `eth_getTransactionReceipt` |
| `debug_trace_call` | read | `debug_traceCall` |
| `eth_get_proof` | read | `eth_getProof` |
| `eth_send_raw_transaction` | **write** | `eth_sendRawTransaction` |

### solana-rpc-server

| Tool | Type |
| --- | --- |
| `get_account_info` | read |
| `simulate_transaction` | read (simulate) |
| `get_token_accounts_by_owner` | read |
| `send_transaction` | **write** |

### near-rpc-server

| Tool | Type |
| --- | --- |
| `view_account` | read |
| `query` | read |
| `view_access_key` | read |
| `send_tx` | **write** |

### cosmos-rpc-server

| Tool | Type |
| --- | --- |
| `abci_query` | read |
| `query_client_state` | read (IBC) |
| `ibc_transfer` | **write** (guarded) |
| `broadcast_tx` | **write** |

### move-rpc-server

| Tool | Type |
| --- | --- |
| `sui_get_object` | read |
| `aptos_view` | read |

### bitcoin-rpc-server

| Tool | Type |
| --- | --- |
| `getblockchaininfo` | read |
| `getrawtransaction` | read |
| `lightning_getinfo` | read |
| `lightning_decodepay` | read |

### substrate-rpc-server

| Tool | Type |
| --- | --- |
| `chain_get_block` | read |
| `system_health` | read |

### hedera-rpc-server

| Tool | Type |
| --- | --- |
| `get_account` | read |
| `get_block` | read |

### ton-rpc-server

| Tool | Type |
| --- | --- |
| `get_address_information` | read |

## Routing from chain name

Use `registry/chains.json` → `mcp` field, or `lib.chain_providers.resolve_chain()`. Example: `ethereum` → `evm-rpc-server`, `solana` → `solana-rpc-server`.

## Operational patterns

1. **Plan/simulate phase** — read-only tools only; no write env vars needed.
2. **Rate limits** — dedicated RPC for production; exponential backoff on 429.
3. **Confidence** — tag responses HIGH (dedicated node), MEDIUM (shared), LOW (public).
4. **Never** pass private keys in MCP `env` or tool arguments.

## Failure modes

| Error | Cause | Fix |
| --- | --- | --- |
| `GuardrailError` on write | Missing simulate/confirm env | Set gates after human review |
| RPC 403 / invalid API key | Wrong `ALCHEMY_*_URL` | Rotate key; update mcp.json |
| Tool not found | Stale client cache | Restart MCP; re-run validate script |
| `debug_trace_call` unsupported | Node tier | Use Alchemy/QuickNode trace addon |

## Worked example (dual-chain read)

```bash
export ALCHEMY_ETH_URL=https://eth-mainnet.g.alchemy.com/v2/KEY
export SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
# Cursor MCP: load evm-rpc.mcp.json + solana-rpc.mcp.json
# Agent: eth_call on L1, simulate_transaction on Solana — no writes
```

## Authoritative sources

- [mcp/README.md](../mcp/README.md)
- [registry/assets.json](../registry/assets.json)
- [registry/chains.json](../registry/chains.json)
- [mcp/_shared/guardrails.py](../mcp/_shared/guardrails.py)
- [using-blockchain-agent-skills SKILL](../skills/using-blockchain-agent-skills/SKILL.md)
- [validate-mcp-servers.py](../scripts/validate-mcp-servers.py)

## Provenance

| Field | Value |
| --- | --- |
| Source document | `references/mcp-blockchain-rpc-patterns.md` |
| Version / effective | 1.0 / 2026-06-13 |
| Last reviewed | 2026-06-13 |
| Reviewer | blockchain-agent-skills maintainers |
| Next review due | 2026-09-13 |
| Notes | Nine servers per registry/assets.json; tool names from server.py |
