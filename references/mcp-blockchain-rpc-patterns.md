# MCP Blockchain RPC Patterns

- Prefer read-only MCP tools for planning and simulation phases.
- One MCP template per chain family (`mcp/*.mcp.json`).
- Validate RPC URLs in CI before enabling write tools.
- Rate-limit and backoff on public endpoints; use dedicated nodes for production.
