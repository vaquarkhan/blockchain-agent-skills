# Solana RPC MCP Server

MCP server for Solana mainnet and devnet. Phase 2 implementation.

## Tools

| Tool | RPC method | Description |
| --- | --- | --- |
| `getAccountInfo` | getAccountInfo | Read account data and lamport balance |
| `getBalance` | getBalance | Native SOL balance |
| `sendTransaction` | sendTransaction | Broadcast signed versioned transaction |
| `simulateTransaction` | simulateTransaction | Simulate before broadcast (mandatory) |
| `getSignaturesForAddress` | getSignaturesForAddress | Tx history for address |
| `getTokenAccountsByOwner` | getTokenAccountsByOwner | SPL token accounts |
| `getProgramAccounts` | getProgramAccounts | Program state scan |
| `getAsset` | getAsset | Metaplex DAS API (via Helius) |
| `getRecentPrioritizationFees` | getRecentPrioritizationFees | Priority fee estimation |

## Anchor / program interaction

- PDA derivation: `findProgramAddressSync(seeds, programId)`
- CPI composition via instruction builder
- Priority fee + optional Jito tip for MEV protection

## Setup

```bash
pip install -r requirements.txt
export HELIUS_SOL_URL=https://mainnet.helius-rpc.com/?api-key=KEY
export MCP_API_KEY=dev-local-key
python server.py
```

## Token standards

SPL Token, Token-2022 (transfer hooks, confidential transfers), Metaplex NFTs, compressed NFTs (Bubblegum).
