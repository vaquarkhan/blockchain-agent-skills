#!/usr/bin/env python3
"""MCP server for Substrate JSON-RPC."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

SHARED = Path(__file__).resolve().parent.parent / "_shared"
sys.path.insert(0, str(SHARED))

from mcp_stdio import run_mcp_server  # noqa: E402
from rpc_client import env_url, rpc_call  # noqa: E402


def substrate_url() -> str:
    return env_url("SUBSTRATE_RPC_URL", default="https://rpc.polkadot.io")


def tool_chain_get_block(arguments: dict[str, Any]) -> str:
    block = arguments.get("block")
    params = [block] if block else []
    result = rpc_call(substrate_url(), "chain_getBlock", params)
    return json.dumps(result)


def tool_system_health(arguments: dict[str, Any]) -> str:
    _ = arguments
    result = rpc_call(substrate_url(), "system_health", [])
    return json.dumps(result)


TOOLS = {
    "chain_getBlock": {
        "description": "Returns Substrate block hash or header.",
        "handler": tool_chain_get_block,
        "schema": {"type": "object", "properties": {"block": {"type": "string"}}},
    },
    "system_health": {
        "description": "Returns node health status.",
        "handler": tool_system_health,
        "schema": {"type": "object", "properties": {}},
    },
}


if __name__ == "__main__":
    raise SystemExit(run_mcp_server(TOOLS, "substrate-rpc-server"))
