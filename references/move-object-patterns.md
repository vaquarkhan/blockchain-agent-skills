# Move Object Patterns (Sui & Aptos)

Move VM chains model state as typed objects (Sui) or resources under accounts (Aptos). MCP: `move-rpc-server` — read-only tools; writes via external signer + guarded broadcast paths.

## MCP tools

| Tool | Chain | Underlying API |
| --- | --- | --- |
| `sui_get_object` | Sui | `sui_getObject` JSON-RPC |
| `aptos_view` | Aptos | `/view` REST function call |

Env:

```bash
export SUI_RPC_URL=https://fullnode.mainnet.sui.io:443
export APTOS_RPC_URL=https://fullnode.mainnet.aptoslabs.com/v1
```

Validate: `python scripts/validate-mcp-servers.py`

## Sui object model

Objects have:

- **Object ID** — unique on-chain reference
- **Owner** — address-owned, shared, or immutable
- **Type** — fully qualified Move type `0xPKG::module::Struct`
- **Version** — increments on mutation (concurrency control)

### sui_get_object pattern

MCP `sui_get_object` parameters:

| Arg | Example |
| --- | --- |
| `object_id` | `0xabc...` |
| `options` | `{ showContent: true, showOwner: true, showType: true }` |

Use cases:

- Verify coin object before merge/split
- Confirm shared object version for PTB (programmable transaction block)
- Audit package upgrade cap ownership

### Sui transaction flow (agent)

1. Build PTB off-chain (no keys in agent if possible).
2. Dry-run via full node `sui_dryRunTransactionBlock` (outside MCP or future tool).
3. Sign with KMS; execute via wallet/guardian service.
4. Confirm object version incremented.

Failure modes:

| Error | Cause |
| --- | --- |
| `ObjectVersionMismatch` | Stale object ref — refresh `sui_get_object` |
| `ObjectNotFound` | Wrong ID or pruned full node |
| Shared object congestion | Retry with higher gas budget |

## Aptos view pattern

MCP `aptos_view` calls read-only Move functions:

```json
{
  "function": "0x1::coin::balance",
  "type_arguments": ["0x1::aptos_coin::AptosCoin"],
  "arguments": ["0xaccount"]
}
```

Use for:

- Balance checks before transfer
- On-chain config (governance, staking params)
- Simulating read path of DeFi pools

Writes: build `entry_function_payload`, simulate via `/transactions/simulate`, sign externally.

## Object vs account mental model

| Aspect | Sui | Aptos |
| --- | --- | --- |
| Primary ID | Object ID | Account address |
| Fungible coin | `Coin<T>` object | `Coin<T>` resource in account |
| Shared state | Shared objects | Global resources + accounts |
| Upgrade | Package upgrade cap object | Resource account pattern |

## Security checks

- Verify package id matches audited release (not typosquat address)
- Shared object ownership — who can mutate?
- `security.yaml` blind signing — decode all Move call args
- Token standards: `token-standards-engine` for Coin vs legacy coin modules

## Worked example (Sui coin transfer planning)

1. `sui_get_object` — source coin object; note `balance` and `version`.
2. `sui_get_object` — recipient address status (exists?).
3. Construct PTB split + transfer; dry-run off MCP.
4. Human confirm if USD > $10k; KMS sign.
5. Poll new object IDs for change output; reconcile balances.

## Worked example (Aptos view before send)

1. `aptos_view` — `0x1::coin::balance` for sender.
2. Simulate transfer transaction via Aptos REST.
3. Set `SIMULATE_PASSED=true`; broadcast signed tx.
4. `aptos_view` balance again at ledger version + confirm depth.

## Failure modes

| Symptom | Action |
| --- | --- |
| Type mismatch in view | Fix `type_arguments` order |
| Object locked | Wait for prior tx finality |
| RPC 503 | Failover RPC; lower confidence to MEDIUM |

## Authoritative sources

- [move-rpc-server/server.py](../mcp/move-rpc-server/server.py)
- [move-rpc.mcp.json](../mcp/move-rpc.mcp.json)
- [token-standards-engine SKILL](../skills/token-standards-engine/SKILL.md)
- [Sui sui_getObject RPC](https://docs.sui.io/sui-api-ref#sui_getObject)
- [Aptos view API](https://aptos.dev/en/build/apis/fullnode-rest-api)

## Provenance

| Field | Value |
| --- | --- |
| Source document | `references/move-object-patterns.md` |
| Version / effective | 1.0 / 2026-06-13 |
| Last reviewed | 2026-06-13 |
| Reviewer | blockchain-agent-skills maintainers |
| Next review due | 2026-09-13 |
| Notes | move-rpc-server currently read-only (2 tools) |
