#!/usr/bin/env python3
"""Generate per-skill Bedrock artifacts from bedrock/manifest.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "bedrock" / "manifest.json"

HANDLER_WRAPPER = '''#!/usr/bin/env python3
"""Bedrock Lambda entrypoint for {skill_name}."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HANDLER = ROOT / "bedrock" / "lambda" / "handler.py"
sys.path.insert(0, str(HANDLER.parent))

spec = importlib.util.spec_from_file_location("bedrock_handler", HANDLER)
if spec is None or spec.loader is None:
    raise RuntimeError("Cannot load bedrock handler")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

lambda_handler = module.lambda_handler
'''

TEST_TEMPLATE = '''"""Tests for {skill_name} Bedrock handler."""

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


def test_{function}_action():
    event = {{
        "messageVersion": "1.0",
        "actionGroup": "{skill_name}",
        "function": "{function}",
        "parameters": {parameters},
        "sessionId": "test",
    }}
    result = mod.lambda_handler(event)
    body = json.loads(result["response"]["functionResponse"]["responseBody"]["application/json"]["body"])
    assert "error" not in body
'''


def openapi_for_skill(skill: dict) -> dict:
    paths = {}
    for fn in skill["functions"]:
        props = {}
        required = []
        for param in fn["parameters"]:
            props[param] = {"type": "string"}
            required.append(param)
        paths[f"/{fn['name']}"] = {
            "post": {
                "operationId": fn["name"],
                "summary": fn["description"],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"type": "object", "properties": props, "required": required}
                        }
                    },
                },
                "responses": {"200": {"description": "Success"}},
            }
        }
    return {"openapi": "3.0.0", "info": {"title": skill["name"], "version": "0.4.0"}, "paths": paths}


def action_group_for_skill(skill: dict) -> dict:
    functions = []
    for fn in skill["functions"]:
        params = []
        for param in fn["parameters"]:
            params.append({"name": param, "type": "string", "required": True})
        functions.append({"name": fn["name"], "description": fn["description"], "parameters": params})
    return {
        "actionGroupName": skill["name"],
        "description": f"Bedrock action group for {skill['name']}",
        "actionGroupExecutor": {"lambda": f"arn:aws:lambda:{{region}}:{{account}}:function:blockchain-{skill['name']}"},
        "functionSchema": {"functions": functions},
    }


def skill_definition(skill: dict) -> str:
    lines = [
        f"name: {skill['name']}",
        'version: "0.4.0"',
        f"phase: {skill['phase']}",
        "frameworks:",
        "  - bedrock-agentcore",
        "  - mcp",
        "mcp_tools:",
    ]
    for tool in skill.get("mcp_tools", []):
        lines.append(f"  - {tool}")
    lines.extend(
        [
            "guardrail_refs:",
            "  - guardrails/transaction-safety.yaml",
            "  - guardrails/security.yaml",
            "  - guardrails/compliance.yaml",
            "bedrock:",
            "  handler: bedrock/lambda/handler.py",
            "  action_group: action-group.json",
            "  openapi: openapi.yaml",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for skill in manifest["skills"]:
        skill_dir = ROOT / "skills" / skill["name"]
        if not skill_dir.exists():
            print(f"skip missing skill dir: {skill_dir}")
            continue
        (skill_dir / "skill-definition.yaml").write_text(skill_definition(skill), encoding="utf-8")
        (skill_dir / "action-group.json").write_text(
            json.dumps(action_group_for_skill(skill), indent=2) + "\n", encoding="utf-8"
        )
        (skill_dir / "openapi.yaml").write_text(
            json.dumps(openapi_for_skill(skill), indent=2) + "\n", encoding="utf-8"
        )
        lambda_dir = skill_dir / "lambda"
        lambda_dir.mkdir(exist_ok=True)
        (lambda_dir / "handler.py").write_text(
            HANDLER_WRAPPER.format(skill_name=skill["name"]), encoding="utf-8"
        )
        tests_dir = skill_dir / "tests"
        tests_dir.mkdir(exist_ok=True)
        if skill["functions"]:
            fn = skill["functions"][0]
            params = []
            defaults = {
                "chain_name": "ethereum",
                "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0",
                "intent": "send token on arbitrum",
                "operation": "transfer",
                "query_type": "balance",
                "language": "solidity",
                "contract_address": "0x0000000000000000000000000000000000000000",
                "l2_chain": "base",
                "da_layer": "celestia",
                "proof_system": "groth16",
            }
            for param in fn["parameters"]:
                params.append({"name": param, "value": defaults.get(param, "test")})
            test_code = TEST_TEMPLATE.format(
                skill_name=skill["name"],
                function=fn["name"],
                parameters=json.dumps(params),
            )
            (tests_dir / "test_handler.py").write_text(test_code, encoding="utf-8")
    print(f"Generated Bedrock artifacts for {len(manifest['skills'])} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
