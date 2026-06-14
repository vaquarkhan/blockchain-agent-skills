# Solana Program Security

Review checklist for Anchor/Rust on-chain programs, SPL tokens, and mainnet deployment via `solana-rpc-server`.

## MCP tools

| Tool | Use |
| --- | --- |
| `get_account_info` | Program, mint, PDA account layout |
| `simulate_transaction` | Pre-broadcast execution + logs |
| `get_token_accounts_by_owner` | SPL holdings audit |
| `send_transaction` | **Write** — requires `SIMULATE_PASSED` + mainnet `HUMAN_CONFIRMED` |

Env: `SOLANA_RPC_URL`, `SOLANA_CLUSTER` (default `mainnet-beta`).

## Program Derived Addresses (PDA)

- Derive with canonical seeds: program id + seed strings + bump.
- Document every seed in program spec; agents must not invent seeds at runtime.
- Verify bump is canonical (`find_program_address`) — wrong bump → signature failure or wrong authority.

Example verification flow:

1. Read program account via `get_account_info`.
2. Recompute PDA off-chain with documented seeds.
3. Compare pubkey before any authority transfer.

## Upgrade authority (UPGRADE concern)

| Risk | Check |
| --- | --- |
| Mutable program after "immutable" claim | `ProgramData` account upgrade authority |
| Single-key upgrade | Multisig or Squads on upgrade authority |
| Unreviewed upgrade | Block mainnet until audit + timelock |

**UPGRADE concern** — flag HIGH severity when:

- Upgrade authority is a hot wallet
- No timelock between upgrade proposal and execution
- Program size increased without review (arbitrary code injection vector)

Before mainnet deploy:

```bash
solana program show <PROGRAM_ID> --url $SOLANA_RPC_URL
# Confirm Authority / Last Deploy Slot / Data Length
```

Simulate post-upgrade behavior on devnet before signing mainnet upgrade tx.

## SPL token authorities

| Authority | Risk if retained |
| --- | --- |
| Mint authority | Infinite inflation |
| Freeze authority | User funds frozen |
| Close authority | Metadata/account griefing |

Validate via `get_account_info` on mint; prefer renouncing or transferring to multisig before launch.

## simulateTransaction patterns

MCP `simulate_transaction` maps to RPC `simulateTransaction`:

```json
{
  "sigVerify": false,
  "replaceRecentBlockhash": true,
  "commitment": "processed"
}
```

Include in tx:

- **Compute budget** — set units and price explicitly
- **Priority fees** — `ComputeBudgetProgram.setComputeUnitPrice` for congested mainnet
- All instructions the production tx will use (including ATA creation)

Failure modes:

| Log / error | Meaning |
| --- | --- |
| `Computational budget exceeded` | Raise unit limit |
| `custom program error: 0x1` | Anchor error — decode error code |
| Simulation OK, send fails | Blockhash expired — refresh and re-sign |

## Priority fees

During congestion, simulate with escalating priority fee:

1. Baseline simulate (no priority fee).
2. Add micro-lamports per CU; re-simulate until landing probability acceptable.
3. Record chosen fee in audit trail.

Do not broadcast without successful simulate at the fee tier you will use.

## Security guardrails

- `security.yaml` → blind signing block: decode all instruction data
- Honeypot pattern: simulate buy + sell in one tx bundle where applicable
- Never pass keypair JSON through MCP — sign with KMS/HSM offline

## Worked example (SPL transfer)

1. `get_token_accounts_by_owner` — confirm source ATA exists.
2. Build transfer instruction + compute budget ixs.
3. `simulate_transaction` — inspect logs for `TransferChecked` success.
4. `export SIMULATE_PASSED=true`; KMS sign; `send_transaction`.
5. Confirm 32 slots (`transaction-safety.yaml` Solana depth) before downstream use.

## Authoritative sources

- [solana-rpc-server/server.py](../mcp/solana-rpc-server/server.py)
- [solana-rpc.mcp.json](../mcp/solana-rpc.mcp.json)
- [token-standards-engine SKILL](../skills/token-standards-engine/SKILL.md)
- [smart-contract-factory SKILL](../skills/smart-contract-factory/SKILL.md)
- [Solana simulateTransaction RPC](https://solana.com/docs/rpc/http/simulatetransaction)
- [Anchor security guidelines](https://www.anchor-lang.com/docs/security)

## Provenance

| Field | Value |
| --- | --- |
| Source document | `references/solana-program-security.md` |
| Version / effective | 1.0 / 2026-06-13 |
| Last reviewed | 2026-06-13 |
| Reviewer | blockchain-agent-skills maintainers |
| Next review due | 2026-09-13 |
| Notes | Upgrade authority flagged as standing UPGRADE concern |
