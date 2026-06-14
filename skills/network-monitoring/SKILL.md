---
name: network-monitoring
description: Node health, mempool analysis, fork detection, reorg handling, and gas market tracking. Real-time alerts on network anomalies, validator set changes, and block production delays. Trigger when diagnosing network issues, tracking gas prices, or detecting forks/reorgs.
---

# Network Monitoring

## Overview

Monitoring dimensions:

- **Node health** — sync status, peer count, latency
- **Mempool** — pending tx count, gas price distribution
- **Fork detection** — competing blocks at same height
- **Reorg handling** — depth tracking, affected tx rollback
- **Gas market** — EIP-1559 base fee prediction, L2 calldata costs

## Core Process

### Step 1: Baseline metrics

```
eth_syncing, net_peerCount, eth_blockNumber
eth_feeHistory (EVM) / getRecentPrioritizationFees (Solana)
```

### Step 2: Anomaly detection

| Signal | Threshold | Action |
| --- | --- | --- |
| Block delay | >3x normal block time | Alert |
| Reorg depth | >0 confirmed blocks | Rewind affected ops |
| Base fee spike | >2x 24h median | Warn on pending txs |
| Validator miss | >1 epoch (ETH) | Alert validator-da-agent |

### Step 3: Gas market tracking

**EIP-1559 next-block base fee:**

```
nextBaseFee = baseFee * (1 + (gasUsed - target) / target / 8)
```

Priority fee: percentile from `eth_feeHistory` or mempool analysis.

## Verification

- [ ] Node sync status confirmed
- [ ] Gas estimates use fresh fee history
- [ ] Reorg events trigger state rewind where applicable
