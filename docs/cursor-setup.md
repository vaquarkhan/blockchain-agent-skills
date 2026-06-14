# Cursor Setup

## Option 1: VS Code Extension (recommended for Cursor)

1. Install **Blockchain Agent Skills** from VSIX or copy `.cursor/rules/` from this repo
2. Command Palette → `Blockchain Skills: Install Full Toolkit`

## Option 2: Script Install

```bash
scripts/install.sh --tool cursor --target /path/to/project
```

Installs:

- `.cursor/rules/00-blockchain-agent-core.mdc`
- `.cursor/rules/10-simulate-first.mdc`
- `.cursor/rules/20-guardrails.mdc`
- `.cursor/rules/30-chain-routing.mdc`

## Option 3: Clone and Reference

Add this repo as project context. Read `AGENTS.md` first, then load skills from `skills/` on demand.

## Lifecycle in Cursor

Use natural language or commands aligned with `.claude/commands/`:

- Plan operation → `/plan`
- Simulate tx → `/simulate`
- Broadcast → `/broadcast` (after guardrails + confirmation)
