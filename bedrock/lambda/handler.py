#!/usr/bin/env python3
"""Unified Bedrock AgentCore Lambda handler for blockchain skills."""

from __future__ import annotations

import json
import traceback
from typing import Any

from actions import ACTIONS
from audit import audit_log


def _params_to_dict(parameters: list[dict[str, Any]] | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in parameters or []:
        name = item.get("name")
        if name:
            result[name] = str(item.get("value", ""))
    return result


def _response(event: dict[str, Any], body: dict[str, Any]) -> dict[str, Any]:
    return {
        "messageVersion": event.get("messageVersion", "1.0"),
        "response": {
            "actionGroup": event.get("actionGroup"),
            "function": event.get("function"),
            "functionResponse": {
                "responseBody": {"application/json": {"body": json.dumps(body)}}
            },
        },
    }


def lambda_handler(event: dict[str, Any], context: Any = None) -> dict[str, Any]:
    _ = context
    function = event.get("function", "")
    params = _params_to_dict(event.get("parameters"))
    try:
        action = ACTIONS.get(function)
        if not action:
            body = {"error": f"Unknown function: {function}", "available": sorted(ACTIONS.keys())}
            return _response(event, body)
        body = action(params)
        audit_log(event, function, body)
        return _response(event, body)
    except Exception as exc:  # noqa: BLE001
        body = {"error": str(exc), "trace": traceback.format_exc(limit=3)}
        return _response(event, body)


if __name__ == "__main__":
    sample = {
        "messageVersion": "1.0",
        "actionGroup": "chain-abstraction",
        "function": "resolveChain",
        "parameters": [{"name": "chain_name", "value": "ethereum"}],
        "sessionId": "local-test",
    }
    print(json.dumps(lambda_handler(sample), indent=2))
