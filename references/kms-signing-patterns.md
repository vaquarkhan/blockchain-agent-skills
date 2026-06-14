# KMS Signing Patterns

- Use cloud KMS or HSM; agents prepare unsigned payloads only.
- Separate signing roles from simulation and broadcast agents.
- Log key IDs and policy version, never key material.
- Rotate keys on compromise; replay simulation after rotation.
