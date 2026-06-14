# GitHub Copilot Instructions — Blockchain Agent Skills

Read `AGENTS.md` and `skills-index.md` before blockchain operations.

## Mandatory

1. Load `using-blockchain-agent-skills` for routing
2. Simulate before broadcast
3. Apply guardrails from `guardrails/`
4. Sign via KMS — never handle raw private keys

## Skill routing

| Task | Skill |
| --- | --- |
| Chain selection | chain-abstraction |
| Send transaction | transaction-lifecycle |
| Read state | block-state-queries |
| Deploy contract | smart-contract-factory |
| Token ops | token-standards-engine |

Full catalog: `skills-index.md`
