---
name: smart-contract-factory
description: Deploy, upgrade (UUPS/Transparent/Diamond), verify, and interact with smart contracts. Supports Solidity, Cairo, Rust (Anchor/Ink!/Move), and CosmWasm across all chains. Trigger when deploying contracts, proxy upgrades, Etherscan verification, or complex multi-sig/diamond interactions. Phase 2 implements Solana Anchor, NEAR, and CosmWasm deploy paths.
---

# Smart Contract Factory

## Overview

Contract lifecycle management across VM families:

- **Deploy** — factory patterns, CREATE2 deterministic addresses
- **Upgrade** — UUPS, Transparent Proxy, Diamond (EIP-2535)
- **Verify** — Etherscan/Blockscout/Sourcify source verification
- **Interact** — ABI/IDL-driven encoding, Multicall3 batching

All deploy/upgrade/interact writes follow `/plan` → `/simulate` → `/confirm` → `/broadcast` → `/confirm-depth`. Signing via KMS only (`security.yaml`). Guardrails: `transaction-safety.yaml` (unverified contract block), `security.yaml` (contract age, blind signing), `compliance.yaml` (audit trail).

**Tier 1** EVM Solidity: full path via `evm-rpc-server`. **Tier 2** Anchor, NEAR WASM, CosmWasm: implemented deploy paths. **Tier 3** Cairo/Move: read paths via `move-rpc-server`; deploy requires external toolchain.

## When to Use

- Deploying new smart contracts (any supported language)
- Upgrading proxy contracts (UUPS, Transparent, Diamond)
- Verifying source on block explorers
- Complex interactions: Multicall3, Diamond facet cuts, multi-sig proposals
- Post-deploy initialization and ownership transfer

Do **not** use for simple token transfers (use `token-standards-engine`) or raw tx retry (use `transaction-lifecycle`).

## Core Process

### Step 1: Compile and audit check

1. Identify language: Solidity, Cairo, Rust/Anchor, CosmWasm, Ink!.
2. Warn if contract **<30 days** old with no audit (`security.yaml` → `contract_age_check`).
3. Escalate to `/confirm` if **<7 days** + high-value interaction.
4. **Block** interaction with unverified contracts on mainnet (`transaction-safety.yaml` → `unverified_contract_block`).
5. Check explorers: Etherscan, Blockscout, Sourcify.

### Step 2: Deploy

1. Estimate gas via `transaction-lifecycle` → `eth_estimateGas`.
2. **Simulate** deploy transaction (`eth_call` with deploy payload).
3. Sign via KMS; broadcast via `eth_sendRawTransaction` or chain equivalent.
4. Capture deployed address from receipt logs (CREATE address or CREATE2 predicted).
5. Log deploy artifact: bytecode hash, constructor args, deployed address.

### Step 3: Verify

Post-deploy verification on chain explorer:

| Chain | Method | MCP / API |
| --- | --- | --- |
| EVM | Etherscan/Blockscout standard-json-input | Explorer API |
| EVM | Sourcify | Sourcify API |
| Solana | Anchor IDL on-chain | `solana-rpc-server` |
| NEAR | NEP-330 source metadata | `near-rpc-server` |
| CosmWasm | Code ID + instantiate hash | `cosmos-rpc-server` |

### Step 4: Upgrade (proxies)

| Pattern | Upgrade function location | Simulation requirement |
| --- | --- | --- |
| UUPS | Implementation contract | Simulate + storage layout check |
| Transparent | ProxyAdmin | Simulate via ProxyAdmin.upgrade |
| Diamond | facet cut on Diamond | Simulate each facet add/replace/remove |

Always simulate upgrade tx; verify storage layout compatibility (OpenZeppelin Upgrades plugin or manual slot audit).

### Step 5: Interact

1. Encode calldata from ABI/IDL — never blind sign (`security.yaml`).
2. Batch via Multicall3 where applicable (EVM).
3. Route broadcast through `transaction-lifecycle`.

## Phase 2 — Alt-L1 deploy paths

