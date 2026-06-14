---
name: data-availability
description: Blob posting per EIP-4844 and DA layer integration — Celestia, EigenDA, Avail, Near DA, Polygon Avail. Calculates blob fees, monitors DA layer availability, routes DA submissions optimally. Trigger when posting blobs, integrating modular DA, or optimizing L2 data costs.
---

# Data Availability

## Overview

Data availability (DA) layer operations for rollup batch posting, EIP-4844 blob transactions, and modular DA integrations.

| Layer | Mechanism | Tier |
| --- | --- | --- |
| Ethereum EIP-4844 | KZG blob transactions (proto-danksharding) | 1 |
| Celestia | Namespace-separated DA, DAS sampling | 2 |
| EigenDA | Restaking-secured quorum DA | 3 roadmap |
| Avail | Kate commitments | 3 roadmap |
| Near DA | NEAR-native blob storage | 2 |

All blob posts route through `transaction-lifecycle` with simulate-first. Blob txs on Ethereum require type-3 (EIP-4844) transaction encoding and KZG commitments.

Guardrails: `transaction-safety.yaml` (gas limit 10x cap, simulate), `compliance.yaml` (audit trail), `security.yaml` (KMS signing).

## When to Use

- Posting EIP-4844 blobs on Ethereum for L2 batch data
- Integrating Celestia or Near DA for modular rollup data
- Calculating blob fee economics vs calldata posting
- Monitoring DA layer availability and sampling status
- Optimizing L2 data costs across DA options

Do **not** use for generic L1 transfers (use `transaction-lifecycle`) or rollup bridge ops (use `rollup-operations`).

## Core Process

### Step 1: Calculate blob fees (EIP-4844)

```
blobBaseFee = from beacon chain / execution payload
target = 3 blobs/block (EIP-4844 target)
max = 6 blobs/block
cost = blobBaseFee * numBlobs + execution_gas_cost
```

Compare against calldata cost: if `blobBaseFee * numBlobs < calldata_gas * baseFee`, prefer blobs.

Fetch current `blobBaseFee` via execution layer RPC or beacon API before `/plan`.

### Step 2: Route optimally

| Workload | Preferred DA | Rationale |
| --- | --- | --- |
| Ethereum L2 batch (OP Stack) | EIP-4844 blobs | Native, lowest latency to L1 |
| Sovereign rollup | Celestia namespace | Decoupled DA cost |
| Restaking-secured quorum | EigenDA (Tier 3) | Roadmap — document gap |
| NEAR ecosystem batch | Near DA | Tier 2 via near-rpc-server |

Document cost/latency tradeoff in plan artifact; assign confidence based on fee data freshness.

### Step 3: Construct blob transaction

1. Generate KZG commitment and proof for blob data (client-side or prover service — never expose secrets in LLM).
2. Build type-3 tx: `maxFeePerBlobGas`, `blobVersionedHashes`, execution payload.
3. Simulate via `eth_call` / blob-capable simulation on evm-rpc-server.
4. Validate gas limit ≤10x estimate per `transaction-safety.yaml`.

### Step 4: Post and monitor

1. Sign via KMS; broadcast via `eth_sendRawTransaction` (type-3).
2. Monitor blob inclusion in beacon block (slot confirmation).
3. For Celestia: submit via `cosmos-rpc-server` namespace tx; monitor DAS sampling.
4. Confirm DA layer availability — blob retrievable at declared height.

### Step 5: Confirm depth

Ethereum blob inclusion: wait 12 blocks for operational finality; 32 slots for high-value batch attestation.

## Decision framework

1. **Ethereum L2 operator vs external DA?** → Native L2 on ETH: EIP-4844. Sovereign: Celestia/EigenDA.
2. **Data size <128 KB?** → Single blob. Larger: multi-blob tx (max 6) or split batches.
3. **blobBaseFee spiking?** → Compare calldata fallback; defer batch if non-urgent.
4. **Celestia namespace available?** → Tier 2 via cosmos-rpc-server; verify namespace ID registered.
5. **Tier 3 DA (EigenDA/Avail)?** → State roadmap; do not post without documented MCP path.

| Scenario | DA layer | MCP / tool |
| --- | --- | --- |
| OP Stack batch on ETH | EIP-4844 | evm-rpc-server type-3 tx |
| Celestia rollup batch | Celestia namespace | cosmos-rpc-server |
| Fee comparison only | Read-only | beacon + execution RPC |
| Near DA storage | Near DA | near-rpc-server (Tier 2) |

## Anti-patterns and rationalizations

| Rationalization | Risk | Required response |
| --- | --- | --- |
| "Post blob without checking blobBaseFee" | 10x cost overrun | Fetch current fee; include in `/plan` |
| "Use calldata when blobs cheaper" | Unnecessary L2 operator cost | Run cost comparison; prefer blobs when cheaper |
| "Skip KZG proof validation" | Blob rejection, failed inclusion | Validate commitment/proof before broadcast |
| "Type-2 tx with blob sidecar" | Invalid tx format | Use type-3 EIP-4844 encoding |
| "Mark posted after broadcast" | Blob not included in block | Verify beacon inclusion |
| "EigenDA without Tier 3 adapter" | Undefined integration | State roadmap gap; block post |
| "Blob data in LLM context" | Data leak, oversized context | Reference hash/commitment only |

## Verification

- [ ] blobBaseFee fetched from fresh beacon/execution data
- [ ] Cost comparison documented: blobs vs calldata
- [ ] KZG commitment and versioned hashes constructed correctly
- [ ] Type-3 transaction simulated before broadcast
- [ ] Gas and blob gas limits within 10x estimate
- [ ] KMS signing used; no private key in context
- [ ] Blob inclusion confirmed in beacon block
- [ ] DA data retrievable at declared height (sampling pass)
- [ ] Confirmation depth reached (12 ETH blocks minimum)
- [ ] Celestia namespace verified if using modular DA
- [ ] Tier 3 limitations documented if EigenDA/Avail requested
- [ ] Audit trail logged per `compliance.yaml`
