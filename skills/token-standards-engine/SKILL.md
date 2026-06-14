---
name: token-standards-engine
description: Deploy and manage tokens per chain-native standards — ERC-20/721/1155/4626/6551 (EVM), NEP-141/171 (NEAR), SPL/Token-2022 (Solana), CW-20/721 (Cosmos), Jettons (TON), Coin/Kiosk (Sui/Aptos). Automatic standard detection and unified interface. Trigger when minting, transferring, or deploying tokens.
---

# Token Standards Engine

## Overview

Unified fungible/NFT interface with chain-specific adapters. All transfers/mints/approvals route writes through `transaction-lifecycle` with simulate-first enforcement.

| Chain | Fungible | NFT | Tier |
| --- | --- | --- | --- |
| Ethereum | ERC-20, ERC-4626 | ERC-721, ERC-1155, ERC-6551 | 1 |
| NEAR | NEP-141 | NEP-171 | 2 |
| Solana | SPL, Token-2022 | Metaplex, cNFTs | 2 |
| Cosmos | CW-20, ICS-20 | CW-721 | 2 |
| TON | Jettons (TEP-74) | TON NFT (TEP-62) | 4 read via `ton-rpc-server` |
| Sui | Coin | Kiosk | 3 read via `move-rpc-server` |
| Aptos | Fungible Asset v2 | Digital Asset | 3 read via `move-rpc-server` |

Security guardrails (`security.yaml`): honeypot detection, GoPlus/forta feeds, top holder concentration >30% warn, unlimited approval warn. Compliance: sanctions screening on all counterparties.

## When to Use

- Deploying new tokens (ERC-20, SPL mint, NEP-141, CW-20)
- Transferring tokens or NFTs
- Approving spenders (EVM) or delegations (Solana)
- Detecting token standard from contract/program address
- IBC transfers (ICS-20) on Cosmos

Do **not** use for raw ETH/SOL/NEAR native transfers without token contract (use `transaction-lifecycle` directly).

## Core Process

### Step 1: Detect standard

From contract address or program ID:

1. EVM: `eth_call` → `symbol()`, `decimals()`, `supportsInterface(0x80ac58cd)` for ERC-721.
2. Solana: `getAccountInfo` → mint account owner (Token vs Token-2022 program).
3. NEAR: `view_function` → NEP-141 `ft_metadata` or NEP-171 `nft_metadata`.
4. Cosmos: smart query `{ "token_info": {} }` or `{ "contract_info": {} }`.

Return: standard, name, symbol, decimals, MCP server.

### Step 2: Security checks (mandatory before interaction)

| Check | Source | Action |
| --- | --- | --- |
| Honeypot | security.yaml | simulate buy + sell; BLOCK if sell fails |
| GoPlus token security | security.yaml | API scan |
| Top holder concentration | security.yaml | WARN if >30% |
| Unlimited approval | transaction-safety.yaml | WARN; suggest bounded `type(uint256).max` alternative |
| Sanctions | compliance.yaml | BLOCK sanctioned addresses |
| Contract age | security.yaml | WARN <30 days; escalate <7 days + high value |

### Step 3: Execute operation

Mint, transfer, approve (EVM), or chain-native equivalent:

| Standard | Transfer method | MCP tool |
| --- | --- | --- |
| ERC-20 | `transfer(to, amount)` | evm-rpc-server → `eth_call` sim, `eth_sendRawTransaction` |
| ERC-721 | `safeTransferFrom` | evm-rpc-server |
| SPL | `Transfer` instruction | solana-rpc-server → `simulateTransaction` |
| NEP-141 | `ft_transfer` | near-rpc-server |
| CW-20 | `Send` execute msg | cosmos-rpc-server |
| ICS-20 | IBC transfer msg | cosmos-rpc-server → `ibc_transfer` |

Route all writes through `/plan` → `/simulate` → `/confirm` (if >$10k) → `/broadcast` → `/confirm-depth`.

