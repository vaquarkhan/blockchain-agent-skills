# Security

Report security issues privately via GitHub Security Advisories or repository issues (mark sensitive details carefully).

## Policy

- Never commit private keys, mnemonics, or API secrets
- Guardrails in `guardrails/` are mandatory for production agents
- Denied topics in `guardrails/denied-topics.yaml` must not be bypassed

## Agent constraints

- KMS/HSM signing only
- OFAC sanctions screening with no override
- Simulate-first on all mainnet writes
