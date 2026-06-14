# KMS Signing Setup

- Agents prepare unsigned payloads and simulation evidence only.
- Signing happens in AWS KMS, Cloud HSM, or equivalent — outside LLM context.
- Log key IDs and payload hashes in your audit trail.
- See `references/kms-signing-patterns.md` and `guardrails/security.yaml`.
