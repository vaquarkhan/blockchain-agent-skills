---
name: rollup-operations
description: L2 deposits and withdrawals, sequencer interaction, batch posting, fraud proofs (Optimistic), and validity proofs (ZK). Handles OP Stack (Arbitrum, Base, Optimism) and ZK Stack (zkSync, Starknet, Scroll). Trigger when bridging L1↔L2, claiming withdrawals, or monitoring challenge windows.
---

# Rollup Operations

## Overview

Rollup families:

| Stack | Type | Withdrawal delay |
| --- | --- | --- |
| OP Stack (Arbitrum, Base, Optimism) | Optimistic | 7-day challenge window |
| ZK Stack (zkSync, Starknet, Scroll) | Validity proof | Minutes (proof verified) |

## Core Process

### Step 1: L1 → L2 deposit

**OP Stack:**

```
OptimismPortal.depositTransaction() or L1StandardBridge.depositERC20()
```

Simulate, sign, broadcast on L1. Monitor L2 execution via bridge event.

### Step 2: L2 → L1 withdrawal

**Optimistic:**

1. Initiate withdrawal on L2 (burn/migrate).
2. Wait 7-day challenge period.
3. Prove via `DisputeGameFactory` / fault proof system.
4. Finalize and claim on L1.

**ZK:**

1. Initiate withdrawal on L2.
2. Wait for validity proof batch on L1.
3. Claim immediately after proof verification.

### Step 3: Batch monitoring

Track sequencer batch posting, L2OutputOracle roots (OP), and proof submission (ZK).

## Human confirmation

All withdrawal finalization and fraud proof interactions require human confirmation.

## Verification

- [ ] Deposit confirmed on L2 via bridge event
- [ ] Withdrawal challenge window tracked (optimistic)
- [ ] Proof verified on L1 (ZK)
- [ ] Human confirmation for finalize/claim steps
