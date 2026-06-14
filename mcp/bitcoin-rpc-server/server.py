#!/usr/bin/env python3
"""MCP server for Bitcoin Core JSON-RPC read tools."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

SHARED = Path(__file__).resolve().parent.parent / "_shared"
sys.path.insert(0, str(SHARED))

from mcp_stdio import run_mcp_server  # noqa: E402
from rpc_client import env_url, rpc_call  # noqa: E402


def btc_url() -> str:
    return env_url("BITCOIN_RPC_URL", default="http://127.0.0.1:8332")


def tool_getblockchaininfo(arguments: dict[str, Any]) -> str:
    _ = arguments
    result = rpc_call(btc_url(), "getblockchaininfo", [])
    return json.dumps(result)


def tool_getrawtransaction(arguments: dict[str, Any]) -> str:
    txid = arguments["txid"]
    verbose = arguments.get("verbose", True)
    result = rpc_call(btc_url(), "getrawtransaction", [txid, verbose])
    return json.dumps(result)


TOOLS = {
    "getblockchaininfo": {
        "description": "Returns Bitcoin blockchain info.",
        "handler": tool_getblockchaininfo,
        "schema": {"type": "object", "properties": {}},
    },
    "getrawtransaction": {
        "description": "Returns raw transaction by txid.",
        "handler": tool_getrawtransaction,
        "schema": {
            "type": "object",
            "required": ["txid"],
            "properties": {"txid": {"type": "string"}, "verbose": {"type": "boolean"}},
        },
    },
}


if __name__ == "__main__":
    raise SystemExit(run_mcp_server(TOOLS, "bitcoin-rpc-server"))
