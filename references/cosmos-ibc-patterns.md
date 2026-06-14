# Cosmos IBC Patterns

- Verify channel ID, port, and connection state before transfer.
- Simulate with node `simulate` endpoint; check gas and fees in native denom.
- Document timeout height and memo for audit trail.
- Reconcile balances on source and destination after confirm depth.
