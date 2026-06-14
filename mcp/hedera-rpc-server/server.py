#!/usr/bin/env python3
"""MCP server for Hedera Mirror Node REST reads."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen

SHARED = Path(__file__).resolve().parent.parent / "_shared"
sys.path.insert(0, str(SHARED))

from mcp_stdio import run_mcp_server  # noqa: E402
from rpc_client import env_url  # noqa: E402


def mirror_base() -> str:
    return env_url("HEDERA_MIRROR_URL", default="https://mainnet-public.mirrornode.hedera.com/api/v1").rstrip("/")


def fetch_json(url: str) -> Any:
    with urlopen(Request(url, method="GET"), timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def tool_get_account(arguments: dict[str, Any]) -> str:
    account_id = quote(arguments["account_id"], safe="")
    result = fetch_json(f"{mirror_base()}/accounts/{account_id}")
    return json.dumps(result)


def tool_get_block(arguments: dict[str, Any]) -> str:
    block_number = quote(str(arguments["block_number"]), safe="")
    result = fetch_json(f"{mirror_base()}/blocks/{block_number}")
    return json.dumps(result)


TOOLS = {
    "getAccount": {
        "description": "Returns Hedera account balance and metadata from mirror node.",
        "handler": tool_get_account,
        "schema": {
            "type": "object",
            "required": ["account_id"],
            "properties": {"account_id": {"type": "string"}},
        },
    },
    "getBlock": {
        "description": "Returns Hedera block metadata by number.",
        "handler": tool_get_block,
        "schema": {
            "type": "object",
            "required": ["block_number"],
            "properties": {"block_number": {"type": "integer"}},
        },
    },
}


if __name__ == "__main__":
    raise SystemExit(run_mcp_server(TOOLS, "hedera-rpc-server"))
