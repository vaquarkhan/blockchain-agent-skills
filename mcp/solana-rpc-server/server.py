#!/usr/bin/env python3
"""MCP stdio server for Solana RPC tools."""

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


def solana_url() -> str:
    return env_url("SOLANA_RPC_URL", default="https://api.mainnet-beta.solana.com")


def commitment(arguments: dict[str, Any]) -> str:
    return arguments.get("commitment", "confirmed")


def tool_get_account_info(arguments: dict[str, Any]) -> str:
    pubkey = arguments["pubkey"]
    config = {"encoding": "jsonParsed", "commitment": commitment(arguments)}
    result = rpc_call(solana_url(), "getAccountInfo", [pubkey, config])
    return json.dumps({"pubkey": pubkey, "account": result.get("value")})


def tool_simulate_transaction(arguments: dict[str, Any]) -> str:
    tx = arguments["transaction"]
    encoding = arguments.get("encoding", "base64")
    config = {
        "encoding": encoding,
        "sigVerify": False,
        "replaceRecentBlockhash": True,
        "commitment": commitment(arguments),
    }
    result = rpc_call(solana_url(), "simulateTransaction", [tx, config])
    return json.dumps(result)


def tool_send_transaction(arguments: dict[str, Any]) -> str:
    require_simulation_evidence("sendTransaction")
    tx = arguments["transaction"]
    skip = arguments.get("skipPreflight", False)
    config = {"encoding": "base64", "skipPreflight": skip, "preflightCommitment": commitment(arguments)}
    result = rpc_call(solana_url(), "sendTransaction", [tx, config])
    return json.dumps({"signature": result})


def tool_get_token_accounts_by_owner(arguments: dict[str, Any]) -> str:
    owner = arguments["owner"]
    mint_filter: dict[str, str] = {}
    if arguments.get("mint"):
        mint_filter = {"mint": arguments["mint"]}
    config = {"encoding": "jsonParsed", "commitment": commitment(arguments)}
    result = rpc_call(solana_url(), "getTokenAccountsByOwner", [owner, mint_filter, config])
    return json.dumps({"owner": owner, "accounts": result.get("value", [])})


TOOLS = {
    "getAccountInfo": {
        "description": "Read Solana account data and lamport balance.",
        "handler": tool_get_account_info,
        "schema": {
            "type": "object",
            "required": ["pubkey"],
            "properties": {
                "pubkey": {"type": "string"},
                "commitment": {"type": "string"},
            },
        },
    },
    "simulateTransaction": {
        "description": "Simulate transaction before broadcast.",
        "handler": tool_simulate_transaction,
        "schema": {
            "type": "object",
            "required": ["transaction"],
            "properties": {
                "transaction": {"type": "string"},
                "encoding": {"type": "string"},
                "commitment": {"type": "string"},
            },
        },
    },
    "sendTransaction": {
        "description": "Broadcast signed transaction to Solana network.",
        "handler": tool_send_transaction,
        "schema": {
            "type": "object",
            "required": ["transaction"],
            "properties": {
                "transaction": {"type": "string"},
                "skipPreflight": {"type": "boolean"},
                "commitment": {"type": "string"},
            },
        },
    },
    "getTokenAccountsByOwner": {
        "description": "List SPL token accounts owned by wallet.",
        "handler": tool_get_token_accounts_by_owner,
        "schema": {
            "type": "object",
            "required": ["owner"],
            "properties": {
                "owner": {"type": "string"},
                "mint": {"type": "string"},
                "commitment": {"type": "string"},
            },
        },
    },
}


if __name__ == "__main__":
    raise SystemExit(run_mcp_server(TOOLS, "solana-rpc-server"))
