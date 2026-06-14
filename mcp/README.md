# MCP Servers — Blockchain Agent Skills

Eight specialized MCP servers cover all blockchain families. Each exposes tools via SSE/Streamable HTTP with OAuth 2.0 authentication (AWS Cognito) and API key fallback for local dev.

## Server catalog

| Server | Chains | Key tools |
| --- | --- | --- |
| [evm-rpc-server](evm-rpc-server/) | ETH, Polygon, Arbitrum, Base, OP, Avalanche, BNB, zkSync, Starknet | eth_call, eth_sendRawTransaction, eth_getLogs, debug_traceCall, eth_getStorageAt, eth_estimateGas |
| [solana-rpc-server](solana-rpc-server/) | Solana mainnet/devnet | getAccountInfo, sendTransaction, simulateTransaction, getTokenAccountsByOwner, getAsset |
| [near-rpc-server](near-rpc-server/) | NEAR, Aurora | query, send_tx, view_access_key, view_account, view_contract_state |
| [cosmos-rpc-server](cosmos-rpc-server/) | Cosmos Hub, Osmosis, Celestia, Injective, dYdX | broadcast_tx, abci_query, ibc_transfer, query_client_state |
| [move-rpc-server](move-rpc-server/) | Sui, Aptos | sui_executeTransactionBlock, sui_getObject, apt_submitTransaction, apt_getAccountResource |
| [bitcoin-rpc-server](bitcoin-rpc-server/) | Bitcoin, Lightning, Stacks | sendrawtransaction, createpsbt, finalizepsbt, listunspent, estimatesmartfee |
| [ton-rpc-server](ton-rpc-server/) | TON | sendBoc, getTransactions, runGetMethod, estimateFee |
| [substrate-rpc-server](substrate-rpc-server/) | Polkadot, Moonbeam, Astar | author_submitExtrinsic, state_getStorage, xcm_send |

## Per-server file set

```
mcp/{server-name}/
├── server.py           # MCP protocol, SSE/HTTP transport, tool handlers
├── tool-schemas.json   # JSON Schema for all tools
├── config.yaml         # RPC endpoints, rate limits, chain config
├── auth.py             # OAuth 2.0 via Cognito, API key fallback
├── Dockerfile          # ECS Fargate deployment, /health endpoint
└── README.md           # Tool catalogue, auth guide, rate limits
```

## Rate limits (per agent)

| Family | Limit |
| --- | --- |
| EVM | 100 req/s |
| Solana | 50 req/s |
| NEAR/Cosmos | 30 req/s |

Exponential backoff with jitter on 429 errors.

## Local development

```bash
cd mcp/evm-rpc-server
export MCP_API_KEY=dev-local-key
python server.py
```

## Protocol integrations

| Category | Providers |
| --- | --- |
| RPC | Alchemy, Infura, QuickNode, Ankr, Blast API |
| Indexers | The Graph, Goldsky, Envio, Subsquid |
| Explorers | Etherscan, Blockscout, Solscan, Nearblocks |
| MEV | Flashbots, Jito, bloXroute |
| Analytics | Dune, Flipside, Nansen |
