---
name: rollup-operations
description: L2 deposits and withdrawals, sequencer interaction, batch posting, fraud proofs (Optimistic), and validity proofs (ZK). Handles OP Stack (Arbitrum, Base, Optimism) and ZK Stack (zkSync, Starknet, Scroll). Trigger when bridging L1↔L2, claiming withdrawals, or monitoring challenge windows.
---

# Rollup Operations

## Overview

L2 rollup operations across optimistic and validity-proof stacks. All L1/L2 writes follow simulate-first lifecycle with **mandatory human confirmation** for withdrawal finalization, fraud proofs, and high-value bridges.

| Stack | Type | Chains | Withdrawal delay |
| --- | --- | --- | --- |
| OP Stack | Optimistic | Arbitrum, Base, Optimism | 7-day challenge window |
| ZK Stack | Validity proof | zkSync Era, Starknet, Scroll | Minutes (proof verified on L1) |

**Tier 1** OP Stack L2s on EVM: full deposit/withdraw via `evm-rpc-server` (L1 + L2 RPC). **Tier 3** Starknet/zkSync native paths: partial — document roadmap for non-EVM L2 tooling.

Guardrails: `transaction-safety.yaml` (simulate, value thresholds), `security.yaml` (blind signing on bridge calldata), `compliance.yaml` (audit trail, sanctions on L1/L2 addresses).

## When to Use

- Depositing assets L1 → L2 (ETH, ERC-20)
- Initiating and finalizing withdrawals L2 → L1
- Monitoring sequencer batch posting and L2OutputOracle roots
- Claiming withdrawals after challenge window (optimistic) or proof verification (ZK)
- Tracking bridge events across L1 and L2

Do **not** use for generic L1 transfers unrelated to bridges (use `transaction-lifecycle`).

## Core Process

### Step 1: Resolve L1 and L2 chains

1. Use `chain-abstraction` for both L1 (e.g., Ethereum chainId 1) and L2 (e.g., Arbitrum 42161).
2. Configure dual MCP endpoints on `evm-rpc-server` with correct chainId per call.
3. Record confirmation depths: L2 fast finality for UX; L1 finality for high-value claims.

### Step 2: L1 → L2 deposit

**OP Stack:**

```
OptimismPortal.depositTransaction(to, value, gasLimit, isCreation, data)
L1StandardBridge.depositERC20(l1Token, l2Token, amount, minGasLimit, extraData)
```

1. Simulate on L1 via `eth_call`.
2. Sign via KMS; broadcast on L1 via `eth_sendRawTransaction`.
3. Monitor L2 execution via bridge event (`TransactionDeposited`, `ERC20DepositInitiated`).
4. Confirm L2 balance via `block-state-queries` on L2 RPC.

### Step 3: L2 → L1 withdrawal

**Optimistic rollup:**

1. Initiate withdrawal on L2 (burn/migrate via L2 bridge contract).
2. Record withdrawal hash and timestamp — **7-day challenge period** starts.
3. Track `OutputProposed` events on L2OutputOracle.
4. After challenge window: prove via `DisputeGameFactory` / fault proof system.
5. Finalize and claim on L1 — **requires human confirmation**.

**ZK rollup:**

1. Initiate withdrawal on L2.
2. Wait for validity proof batch posted on L1.
3. Claim on L1 after proof verification (minutes, not days).

### Step 4: Batch monitoring

Track:

- Sequencer batch posting frequency
- L2OutputOracle roots (OP Stack)
- Proof submission cadence (ZK Stack)
- Sequencer downtime → alert via `network-monitoring`

### Step 5: Confirm depth

- L1 deposit: wait 12 Ethereum blocks before treating L2 credit as final for high value.
- L1 claim: wait 12 blocks after finalize tx.
- L2 ops: 20 blocks on Arbitrum/Base for operational finality.

## Decision framework

1. **Deposit or withdrawal?** → Deposit: L1 tx first. Withdrawal: L2 initiate → wait → L1 claim.
2. **Optimistic or ZK stack?** → Optimistic: 7-day wait + prove. ZK: proof polling + claim.
3. **ETH or ERC-20?** → ETH: OptimismPortal. ERC-20: L1StandardBridge with correct L1/L2 token pair.
4. **High value (>$10k)?** → `/confirm` at deposit, initiate, and claim steps.
5. **Withdrawal ready to finalize?** → Verify challenge window elapsed (OP) or proof submitted (ZK) before L1 claim.
6. **Native bridge vs third-party?** → Prefer canonical bridge; third-party requires extra security checks.

| Stack | Initiate | Wait | Finalize |
| --- | --- | --- | --- |
| OP (Arbitrum) | L2 → L1 tx on L2 | 7 days | Prove + claim on L1 |
| ZK (zkSync) | L2 withdraw | Proof batch | Claim on L1 |
| Deposit (Base) | L1 deposit tx | ~minutes | L2 balance check |

## Anti-patterns and rationalizations

| Rationalization | Risk | Required response |
| --- | --- | --- |
| "Claim withdrawal before challenge window ends" | Failed claim, lost gas | Verify 7-day elapsed on OP Stack |
| "Use wrong L2 token address for bridge" | Bricked deposit | Verify L1/L2 token mapping from official docs |
| "L2 balance updated — skip L1 confirm-depth" | Reorg on L1 deposit | Confirm L1 tx finality for high value |
| "Third-party bridge — skip simulate" | Bridge exploit, fund loss | Simulate; verify contract on both chains |
| "Finalize claim without human confirm" | Irreversible high-value L1 tx | Require `/confirm` for all finalize steps |
| "Single RPC for L1 and L2" | Wrong chainId replay | Separate chainId per MCP call |
| "Mark withdrawal complete at initiate" | 7-day wait not tracked | Track state machine; set calendar alert |

## Verification

- [ ] L1 and L2 chains resolved with correct chainIds via `chain-abstraction`
- [ ] Deposit simulated on L1 before broadcast (`eth_call`)
- [ ] L1 deposit tx confirmed; L2 bridge event observed
- [ ] L2 balance delta verified via `block-state-queries`
- [ ] Withdrawal initiate tx confirmed on L2 with hash recorded
- [ ] Challenge window tracked for OP Stack (7 days from initiate)
- [ ] Validity proof verified on L1 for ZK Stack before claim
- [ ] Human confirmation obtained for finalize/claim steps
- [ ] L1 claim tx simulated and broadcast via KMS signing
- [ ] Confirmation depth reached on L1 (12 blocks) post-claim
- [ ] Sanctions screening on L1 and L2 counterparties
- [ ] Audit trail logged with bridge tx hashes and timestamps per `compliance.yaml`
