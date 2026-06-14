# Cosmos IBC Patterns

Inter-Blockchain Communication (IBC) transfers across Cosmos SDK chains. MCP: `cosmos-rpc-server`.

## MCP tools

| Tool | Purpose | Write? |
| --- | --- | --- |
| `query_client_state` | IBC client status on counterparty | read |
| `abci_query` | Generic module / store query | read |
| `ibc_transfer` | Build/validate transfer intent | guarded write path |
| `broadcast_tx` | Submit signed tx bytes | **write** |

Env: `COSMOS_RPC_URL`, `COSMOS_CHAIN_ID` (e.g. `cosmoshub-4`, `osmosis-1`).

## Pre-transfer verification

Before any IBC send, confirm:

| Check | How |
| --- | --- |
| Channel ID | Active channel on source (e.g. `channel-141`) |
| Port | Usually `transfer` (ICS-20) |
| Connection state | `OPEN` via `query_client_state` |
| Counterparty chain | Matches destination bech32 prefix (`cosmos`, `osmo`) |
| Denom trace | IBC hash → human denom on destination |

MCP `query_client_state` wraps light client verification — reject if client frozen or expired.

## Timeout parameters

IBC packets require timeout to prevent stuck funds:

| Field | Guidance |
| --- | --- |
| `timeout_height` | `{revision_number, revision_height}` — set above current + buffer |
| `timeout_timestamp` | Nanoseconds; use if height unreliable |
| Buffer | +500–2000 blocks for congested paths |

Document timeout in `templates/tx-plan.yaml` memo for audit.

Failure mode: timeout on destination → funds refunded on source after timeout period; reconcile both sides.

## Simulation

Cosmos SDK `/cosmos/tx/v1beta1/simulate` (or legacy `/txs/simulate`):

1. Build `MsgTransfer` with channel, port, amount, memo.
2. Simulate gas; fees in native denom (uatom, uosmo).
3. Set `SIMULATE_PASSED=true` before `broadcast_tx`.

Gas failure modes:

- Insufficient fee → raise gas price within chain minimum
- Channel closed → halt; open new channel path only after governance

## Memo and compliance

Include structured memo for travel-rule / internal audit:

```
memo: "ref:20260613-treasury-osmo|beneficiary:ops vault"
```

Screen destination bech32 against `compliance.yaml` OFAC lists — no override.

## Reconciliation after IBC transfer

After broadcast, reconcile **source** and **destination** at confirm depth:

### Source chain

1. Tx included in block; no `timeout` or `error` events.
2. Balance decreased by amount + fee.
3. `send_packet` event emitted with sequence number.

### Destination chain

1. Wait for IBC relay (minutes to hours depending on relayers).
2. Query recipient balance or `recv_packet` / `write_acknowledgement` events.
3. Confirm denom matches expected IBC trace (`ibc/HASH`).

### Reconciliation table

| Step | Source | Destination |
| --- | --- | --- |
| T+0 | Tx hash recorded | — |
| T+confirm | Balance −amount | Pending IBC |
| T+relay | Escrow updated | Balance +amount |
| Mismatch | Refund after timeout? | Alert relayer ops |

Use `abci_query` for bank balances; cross-check sequence in IBC events.

## Worked example (Cosmos Hub → Osmosis)

```bash
export COSMOS_RPC_URL=https://rpc.cosmos.network
export COSMOS_CHAIN_ID=cosmoshub-4
# 1. query_client_state — verify Osmosis client OPEN
# 2. Simulate MsgTransfer: 1000000 uatom, channel-141, receiver osmo1...
# 3. Sign offline; broadcast_tx with SIMULATE_PASSED=true
# 4. Switch COSMOS_RPC_URL to Osmosis; reconcile ibc/ denom credit
```

## Failure modes

| Failure | Response |
| --- | --- |
| Client expired | Governance update; pause transfers |
| Wrong channel ID | Funds stuck until timeout refund |
| Relayer down | Wait; monitor; do not double-send |
| Ack error | Parse error ack; refund path |

## Authoritative sources

- [cosmos-rpc-server/server.py](../mcp/cosmos-rpc-server/server.py)
- [cosmos-ibc-starter.yaml](../starter-packs/cosmos-ibc-starter.yaml)
- [chain-abstraction SKILL](../skills/chain-abstraction/SKILL.md)
- [IBC protocol specification](https://github.com/cosmos/ibc)
- [ICS-20 fungible token transfer](https://github.com/cosmos/ibc/blob/main/spec/app/ics-020-fungible-token-transfer/README.md)

## Provenance

| Field | Value |
| --- | --- |
| Source document | `references/cosmos-ibc-patterns.md` |
| Version / effective | 1.0 / 2026-06-13 |
| Last reviewed | 2026-06-13 |
| Reviewer | blockchain-agent-skills maintainers |
| Next review due | 2026-09-13 |
| Notes | Reconciliation procedure mandatory post-transfer |
