# Blockchain Agent Skills — Comprehensive Technical Reference

Amazon Bedrock AgentCore + MCP Architecture | Companion: [compliance-agent-skills](https://github.com/vaquarkhan/compliance-agent-skills)

---

## Section 1: 12 Core Blockchain Agent Skills

| # | Skill | What It Does |
| --- | --- | --- |
| 1 | Chain Abstraction | Unified multi-chain interaction — EVM, Solana, Cosmos, Move (Sui/Aptos), NEAR, UTXO (Bitcoin). Single interface resolves chain-specific tx models, address formats, RPC endpoints. |
| 2 | Transaction Lifecycle | Build, sign, simulate, broadcast, confirm, retry, replace transactions. Nonces, gas/fees, mempool monitoring, stuck-tx recovery. |
| 3 | Smart Contract Factory | Deploy, upgrade (UUPS/Transparent/Diamond), verify, interact. Solidity, Cairo, Rust (Anchor/Ink!/Move), CosmWasm. |
| 4 | Block & State Queries | Read chain state, trace calls, parse receipts, historical blocks. Unified query API across EVM, SVM, NEAR, Cosmos, Move VMs. |
| 5 | Event Indexing | Subscribe to events, parse logs, real-time pipelines. The Graph, Goldsky, Envio, Subsquid. |
| 6 | Consensus & Validator Ops | Staking, validator management, slashing protection, MEV-Boost. PoS, PoW, PoSA, Hashgraph, Snow consensus. |
| 7 | Storage & State Proofs | Merkle/Patricia proofs, storage slots, cross-chain verification, zkBridge, light clients. |
| 8 | Token Standards Engine | ERC-20/721/1155/4626/6551, NEP-141/171, SPL/Token-2022, CW-20/721, Jettons, Coin/Kiosk. |
| 9 | Privacy & ZK | ZK proof generation/verification, private txs, ZK-KYC. STARK, SNARK, Groth16/PLONK, Aztec. |
| 10 | Network Monitoring | Node health, mempool, fork detection, reorg handling, gas market tracking. |
| 11 | Data Availability | EIP-4844 blobs, Celestia, EigenDA, Avail, Near DA, Polygon Avail. |
| 12 | Rollup Operations | L2 deposits/withdrawals, sequencer, batch posting, fraud/validity proofs. OP Stack + ZK Stack. |

### Layer Coverage

| Layer | Components |
| --- | --- |
| L1 | Ethereum, Bitcoin, Solana, Avalanche, Cosmos Hub, BNB, NEAR, Hedera |
| L2 Optimistic | Arbitrum, Optimism, Base, Mantle, Blast, Zora |
| L2 ZK | zkSync Era, Starknet, Scroll, Linea, Polygon zkEVM |
| L3/App-chains | Arbitrum Orbit, OP app-chains, Cosmos SDK, Avalanche Subnets, Polygon CDK |
| DA Layers | Celestia, EigenDA, Avail, Near DA, Ethereum blobs (EIP-4844) |
| Sidechains | Polygon PoS, Gnosis, Ronin, Skale, Palm, Immutable X |

---

## Section 2: All Chains — Detailed Coverage

18 chains documented in full spec. Key highlights:

| Chain | VM | Consensus | Token Std. | Unique |
| --- | --- | --- | --- | --- |
| Ethereum | EVM | PoS/Casper | ERC-20/721 | ERC-4337, EIP-4844, MEV-Boost |
| NEAR | NEAR VM | PoS/Nightshade | NEP-141/171 | Chain signatures, Aurora EVM |
| Solana | SVM | PoH+Tower BFT | SPL/Token-2022 | Sealevel, cNFTs, Jito |
| Polygon | EVM+zkEVM | PoS/ZK | ERC-20/721 | CDK, AggLayer |
| Arbitrum | EVM+Stylus | Optimistic | ERC-20/721 | WASM contracts, Orbit L3s |
| Optimism | EVM | Optimistic | ERC-20/721 | Superchain, fault proofs |
| Base | EVM | Optimistic | ERC-20/721 | Coinbase sequencer, Smart Wallet |
| Avalanche | EVM+custom | Snow | ERC-20/721 | Subnets, Warp, HyperSDK |
| BNB | EVM | PoSA | BEP-20/721 | Greenfield, opBNB |
| Cosmos | CosmWasm | CometBFT | CW-20/721 | IBC, ICA, ICQ |
| Bitcoin | Script/UTXO | PoW | Runes/BRC-20 | Ordinals, Lightning, BitVM |
| TON | TVM | PoS BFT | Jettons | Telegram, actor model |
| Sui | Move | Narwhal/Bullshark | Coin/Kiosk | Object-centric, zkLogin, PTBs |
| Aptos | Move | AptosBFT | Fungible Asset v2 | Block-STM, keyless accounts |
| Starknet | Cairo | ZK/STARK | ERC-20/721 | Native AA, Sierra |
| zkSync | zkEVM | ZK/Boojum | ERC-20/721 | ZK Stack, paymaster |
| Polkadot | Substrate | NPoS+GRANDPA | Assets pallet | XCM, parachains |
| Hedera | EVM+HTS | Hashgraph | HTS | Enterprise council, HCS |

---

## Section 3: Chain-Specific Token Standards

See [skills/token-standards-engine/SKILL.md](../skills/token-standards-engine/SKILL.md) and registry for full mapping across all 18 chains.

---

## Section 4: MCP Server Architecture

8 chain-family MCP servers. See [mcp/README.md](../mcp/README.md).

| Server | Chains |
| --- | --- |
| evm-rpc-server | ETH, Polygon, Arbitrum, Base, OP, Avalanche, BNB, zkSync, Starknet |
| solana-rpc-server | Solana |
| near-rpc-server | NEAR, Aurora |
| cosmos-rpc-server | Cosmos Hub, Osmosis, Celestia, Injective, dYdX |
| move-rpc-server | Sui, Aptos |
| bitcoin-rpc-server | Bitcoin, Lightning, Stacks, Liquid |
| ton-rpc-server | TON |
| substrate-rpc-server | Polkadot, Kusama, Moonbeam, Astar |

---

## Section 5: Guardrails Configuration

Implemented in [guardrails/](../guardrails/):

- **transaction-safety.yaml** — simulate-first, $10k threshold, unverified contract block, gas limits, nonce management, reorg protection
- **security.yaml** — key protection, blind signing block, phishing/rug/honeypot detection, scam screening
- **compliance.yaml** — sanctions (OFAC/EU/UN/UK), travel rule, mixer block, audit trail (7-year DynamoDB), AML monitoring, rate limits
- **denied-topics.yaml** — private key extraction, sanctions evasion, exploit/rug creation, front-running, financial advice

---

## Section 6: Implementation Priority Phases

| Phase | Focus | Chains |
| --- | --- | --- |
| **1** | EVM Core — chain abstraction, tx lifecycle, state queries, gas | Ethereum, Arbitrum, Base, Polygon |
| **2** | Alt-L1s — contracts, tokens, events | Solana, NEAR, Cosmos |
| **3** | ZK & Move — rollups, DA, privacy, proofs | Starknet, zkSync, Sui, Aptos |
| **4** | Legacy & niche — validators, monitoring, Bitcoin, TON, Polkadot, Hedera | Specialized chains |

See [coverage-roadmap.md](coverage-roadmap.md).

---

## Section 7: Skill File Structure & Agent Orchestration

### Per-skill file set

- `skill-definition.yaml` — metadata, chains, MCP tools, guardrails
- `action-group.json` — Bedrock action group
- `lambda/handler.py` — Python 3.12 Lambda router + DynamoDB audit
- `openapi.yaml` — OpenAPI 3.0 schemas
- `tests/test_*.py` — pytest with mocked RPC
- `SKILL.md` — Cursor agent skill (this repo)

### Supervisor-worker pattern

| Agent | Skills | Role |
| --- | --- | --- |
| blockchain-supervisor | All | Orchestration, guardrails, aggregation |
| chain-interaction-agent | 1, 2, 4 | RPC, tx build/simulate/broadcast |
| contract-agent | 3, 8 | Deploy/upgrade/verify, tokens |
| validator-da-agent | 6, 7, 10, 11 | Validators, proofs, monitoring, DA |
| rollup-zk-agent | 9, 12 | ZK proofs, rollup ops, privacy |

### Multi-region CDK

| Region | Purpose |
| --- | --- |
| us-east-1 | EVM primary, Bedrock, supervisor |
| ap-south-1 | NEAR, Solana, India DPDP |
| ap-southeast-1 | TON, BNB, Cosmos SEA, Sui |
| eu-west-1 | Polkadot, zkSync, Starknet — MiCA |
| me-south-1 | Hedera, Bitcoin — VARA/Tadawul |

---

## Section 8: Blockchain vs Web3 Skills

See [BLOCKCHAIN-VS-WEB3.md](BLOCKCHAIN-VS-WEB3.md).

---

## Section 9: Key Design Principles

| Principle | Description |
| --- | --- |
| Chain-agnostic interface | Every skill accepts chainId/chainName; no hardcoded chain logic in business layer |
| Simulate-first | No broadcast without simulation; decode revert reasons structurally |
| Audit-complete | All payloads, simulations, receipts logged to DynamoDB — 7-year retention |
| Confidence scoring | HIGH/MEDIUM/LOW based on RPC freshness, simulation, edge cases |
| Human-in-the-loop | Mandatory for >$10k, unaudited contracts, validator ops, rollup exits, LOW confidence |
| Modular & composable | Skills chain via MCP tool composition |
| Temporal state awareness | Track finality depth, reorg risk, L2 challenge windows |

---

## Quick Reference: All Chains at a Glance

Full chain table with VM, consensus, token standards, and agent skill focus — see Section 2 above and [skills-index.md](../skills-index.md).
