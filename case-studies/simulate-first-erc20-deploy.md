# Case Study: Simulate-First ERC-20 Deploy

## Situation

Team needed ERC-20 on an EVM L2 with upgrade path and audit evidence.

## Actions

1. Used `examples/evm-erc20-deploy` runnable pack.
2. Simulated deploy via `eth_call` on fork.
3. Filled `templates/mainnet-readiness.yaml` and broadcast via KMS.

## Outcome

Deploy succeeded with documented confirmation depth and rollback plan.

## Lessons

- Runnable examples accelerate consistent agent behavior.
- Readiness template catches missing access-control review.