### Solana (Anchor) — Tier 2

1. Parse Anchor IDL for automatic instruction builders.
2. Deploy program via `solana program deploy`; record program ID.
3. Initialize PDAs via `findProgramAddressSync(seeds, programId)`.
4. Verify IDL on-chain; use `getProgramAccounts` for state reads.

MCP: `solana-rpc-server` — `simulateTransaction` before every deploy/upgrade.

### NEAR (Rust / near-sdk-rs) — Tier 2

1. Deploy WASM contract to named account (e.g., `token.alice.near`).
2. Register NEP-330 source metadata for explorer verification.
3. Manage access keys: full-access for admin, function-call keys with method whitelist for agents.
4. Cross-contract calls via async promises; handle callback gas.

MCP: `near-rpc-server` — `view_contract_state`, `send_tx`.

### Cosmos (CosmWasm) — Tier 2

1. Upload WASM bytecode via `MsgStoreCode`.
2. Instantiate contract with init msg JSON.
3. Execute via `MsgExecuteContract`; query via `abci_query` with smart query JSON.
4. IBC-enabled contracts: verify channel OPEN before cross-chain execute.

MCP: `cosmos-rpc-server` — `broadcast_tx`, `abci_query`.

## Decision framework

1. **New deployment vs upgrade?** → Deploy: CREATE/CREATE2. Upgrade: identify proxy pattern first.
2. **Which proxy pattern?** → UUPS (implementation holds logic), Transparent (ProxyAdmin), Diamond (EIP-2535 facets).
3. **Deterministic address needed?** → CREATE2 with factory + salt.
4. **Multi-chain deployment?** → Separate deploy per chain; resolve each via `chain-abstraction`.
5. **Unverified contract on mainnet?** → BLOCK interaction unless explicit verified override workflow.
6. **Language/chain Tier 3?** → State roadmap; do not deploy without documented MCP path.

| Task | Primary path | Simulation tool |
| --- | --- | --- |
| ERC-20 deploy | Solidity + evm-rpc-server | `eth_call` |
| UUPS upgrade | ProxyAdmin or implementation | `eth_call` |
| Anchor program | solana-rpc-server | `simulateTransaction` |
| CosmWasm instantiate | cosmos-rpc-server | `simulate` |

## Anti-patterns and rationalizations

| Rationalization | Risk | Required response |
| --- | --- | --- |
| "Deploy to mainnet without verification plan" | Unverified contract block on future interactions | Verify immediately post-deploy |
| "Upgrade without storage layout check" | Storage collision, bricked proxy | Run layout diff; simulate upgrade |
| "User sent bytecode — deploy as-is" | Honeypot, malicious logic | Require source + audit check |
| "Diamond facet cut — skip simulate" | Broken fallback, bricked contract | Simulate each cut operation |
| "Use CREATE without gas estimate" | Out-of-gas deploy, lost gas | `eth_estimateGas` + 10x cap |
| "Interact with 3-day-old unaudited contract" | Rug pull, unaudited logic | Warn; require `/confirm` for high value |
| "Sign upgrade calldata without decode" | Blind signing drain | Decode all params per `security.yaml` |

## Verification

- [ ] Contract language and target chain identified; Tier status documented
- [ ] Audit age check applied (`security.yaml` → contract_age_check)
- [ ] Simulation passed for deploy/upgrade/interact via chain MCP tool
- [ ] Unverified contract block enforced on mainnet interactions
- [ ] Deployed address captured from receipt; CREATE2 address predicted if applicable
- [ ] Source verified on Etherscan/Blockscout/Sourcify or chain equivalent
- [ ] Proxy pattern documented (UUPS/Transparent/Diamond) if applicable
- [ ] Storage layout compatibility verified for upgrades
- [ ] KMS signing used; no private key in context
- [ ] Human confirmation for unaudited <7 days + high value
- [ ] Audit trail logged to DynamoDB per `compliance.yaml`
- [ ] Confirmation depth reached before marking deploy/upgrade complete
