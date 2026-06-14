# Contributing

1. Fork and branch from `main`
2. Follow existing skill structure (`skills/*/SKILL.md` with YAML frontmatter)
3. Run validators before PR:

```bash
python scripts/validate-skills.py
python tests/test_chain_providers.py
```

4. Keep SKILL.md under 500 lines; use `docs/` for long reference
5. Do not commit secrets, private keys, or `.env` files

See `docs/coverage-roadmap.md` for phase priorities.
