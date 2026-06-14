# Installing VS Code and JetBrains Plugins

## VS Code / Cursor / Windsurf

### From VSIX (GitHub Releases)

1. Download `.vsix` from [latest release](https://github.com/vaquarkhan/blockchain-agent-skills/releases/latest)
2. `Ctrl+Shift+P` → **Extensions: Install from VSIX...**
3. Reload editor
4. `Ctrl+Shift+P` → search **Blockchain Skills:**

### Commands

| Command | Installs |
| --- | --- |
| Install Full Toolkit | Core + adapters + starter packs + MCP |
| Install Core Pack | AGENTS.md, guardrails, hooks, scripts |
| Install Starter Pack | EVM, Solana, NEAR, Cosmos, or Compliance pack |
| Install MCP Templates | evm/solana/near/cosmos RPC configs |
| Scaffold Example | Example project folder |

## JetBrains

1. Download plugin ZIP from Releases
2. **Settings** → **Plugins** → **Install Plugin from Disk...**
3. Restart IDE
4. **Find Action** → "Install Full Toolkit"

## Verify Install

```bash
python scripts/validate-skills.py
ls AGENTS.md guardrails/ skills/
```

## Troubleshooting

- **No workspace folder:** Open a project folder before running install commands
- **Download failed:** Check `blockchainSkills.rawBaseUrl` setting (VS Code) or network access to GitHub raw URLs
