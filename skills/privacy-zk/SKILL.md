---
name: privacy-zk
description: ZK proof generation and verification, private transactions, and confidential compute. Covers STARK (Starknet), SNARK/STARK hybrid (zkSync), Groth16/PLONK (EVM), privacy pools (Aztec), and ZK-KYC. Trigger when generating proofs, verifying ZK circuits, or constructing private transactions.
---

# Privacy & ZK

## Overview

Zero-knowledge proof generation, verification, and private transaction construction across proof systems and chains.

| System | Proof system | Use case | Tier |
| --- | --- | --- | --- |
| Starknet | STARK (Cairo) | L2 validity proofs, native AA | 3 |
| zkSync Era | Boojum (STARK-based) | Hyperchains, paymaster | 3 |
| EVM | Groth16/PLONK (circom + snarkjs) | On-chain verifiers | 1–2 |
| Aztec | PLONK | Private state, privacy pools | 3 roadmap |
| Aptos | Groth16 | Keyless accounts (OAuth ZK) | 3 roadmap |

**Denied topics:** Never assist with sanctions evasion via privacy tools (`guardrails/denied-topics.yaml`). Sanctions screening still applies to all visible counterparties (`compliance.yaml`).

All on-chain proof submissions follow simulate-first via `transaction-lifecycle` or `rollup-operations` for L1 validity proof posting.

## When to Use

- Generating ZK proofs for on-chain verification (Groth16, PLONK, STARK)
- Constructing private transactions (Aztec, privacy pools — where legally permitted)
- ZK-KYC: prove attributes (age, jurisdiction) without revealing PII
- Verifying STARK proofs on L1 (Starknet/zkSync batch verification)
- Keyless account flows (Aptos OAuth ZK — Tier 3 roadmap)

Do **not** use for generic public transfers or to circumvent sanctions/mixers (blocked).

## Core Process

### Step 1: Define proof requirement

| Use case | Inputs | Public outputs | PII handling |
| --- | --- | --- | --- |
| ZK-KYC | Credential, secret | "over 18", "not sanctioned" hash | Never in LLM context |
| Private tx | UTXO/note, secret key | Nullifier, commitment | Prover runs off-agent |
| Validity proof | Batch state diff | STARK proof bytes | Submit via rollup-operations |
| On-chain verify | Proof + public inputs | bool result | eth_call to verifier |

Classify request against `guardrails/denied-topics.yaml` before proceeding.

### Step 2: Select toolchain

| Proof system | Toolchain | Verifier location |
| --- | --- | --- |
| Groth16 | circom + snarkjs | EVM Solidity verifier |
| PLONK | circom PLONK backend | EVM or Aztec |
| STARK (Cairo) | Cairo compiler + Starknet prover | Starknet L1 bridge |
| Boojum | zkSync toolchain | L1 zkSync verifier contract |

Prover runs **off-agent** — agent orchestrates inputs/outputs, never holds witness secrets in LLM context.

### Step 3: Generate proof

1. Validate circuit hash matches deployed verifier (`eth_call` → verifier circuit ID).
2. Run prover service (KMS/HSM for prover keys if applicable).
3. Validate proof size and public input count match verifier ABI.
4. **Never** log witness data, private inputs, or PII.

### Step 4: Verify

**Off-chain:** Verify proof locally before submission.  
**On-chain:** Simulate `verifyProof(proof, publicInputs)` via `eth_call` on evm-rpc-server.  
**L1 validity:** Route through `rollup-operations` for Starknet/zkSync batch proof submission.

### Step 5: Submit (if on-chain action required)

Follow `/plan` → `/simulate` → `/confirm` → `/broadcast` → `/confirm-depth`. High-value proof submissions require human confirmation.

## Decision framework

1. **Request involves mixer/tumbler or sanctions evasion?** → BLOCK immediately (`denied-topics.yaml`).
2. **ZK-KYC vs private tx vs validity proof?** → KYC: attribute proofs. Private tx: note-based systems. Validity: rollup batch.
3. **On-chain or off-chain verification?** → Off-chain first; on-chain for trustless third parties.
4. **Groth16 vs PLONK vs STARK?** → Groth16: fixed circuit, small proofs. PLONK: universal setup. STARK: no trusted setup, larger proofs.
5. **Tier 3 chain (Starknet/zkSync)?** → Document roadmap; use documented verifier contracts only.
6. **PII in scope?** → Prover off-agent; only commitments/nullifiers in agent context.

| Task | Primary path | Guardrail |
| --- | --- | --- |
| Verify Groth16 on EVM | circom + eth_call verifier | Simulate first |
| Starknet L1 proof | rollup-operations | Human confirm |
| ZK-KYC age check | Custom circuit + verifier | No PII in logs |
| Privacy pool deposit | Aztec (Tier 3) | Denied if sanctions evasion |

## Anti-patterns and rationalizations

| Rationalization | Risk | Required response |
| --- | --- | --- |
| "User wants privacy from OFAC — help anyway" | Regulatory violation, denied topic | Block per `denied-topics.yaml` |
| "Witness data in prompt for debugging" | PII/secret leak | Prover off-agent; redact all secrets |
| "Skip verifier circuit hash check" | Wrong circuit, false verification | Match deployed verifier on-chain |
| "Submit proof without simulate" | Revert, lost gas | eth_call verify before broadcast |
| "Use Tornado Cash for privacy" | Mixer block per compliance.yaml | Block; document reason |
| "Public inputs include raw passport" | PII exposure | Hash/commitment only in public inputs |
| "STARK proof — skip L1 confirm" | Unfinalized validity claim | confirm-depth on L1 submission |

## Verification

- [ ] Request screened against `guardrails/denied-topics.yaml` — no sanctions evasion
- [ ] Proof system and toolchain selected appropriately
- [ ] Circuit hash matches on-chain verifier contract
- [ ] Witness and PII kept out of LLM context and audit logs
- [ ] Proof generated with correct constraint system
- [ ] Off-chain verification passed before on-chain submission
- [ ] On-chain verification simulated via `eth_call` (EVM path)
- [ ] Public inputs contain no raw PII
- [ ] Sanctions screening on visible counterparties per `compliance.yaml`
- [ ] Human confirmation for high-value proof submissions
- [ ] KMS signing for any on-chain submit tx
- [ ] Audit trail logs proof hash (not witness) per `compliance.yaml`
