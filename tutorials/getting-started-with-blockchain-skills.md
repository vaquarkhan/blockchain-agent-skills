# Getting Started with Blockchain Agent Skills

1. Clone the repository and open it in your IDE.
2. Run `python scripts/validate-skills.py` and `python scripts/validate-assets.py`.
3. Load `skills/using-blockchain-agent-skills/SKILL.md` for routing.
4. Pick a preset under `presets/` matching your chain family.
5. Install adapters with `python scripts/install_toolkit.py --tool all --target .` (into a consumer repo).

Always follow simulate-first: `/plan` → `/simulate` → `/confirm` → `/broadcast` → `/confirm-depth`.
