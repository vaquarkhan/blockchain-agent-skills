"""Shared MCP stdio JSON-RPC loop for blockchain RPC servers."""

from __future__ import annotations

import json
import sys
from typing import Any, Callable


ToolHandler = Callable[[dict[str, Any]], str]


def run_mcp_server(tools: dict[str, dict[str, Any]], server_name: str, version: str = "0.3.0") -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        handle_message(json.loads(line), tools, server_name, version)
    return 0


def send(message: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(message) + "\n")
    sys.stdout.flush()


def handle_message(
    message: dict[str, Any],
    tools: dict[str, dict[str, Any]],
    server_name: str,
    version: str,
) -> None:
    msg_id = message.get("id")
    method = message.get("method", "")
    params = message.get("params", {})

    if method == "initialize":
        send(
            {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": server_name, "version": version},
                },
            }
        )
        return

    if method == "notifications/initialized":
        return

    if method == "tools/list":
        listed = [
            {
                "name": name,
                "description": meta["description"],
                "inputSchema": meta["schema"],
            }
            for name, meta in tools.items()
        ]
        send({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": listed}})
        return

    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        meta = tools.get(tool_name)
        if not meta:
            send(
                {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
                }
            )
            return
        handler: ToolHandler = meta["handler"]
        try:
            content = handler(arguments)
            send(
                {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": content}], "isError": False},
                }
            )
        except Exception as exc:  # noqa: BLE001
            send(
                {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": str(exc)}],
                        "isError": True,
                    },
                }
            )
        return

    if msg_id is not None:
        send({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": method}})
