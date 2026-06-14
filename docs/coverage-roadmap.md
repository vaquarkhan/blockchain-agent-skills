# Coverage Roadmap

Implementation priority aligned with [TECHNICAL-REFERENCE.md](TECHNICAL-REFERENCE.md) Section 6.

## Phase 1 — EVM Core (complete)

**Skills:** chain-abstraction, transaction-lifecycle, block-state-queries  
**MCP:** evm-rpc-server (config scaffold)  
**Chains:** Ethereum, Arbitrum, Base, Polygon

| Component | Status |
| --- | --- |
| ChainProvider interface + EVM adapters | Done (`lib/chain_providers/evm.py`) |
| EIP-1559 tx build/sign/simulate/broadcast | Skill scaffold |
| eth_getBlock, eth_call, debug_traceCall | MCP scaffold |
| Gas optimization | Planned |
| Guardrails integration | Done |
| Bedrock action groups (Lambda) | Template only |

## Phase 2 — Alt-L1s (current)

**Skills:** smart-contract-factory, token-standards-engine, event-indexing  
**MCP:** solana-rpc-server, near-rpc-server, cosmos-rpc-server  
**Chains:** Solana, NEAR, Aurora, Cosmos Hub, Osmosis, Celestia, Injective

| Component | Status |
| --- | --- |
| Solana/NEAR/Cosmos ChainProvider adapters | Done (`lib/chain_providers/`) |
| solana-rpc-server config + tool schemas | Done |
| near-rpc-server config + tool schemas | Done |
| cosmos-rpc-server config + IBC tools | Done |
| Phase 2 skill expansions (Anchor, NEP, CW) | Done |
| MCP server.py runtime (Python) | Planned |
| Lambda handlers for Phase 2 skills | Planned |

## Phase 3 — ZK & Move

**Skills:** rollup-operations, data-availability, privacy-zk, storage-state-proofs  
**MCP:** move-rpc-server (+ extended evm for zkSync/Starknet)  
**Chains:** Starknet, zkSync Era, Sui, Aptos

## Phase 4 — Legacy & Niche

**Skills:** consensus-validator-ops, network-monitoring  
**MCP:** bitcoin-rpc-server, ton-rpc-server, substrate-rpc-server  
**Chains:** Bitcoin L2s, TON, Polkadot, Hedera

## Multi-region CDK (Bedrock AgentCore)

| Region | Purpose |
| --- | --- |
| us-east-1 | Primary — EVM chains, Bedrock, supervisor |
| ap-south-1 | NEAR, Solana, India DPDP compliance |
| ap-southeast-1 | TON, BNB, Cosmos SEA, Sui |
| eu-west-1 | Polkadot, zkSync, Starknet — MiCA |
| me-south-1 | Hedera, Bitcoin — VARA / Tadawul |
