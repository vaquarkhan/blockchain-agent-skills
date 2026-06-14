#!/usr/bin/env python3
"""MCP stdio server for NEAR RPC tools."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

SHARED = Path(__file__).resolve().parent.parent / "_shared"
sys.path.insert(0, str(SHARED))

from guardrails import require_simulation_evidence  # noqa: E402
from mcp_stdio import run_mcp_server  # noqa: E402
from rpc_client import RpcError, env_url, rpc_call  # noqa: E402


def near_url() -> str:
    return env_url("NEAR_RPC_URL", default="https://rpc.mainnet.near.org")


def finality(arguments: dict[str, Any]) -> str:
    return arguments.get("finality", "final")


def tool_view_account(arguments: dict[str, Any]) -> str:
    account_id = arguments["account_id"]
    result = rpc_call(
        near_url(),
        "query",
        {
            "request_type": "view_account",
            "finality": finality(arguments),
            "account_id": account_id,
        },
    )
    return json.dumps({"account_id": account_id, "account": result})


def tool_query(arguments: dict[str, Any]) -> str:
    account_id = arguments["account_id"]
    method_name = arguments["method_name"]
    args_base64 = arguments.get("args_base64", "")
    result = rpc_call(
        near_url(),
        "query",
        {
            "request_type": arguments.get("request_type", "call_function"),
            "finality": finality(arguments),
            "account_id": account_id,
            "method_name": method_name,
            "args_base64": args_base64,
        },
    )
    return json.dumps({"account_id": account_id, "method_name": method_name, "result": result})


def tool_view_access_key(arguments: dict[str, Any]) -> str:
    account_id = arguments["account_id"]
    public_key = arguments["public_key"]
    result = rpc_call(
        near_url(),
        "query",
        {
            "request_type": "view_access_key",
            "finality": finality(arguments),
            "account_id": account_id,
            "public_key": public_key,
        },
    )
    return json.dumps({"account_id": account_id, "public_key": public_key, "access_key": result})


def tool_send_tx(arguments: dict[str, Any]) -> str:
    require_simulation_evidence("send_tx")
    signed = arguments["signed_tx_base64"]
    result = rpc_call(near_url(), "broadcast_tx_commit", [signed])
    return json.dumps({"result": result})


TOOLS = {
    "view_account": {
        "description": "View NEAR account balance and storage.",
        "handler": tool_view_account,
        "schema": {
            "type": "object",
            "required": ["account_id"],
            "properties": {
                "account_id": {"type": "string"},
                "finality": {"type": "string"},
            },
        },
    },
    "query": {
        "description": "Call view method on NEAR contract.",
        "handler": tool_query,
        "schema": {
            "type": "object",
            "required": ["account_id", "method_name"],
            "properties": {
                "request_type": {"type": "string"},
                "account_id": {"type": "string"},
                "method_name": {"type": "string"},
                "args_base64": {"type": "string"},
                "finality": {"type": "string"},
            },
        },
    },
    "view_access_key": {
        "description": "View access key nonce and allowance.",
        "handler": tool_view_access_key,
        "schema": {
            "type": "object",
            "required": ["account_id", "public_key"],
            "properties": {
                "account_id": {"type": "string"},
                "public_key": {"type": "string"},
                "finality": {"type": "string"},
            },
        },
    },
    "send_tx": {
        "description": "Broadcast signed NEAR transaction.",
        "handler": tool_send_tx,
        "schema": {
            "type": "object",
            "required": ["signed_tx_base64"],
            "properties": {"signed_tx_base64": {"type": "string"}},
        },
    },
}


if __name__ == "__main__":
    raise SystemExit(run_mcp_server(TOOLS, "near-rpc-server"))
