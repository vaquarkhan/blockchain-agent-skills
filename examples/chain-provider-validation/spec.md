# Spec — Chain Provider Validation

## Goal

Verify unified chain resolution and address validation for Phase 1 (EVM) and Phase 2 (Solana, NEAR, Cosmos) chains.

## Acceptance

- [ ] `resolve_chain("ethereum")` returns chainId `1`
- [ ] Solana base58 pubkeys validate
- [ ] NEAR named and implicit accounts validate
- [ ] Cosmos bech32 addresses validate with correct prefix
- [ ] All 8 unit tests pass
