# MCP Servers

Eight implemented Python MCP stdio servers with schema-validated tool registries.

| Server | Tools | Chains |
| --- | ---: | --- |
| `evm-rpc-server` | 11 | Ethereum, Arbitrum, Base, Polygon |
| `solana-rpc-server` | 4 | Solana |
| `near-rpc-server` | 4 | NEAR, Aurora |
| `cosmos-rpc-server` | 4 | Cosmos Hub, Osmosis, Celestia, Injective |
| `move-rpc-server` | 2 | Sui, Aptos |
| `bitcoin-rpc-server` | 2 | Bitcoin |
| `ton-rpc-server` | 1 | TON |
| `substrate-rpc-server` | 2 | Polkadot, Kusama, Moonbeam |

## Flat install templates

`mcp/*.mcp.json` — copy into MCP client config; each points at `python mcp/<server>/server.py`.

## Validate

```bash
python scripts/validate-mcp-servers.py
python tests/test_mcp_servers.py
```

## Write guardrails

Broadcast tools require `SIMULATE_PASSED=true` or `SIMULATION_RUN_ID`. Mainnet also requires `HUMAN_CONFIRMED=true`. Never pass private keys through MCP — sign with KMS externally.
