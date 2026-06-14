"""Tests for smart-contract-factory Bedrock handler."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "bedrock" / "lambda"))

spec = importlib.util.spec_from_file_location("handler", ROOT / "bedrock" / "lambda" / "handler.py")
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_deployChecklist_action():
    event = {
        "messageVersion": "1.0",
        "actionGroup": "smart-contract-factory",
        "function": "deployChecklist",
        "parameters": [{"name": "chain_name", "value": "ethereum"}, {"name": "language", "value": "solidity"}],
        "sessionId": "test",
    }
    result = mod.lambda_handler(event)
    body = json.loads(result["response"]["functionResponse"]["responseBody"]["application/json"]["body"])
    assert "error" not in body
