# Hedera HTS Patterns

Hedera Hashgraph account model, Mirror Node queries, and Hedera Token Service (HTS). MCP: `hedera-rpc-server`.

## MCP tools

| Tool | Mirror REST | Purpose |
| --- | --- | --- |
| `get_account` | `GET /api/v1/accounts/{id}` | Balance, keys, token associations |
| `get_block` | `GET /api/v1/blocks/{number}` | Block records, timestamps |

Env:

```bash
export HEDERA_MIRROR_URL=https://mainnet-public.mirrornode.hedera.com
```

Validate: `python scripts/validate-mcp-servers.py`

## Account ID format (0.0.x)

Hedera uses shard.realm.num numeric IDs — not hex:

| Form | Example |
| --- | --- |
| Account | `0.0.12345` |
| Token | `0.0.98765` |
| Topic | `0.0.555` |

Always validate three-part numeric format before transfers. EVM alias `0.0.12345-abcdef` maps to same entity — cross-check in mirror.

MCP `get_account` argument:

```json
{ "account_id": "0.0.12345" }
```

Returns: `balance` (tinybars), `key` structure, `account` memo, associated tokens.

## Hedera Token Service (HTS)

Tokens are entities, not contracts (though HTS has EVM mirror):

| Operation | Notes |
| --- | --- |
| Token create | Supply key, admin key, freeze, wipe — document in plan |
| Associate | Account must associate before receiving token |
| Transfer | `CryptoTransfer` — fees in HBAR |
| Mint/Burn | Requires supply key in KMS/HSM |

### Pre-transfer checklist

1. `get_account` — sender HBAR for fees.
2. Confirm recipient **associated** with token ID (`0.0.TOKEN`).
3. Simulate via SDK `preview` or testnet mirror replay.
4. Mainnet: `HUMAN_CONFIRMED=true` if value > threshold.

## Keys and signing

- ED25519 / ECDSA keys on accounts — store in HSM; never in agent chat.
- `security.yaml` → private key protection applies without override.
- Multi-sig (`KeyList`, `ThresholdKey`) — decode full key structure before sign.

## Mirror vs consensus node

| Layer | Role |
| --- | --- |
| Mirror Node | Read-only REST (MCP tools) |
| Consensus node | Submit transactions (outside MCP) |

Agents plan with mirror; sign/broadcast via Hedera SDK + KMS.

## Fees

- HBAR denominated in tinybars (1 HBAR = 10^8 tinybars).
- HTS transfers consume crypto transfer plus token custom fees if configured.
- Query `get_account` after tx for balance reconciliation.

## Worked example (HTS transfer planning)

```bash
export HEDERA_MIRROR_URL=https://mainnet-public.mirrornode.hedera.com
# 1. get_account 0.0.SENDER — HBAR + token 0.0.USDC association
# 2. get_account 0.0.RECEIVER — associated with 0.0.USDC
# 3. Build CryptoTransfer; simulate on testnet
# 4. SIMULATE_PASSED=true; KMS sign; submit via SDK
# 5. get_account both sides — reconcile balances
```

## Failure modes

| Error | Cause | Action |
| --- | --- | --- |
| `TOKEN_NOT_ASSOCIATED_TO_ACCOUNT` | Missing association | Associate first |
| `INSUFFICIENT_PAYER_BALANCE` | Low HBAR | Top up payer |
| Invalid `0.0.x` format | Typo | Re-validate ID |
| Mirror lag | Indexing delay | Wait; compare record timestamps |

## EVM on Hedera

Smart contracts use `0.0.x` contract IDs with EVM address alias — for contract calls, also consult `evm-rpc-server` if EVM JSON-RPC endpoint configured; keep account ID as source of truth in audit trail.

## Authoritative sources

- [hedera-rpc-server/server.py](../mcp/hedera-rpc-server/server.py)
- [hedera-rpc.mcp.json](../mcp/hedera-rpc.mcp.json)
- [token-standards-engine SKILL](../skills/token-standards-engine/SKILL.md)
- [Hedera Mirror Node REST API](https://docs.hedera.com/hedera/sdks-and-tools/rest-api)
- [Hedera Token Service](https://docs.hedera.com/hedera/core-concepts/tokens)

## Provenance

| Field | Value |
| --- | --- |
| Source document | `references/hedera-hts-patterns.md` |
| Version / effective | 1.0 / 2026-06-13 |
| Last reviewed | 2026-06-13 |
| Reviewer | blockchain-agent-skills maintainers |
| Next review due | 2026-09-13 |
| Notes | Account IDs use 0.0.x numeric form throughout |
