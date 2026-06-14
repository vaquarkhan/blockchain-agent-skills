# EVM Mainnet Guardrails

Checklist and thresholds for Ethereum mainnet and high-value EVM L1/L2 operations. Applies to `evm-rpc-server` write path and Foundry/Hardhat deploy scripts orchestrated by agents.

## Pre-flight checklist

Complete `templates/mainnet-readiness.yaml` before any mainnet deploy or transfer above policy threshold:

| Field | Requirement |
| --- | --- |
| `simulation_passed` | `eth_call` or fork test succeeded |
| `gas_estimated` | `eth_estimate_gas` within 10× estimate |
| `access_control_reviewed` | Owner/admin roles documented |
| `upgrade_path_documented` | Proxy admin + timelock if upgradeable |
| `kms_signing_configured` | No raw private keys in agent context |
| `confirmation_depth_defined` | Per-chain reorg depth recorded |
| `compliance_review_complete` | OFAC screen on `to` and contract |

Attach `templates/release-gate-evidence.yaml` to release PRs and incident records.

## Value and confirmation thresholds

From `guardrails/transaction-safety.yaml`:

| Rule | Threshold | Action |
| --- | --- | --- |
| `max_value_without_confirmation` | $10,000 USD | `REQUIRE_HUMAN_CONFIRM` → `HUMAN_CONFIRMED=true` |
| `gas_limit_validation` | >10× estimate | BLOCK broadcast |
| `unverified_contract_block` | No Etherscan/Sourcify match | BLOCK interaction |
| `unlimited_approval_warning` | `type(uint256).max` | WARN; prefer bounded allowance |

## Confirmation depths (`reorg_protection`)

| Chain | Min blocks | MCP poll tool |
| --- | ---: | --- |
| Ethereum mainnet | 12 | `eth_get_block_by_number` |
| BNB Chain | 15 | `eth_block_number` |
| Arbitrum / Base / OP (L2 UX) | 20+ for high value | L1 finality for bridges |
| Generic L2 fast path | 1–2 for low value reads only | Not for settlement |

## Simulation (`eth_call`) patterns

Always simulate state-changing calls before `eth_send_raw_transaction`:

```json
{
  "method": "eth_call",
  "params": [{
    "from": "0xSigner...",
    "to": "0xContract...",
    "data": "0xa9059cbb...",
    "value": "0x0"
  }, "latest"]
}
```

MCP tools: `eth_call`, `eth_estimate_gas`, `debug_trace_call` (if node supports).

Decode reverts structurally (`Error(string)`, custom errors) — never broadcast on revert.

## MCP write gate

`evm-rpc-server` tool `eth_send_raw_transaction` requires:

```bash
export SIMULATE_PASSED=true
export HUMAN_CONFIRMED=true   # mainnet
export ALCHEMY_ETH_URL=https://...
```

Sign with AWS KMS / HSM outside MCP; pass only signed raw hex.

## Security guardrails (`security.yaml`)

| Check | Method |
| --- | --- |
| Blind signing block | Full calldata decode before sign |
| Honeypot | `simulate_buy_and_sell` via GoPlus or local fork |
| Scam addresses | OFAC + abuse DB screen |
| Contract age | WARN <30 days; escalate <7 days on high value |
| Phishing | GoPlus / Forta feeds |

## Release gate evidence

`templates/release-gate-evidence.yaml` bundles:

- Simulation artifact (`simulate_tx_hash_or_trace`)
- Guardrail file references
- Human signoff (`reviewer`, `timestamp_utc`, `network`)
- Rollback plan → `templates/incident-runbook.md`

Run before `/ship`:

```bash
bash hooks/release-guard.sh
python scripts/hook_runner.py mainnet-guard
```

## Worked example (mainnet contract deploy)

1. Verify bytecode on testnet; Sourcify/Etherscan verify source.
2. Fork mainnet locally; simulate constructor + initializer via `eth_call`.
3. Fill `mainnet-readiness.yaml`; obtain human signoff.
4. Deploy via KMS-signed tx; record deploy address and tx hash.
5. Wait 12 blocks; verify contract code with `eth_get_code`.
6. Attach `release-gate-evidence.yaml` to change record.

## Failure modes

| Failure | Response |
| --- | --- |
| `eth_call` revert | Fix args/permissions; no broadcast |
| Unverified target contract | Block until verified on explorer |
| Gas limit 10× over estimate | Re-estimate; check malicious loop |
| Receipt dropped from mempool | Replace-by-fee only with explicit override |
| L2 sequencer down | Pause writes; monitor via `network-monitoring` |

## Authoritative sources

- [transaction-safety.yaml](../guardrails/transaction-safety.yaml)
- [security.yaml](../guardrails/security.yaml)
- [compliance.yaml](../guardrails/compliance.yaml)
- [mainnet-readiness.yaml](../templates/mainnet-readiness.yaml)
- [release-gate-evidence.yaml](../templates/release-gate-evidence.yaml)
- [evm-rpc-server README](../mcp/evm-rpc-server/README.md)
- [mainnet guardrails walkthrough](../tutorials/mainnet-guardrails-walkthrough.md)

## Provenance

| Field | Value |
| --- | --- |
| Source document | `references/evm-mainnet-guardrails.md` |
| Version / effective | 1.0 / 2026-06-13 |
| Last reviewed | 2026-06-13 |
| Reviewer | blockchain-agent-skills maintainers |
| Next review due | 2026-09-13 |
| Notes | Thresholds mirror `transaction-safety.yaml` v1.0 |
