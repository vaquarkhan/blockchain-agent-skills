# Substrate Validator Patterns

Polkadot-ecosystem Substrate chains: validator ops, RPC health, and incident communication. MCP: `substrate-rpc-server`.

## MCP tools

| Tool | JSON-RPC method | Purpose |
| --- | --- | --- |
| `chain_get_block` | `chain_getBlock` | Block header, extrinsics hash |
| `system_health` | `system_health` | Peers, sync state, best/finalized height |

Env: `SUBSTRATE_RPC_URL` (e.g. `wss://rpc.polkadot.io` or HTTP provider).

```bash
python scripts/validate-mcp-servers.py
```

## Polkadot RPC essentials

Common methods (via node or subxt — not all exposed as MCP tools):

| Method | Use |
| --- | --- |
| `chain_getHeader` | Latest block |
| `state_getStorage` | Validator keys, staking ledger |
| `author_pendingExtrinsics` | Mempool visibility |
| `grandpa_roundState` | Finality gadget status |

Use `chain_get_block` for extrinsic inclusion checks after broadcast.

## Validator rotation

| Phase | Action |
| --- | --- |
| Era change | Session keys rotate; monitor `session` pallet events |
| Chilled / offline | Validator drops in active set — alert |
| Nomination limits | Track min bond and max nominators |

Before key operations:

1. `system_health` — `isSyncing: false`, peers ≥ 3.
2. Compare `best` vs `finalized` block gap — large gap → finality lag incident.
3. Document era index in change record.

Human confirmation required for validator operations per `release-gate-evidence.yaml` → `human_approval.validator_operations`.

## Staking and keys

- **Controller** vs **stash** — never expose stash seed; rotate controller on compromise.
- Session keys on disk — HSM where supported (e.g. remote signers).
- Slashing risk: double-signing → use `--keystore` isolation and key ownership audit.

## Incident communication

During validator or finality incidents, follow `templates/incident-runbook.md`:

### Triage (0–15 min)

1. Run `system_health` — record peers, best, finalized.
2. `chain_get_block` at best hash — timestamp drift?
3. Classify: node desync vs chain halt vs widespread finality stall.

### Communication template

| Audience | Channel | Content |
| --- | --- | --- |
| Internal ops | Pager / Slack | Block lag, peer count, last finalized |
| Nominators | Status page | Expected downtime, no slash yet / slash risk |
| Ecosystem | Forum / X | Factual, no key material, link to release-gate evidence |

### Do not

- Broadcast panic transactions without simulation
- Rotate session keys on live network without governance timeline
- Share keystore paths or mnemonics in tickets

### Recovery checklist

- [ ] Resync from trusted snapshot if corrupt
- [ ] Verify `--chain` spec matches production (Polkadot vs Kusama)
- [ ] Replay missed votes only after sync to head
- [ ] Post-incident: attach `release-gate-evidence.yaml` addendum

## Moonbeam / Astar note

EVM-compatible parachains: combine `substrate-rpc-server` health checks with `evm-rpc-server` for contract ops on the same incident timeline.

## Worked example (health check)

```bash
export SUBSTRATE_RPC_URL=https://polkadot-rpc.publicnode.com
# MCP system_health → { peers: 42, isSyncing: false, shouldHavePeers: true }
# MCP chain_get_block → extrinsicsRoot, number
# If finalized lag > 10 blocks → open incident, pause validator key ops
```

## Failure modes

| Symptom | Likely cause |
| --- | --- |
| `isSyncing: true` prolonged | Disk / snapshot issue |
| 0 peers | Firewall, bootnode misconfig |
| Finality stall | GRANDPA equivocation investigation |
| Extrinsic dropped | Priority fee / weight too low |

## Authoritative sources

- [substrate-rpc-server/server.py](../mcp/substrate-rpc-server/server.py)
- [consensus-validator-ops SKILL](../skills/consensus-validator-ops/SKILL.md)
- [network-monitoring SKILL](../skills/network-monitoring/SKILL.md)
- [incident-runbook.md](../templates/incident-runbook.md)
- [Polkadot JSON-RPC](https://polkadot.js.org/docs/substrate/rpc)

## Provenance

| Field | Value |
| --- | --- |
| Source document | `references/substrate-validator-patterns.md` |
| Version / effective | 1.0 / 2026-06-13 |
| Last reviewed | 2026-06-13 |
| Reviewer | blockchain-agent-skills maintainers |
| Next review due | 2026-09-13 |
| Notes | Incident comms aligned with incident-runbook.md |
