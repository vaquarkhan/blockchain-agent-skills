# Blockchain vs Web3 Skills — Distinction

| Blockchain Skills (Infrastructure) | Web3 Skills (Application Layer) |
| --- | --- |
| Chain interaction primitives (RPC, encoding) | DeFi: swap, lend/borrow, yield farming |
| Transaction construction, signing, broadcast | NFT: mint, trade, marketplace |
| Validator/sequencer/consensus operations | DAO governance: proposals, voting, treasury |
| State reading and proof generation | Portfolio tracking and wallet analytics |
| Rollup mechanics, DA layer posting | MEV protection and intent-based trading |
| Network monitoring, fork detection | Social (Lens/Farcaster), SocialFi |
| Cross-chain protocols (IBC, XCM, CCIP) | RWA tokenization, compliance, identity |

**Analogy:** Blockchain = plumbing (pipes, pumps, valves). Web3 = applications (kitchen, bathroom, irrigation).

This repository implements **Blockchain Skills only**. Route DeFi/NFT/DAO requests to a separate Web3 skills layer that composes on top of these primitives.
