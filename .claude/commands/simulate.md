Simulate a blockchain transaction before broadcast.

Load `skills/transaction-lifecycle/SKILL.md` and run `/simulate`:

1. Build unsigned transaction
2. Run chain-specific simulation
3. Decode revert reason on failure — block broadcast
4. Assign confidence score

Never broadcast if simulation fails.
