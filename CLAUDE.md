# CLAUDE.md — Blockchain Agent Skills

Read `AGENTS.md` first. Load `skills/using-blockchain-agent-skills/SKILL.md` for routing.

## Lifecycle

`/plan` → `/simulate` → `/confirm` → `/broadcast` → `/confirm-depth`

## Rules

- Simulate-first on all mainnet writes
- Never expose private keys
- Block sanctioned addresses (no override)
- One primary skill per operation thread

## Commands

See `.claude/commands/` for plan, simulate, broadcast, confirm-depth.
