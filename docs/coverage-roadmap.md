# Coverage Roadmap

Implementation status as of **v0.3.1**. See [TECHNICAL-REFERENCE.md](TECHNICAL-REFERENCE.md).

## Phase 1 — EVM Core (implemented)

**Skills:** chain-abstraction, transaction-lifecycle, block-state-queries  
**MCP:** evm-rpc-server (11 tools, guarded write)  
**Chains:** Ethereum, Arbitrum, Base, Polygon, Optimism, Avalanche, BNB, zkSync, Starknet

| Component | Status |
| --- | --- |
| ChainProvider + EVM adapters | Done |
| MCP `server.py` + schema parity | Done |
| Simulate-first + guardrails | Done |
| Bedrock Lambda templates | Template scaffold in `templates/skill-definition.yaml` |

## Phase 2 — Alt-L1s (implemented)

**Skills:** smart-contract-factory, token-standards-engine, event-indexing  
**MCP:** solana-rpc-server, near-rpc-server, cosmos-rpc-server  
**Chains:** Solana, NEAR, Aurora, Cosmos Hub, Osmosis, Celestia, Injective

| Component | Status |
| --- | --- |
| ChainProvider adapters | Done |
| MCP servers (4 tools each) | Done |
| Skill depth + verification checklists | Done |

## Phase 3 — ZK & Move (implemented — read paths)

**Skills:** rollup-operations, data-availability, privacy-zk, storage-state-proofs  
**MCP:** move-rpc-server + extended EVM for L2/zkSync/Starknet routing  
**Chains:** Sui, Aptos, Starknet, zkSync Era

| Component | Status |
| --- | --- |
| move-rpc-server | Done (Sui + Aptos view tools) |
| ChainProvider metadata | Done |
| ZK proof generation | Skill guidance; prover integration external |

## Phase 4 — Legacy & Niche (implemented — read paths)

**Skills:** consensus-validator-ops, network-monitoring  
**MCP:** bitcoin-rpc-server, ton-rpc-server, substrate-rpc-server  
**Chains:** Bitcoin, TON, Polkadot, Kusama, Moonbeam

| Component | Status |
| --- | --- |
| MCP servers | Done |
| ChainProvider metadata | Done |
| Validator key rotation templates | Done (`templates/validator-rotation-plan.yaml`) |

## Validation

```bash
python scripts/validate-skills.py
python scripts/validate-assets.py
python scripts/validate-mcp-servers.py
python tests/test_chain_providers.py
python tests/test_mcp_servers.py
python evals/run.py
```

## Multi-region CDK (Bedrock AgentCore)

| Region | Purpose |
| --- | --- |
| us-east-1 | Primary — EVM chains, Bedrock, supervisor |
| ap-south-1 | NEAR, Solana, India DPDP compliance |
| ap-southeast-1 | TON, BNB, Cosmos SEA, Sui |
| eu-west-1 | Polkadot, zkSync, Starknet — MiCA |
| me-south-1 | Bitcoin, Hedera — VARA / Tadawul |
