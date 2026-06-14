# NEAR Account Model Patterns

NEAR uses human-readable account names (not hex addresses). Tokens follow NEP standards. MCP access via `near-rpc-server`.

## MCP tools

| Tool | RPC method | Purpose |
| --- | --- | --- |
| `view_account` | `query` (account view) | Balance, storage usage, code hash |
| `query` | `query` (call_function) | View method calls (simulate read path) |
| `view_access_key` | `query` (access_key) | Nonce, allowance, method permissions |
| `send_tx` | `send_tx` | **Write** — guarded by simulate + mainnet confirm |

Env: `NEAR_RPC_URL`, `NEAR_NETWORK` (default `mainnet`).

## Account types

| Type | Pattern | Notes |
| --- | --- | --- |
| Named account | `alice.near`, `app.example.near` | 2–64 chars, `.near` or TLD |
| Implicit account | 64-char hex (deprecated for new) | Legacy ed25519-derived |
| Sub-account | `sub.parent.near` | Parent pays creation storage |

Always validate recipient format per `transaction-safety.yaml` → `destination_validation.near`.

## Access keys

| Key type | Capability |
| --- | --- |
| Full access | All actions — HSM only for production |
| Function-call | Restricted to contract + methods + allowance |

Before mainnet ops:

1. `view_access_key` — check nonce continuity (gap → alert).
2. Confirm allowance covers gas for batched calls.
3. Prefer limited keys for automated agents.

## NEP-141 (fungible token)

Metadata required before mainnet launch:

| Field | NEP-141 |
| --- | --- |
| `spec` | `ft-1.0.0` |
| `name`, `symbol`, `decimals` | On-chain or contract metadata |
| Storage | ~0.00125 NEAR per registration |

View patterns via MCP `query`:

```json
{
  "request_type": "call_function",
  "account_id": "token.example.near",
  "method_name": "ft_balance_of",
  "args_base64": "..."
}
```

Simulate state change: dry-run via local sandbox or `near-cli` view before `send_tx`.

## NEP-171 / NEP-177 (NFT)

- Check `nft_metadata` for royalty standard (NEP-199 where applicable).
- Verify approval management for marketplace integrations.

## Aurora bridge context

NEAR MCP server also routes Aurora (EVM-on-NEAR) context:

- Confirm L1/L2 gas on Aurora RPC when bridging.
- Finality: treat Aurora as EVM — `eth_call` on Aurora endpoint + NEAR `view_account` for bridge state.

## Chain signatures (cross-chain)

For multichain intents:

1. Plan intent hash and target chain.
2. Simulate on NEAR signing contract via `query` (view) where possible.
3. Full tx simulation before `send_tx`; set `SIMULATE_PASSED=true`.

## Worked example (NEP-141 transfer)

1. `view_account` on sender — sufficient NEAR for gas + storage deposit.
2. `query` — `ft_balance_of` sender ≥ amount.
3. Build `ft_transfer` args; simulate on testnet.
4. KMS sign `send_tx`; mainnet requires `HUMAN_CONFIRMED=true`.
5. Confirm receipt via transaction hash query; reconcile balances.

## Failure modes

| Symptom | Cause | Action |
| --- | --- | --- |
| `AccountDoesNotExist` | Typo in named account | Re-validate `.near` name |
| `InsufficientBalance` | Low NEAR for storage | Top up before token transfer |
| Nonce mismatch | Parallel sends | Serialize txs per access key |
| Simulation pass, send fail | Block hash expired | Rebuild tx with fresh hash |

## Authoritative sources

- [near-rpc-server/server.py](../mcp/near-rpc-server/server.py)
- [near-rpc.mcp.json](../mcp/near-rpc.mcp.json)
- [token-standards-engine SKILL](../skills/token-standards-engine/SKILL.md)
- [NEP-141 FT standard](https://nomicon.io/Standards/Tokens/FungibleToken/Core)
- [NEAR docs — accounts](https://docs.near.org/concepts/basics/accounts/account-id)

## Provenance

| Field | Value |
| --- | --- |
| Source document | `references/near-account-model-patterns.md` |
| Version / effective | 1.0 / 2026-06-13 |
| Last reviewed | 2026-06-13 |
| Reviewer | blockchain-agent-skills maintainers |
| Next review due | 2026-09-13 |
| Notes | NEP-141 metadata checklist for token launches |
