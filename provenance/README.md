# Provenance and SME Review

This folder records subject-matter review for skills, guardrails, MCP servers, and examples.

## Files

| File | Purpose |
| --- | --- |
| `SME-REVIEW-LOG.md` | Chronological review entries with reviewer, scope, and outcome |
| `skills-provenance.json` | Machine-readable map of skill → owner → last review → source refs |

## Review cadence

- **Tier 1 skills** (chain-abstraction, transaction-lifecycle, block-state-queries): quarterly
- **Tier 2 skills** (contracts, tokens, indexing): quarterly after Phase 2 changes
- **Tier 3 skills** (rollup, DA, ZK, validators): before marking `implemented` in registry
- **Guardrails:** review on any threshold or sanctions list change

## Adding a review entry

1. Run validation: `python scripts/validate-skills.py && python scripts/validate-assets.py`
2. Append a row to `SME-REVIEW-LOG.md`
3. Update `last_reviewed` in `skills-provenance.json`
