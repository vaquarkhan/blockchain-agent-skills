---
inclusion: always
---

# Technical Context

- **Skills:** `skills/` — 12 core workflows plus meta skill
- **Guardrails:** `guardrails/` — transaction safety, security, compliance
- **Chain providers:** `lib/chain_providers/` — unified routing across 18 chains
- **MCP:** `mcp/*.mcp.json` templates + server scaffolds under `mcp/*-rpc-server/`
- **Lifecycle:** plan → simulate → confirm → broadcast → confirm-depth
- **Validation:** `python scripts/validate-skills.py`, `python scripts/validate-assets.py`

Never expose private keys in agent context. Use KMS for signing.
