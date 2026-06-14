# EVM RPC MCP Server

MCP server for EVM-compatible chains. Phase 1 implementation covers Ethereum, Arbitrum, Base, and Polygon.

## Implemented server (`server.py`)

Read-only MCP stdio tools (v0.2.0):

| Tool | RPC method |
| --- | --- |
| `eth_blockNumber` | eth_blockNumber |
| `eth_getBalance` | eth_getBalance |
| `eth_call` | eth_call |
| `eth_estimateGas` | eth_estimateGas |

```bash
export ALCHEMY_ETH_URL=https://eth-mainnet.g.alchemy.com/v2/KEY
python server.py
python ../../scripts/validate-mcp-servers.py
```

Write tools (`eth_sendRawTransaction`, etc.) remain roadmap — use KMS signing outside MCP.

## Deployment

Docker → ECS Fargate behind ALB. OAuth 2.0 via AWS Cognito for production.

See [../README.md](../README.md) for architecture overview.
