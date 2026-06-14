---
name: privacy-zk
description: ZK proof generation and verification, private transactions, and confidential compute. Covers STARK (Starknet), SNARK/STARK hybrid (zkSync), Groth16/PLONK (EVM), privacy pools (Aztec), and ZK-KYC. Trigger when generating proofs, verifying ZK circuits, or constructing private transactions.
---

# Privacy & ZK

## Overview

ZK stack by chain:

| System | Proof system | Use case |
| --- | --- | --- |
| Starknet | STARK (Cairo) | L2 validity proofs, native AA |
| zkSync Era | Boojum (STARK-based) | Hyperchains, paymaster |
| EVM | Groth16/PLONK (circom + snarkjs) | On-chain verifiers |
| Aztec | PLONK | Private state, privacy pools |
| Aptos | Groth16 | Keyless accounts (OAuth ZK) |

## Core Process

### Step 1: Define proof requirement

- **ZK-KYC**: prove attribute (age >18, not sanctioned) without revealing PII
- **Private tx**: Aztec/private pool deposit/withdraw
- **Validity proof**: verify STARK proof on L1 (Starknet/zkSync batch)

### Step 2: Generate proof

Use chain-appropriate toolchain:

- circom + snarkjs → Groth16/PLONK for EVM verifiers
- Cairo → Starknet prover
- Boojum → zkSync batch proofs

### Step 3: Verify

On-chain verifier contract or L1 proof submission via `rollup-operations`.

## Denied

Never assist with sanctions evasion via privacy tools (see `guardrails/denied-topics.yaml`).

## Verification

- [ ] Proof generated with correct circuit/constraint system
- [ ] On-chain verification passes
- [ ] No PII leaked in proof public inputs
