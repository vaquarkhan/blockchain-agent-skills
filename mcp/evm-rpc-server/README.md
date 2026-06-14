# EVM RPC MCP Server

MCP server for EVM-compatible chains. Covers Ethereum, Arbitrum, Base, Polygon, and additional EVM L1/L2 chains via env-configured RPC URLs.

## Tools (11)

| Tool | RPC method | Mode |
| --- | --- | --- |
| `eth_blockNumber` | eth_blockNumber | read |
| `eth_getBlockByNumber` | eth_getBlockByNumber | read |
| `eth_getBalance` | eth_getBalance | read |
| `eth_call` | eth_call | simulate |
| `eth_estimateGas` | eth_estimateGas | simulate |
| `eth_getLogs` | eth_getLogs | read |
| `eth_getStorageAt` | eth_getStorageAt | read |
| `eth_getTransactionReceipt` | eth_getTransactionReceipt | read |
| `debug_traceCall` | debug_traceCall | read |
| `eth_getProof` | eth_getProof | read |
| `eth_sendRawTransaction` | eth_sendRawTransaction | write (guarded) |

## Run

```bash
export ALCHEMY_ETH_URL=https://eth-mainnet.g.alchemy.com/v2/KEY
python server.py
python ../../scripts/validate-mcp-servers.py
```

## Write guardrails

`eth_sendRawTransaction` requires `SIMULATE_PASSED=true` or `SIMULATION_RUN_ID`. Mainnet also requires `HUMAN_CONFIRMED=true`. Sign with KMS outside MCP — pass only the raw signed hex.

## Deployment

Docker → ECS Fargate behind ALB. OAuth 2.0 via AWS Cognito for production.

See [../README.md](../README.md).
