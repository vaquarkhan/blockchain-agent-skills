# Bitcoin UTXO & Lightning Patterns

Bitcoin layer-1 UTXO model and Lightning Network (LND) operations via `bitcoin-rpc-server`.

## MCP tools

| Tool | Backend | Purpose |
| --- | --- | --- |
| `getblockchaininfo` | Bitcoin Core JSON-RPC | Chain sync, best block, network |
| `getrawtransaction` | Bitcoin Core | UTXO proof / tx decode (with indexer) |
| `lightning_getinfo` | LND REST `/v1/getinfo` | Node identity, synced, block height |
| `lightning_decodepay` | LND REST `/v1/payreq/decode` | Parse BOLT11 invoice |

Env:

```bash
export BITCOIN_RPC_URL=http://user:pass@127.0.0.1:8332
export LND_REST_URL=https://127.0.0.1:8080
export LND_MACAROON=<hex-admin-or-invoice-macaroon>
```

## UTXO fundamentals

Bitcoin spends **outputs** (UTXOs), not account balances:

| Concept | Agent check |
| --- | --- |
| UTXO set | Sum of unspent outputs for wallet address |
| Confirmations | `transaction-safety.yaml` → 6 blocks for high value |
| Change output | Verify return to same wallet derivation path |
| Fee rate | sat/vB from mempool estimate (node `estimatesmartfee`) |

MCP read path: `getblockchaininfo` for tip height; `getrawtransaction` for tx structure.

```bash
# Validate Bitcoin RPC
curl -s $BITCOIN_RPC_URL -d '{"jsonrpc":"1.0","method":"getblockchaininfo","params":[]}'
```

## getblockchaininfo fields

| Field | Use |
| --- | --- |
| `blocks` | Current height for confirm-depth |
| `verificationprogress` | Must be ~1.0 for production |
| `chain` | `main`, `test`, `regtest` — gate mainnet writes |
| `initialblockdownload` | If true, pause high-value ops |

Failure: node syncing → LOW confidence; do not broadcast spends until synced.

## Lightning (LND)

### lightning_getinfo

Confirms:

- `synced_to_chain` / `synced_to_graph`
- `identity_pubkey` matches expected node
- `block_height` aligns with `getblockchaininfo`

### BOLT11 invoices — lightning_decodepay

Decode before pay (human confirm always for mainnet sends):

| Field | Verify |
| --- | --- |
| `num_satoshis` / `num_msat` | Matches intent |
| `description` | Phishing check |
| `expiry` | Not expired |
| `payment_addr` | MPP route safety |
| `destination` | Known counterparty |

MCP `lightning_decodepay` argument: `{ "pay_req": "lnbc..." }`

Never pay undecoded BOLT11 strings — `security.yaml` blind signing block applies.

## Simulate-first on Bitcoin

Bitcoin has no `eth_call` equivalent. Pre-broadcast checks:

1. `testmempoolaccept` on signed raw tx (Bitcoin Core 24+).
2. Decode with `decoderawtransaction` — outputs match plan.
3. Set `SIMULATE_PASSED=true` after accept.
4. Mainnet: `HUMAN_CONFIRMED=true`.

## Confirm depth

| Asset | Depth |
| --- | --- |
| BTC on-chain | 6 confirmations (high value) |
| Lightning | Instant with caveat — only if channel trusted; reconcile on-chain if force-close |

## Worked example (invoice review)

```bash
export LND_REST_URL=https://localhost:8080
export LND_MACAROON=0201036c6e64...
# 1. lightning_getinfo — synced_to_chain true
# 2. lightning_decodepay — lnbc1... amount 50k sats, expiry OK
# 3. Human confirms payee; HUMAN_CONFIRMED=true
# 4. Pay via LND CLI outside MCP; record preimage hash
```

## Failure modes

| Failure | Response |
| --- | --- |
| Invoice expired | Reissue; do not retry same hash |
| Mempool reject (non-standard) | Adjust fee / size |
| LND not synced | Wait; poll `lightning_getinfo` |
| Wrong network (testnet invoice) | Block mainnet pay |
| RBF double-spend attempt | Alert; follow incident runbook |

## Stacks / Liquid note

Registry maps extended Bitcoin-family chains to `bitcoin-rpc-server` where configured; validate RPC schema per network before production use.

## Authoritative sources

- [bitcoin-rpc-server/server.py](../mcp/bitcoin-rpc-server/server.py)
- [bitcoin-rpc.mcp.json](../mcp/bitcoin-rpc.mcp.json)
- [transaction-safety.yaml](../guardrails/transaction-safety.yaml)
- [BOLT #11 invoice format](https://github.com/lightning/bolts/blob/master/11-payment-encoding.md)
- [Bitcoin Core RPC docs](https://developer.bitcoin.org/reference/rpc/)

## Provenance

| Field | Value |
| --- | --- |
| Source document | `references/bitcoin-utxo-lightning-patterns.md` |
| Version / effective | 1.0 / 2026-06-13 |
| Last reviewed | 2026-06-13 |
| Reviewer | blockchain-agent-skills maintainers |
| Next review due | 2026-09-13 |
| Notes | BOLT11 decode mandatory before Lightning pay |
