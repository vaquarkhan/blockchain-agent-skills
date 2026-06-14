#!/usr/bin/env python3
"""MCP stdio server for Cosmos SDK REST/RPC tools."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen

SHARED = Path(__file__).resolve().parent.parent / "_shared"
sys.path.insert(0, str(SHARED))

from guardrails import require_simulation_evidence  # noqa: E402
from mcp_stdio import run_mcp_server  # noqa: E402
from rpc_client import RpcError, env_url  # noqa: E402


def cosmos_base() -> str:
    return env_url("COSMOS_RPC_URL", default="https://rpc.cosmos.directory/cosmoshub").rstrip("/")


def http_get(path: str) -> Any:
    with urlopen(f"{cosmos_base()}{path}", timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def http_post(path: str, payload: dict[str, Any]) -> Any:
    body = json.dumps(payload).encode("utf-8")
    request = Request(
        f"{cosmos_base()}{path}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def tool_broadcast_tx(arguments: dict[str, Any]) -> str:
    require_simulation_evidence("broadcast_tx")
    chain_id = arguments["chain_id"]
    tx_bytes = arguments["tx_bytes_base64"]
    payload = {
        "tx_bytes": tx_bytes,
        "mode": "BROADCAST_MODE_SYNC",
    }
    result = http_post("/cosmos/tx/v1beta1/txs", payload)
    return json.dumps({"chain_id": chain_id, "broadcast": result})


def tool_abci_query(arguments: dict[str, Any]) -> str:
    path = quote(arguments["path"], safe="")
    data = arguments.get("data_base64", "")
    height = arguments.get("height", "0")
    result = http_get(f"/abci_query?path={path}&data={data}&height={height}")
    return json.dumps(result)


def tool_query_client_state(arguments: dict[str, Any]) -> str:
    client_id = arguments["client_id"]
    result = http_get(f"/ibc/core/client/v1/client_states/{client_id}")
    return json.dumps(result)


def tool_ibc_transfer(arguments: dict[str, Any]) -> str:
    """Build unsigned ICS-20 transfer plan (signing happens via KMS outside MCP)."""
    plan = {
        "type": "ics20_transfer_plan",
        "source_port": arguments.get("source_port", "transfer"),
        "source_channel": arguments["source_channel"],
        "token": {"denom": arguments["token_denom"], "amount": arguments["amount"]},
        "sender": arguments["sender"],
        "receiver": arguments["receiver"],
        "timeout_height": arguments.get("timeout_height"),
        "memo": arguments.get("memo", ""),
        "next_steps": [
            "Simulate MsgTransfer with node simulate endpoint",
            "Sign with KMS",
            "broadcast_tx with tx_bytes_base64 after SIMULATE_PASSED=true",
        ],
    }
    return json.dumps(plan)


TOOLS = {
    "broadcast_tx": {
        "description": "Broadcast signed Cosmos SDK transaction.",
        "handler": tool_broadcast_tx,
        "schema": {
            "type": "object",
            "required": ["chain_id", "tx_bytes_base64"],
            "properties": {
                "chain_id": {"type": "string"},
                "tx_bytes_base64": {"type": "string"},
            },
        },
    },
    "abci_query": {
        "description": "Query CosmWasm contract or module state.",
        "handler": tool_abci_query,
        "schema": {
            "type": "object",
            "required": ["path"],
            "properties": {
                "path": {"type": "string"},
                "data_base64": {"type": "string"},
                "height": {"type": "string"},
            },
        },
    },
    "query_client_state": {
        "description": "Query IBC client state.",
        "handler": tool_query_client_state,
        "schema": {
            "type": "object",
            "required": ["client_id"],
            "properties": {"client_id": {"type": "string"}},
        },
    },
    "ibc_transfer": {
        "description": "Build ICS-20 transfer plan for simulate-sign-broadcast workflow.",
        "handler": tool_ibc_transfer,
        "schema": {
            "type": "object",
            "required": ["source_channel", "token_denom", "amount", "sender", "receiver"],
            "properties": {
                "source_port": {"type": "string"},
                "source_channel": {"type": "string"},
                "token_denom": {"type": "string"},
                "amount": {"type": "string"},
                "sender": {"type": "string"},
                "receiver": {"type": "string"},
                "timeout_height": {"type": "object"},
                "memo": {"type": "string"},
            },
        },
    },
}


if __name__ == "__main__":
    raise SystemExit(run_mcp_server(TOOLS, "cosmos-rpc-server"))
