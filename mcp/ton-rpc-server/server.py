#!/usr/bin/env python3
"""MCP server for TON HTTP API."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import urlopen

SHARED = Path(__file__).resolve().parent.parent / "_shared"
sys.path.insert(0, str(SHARED))

from mcp_stdio import run_mcp_server  # noqa: E402
from rpc_client import env_url  # noqa: E402


def ton_base() -> str:
    return env_url("TON_API_URL", default="https://toncenter.com/api/v2").rstrip("/")


def tool_get_address_information(arguments: dict[str, Any]) -> str:
    address = quote(arguments["address"], safe="")
    with urlopen(f"{ton_base()}/getAddressInformation?address={address}", timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))
    return json.dumps(result)


TOOLS = {
    "getAddressInformation": {
        "description": "Returns TON address balance and state.",
        "handler": tool_get_address_information,
        "schema": {
            "type": "object",
            "required": ["address"],
            "properties": {"address": {"type": "string"}},
        },
    },
}


if __name__ == "__main__":
    raise SystemExit(run_mcp_server(TOOLS, "ton-rpc-server"))
