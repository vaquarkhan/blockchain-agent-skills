# Codex / AGENTS.md Setup

Point your agent at:

1. `AGENTS.md` — primary routing
2. `skills-index.md` — skill catalog
3. `skills/using-blockchain-agent-skills/SKILL.md` — orchestration

Install full toolkit:

```bash
scripts/install.sh --tool codex --target .
```

Key constraints from guardrails:

- Simulate before broadcast
- Never expose private keys
- Block OFAC-sanctioned addresses
