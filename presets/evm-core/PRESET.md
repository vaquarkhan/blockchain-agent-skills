# EVM Core Preset

**Chains:** Ethereum, Arbitrum, Base, Polygon  
**MCP:** evm-rpc-server  
**Phase:** 1

## Default RPC providers

Alchemy, Infura, QuickNode, Ankr

## Confirmation depth

| Chain | Blocks |
| --- | --- |
| Ethereum | 12 |
| Arbitrum | 20 |
| Base | 20 |
| Polygon | 128 |

## Skills to load

1. using-blockchain-agent-skills
2. chain-abstraction
3. transaction-lifecycle
4. block-state-queries

## Starter pack

`starter-packs/evm-core-starter.yaml`

## Guardrails

All writes require simulation. Mainnet txs >$10k need human confirmation.
