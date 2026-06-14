# Blockchain Agent Skills

12 core agent skills for multi-chain blockchain infrastructure — chain abstraction, transaction lifecycle, smart contracts, state queries, event indexing, validator ops, storage proofs, token standards, privacy/ZK, network monitoring, data availability, and rollup operations.

Built for **Amazon Bedrock AgentCore + MCP** architecture. Companion to [compliance-agent-skills](https://github.com/vaquarkhan/compliance-agent-skills).

## Quick start

1. Read [AGENTS.md](AGENTS.md) — primary routing document for AI agents.
2. Load the meta skill `using-blockchain-agent-skills` for orchestration.
3. Configure MCP servers from [mcp/README.md](mcp/README.md).
4. Apply guardrails from [guardrails/](guardrails/) before any mainnet transaction.

## Supported chains (18)

Ethereum, NEAR, Solana, Polygon, Arbitrum, Optimism, Base, Avalanche, BNB Chain, Cosmos/IBC, Bitcoin (+ L2s), TON, Sui, Aptos, Starknet, zkSync Era, Polkadot/Substrate, Hedera.

## Implementation phases

| Phase | Focus | Status |
| --- | --- | --- |
| **Phase 1** | EVM Core — chain abstraction, tx lifecycle, state queries, gas | Complete |
| **Phase 2** | Alt-L1s — contracts, tokens, events, Solana/NEAR/Cosmos MCP | In progress |
| **Phase 3** | ZK & Move — rollups, DA, privacy, Sui/Aptos | Planned |
| **Phase 4** | Legacy & niche — Bitcoin, TON, Polkadot, Hedera, validator ops | Planned |

See [docs/coverage-roadmap.md](docs/coverage-roadmap.md) and [docs/TECHNICAL-REFERENCE.md](docs/TECHNICAL-REFERENCE.md).

## Repository layout

```
blockchain-agent-skills/
├── AGENTS.md                 # Agent entry point and routing
├── skills-index.md           # Human-readable skill catalog
├── skills/                   # 12 core + meta orchestration skill
├── agents/                   # Supervisor-worker agent personas
├── mcp/                      # 8 chain-family MCP server templates
├── guardrails/               # Transaction, security, compliance rules
├── templates/                # Bedrock action group and Lambda scaffolds
├── registry/assets.json      # Machine-readable asset index
└── scripts/validate-skills.py
```

## Design principles

- **Chain-agnostic interface** — every skill accepts `chainId` / `chainName`; no hardcoded chain logic in business layer.
- **Simulate-first** — no transaction broadcast without prior simulation.
- **Audit-complete** — all signed payloads, simulations, and receipts logged with 7-year retention.
- **Confidence scoring** — every output includes HIGH / MEDIUM / LOW based on RPC reliability and simulation results.
- **Human-in-the-loop** — mandatory review for txs >$10k, validator ops, rollup exits, and LOW confidence operations.

## Validation

```bash
python scripts/validate-skills.py
```

## License

MIT — see [LICENSE](LICENSE).
