# KMS Signing Patterns

Agents prepare **unsigned** transaction payloads. Signing happens in AWS KMS, GCP Cloud HSM, or enterprise HSM — never in chat, MCP env vars, or repository files.

## Core rules (`security.yaml`)

| Rule | Action |
| --- | --- |
| `private_key_protection` | BLOCK — never log/return keys or seed phrases |
| `blind_signing_block` | BLOCK — decode all params before sign |
| `key_storage` | Allowed: `aws_kms`, `hsm` only |
| Override | **none** for key exposure |

MCP broadcast tools explicitly state: *Never pass private keys through MCP.*

## Architecture pattern

```
Agent (plan/simulate) → Unsigned payload JSON
        ↓
KMS/HSM signer (isolated role) → Signed raw tx
        ↓
MCP broadcast tool (SIMULATE_PASSED + HUMAN_CONFIRMED) → network
```

Separate IAM roles:

- **Simulator** — read RPC, `eth_call`, no sign permission
- **Signer** — `kms:Sign` / HSM sign only on approved payload hash
- **Broadcaster** — `eth_sendRawTransaction` with pre-signed hex

## AWS KMS (EVM secp256k1)

Typical flow with EIP-155 typed transactions:

1. Build unsigned tx (chainId, nonce, gas, to, data, value).
2. Hash per chain signing algorithm (Keccak-256 for Ethereum).
3. Call `kms.sign` with `MessageType=DIGEST`, `SigningAlgorithm=ECDSA_SHA_256` (key spec dependent).
4. Normalize `(r, s)` to low-S; assemble signed tx RLP.
5. Pass hex to `eth_send_raw_transaction` — not the key ARN contents.

Environment (signer side only):

```bash
export AWS_REGION=us-east-1
export KMS_KEY_ID=alias/evm-mainnet-signer
# Never export AWS_SECRET_ACCESS_KEY into agent sessions
```

Failure modes:

- Wrong key spec (P-256 vs secp256k1) → invalid signature on chain
- Missing chainId in typed tx → replay across chains
- Signer role can sign arbitrary digests → enforce payload whitelist in Lambda

## GCP Cloud HSM

Use Cloud KMS with HSM protection level or Cloud HSM cluster for FIPS requirements:

```bash
gcloud kms keys versions list --key=evm-signer --keyring=blockchain --location=global
```

Sign digest via `gcloud kms asymmetric-sign` or application Default Credentials in isolated Cloud Function. Same separation: agent never sees PEM or PKCS#11 PIN.

## Solana / Ed25519 keys

Solana uses Ed25519 — use KMS keys with compatible curve or dedicated HSM partition. Agent calls `simulate_transaction`; signer produces signed wire transaction; MCP `send_transaction` receives base64/hex serialized tx only.

## NEAR / Cosmos / Move

- **NEAR**: Access keys on accounts; prefer limited-function-call keys; full-access keys only in HSM-backed cold path.
- **Cosmos**: Sign `TxRaw` with Ledger/KMS in offline module; broadcast `tx_bytes_base64` via `broadcast_tx`.
- **Move (Sui/Aptos)**: Sponsor or user sig via HSM; simulate before sign.

## Audit logging

Log (never secret material):

| Field | Example |
| --- | --- |
| Key ID / ARN | `arn:aws:kms:...:key/abc` |
| Policy version | `2026-06-01-v3` |
| Payload hash | `0x7f3a...` |
| Simulation run ID | `sim-20260613-001` |
| Signer principal | `role/evm-signer-prod` |

## Key rotation

1. Generate new KMS key; dual-sign period if multisig.
2. Update signer Lambda / CI reference.
3. **Re-simulate** pending txs — nonce and calldata may change.
4. Revoke old key `DisableKey` after confirm-depth on migration txs.

## Anti-patterns (blocked)

- Pasting `0x` private key or mnemonic into Cursor chat
- Storing `.env` with `PRIVATE_KEY=` in repo
- Passing seed phrase to MCP `env` block
- Agent invoking `personal_sign` with exported key

## Worked example

```bash
# Agent session (no secrets)
python scripts/hook_runner.py tx-simulate-pre
export SIMULATE_PASSED=true

# Signer job (isolated)
python scripts/sign-evm-kms.py --payload unsigned.json --key-id alias/prod-signer > signed.hex

# Broadcast
export HUMAN_CONFIRMED=true
# MCP eth_send_raw_transaction(raw_hex=signed.hex)
```

## Authoritative sources

- [security.yaml](../guardrails/security.yaml)
- [MCP guardrails](../mcp/_shared/guardrails.py)
- [evm-rpc-server README](../mcp/evm-rpc-server/README.md)
- [smart-contract-factory SKILL](../skills/smart-contract-factory/SKILL.md)
- [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/)
- [GCP Cloud HSM documentation](https://cloud.google.com/kms/docs/hsm)

## Provenance

| Field | Value |
| --- | --- |
| Source document | `references/kms-signing-patterns.md` |
| Version / effective | 1.0 / 2026-06-13 |
| Last reviewed | 2026-06-13 |
| Reviewer | blockchain-agent-skills maintainers |
| Next review due | 2026-09-13 |
| Notes | No override for `private_key_protection` per security.yaml |
