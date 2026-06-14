# Event Indexing Pipeline Tutorial

1. Load `skills/event-indexing` with `skills/block-state-queries`.
2. Choose MCP + archive RPC tier for historical logs.
3. Define idempotent cursor storage and replay procedure.
4. Validate schema changes against downstream consumers before backfill.
