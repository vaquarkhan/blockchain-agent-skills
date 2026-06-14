#!/usr/bin/env python3
"""Shared JSON-RPC HTTP client for blockchain MCP servers."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


class RpcError(RuntimeError):
    pass


def rpc_call(url: str, method: str, params: list[Any] | dict[str, Any] | None = None, timeout: int = 30) -> Any:
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params if params is not None else []}
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RpcError(f"HTTP {exc.code} from RPC endpoint") from exc
    except urllib.error.URLError as exc:
        raise RpcError(f"RPC unreachable: {exc.reason}") from exc

    if "error" in body:
        raise RpcError(json.dumps(body["error"]))
    return body.get("result")


def env_url(*names: str, default: str = "") -> str:
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    if default:
        return default
    raise RpcError(f"Missing RPC URL env var; set one of: {', '.join(names)}")
