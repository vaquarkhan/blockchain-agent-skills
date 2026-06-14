#!/usr/bin/env python3
"""MCP server for Move chains (Sui + Aptos read paths)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
import urllib.request

SHARED = Path(__file__).resolve().parent.parent / "_shared"
sys.path.insert(0, str(SHARED))

from mcp_stdio import run_mcp_server  # noqa: E402
from rpc_client import env_url  # noqa: E402


def sui_url() -> str:
    return env_url("SUI_RPC_URL", default="https://fullnode.mainnet.sui.io:443").rstrip("/")


def aptos_url() -> str:
    return env_url("APTOS_RPC_URL", default="https://fullnode.mainnet.aptoslabs.com/v1").rstrip("/")


def tool_sui_get_object(arguments: dict[str, Any]) -> str:
    object_id = arguments["object_id"]
    import urllib.request

    payload = {"jsonrpc": "2.0", "id": 1, "method": "sui_getObject", "params": [object_id, {"showContent": True}]}
    request = urllib.request.Request(
        sui_url(),
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))
    return json.dumps(result)


def tool_aptos_view(arguments: dict[str, Any]) -> str:
    function = arguments["function"]
    type_args = arguments.get("type_arguments", [])
    args = arguments.get("arguments", [])
    path = f"{aptos_url()}/view"
    body = {"function": function, "type_arguments": type_args, "arguments": args}
    import urllib.request

    request = urllib.request.Request(
        path,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))
    return json.dumps(result)


TOOLS = {
    "sui_getObject": {
        "description": "Read Sui object by ID.",
        "handler": tool_sui_get_object,
        "schema": {
            "type": "object",
            "required": ["object_id"],
            "properties": {"object_id": {"type": "string"}},
        },
    },
    "aptos_view": {
        "description": "Call Aptos view function.",
        "handler": tool_aptos_view,
        "schema": {
            "type": "object",
            "required": ["function", "type_arguments", "arguments"],
            "properties": {
                "function": {"type": "string"},
                "type_arguments": {"type": "array"},
                "arguments": {"type": "array"},
            },
        },
    },
}


if __name__ == "__main__":
    raise SystemExit(run_mcp_server(TOOLS, "move-rpc-server"))
