# Cosmos IBC Transfer Planning

1. Load `skills/chain-abstraction` and `presets/cosmos-ibc/PRESET.md`.
2. Fill `templates/ibc-transfer-plan.yaml` with channel, timeout, and fees.
3. Use `mcp/cosmos-rpc-server/server.py` tool `ibc_channels` for channel discovery.
4. Simulate before `MsgTransfer` broadcast; reconcile balances after confirm depth.
