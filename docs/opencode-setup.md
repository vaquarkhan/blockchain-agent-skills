# OpenCode Setup

Use this repository with OpenCode by linking the shared skill surface under `.opencode/`.

## Recommended Setup

1. Install the core toolkit or clone this repository locally.
2. Copy or symlink:
   - `.opencode/README.md`
   - `.opencode/skills`
   - `AGENTS.md`
   - `CLAUDE.md`
3. Point OpenCode at `skills/` for task-specific workflows.

## Suggested Flow

1. Start with `skills/using-blockchain-agent-skills/SKILL.md`
2. Load the preset for your target chain family
3. Use simulate-first lifecycle commands before any broadcast
4. Apply guardrails from `guardrails/` for mainnet and compliance work
