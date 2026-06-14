# Getting Started

Works with any AI agent that consumes Markdown instructions, rules files, or repository-level guidance.

## What You Get

- 12 core blockchain infrastructure skills (+ meta orchestration)
- 8 chain-family MCP server templates
- Guardrails (transaction safety, security, compliance)
- Platform presets for EVM, Solana, NEAR, Cosmos
- VS Code and JetBrains installer plugins
- Runnable and blueprint examples

## 5-Minute Quick Start

1. Clone the repository:

```bash
git clone https://github.com/vaquarkhan/blockchain-agent-skills.git
cd blockchain-agent-skills
pip install -r requirements.txt
```

2. Load the entry skill: `skills/using-blockchain-agent-skills/SKILL.md`

3. Pick a preset from `presets/`:
   - `presets/evm-core/PRESET.md` — Ethereum, Arbitrum, Base, Polygon
   - `presets/solana-mainnet/PRESET.md`
   - `presets/near-mainnet/PRESET.md`
   - `presets/cosmos-ibc/PRESET.md`

4. Run the lifecycle: `/plan` → `/simulate` → `/confirm` → `/broadcast` → `/confirm-depth`

5. Validate skills:

```bash
python scripts/validate-skills.py
python tests/test_chain_providers.py
```

## Install Into Another Project

```bash
scripts/install.sh --tool all --target /path/to/project
```

Windows:

```powershell
pwsh scripts/install.ps1 --tool all --target C:\path\to\project
```

Bootstrap shortcut:

```bash
./bootstrap.sh /path/to/project auto
```

## Plugin Install

- **VS Code / Cursor:** Install extension or `.vsix` from [Releases](https://github.com/vaquarkhan/blockchain-agent-skills/releases/latest)
- **JetBrains:** Install plugin or `.zip` from Releases

See `tutorials/installing-vscode-and-jetbrains-plugins.md`.

## Tool Setup Guides

- `docs/cursor-setup.md`
- `docs/jetbrains-setup.md`
- `docs/codex-setup.md`
- `docs/windsurf-setup.md`
- `docs/plugin-publishing.md`

## Hooks

```bash
bash hooks/session-start.sh
python scripts/hook_runner.py tx-simulate-pre
```
