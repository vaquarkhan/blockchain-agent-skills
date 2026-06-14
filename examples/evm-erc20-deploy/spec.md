# Spec — EVM ERC-20 Deploy

Deploy a minimal ERC-20 on EVM testnet with:

- Simulation before broadcast
- Explorer verification post-deploy
- Guardrails applied (unverified contract block on mainnet)

## Acceptance

- [ ] Contract simulates successfully
- [ ] Deploy tx confirmed with 12+ blocks (or L2 equivalent)
- [ ] Token metadata: name, symbol, decimals
