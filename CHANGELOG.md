# Changelog

## 0.5.0

- Add `provenance/provenance.yaml` with authoritative standards (EIP, OFAC, NIST, IBC, BOLT, HTS, OP Stack)
- Expand all reference guides to 80–130 lines with provenance footers; add 5 new chain/topic guides
- Eval coverage **40/40** with per-task breakdown in `evals/report.json` and `evals/gaps.md`
- `scripts/validate-provenance.py` enforced in CI; skills-provenance links to external standard IDs
- Reconcile skill tier tables with implemented MCP read paths (Move, Bitcoin, Hedera, TON)
- VS Code extension version aligned to 0.5.0

## 0.4.0

- Bedrock AgentCore Lambda handlers with per-skill artifacts (manifest, OpenAPI, action groups)
- Hedera and Lightning chain providers; 24-chain registry
- Hedera MCP server (mirror node reads); Lightning tools on bitcoin-rpc-server (LND REST)
- Nine MCP installer templates across VS Code and JetBrains (Move, Bitcoin, TON, Substrate, Hedera)
- Architecture diagrams in `images/`

## 0.3.1

- Phase 3–4 chain providers (Move, Bitcoin, TON, Substrate) and 22-chain registry
- MCP flat templates for move, bitcoin, ton, substrate servers
- Updated coverage roadmap and EVM MCP docs to reflect implemented status
- Removed DE placeholder images and reference tree artifact

## 0.3.0

- Full MCP server implementations (8 servers, 30 tools) with schema parity validation
- Write guardrails (`SIMULATE_PASSED`, `HUMAN_CONFIRMED`) on broadcast tools
- Skill depth expansion (80–190 lines, decision frameworks, anti-patterns, checklists)
- Governance: VERSION, pre-commit, dependabot, provenance/SME review trail
- 11 templates, 16 tutorials, 3 runnable examples
- Blockchain-only hook_runner; removed DE case study artifacts
- evals + benchmarks in CI

## 0.2.0
- Phase 2 Alt-L1 chain providers (Solana, NEAR, Cosmos)
- MCP scaffolds for solana, near, cosmos RPC servers
- VS Code extension and JetBrains plugin installers
- Install scripts, bootstrap, hooks, Cursor rules
- Examples, starter packs, presets, tutorials
- GitHub Actions validate-and-package workflow

## 0.1.0

- Initial scaffold: 12 skills, guardrails, evm-rpc-server, AGENTS.md
