# Plan — Cosmos IBC Transfer

1. Query IBC client and channel state
2. Build MsgTransfer with timeout height
3. Simulate and broadcast on cosmoshub-4
4. Monitor packet ack via event indexing
