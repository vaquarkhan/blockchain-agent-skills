#!/usr/bin/env python3
"""MCP stdio server for EVM RPC tools (read + guarded write)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

SHARED = Path(__file__).resolve().parent.parent / "_shared"
sys.path.insert(0, str(SHARED))

from guardrails import require_human_mainnet_confirm, require_simulation_evidence  # noqa: E402
from mcp_stdio import run_mcp_server  # noqa: E402
from rpc_client import RpcError, env_url, rpc_call  # noqa: E402

CHAIN_ENV = {
    "ethereum": ("ALCHEMY_ETH_URL", "INFURA_ETH_URL", "EVM_RPC_URL"),
    "arbitrum": ("ALCHEMY_ARB_URL", "EVM_ARB_RPC_URL"),
    "base": ("ALCHEMY_BASE_URL", "EVM_BASE_RPC_URL"),
    "polygon": ("ALCHEMY_POLYGON_URL", "EVM_POLYGON_RPC_URL"),
}


def chain_url(chain: str) -> str:
    keys = CHAIN_ENV.get(chain.lower())
    if not keys:
        raise RpcError(f"Unsupported chain: {chain}")
    return env_url(*keys)


def chain(arguments: dict[str, Any]) -> str:
    return arguments.get("chain", "ethereum")


def tool_eth_block_number(arguments: dict[str, Any]) -> str:
    name = chain(arguments)
    result = rpc_call(chain_url(name), "eth_blockNumber", [])
    return json.dumps({"chain": name, "blockNumber": result})


def tool_eth_get_block_by_number(arguments: dict[str, Any]) -> str:
    name = chain(arguments)
    block = arguments["block"]
    full = arguments.get("full_transactions", False)
    result = rpc_call(chain_url(name), "eth_getBlockByNumber", [block, full])
    return json.dumps({"chain": name, "block": result})


def tool_eth_get_balance(arguments: dict[str, Any]) -> str:
    name = chain(arguments)
    address = arguments["address"]
    block = arguments.get("block", "latest")
    result = rpc_call(chain_url(name), "eth_getBalance", [address, block])
    return json.dumps({"chain": name, "address": address, "balanceWei": result, "block": block})


def tool_eth_call(arguments: dict[str, Any]) -> str:
    name = chain(arguments)
    call_obj: dict[str, Any] = {"to": arguments["to"], "data": arguments["data"]}
    if arguments.get("from"):
        call_obj["from"] = arguments["from"]
    block = arguments.get("block", "latest")
    result = rpc_call(chain_url(name), "eth_call", [call_obj, block])
    return json.dumps({"chain": name, "result": result})


def tool_eth_estimate_gas(arguments: dict[str, Any]) -> str:
    name = chain(arguments)
    tx_obj: dict[str, Any] = {"to": arguments["to"], "data": arguments["data"]}
    if arguments.get("from"):
        tx_obj["from"] = arguments["from"]
    result = rpc_call(chain_url(name), "eth_estimateGas", [tx_obj])
    return json.dumps({"chain": name, "gas": result})


def tool_eth_get_logs(arguments: dict[str, Any]) -> str:
    name = chain(arguments)
    result = rpc_call(chain_url(name), "eth_getLogs", [arguments["filter"]])
    return json.dumps({"chain": name, "logs": result})


def tool_eth_get_storage_at(arguments: dict[str, Any]) -> str:
    name = chain(arguments)
    block = arguments.get("block", "latest")
    result = rpc_call(
        chain_url(name),
        "eth_getStorageAt",
        [arguments["address"], arguments["slot"], block],
    )
    return json.dumps({"chain": name, "value": result})


def tool_eth_get_transaction_receipt(arguments: dict[str, Any]) -> str:
    name = chain(arguments)
    result = rpc_call(chain_url(name), "eth_getTransactionReceipt", [arguments["tx_hash"]])
    return json.dumps({"chain": name, "receipt": result})


def tool_debug_trace_call(arguments: dict[str, Any]) -> str:
    name = chain(arguments)
    call_obj: dict[str, Any] = {"to": arguments["to"], "data": arguments["data"]}
    if arguments.get("from"):
        call_obj["from"] = arguments["from"]
    block = arguments.get("block", "latest")
    trace_opts = {"tracer": "callTracer"}
    result = rpc_call(chain_url(name), "debug_traceCall", [call_obj, block, trace_opts])
    return json.dumps({"chain": name, "trace": result})


def tool_eth_get_proof(arguments: dict[str, Any]) -> str:
    name = chain(arguments)
    block = arguments.get("block", "latest")
    storage_keys = arguments.get("storage_keys", [])
    result = rpc_call(
        chain_url(name),
        "eth_getProof",
        [arguments["address"], storage_keys, block],
    )
    return json.dumps({"chain": name, "proof": result})


def tool_eth_send_raw_transaction(arguments: dict[str, Any]) -> str:
    name = chain(arguments)
    network = arguments.get("network", name)
    require_simulation_evidence("eth_sendRawTransaction")
    require_human_mainnet_confirm("eth_sendRawTransaction", network)
    raw = arguments["raw_transaction"]
    if not raw.startswith("0x"):
        raw = "0x" + raw
    result = rpc_call(chain_url(name), "eth_sendRawTransaction", [raw])
    return json.dumps({"chain": name, "txHash": result})


TOOLS = {
    "eth_blockNumber": {
        "description": "Returns latest block number for configured EVM chain.",
        "handler": tool_eth_block_number,
        "schema": {"type": "object", "properties": {"chain": {"type": "string"}}},
    },
    "eth_getBlockByNumber": {
        "description": "Returns block header and optional transaction hashes.",
        "handler": tool_eth_get_block_by_number,
        "schema": {
            "type": "object",
            "required": ["block"],
            "properties": {
                "chain": {"type": "string"},
                "block": {"type": "string"},
                "full_transactions": {"type": "boolean"},
            },
        },
    },
    "eth_getBalance": {
        "description": "Returns native balance for an address.",
        "handler": tool_eth_get_balance,
        "schema": {
            "type": "object",
            "required": ["address"],
            "properties": {
                "chain": {"type": "string"},
                "address": {"type": "string"},
                "block": {"type": "string"},
            },
        },
    },
    "eth_call": {
        "description": "Simulate a contract call without broadcasting.",
        "handler": tool_eth_call,
        "schema": {
            "type": "object",
            "required": ["to", "data"],
            "properties": {
                "chain": {"type": "string"},
                "to": {"type": "string"},
                "data": {"type": "string"},
                "from": {"type": "string"},
                "block": {"type": "string"},
            },
        },
    },
    "eth_estimateGas": {
        "description": "Estimate gas for a transaction payload.",
        "handler": tool_eth_estimate_gas,
        "schema": {
            "type": "object",
            "required": ["to", "data"],
            "properties": {
                "chain": {"type": "string"},
                "to": {"type": "string"},
                "data": {"type": "string"},
                "from": {"type": "string"},
            },
        },
    },
    "eth_getLogs": {
        "description": "Query event logs with filter object.",
        "handler": tool_eth_get_logs,
        "schema": {
            "type": "object",
            "required": ["filter"],
            "properties": {"chain": {"type": "string"}, "filter": {"type": "object"}},
        },
    },
    "eth_getStorageAt": {
        "description": "Read contract storage slot.",
        "handler": tool_eth_get_storage_at,
        "schema": {
            "type": "object",
            "required": ["address", "slot"],
            "properties": {
                "chain": {"type": "string"},
                "address": {"type": "string"},
                "slot": {"type": "string"},
                "block": {"type": "string"},
            },
        },
    },
    "eth_getTransactionReceipt": {
        "description": "Fetch transaction receipt by hash.",
        "handler": tool_eth_get_transaction_receipt,
        "schema": {
            "type": "object",
            "required": ["tx_hash"],
            "properties": {"chain": {"type": "string"}, "tx_hash": {"type": "string"}},
        },
    },
    "debug_traceCall": {
        "description": "Trace a call execution (requires debug-enabled RPC).",
        "handler": tool_debug_trace_call,
        "schema": {
            "type": "object",
            "required": ["to", "data"],
            "properties": {
                "chain": {"type": "string"},
                "to": {"type": "string"},
                "data": {"type": "string"},
                "from": {"type": "string"},
                "block": {"type": "string"},
            },
        },
    },
    "eth_getProof": {
        "description": "Returns account and storage Merkle proofs.",
        "handler": tool_eth_get_proof,
        "schema": {
            "type": "object",
            "required": ["address"],
            "properties": {
                "chain": {"type": "string"},
                "address": {"type": "string"},
                "storage_keys": {"type": "array", "items": {"type": "string"}},
                "block": {"type": "string"},
            },
        },
    },
    "eth_sendRawTransaction": {
        "description": "Broadcast KMS-signed raw transaction (requires simulate-first guardrails).",
        "handler": tool_eth_send_raw_transaction,
        "schema": {
            "type": "object",
            "required": ["raw_transaction"],
            "properties": {
                "chain": {"type": "string"},
                "raw_transaction": {"type": "string"},
                "network": {"type": "string"},
            },
        },
    },
}


if __name__ == "__main__":
    raise SystemExit(run_mcp_server(TOOLS, "evm-rpc-server"))
