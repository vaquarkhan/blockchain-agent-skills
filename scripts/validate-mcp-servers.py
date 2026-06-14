#!/usr/bin/env python3
"""Verify MCP servers implement all tools declared in tool-schemas.json."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVERS = [
    "mcp/evm-rpc-server/server.py",
    "mcp/solana-rpc-server/server.py",
    "mcp/near-rpc-server/server.py",
    "mcp/cosmos-rpc-server/server.py",
    "mcp/move-rpc-server/server.py",
    "mcp/bitcoin-rpc-server/server.py",
    "mcp/ton-rpc-server/server.py",
    "mcp/substrate-rpc-server/server.py",
]


def load_module(relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(path.stem + path.parent.name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {relative_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def schema_tools(server_py: str) -> set[str]:
    schema_path = ROOT / Path(server_py).parent / "tool-schemas.json"
    if not schema_path.exists():
        raise RuntimeError(f"missing {schema_path}")
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    return {item["name"] for item in data["tools"]}


def main() -> int:
    errors: list[str] = []
    total_tools = 0

    for server in SERVERS:
        try:
            module = load_module(server)
            tools = getattr(module, "TOOLS", None)
            if not isinstance(tools, dict) or not tools:
                raise RuntimeError("missing non-empty TOOLS dict")
            expected = schema_tools(server)
            actual = set(tools.keys())
            if expected != actual:
                missing = sorted(expected - actual)
                extra = sorted(actual - expected)
                details = []
                if missing:
                    details.append(f"missing {missing}")
                if extra:
                    details.append(f"extra {extra}")
                raise RuntimeError("; ".join(details))
            total_tools += len(tools)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{server}: {exc}")

    if errors:
        print("MCP server validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"MCP server validation passed ({len(SERVERS)} servers, {total_tools} tools, schema parity OK).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
