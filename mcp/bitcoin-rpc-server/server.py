#!/usr/bin/env python3
"""MCP server for Bitcoin Core JSON-RPC read tools."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

SHARED = Path(__file__).resolve().parent.parent / "_shared"
sys.path.insert(0, str(SHARED))

from mcp_stdio import run_mcp_server  # noqa: E402
from rpc_client import RpcError, env_url, rpc_call  # noqa: E402


def btc_url() -> str:
    return env_url("BITCOIN_RPC_URL", default="http://127.0.0.1:8332")


def lnd_base() -> str:
    return env_url("LND_REST_URL", default="https://127.0.0.1:8080").rstrip("/")


def lnd_headers() -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    macaroon = os.environ.get("LND_MACAROON", "").strip()
    if macaroon:
        headers["Grpc-Metadata-macaroon"] = macaroon
    return headers


def lnd_request(method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
    url = f"{lnd_base()}{path}"
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(url, data=data, headers=lnd_headers(), method=method)
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise RpcError(f"LND REST error: {exc}") from exc


def tool_getblockchaininfo(arguments: dict[str, Any]) -> str:
    _ = arguments
    result = rpc_call(btc_url(), "getblockchaininfo", [])
    return json.dumps(result)


def tool_getrawtransaction(arguments: dict[str, Any]) -> str:
    txid = arguments["txid"]
    verbose = arguments.get("verbose", True)
    result = rpc_call(btc_url(), "getrawtransaction", [txid, verbose])
    return json.dumps(result)


def tool_lightning_getinfo(arguments: dict[str, Any]) -> str:
    _ = arguments
    result = lnd_request("GET", "/v1/getinfo")
    return json.dumps(result)


def tool_lightning_decodepay(arguments: dict[str, Any]) -> str:
    pay_req = arguments["pay_req"]
    result = lnd_request("POST", "/v1/payreq/decode", {"pay_req": pay_req})
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
    "lightning_getinfo": {
        "description": "Returns Lightning node info via LND REST.",
        "handler": tool_lightning_getinfo,
        "schema": {"type": "object", "properties": {}},
    },
    "lightning_decodepay": {
        "description": "Decodes a BOLT11 payment request via LND REST.",
        "handler": tool_lightning_decodepay,
        "schema": {
            "type": "object",
            "required": ["pay_req"],
            "properties": {"pay_req": {"type": "string"}},
        },
    },
}


if __name__ == "__main__":
    raise SystemExit(run_mcp_server(TOOLS, "bitcoin-rpc-server"))
