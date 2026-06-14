"""Tests for unified Bedrock Lambda handler."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "bedrock" / "lambda"))

spec = importlib.util.spec_from_file_location("handler", ROOT / "bedrock" / "lambda" / "handler.py")
assert spec and spec.loader
handler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handler)


def _invoke(function: str, parameters: list[dict[str, str]], action_group: str = "chain-abstraction") -> dict:
    event = {
        "messageVersion": "1.0",
        "actionGroup": action_group,
        "function": function,
        "parameters": parameters,
        "sessionId": "test",
    }
    return handler.lambda_handler(event)


def _body(result: dict) -> dict:
    raw = result["response"]["functionResponse"]["responseBody"]["application/json"]["body"]
    return json.loads(raw)


def test_resolve_chain():
    result = _invoke("resolveChain", [{"name": "chain_name", "value": "hedera"}])
    body = _body(result)
    assert "error" not in body
    assert body["mcp_server"] == "hedera-rpc-server"


def test_list_skills():
    result = _invoke("listSkills", [], action_group="using-blockchain-agent-skills")
    body = _body(result)
    assert body["count"] == 13


def test_route_skill():
    result = _invoke(
        "routeSkill",
        [{"name": "intent", "value": "deploy erc20 on base"}],
        action_group="using-blockchain-agent-skills",
    )
    body = _body(result)
    assert body["primary_skill"] == "smart-contract-factory"


if __name__ == "__main__":
    test_resolve_chain()
    test_list_skills()
    test_route_skill()
    print("All 3 Bedrock handler tests passed")
