# Configuring the EVM MCP Server

1. Copy `mcp/evm-rpc.mcp.json` into your MCP client config.
2. Set `ALCHEMY_ETH_URL` or `EVM_RPC_URL` in the environment.
3. Start the server: `python mcp/evm-rpc-server/server.py` (stdio MCP).
4. Validate: `python scripts/validate-mcp-servers.py`.
5. Test `eth_blockNumber` via your MCP client before enabling write workflows elsewhere.
