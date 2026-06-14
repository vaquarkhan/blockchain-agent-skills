# EVM RPC MCP Server

MCP server for EVM-compatible chains. Phase 1 implementation covers Ethereum, Arbitrum, Base, and Polygon.

## Tools

| Tool | RPC method | Description |
| --- | --- | --- |
| `eth_call` | eth_call | Simulate contract call |
| `eth_estimateGas` | eth_estimateGas | Estimate gas for transaction |
| `eth_sendRawTransaction` | eth_sendRawTransaction | Broadcast signed tx |
| `eth_getLogs` | eth_getLogs | Query event logs |
| `eth_getStorageAt` | eth_getStorageAt | Read storage slot |
| `eth_getTransactionReceipt` | eth_getTransactionReceipt | Get tx receipt |
| `debug_traceCall` | debug_traceCall | Trace call execution |
| `eth_getProof` | eth_getProof | Merkle-Patricia storage proof |
| `eth_getBlockByNumber` | eth_getBlockByNumber | Get block by number |
| `eth_getBalance` | eth_getBalance | Get account balance |

## Setup

```bash
pip install -r requirements.txt
export ALCHEMY_ETH_URL=https://eth-mainnet.g.alchemy.com/v2/KEY
export MCP_API_KEY=dev-local-key
python server.py
```

## Health check

`GET /health` — returns RPC connectivity status per configured chain.

## Deployment

Docker → ECS Fargate behind ALB. OAuth 2.0 via AWS Cognito for production.

See [../README.md](../README.md) for architecture overview.
