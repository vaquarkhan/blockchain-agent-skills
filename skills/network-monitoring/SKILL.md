---
name: network-monitoring
description: Node health, mempool analysis, fork detection, reorg handling, and gas market tracking. Real-time alerts on network anomalies, validator set changes, and block production delays. Trigger when diagnosing network issues, tracking gas prices, or detecting forks/reorgs.
---

# Network Monitoring

## Overview

Real-time and historical network health monitoring across supported chains. Read-only skill — alerts may trigger downstream writes via `transaction-lifecycle` or `consensus-validator-ops`, but monitoring itself does not broadcast.

Monitoring dimensions:

- **Node health** — sync status, peer count, latency, block lag
- **Mempool** — pending tx count, gas price distribution, congestion
- **Fork detection** — competing blocks at same height
- **Reorg handling** — depth tracking, affected tx/event rollback
- **Gas market** — EIP-1559 base fee prediction, L2 calldata costs, Solana priority fees

**Tier 1** EVM: full via evm-rpc-server (`eth_syncing`, `eth_feeHistory`, `net_peerCount`). **Tier 2** Solana/NEAR/Cosmos: chain-specific health RPCs. **Tier 3–4**: partial — document coverage gaps.

Integrates with `consensus-validator-ops` for validator miss alerts and `event-indexing` for reorg rewind triggers.

## When to Use

- Diagnosing network issues (stalled blocks, sync lag, RPC failures)
- Tracking gas prices before `transaction-lifecycle` fee setting
- Detecting forks and reorgs affecting indexed events or pending ops
- Monitoring validator performance (missed slots, attestation delays)
- Mempool congestion analysis for tx timing

Do **not** use as primary skill for sending transactions or validator configuration changes.

## Core Process

### Step 1: Baseline metrics

Resolve chain via `chain-abstraction`; query health endpoints:

**EVM (evm-rpc-server):**

```
eth_syncing          → false = synced; object = syncing with current/ highest block
net_peerCount        → peer count (alert if <3)
eth_blockNumber      → compare against public reference block explorer
eth_feeHistory(blocks, rewardPercentiles) → base fee trend + priority fee percentiles
txpool_status        → pending/queued counts (if supported)
```

**Solana (solana-rpc-server):**

```
getHealth            → ok / behind / unknown
getSlot              → compare against cluster reference
getRecentPrioritizationFees → priority fee market
```

**NEAR / Cosmos:** sync info via status endpoint; block height vs reference.

Apply rate limits per `compliance.yaml`: EVM 100 req/s with exponential backoff on 429.

### Step 2: Anomaly detection

| Signal | Threshold | Action |
| --- | --- | --- |
| Block delay | >3× normal block time | Alert; downgrade confidence to LOW |
| Sync lag | >10 blocks behind reference | Alert; switch RPC fallback via chain-abstraction |
| Reorg depth | >0 confirmed blocks affected | Trigger event-indexing rewind; alert transaction-lifecycle |
| Base fee spike | >2× 24h median | Warn pending txs; suggest fee bump |
| Validator miss | >1 epoch (ETH) | Alert consensus-validator-ops |
| Peer count | <3 peers | Alert; rotate RPC endpoint |
| Mempool backlog | >10× normal pending | Warn; delay non-urgent broadcasts |

### Step 3: Gas market tracking

**EIP-1559 next-block base fee estimate:**

```
nextBaseFee = baseFee * (1 + (gasUsed - target) / target / 8)
target = 15M gas (Ethereum)
```

Priority fee: 50th–75th percentile from `eth_feeHistory` or mempool analysis. Pass estimates to `transaction-lifecycle` for `maxFeePerGas` / `maxPriorityFeePerGas`.

**Solana:** `getRecentPrioritizationFees` → median + 75th percentile for priority fee.

**L2:** Track L1 base fee separately for batch posting (`data-availability`).

### Step 4: Fork and reorg handling

1. Detect competing blocks at same height via block hash mismatch across RPCs.
2. Track reorg depth; if confirmed txs affected, notify downstream skills.
3. Apply `transaction-safety.yaml` → `reorg_protection` confirmation depths before marking ops final.
4. Trigger `event-indexing` cursor rewind for affected block range.

### Step 5: Alerting and audit

Emit alerts: SNS, webhook, or DynamoDB stream. Log monitoring snapshot with timestamp, chain, metrics, confidence score.

## Decision framework

1. **Pre-tx gas check?** → Query feeHistory; pass to transaction-lifecycle before `/simulate`.
2. **RPC returning stale blocks?** → Compare 2+ endpoints; rotate fallback; MEDIUM confidence.
3. **Reorg detected?** → Quantify depth; rewind event-indexing; hold confirm-depth on affected txs.
4. **Validator misses?** → Route alert to consensus-validator-ops; do not auto-modify validator config.
5. **Network congested?** → Recommend fee bump or delay; warn on >$10k txs during spike.
6. **Tier 3–4 chain monitoring?** → Document limited metrics; LOW confidence.

| Scenario | Key metric | Downstream action |
| --- | --- | --- |
| Stuck pending EVM tx | txpool + base fee | transaction-lifecycle replace |
| Subgraph reorg | block hash mismatch | event-indexing rewind |
| Pre-bridge deposit | L1 block production | rollup-operations delay |
| Validator miss epoch | attestation rate | consensus-validator-ops alert |

## Anti-patterns and rationalizations

| Rationalization | Risk | Required response |
| --- | --- | --- |
| "Single RPC source — skip cross-check" | Stale state, missed reorg | Compare against reference explorer |
| "Ignore 2-block reorg" | Wrong finality assumptions | Rewind affected indexers; alert |
| "Gas estimate from 1-hour-old data" | Stuck tx during spike | Fresh feeHistory within 5 minutes |
| "Syncing node OK for production reads" | Incomplete state | Require `eth_syncing: false` for HIGH confidence |
| "No alert on validator miss" | Silent slashing risk | Alert consensus-validator-ops after 1 epoch |
| "Poll mempool every 100ms" | Rate limit ban | Respect compliance.yaml limits |
| "Mark network healthy without peer check" | Partition risk | Include peerCount in health snapshot |

## Verification

- [ ] Chain resolved via `chain-abstraction` with correct MCP server
- [ ] Sync status confirmed (`eth_syncing: false` or equivalent)
- [ ] Block height cross-checked against public reference
- [ ] Peer count above minimum threshold (≥3)
- [ ] Gas estimates from fresh feeHistory (within 5 minutes)
- [ ] Anomaly thresholds applied; alerts emitted for breaches
- [ ] Reorg detection active; depth quantified if detected
- [ ] Event-indexing rewind triggered for affected reorg range (if applicable)
- [ ] Rate limits respected per `compliance.yaml`
- [ ] Confidence score assigned based on RPC health and sync status
- [ ] Monitoring snapshot logged with timestamp and metrics
- [ ] Downstream skills notified (transaction-lifecycle, consensus-validator-ops) when relevant