### Step 4: Verify receipt

1. Parse Transfer/Mint events from receipt logs (`event-indexing` or `eth_getTransactionReceipt`).
2. Confirm balance change via `block-state-queries` → `eth_getBalance` / `getTokenAccountsByOwner`.
3. Match expected delta to requested amount.

## Phase 2 — Chain-specific adapters

### Solana SPL / Token-2022 — Tier 2

- Detect mint via `getTokenAccountsByOwner`
- Token-2022 extensions: transfer hook, confidential transfers, non-transferable — simulate before transfer
- cNFTs: Merkle tree state via Bubblegum program + DAS API (`getAsset`)

### NEAR NEP-141 / NEP-171 — Tier 2

- Fungible: `ft_transfer`, `ft_transfer_call` with storage deposit (NEP-145)
- NFT: `nft_transfer`, metadata via NEP-177
- Storage: ~0.0001 NEAR/byte — check `view_account` storage before transfer

### Cosmos CW-20 / CW-721 / ICS-20 — Tier 2

- Query token info via CosmWasm smart query: `{ "token_info": {} }`
- IBC transfer: build ICS-20 msg via `cosmos-rpc-server` `ibc_transfer`
- Track IBC denom trace via `get_ibc_denom_trace`

## Decision framework

1. **Address provided — fungible or NFT?** → Probe interfaces/metadata; check `supportsInterface` on EVM.
2. **Unknown token on mainnet?** → Run full security suite before any transfer/approve.
3. **Approve vs permit (EIP-2612)?** → Prefer permit if supported; else bounded approve (never unlimited without warn).
4. **ICS-20 cross-chain?** → Verify channel OPEN; resolve denom trace on destination.
5. **Token-2022 with transfer hook?** → Extra simulation required; may block if hook reverts.
6. **Deploy new token?** → Primary `smart-contract-factory`; this skill for standard-specific init params.

| Operation | ERC-20 | SPL | NEP-141 |
| --- | --- | --- | --- |
| Transfer | transfer() | Transfer ix | ft_transfer |
| Approve | approve(spender, amt) | Delegate | storage_deposit + ft_transfer_call |
| Mint | mint(to, amt) | MintTo ix | ft_mint (if minter role) |

## Anti-patterns and rationalizations

| Rationalization | Risk | Required response |
| --- | --- | --- |
| "Skip honeypot check — popular token" | Honeypot drain on sell | Always simulate buy+sell per `security.yaml` |
| "Approve unlimited for convenience" | Full wallet drain if spender compromised | Warn; suggest bounded approval |
| "Transfer without decimals check" | 1000x amount error | Fetch decimals; display human-readable amount |
| "ICS-20 without channel check" | Lost tokens in transit | Verify channel OPEN and connection |
| "NEAR transfer without storage deposit" | Transfer fails silently | Check NEP-145 storage; attach deposit |
| "Ignore 35% top holder concentration" | Rug pull risk | Warn user; require `/confirm` for high value |
| "Mint on Tier 3 Sui without adapter" | Undefined behavior | State Tier 3 roadmap; block if no MCP path |

## Verification

- [ ] Token standard detected correctly from on-chain metadata
- [ ] Honeypot simulation passed (buy + sell) for unknown tokens
- [ ] GoPlus/security API scan completed for mainnet tokens
- [ ] Top holder concentration checked; warning issued if >30%
- [ ] Sanctions screening passed for sender and recipient
- [ ] Decimals and human-readable amount confirmed with user
- [ ] Simulation passed via chain MCP tool before broadcast
- [ ] Bounded approval used or unlimited approval warning documented
- [ ] Transfer confirmed with matching Transfer event in receipt
- [ ] Balance delta verified via `block-state-queries`
- [ ] Human confirmation for >$10k or LOW confidence tokens
- [ ] Audit trail logged per `compliance.yaml`
