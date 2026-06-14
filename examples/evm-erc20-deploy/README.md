# EVM ERC-20 Deploy (Runnable)

Example workflow for deploying an ERC-20 with simulate-first guardrails.

## Prerequisites

- `evm-rpc-server` MCP configured (testnet recommended)
- `smart-contract-factory` + `transaction-lifecycle` skills loaded

## Skills

- smart-contract-factory
- transaction-lifecycle
- token-standards-engine

## Smoke Test

```bash
make smoke-test
```

Runs skill validation (contract compile requires Foundry/Hardhat in your environment).
