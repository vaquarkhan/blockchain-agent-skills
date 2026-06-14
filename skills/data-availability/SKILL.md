---
name: data-availability
description: Blob posting per EIP-4844 and DA layer integration — Celestia, EigenDA, Avail, Near DA, Polygon Avail. Calculates blob fees, monitors DA layer availability, routes DA submissions optimally. Trigger when posting blobs, integrating modular DA, or optimizing L2 data costs.
---

# Data Availability

## Overview

DA options:

| Layer | Mechanism |
| --- | --- |
| Ethereum EIP-4844 | KZG blob transactions (proto-danksharding) |
| Celestia | Namespace-separated DA, DAS sampling |
| EigenDA | Restaking-secured quorum DA |
| Avail | Kate commitments |
| Near DA | NEAR-native blob storage |

## Core Process

### Step 1: Calculate blob fees (EIP-4844)

```
blobBaseFee from beacon chain
target: 3 blobs/block
cost = blobBaseFee * numBlobs + execution gas
```

### Step 2: Route optimally

Compare cost and latency across DA layers for the workload (rollup batch vs standalone blob).

### Step 3: Post and monitor

1. Construct blob transaction with KZG commitment.
2. Broadcast via `transaction-lifecycle`.
3. Monitor blob inclusion and DA layer availability sampling.

## Verification

- [ ] Blob fee calculated from current base fee
- [ ] Blob included in beacon block
- [ ] DA layer availability confirmed
