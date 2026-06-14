# Blockchain Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-12%20%2B%201%20meta-brightgreen.svg)](#core-skills)
[![Presets](https://img.shields.io/badge/Presets-4-blue.svg)](#platform-presets)
[![Examples](https://img.shields.io/badge/Examples-4%20(2%20runnable)-purple.svg)](#examples)
[![MCP Servers](https://img.shields.io/badge/MCP%20Servers-4%20(scaffold)-orange.svg)](#mcp-servers)
[![Starter Packs](https://img.shields.io/badge/Starter%20Packs-5-red.svg)](#starter-packs)
[![Validate and Package](https://github.com/vaquarkhan/blockchain-agent-skills/actions/workflows/validate-and-package.yml/badge.svg?branch=main)](https://github.com/vaquarkhan/blockchain-agent-skills/actions/workflows/validate-and-package.yml)
[![GitHub Release](https://img.shields.io/github/v/release/vaquarkhan/blockchain-agent-skills)](https://github.com/vaquarkhan/blockchain-agent-skills/releases)

> **📦 [GitHub Releases](https://github.com/vaquarkhan/blockchain-agent-skills/releases/latest)** — VS Code `.vsix` and JetBrains plugin ZIP  
> Companion: [compliance-agent-skills](https://github.com/vaquarkhan/compliance-agent-skills) | Pattern: [data-engineering-agent-skills](https://github.com/vaquarkhan/data-engineering-agent-skills)

Production-grade **blockchain infrastructure** skills for AI agents — multi-chain RPC, transaction lifecycle, smart contracts, guardrails, MCP servers, and Bedrock AgentCore orchestration.

The goal is not generic Web3 prompts. The goal is **operating procedures** for simulate-first transactions, chain abstraction, compliance guardrails, and auditable multi-chain operations across 18 chains.

## Agent Skills Registry Compatibility

- Every capability lives in a directory with `SKILL.md`
- YAML frontmatter: `name` + `description` (third person, trigger terms)
- Progressive disclosure — load skills on demand
- Supporting assets in `guardrails/`, `mcp/`, `presets/`, `examples/`, `hooks/`

## Quick Start

### 1. Clone and validate

```bash
git clone https://github.com/vaquarkhan/blockchain-agent-skills.git
cd blockchain-agent-skills
pip install -r requirements.txt
python scripts/validate-skills.py
python tests/test_chain_providers.py
```

### 2. Load entry skill

`skills/using-blockchain-agent-skills/SKILL.md`

### 3. Pick a preset

| Preset | Path |
| --- | --- |
| EVM Core | `presets/evm-core/PRESET.md` |
| Solana | `presets/solana-mainnet/PRESET.md` |
| NEAR | `presets/near-mainnet/PRESET.md` |
| Cosmos IBC | `presets/cosmos-ibc/PRESET.md` |

### 4. Lifecycle

`/plan` → `/simulate` → `/confirm` → `/broadcast` → `/confirm-depth`

## Install Surfaces

### VS Code / Cursor / Windsurf

1. Download `.vsix` from [Releases](https://github.com/vaquarkhan/blockchain-agent-skills/releases/latest)
2. `Ctrl+Shift+P` → **Extensions: Install from VSIX...**
3. `Ctrl+Shift+P` → **Blockchain Skills: Install Full Toolkit**

See `vscode-extension/README.md` and `tutorials/installing-vscode-and-jetbrains-plugins.md`.

### JetBrains (IntelliJ, PyCharm, WebStorm)

1. Download plugin ZIP from Releases
2. **Settings** → **Plugins** → **Install Plugin from Disk...**

See `jetbrains-plugin/README.md` and `docs/jetbrains-setup.md`.

### Script install

```bash
scripts/install.sh --tool all --target /path/to/project
scripts/install.sh --tool cursor,claude --target /path/to/project
```

Windows:

```powershell
pwsh scripts/install.ps1 --tool all --target C:\path\to\project
pwsh .\bootstrap.ps1 C:\path\to\project auto
```

### Install by tool

| Tool | Guide | Install |
| --- | --- | --- |
| Cursor | `docs/cursor-setup.md` | `.cursor/rules/` or extension |
| Claude | `CLAUDE.md` | `.claude/commands/` |
| Copilot | `docs/getting-started.md` | `.github/copilot-instructions.md` |
| Windsurf | `docs/windsurf-setup.md` | `.windsurfrules.example` |
| Codex | `docs/codex-setup.md` | `AGENTS.md` + skills |
| JetBrains | `docs/jetbrains-setup.md` | Plugin or script |

## Core Skills

| # | Skill | Phase |
| --- | --- | --- |
| — | using-blockchain-agent-skills | Meta |
| 1 | chain-abstraction | 1 |
| 2 | transaction-lifecycle | 1 |
| 3 | smart-contract-factory | 2 |
| 4 | block-state-queries | 1 |
| 5 | event-indexing | 2 |
| 6 | consensus-validator-ops | 4 |
| 7 | storage-state-proofs | 3 |
| 8 | token-standards-engine | 2 |
| 9 | privacy-zk | 3 |
| 10 | network-monitoring | 4 |
| 11 | data-availability | 3 |
| 12 | rollup-operations | 3 |

Full catalog: [skills-index.md](skills-index.md) | Registry: [registry/assets.json](registry/assets.json)

## Platform Presets

| Preset | Chains |
| --- | --- |
| evm-core | Ethereum, Arbitrum, Base, Polygon |
| solana-mainnet | Solana mainnet/devnet |
| near-mainnet | NEAR, Aurora |
| cosmos-ibc | Cosmos Hub, Osmosis, Celestia, Injective |

## Starter Packs

| Pack | File |
| --- | --- |
| EVM Core | `starter-packs/evm-core-starter.yaml` |
| Solana Programs | `starter-packs/solana-programs-starter.yaml` |
| NEAR Multi-chain | `starter-packs/near-multichain-starter.yaml` |
| Cosmos IBC | `starter-packs/cosmos-ibc-starter.yaml` |
| Compliance Guardrails | `starter-packs/compliance-guardrails-starter.yaml` |

## MCP Servers

| Server | Chains | Status |
| --- | --- | --- |
| evm-rpc-server | ETH, Arbitrum, Base, Polygon, … | Scaffold |
| solana-rpc-server | Solana | Scaffold |
| near-rpc-server | NEAR, Aurora | Scaffold |
| cosmos-rpc-server | Cosmos, Osmosis, … | Scaffold |

See [mcp/README.md](mcp/README.md).

## Examples

| Example | Type | Description |
| --- | --- | --- |
| chain-provider-validation | Runnable | pytest proof for chain adapters |
| evm-erc20-deploy | Runnable | ERC-20 deploy with simulate-first |
| solana-spl-token | Blueprint | SPL token workflow |
| cosmos-ibc-transfer | Blueprint | ICS-20 transfer |

See [examples/README.md](examples/README.md).

## Guardrails

| File | Purpose |
| --- | --- |
| `guardrails/transaction-safety.yaml` | Simulate-first, $10k threshold, reorg depth |
| `guardrails/security.yaml` | Key protection, honeypot, blind signing block |
| `guardrails/compliance.yaml` | OFAC, travel rule, audit trail |
| `guardrails/denied-topics.yaml` | Block exploits, sanctions evasion |

## Design Principles

- **Chain-agnostic** — every skill accepts `chainId` / `chainName`
- **Simulate-first** — no broadcast without simulation
- **Audit-complete** — 7-year DynamoDB retention spec
- **Confidence scoring** — HIGH / MEDIUM / LOW on every output
- **Human-in-the-loop** — >$10k, validator ops, LOW confidence

## Repository Layout

```
blockchain-agent-skills/
├── AGENTS.md                 # Agent entry point
├── skills/                   # 12 core + meta skill
├── vscode-extension/         # VS Code / Cursor installer
├── jetbrains-plugin/         # JetBrains IDE installer
├── mcp/                      # Chain-family MCP servers
├── guardrails/               # Safety, security, compliance
├── presets/                  # Platform presets
├── starter-packs/            # Adoption bundles
├── examples/                 # Runnable + blueprint examples
├── lib/chain_providers/      # Python chain adapters
├── hooks/                    # Session and tx safety hooks
├── scripts/                  # install, validate, hooks
├── docs/                     # Setup guides
└── tutorials/                # Plugin install walkthrough
```

## Validation

```bash
python scripts/validate-skills.py
python tests/test_chain_providers.py
```

## Implementation Phases

| Phase | Focus | Status |
| --- | --- | --- |
| 1 | EVM Core | Complete |
| 2 | Alt-L1s (Solana, NEAR, Cosmos) | In progress |
| 3 | ZK & Move | Planned |
| 4 | Bitcoin, TON, Polkadot, Hedera | Planned |

See [docs/coverage-roadmap.md](docs/coverage-roadmap.md) and [docs/TECHNICAL-REFERENCE.md](docs/TECHNICAL-REFERENCE.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
