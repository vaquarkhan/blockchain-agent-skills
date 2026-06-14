# Coverage Roadmap

Implementation priority aligned with [TECHNICAL-REFERENCE.md](TECHNICAL-REFERENCE.md) Section 6.

## Phase 1 — EVM Core (current)

**Skills:** chain-abstraction, transaction-lifecycle, block-state-queries  
**MCP:** evm-rpc-server (full), others stubbed  
**Chains:** Ethereum, Arbitrum, Base, Polygon

| Component | Status |
| --- | --- |
| ChainProvider interface + EVM adapters | Scaffold |
| EIP-1559 tx build/sign/simulate/broadcast | Scaffold |
| eth_getBlock, eth_call, debug_traceCall | Scaffold |
| Gas optimization (base fee, priority fee, L2 calldata) | Planned |
| Guardrails integration | Done |
| Bedrock action groups (Lambda) | Template only |

## Phase 2 — Alt-L1s

**Skills:** smart-contract-factory, token-standards-engine, event-indexing  
**MCP:** solana-rpc-server, near-rpc-server, cosmos-rpc-server  
**Chains:** Solana, NEAR, Cosmos Hub + IBC

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
