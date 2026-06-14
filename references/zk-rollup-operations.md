# ZK & Rollup Operations

L2 rollup deposits, withdrawals, batch posting, and sequencer failure handling. Primary MCP: `evm-rpc-server` (L1 + L2 RPC). Skill: `rollup-operations`.

## Stack overview

| Stack | Type | Chains | Withdrawal finality |
| --- | --- | --- | --- |
| OP Stack | Optimistic | Optimism, Base, Arbitrum (Nitro) | ~7-day challenge window |
| ZK Stack | Validity proof | zkSync Era, Scroll, Starknet* | Minutes after L1 proof verify |

\*Starknet: native tooling partial — document EVM bridge paths separately.

## OP Stack operations

### L1 → L2 deposit

Contracts (examples):

- `OptimismPortal.depositTransaction(...)`
- `L1StandardBridge.depositERC20(...)`

Workflow:

1. Dual RPC: Ethereum L1 + target L2 in `ALCHEMY_ETH_URL` / L2 URL.
2. Simulate L1 via MCP `eth_call`.
3. KMS sign; `eth_send_raw_transaction` with `SIMULATE_PASSED=true`.
4. Monitor L2: `TransactionDeposited` / bridge events via `eth_get_logs`.
5. Confirm L2 balance — 12 L1 blocks for high-value credit.

### L2 → L1 withdrawal (optimistic)

1. Initiate burn on L2 bridge.
2. Record withdrawal hash — challenge period starts.
3. Track `OutputProposed` on `L2OutputOracle`.
4. After window: prove via fault proof system (`DisputeGameFactory`).
5. Finalize on L1 — **mandatory `HUMAN_CONFIRMED=true`**.

### Batch cost monitoring

Track sequencer economics:

| Metric | Source | Alert if |
| --- | --- | --- |
| L1 batch posting gas | L1 receipts (`eth_get_transaction_receipt`) | > budget per batch |
| Batch frequency | Sequencer address tx rate | Gap > SLA |
| Calldata / blob cost | EIP-4844 blob base fee | Spike vs 7d median |
| L2 gas price | L2 `eth_gasPrice` | Sustained > user cap |

Document batch cost in ops dashboard; tie to `network-monitoring` skill.

## ZK rollup operations

| Step | Action |
| --- | --- |
| L2 withdraw init | Burn on L2 |
| Proof generation | Prover submits validity proof to L1 |
| L1 verify | `eth_call` verify contract |
| Claim | L1 claim tx after proof accepted |

Withdrawal delay: minutes (proof latency), not 7 days — still require confirm-depth on L1 claim tx.

## Sequencer failure

When sequencer or batch poster stops:

### Detection

- L2 block time stalls (no new `eth_block_number` increment)
- Forced inclusion queue grows (OP Stack)
- Alert from `network-monitoring` — mempool depth anomaly

### Response playbook

| Severity | Action |
| --- | --- |
| Degraded | Switch to backup RPC; pause user withdrawals initiation |
| Halted | Engage `templates/incident-runbook.md`; status comms |
| Extended outage | Evaluate forced withdrawal / escape hatch (chain-specific) |

Never finalize L1 claims during ambiguous sequencer state without human review.

### OP Stack forced transaction path

Users may force-include via `OptimismPortal` after max sequencer downtime — simulate gas-heavy path; expect elevated batch cost when sequencer recovers.

## Monitoring checklist

- [ ] Sequencer uptime (block production rate)
- [ ] L1 batch poster balance and nonce
- [ ] `L2OutputOracle` latest output index vs L2 head
- [ ] ZK: proof submission latency and verifier gas
- [ ] Bridge TVL reconcile L1 escrow vs L2 minted supply

## MCP tool reference (rollup context)

| Tool | Use |
| --- | --- |
| `eth_call` | Simulate bridge deposit/withdraw/prove |
| `eth_get_logs` | Bridge events across L1/L2 |
| `eth_get_transaction_receipt` | Batch tx success |
| `eth_block_number` | Sequencer liveness |
| `eth_estimate_gas` | Batch and claim cost projection |

Env gates unchanged: `SIMULATE_PASSED`, `HUMAN_CONFIRMED` on mainnet high-value claims.

## Worked example (OP Stack deposit)

```bash
export ALCHEMY_ETH_URL=https://eth-mainnet.g.alchemy.com/v2/KEY
export ALCHEMY_BASE_URL=https://base-mainnet.g.alchemy.com/v2/KEY
# 1. eth_call depositTransaction on L1
# 2. SIMULATE_PASSED=true; KMS sign L1 tx
# 3. eth_get_logs — TransactionDeposited
# 4. eth_get_balance recipient on Base L2
# 5. confirm-depth: 12 L1 blocks before treasury marks received
```

## Failure modes

| Failure | Response |
| --- | --- |
| L2 credit delayed | Indexer lag; verify L1 deposit finality |
| Challenge period not elapsed | Block L1 finalize — calendar not optional |
| Invalid output root | Halt claims; incident severity 1 |
| Proof verifier revert | Decode revert; prover version mismatch |
| Sequencer censorship | Document forced tx path; legal/comms review |

## Authoritative sources

- [rollup-operations SKILL](../skills/rollup-operations/SKILL.md)
- [network-monitoring SKILL](../skills/network-monitoring/SKILL.md)
- [data-availability SKILL](../skills/data-availability/SKILL.md)
- [evm-rpc-server](../mcp/evm-rpc-server/)
- [OP Stack specs](https://specs.optimism.io/)
- [transaction-safety.yaml](../guardrails/transaction-safety.yaml)

## Provenance

| Field | Value |
| --- | --- |
| Source document | `references/zk-rollup-operations.md` |
| Version / effective | 1.0 / 2026-06-13 |
| Last reviewed | 2026-06-13 |
| Reviewer | blockchain-agent-skills maintainers |
| Next review due | 2026-09-13 |
| Notes | OP Stack batch cost + sequencer failure are standing monitor items |
