"""Bedrock Lambda action implementations."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from lib.chain_providers import resolve_chain, validate_address  # noqa: E402

SKILL_NAMES = [
    "using-blockchain-agent-skills",
    "chain-abstraction",
    "transaction-lifecycle",
    "block-state-queries",
    "smart-contract-factory",
    "event-indexing",
    "token-standards-engine",
    "rollup-operations",
    "data-availability",
    "privacy-zk",
    "storage-state-proofs",
    "consensus-validator-ops",
    "network-monitoring",
]


def route_skill(intent: str) -> dict[str, Any]:
    intent_lower = intent.lower()
    if any(word in intent_lower for word in ("deploy", "contract", "upgrade")):
        skill = "smart-contract-factory"
    elif any(word in intent_lower for word in ("send", "broadcast", "transfer", "tx")):
        skill = "transaction-lifecycle"
    elif any(word in intent_lower for word in ("balance", "read", "query", "block")):
        skill = "block-state-queries"
    elif any(word in intent_lower for word in ("validator", "stake", "slashing")):
        skill = "consensus-validator-ops"
    else:
        skill = "chain-abstraction"
    return {"primary_skill": skill, "intent": intent, "next": f"skills/{skill}/SKILL.md"}


def list_skills() -> dict[str, Any]:
    return {"skills": SKILL_NAMES, "count": len(SKILL_NAMES)}


def resolve_chain_action(chain_name: str) -> dict[str, Any]:
    meta = resolve_chain(chain_name)
    return {
        "name": meta.name,
        "chain_id": meta.chain_id,
        "vm_type": meta.vm_type.value,
        "mcp_server": meta.mcp_server,
        "confirmation_depth": meta.confirmation_depth,
        "native_currency": meta.native_currency,
    }


def validate_address_action(chain_name: str, address: str) -> dict[str, Any]:
    valid = validate_address(chain_name, address)
    return {"chain_name": chain_name, "address": address, "valid": valid}


def plan_transaction(chain_name: str, operation: str) -> dict[str, Any]:
    meta = resolve_chain(chain_name)
    return {
        "chain_name": chain_name,
        "operation": operation,
        "mcp_server": meta.mcp_server,
        "templates": ["templates/tx-plan.yaml", "templates/simulate-evidence.yaml"],
        "lifecycle": ["plan", "simulate", "confirm", "broadcast", "confirm-depth"],
    }


def check_simulate_ready(chain_name: str) -> dict[str, Any]:
    return {
        "chain_name": chain_name,
        "required": ["templates/tx-plan.yaml", "SIMULATE_PASSED or SIMULATION_RUN_ID before broadcast"],
        "guardrails": [
            "guardrails/transaction-safety.yaml",
            "guardrails/security.yaml",
            "guardrails/compliance.yaml",
        ],
    }


def query_plan(chain_name: str, query_type: str) -> dict[str, Any]:
    meta = resolve_chain(chain_name)
    tool_map = {
        "balance": "eth_getBalance",
        "call": "eth_call",
        "logs": "eth_getLogs",
        "receipt": "eth_getTransactionReceipt",
    }
    return {"chain_name": chain_name, "query_type": query_type, "suggested_tool": tool_map.get(query_type, "eth_call"), "mcp_server": meta.mcp_server}


def deploy_checklist(chain_name: str, language: str) -> dict[str, Any]:
    return {
        "chain_name": chain_name,
        "language": language,
        "templates": ["templates/contract-audit-checklist.yaml", "templates/mainnet-readiness.yaml"],
    }


def index_plan(chain_name: str, contract_address: str) -> dict[str, Any]:
    return {
        "chain_name": chain_name,
        "contract_address": contract_address,
        "tools": ["eth_getLogs"],
        "references": ["references/mcp-blockchain-rpc-patterns.md"],
    }


def token_standard_info(chain_name: str) -> dict[str, Any]:
    meta = resolve_chain(chain_name)
    return {"chain_name": chain_name, "token_standards": list(meta.token_standards), "mcp_server": meta.mcp_server}


def rollup_route(l2_chain: str) -> dict[str, Any]:
    return {"l2_chain": l2_chain, "templates": ["templates/bridge-transfer-plan.yaml"]}


def da_posture(da_layer: str) -> dict[str, Any]:
    return {"da_layer": da_layer, "skill": "data-availability", "references": ["docs/coverage-roadmap.md"]}


def zk_workflow(proof_system: str) -> dict[str, Any]:
    return {"proof_system": proof_system, "skill": "privacy-zk", "human_confirm_required": True}


def proof_plan(chain_name: str) -> dict[str, Any]:
    return {"chain_name": chain_name, "tools": ["eth_getProof"], "mcp_server": "evm-rpc-server"}


def validator_rotation_plan(chain_name: str) -> dict[str, Any]:
    return {"chain_name": chain_name, "templates": ["templates/validator-rotation-plan.yaml"], "human_confirm_required": True}


def monitoring_plan(chain_name: str) -> dict[str, Any]:
    meta = resolve_chain(chain_name)
    return {"chain_name": chain_name, "mcp_server": meta.mcp_server, "hooks": ["hooks/mainnet-guard.sh"]}


ACTIONS: dict[str, Any] = {
    "routeSkill": lambda p: route_skill(p.get("intent", "")),
    "listSkills": lambda _p: list_skills(),
    "resolveChain": lambda p: resolve_chain_action(p["chain_name"]),
    "validateAddress": lambda p: validate_address_action(p["chain_name"], p["address"]),
    "planTransaction": lambda p: plan_transaction(p["chain_name"], p.get("operation", "transfer")),
    "checkSimulateReady": lambda p: check_simulate_ready(p["chain_name"]),
    "queryPlan": lambda p: query_plan(p["chain_name"], p.get("query_type", "balance")),
    "deployChecklist": lambda p: deploy_checklist(p["chain_name"], p.get("language", "solidity")),
    "indexPlan": lambda p: index_plan(p["chain_name"], p.get("contract_address", "")),
    "tokenStandardInfo": lambda p: token_standard_info(p["chain_name"]),
    "rollupRoute": lambda p: rollup_route(p.get("l2_chain", "base")),
    "daPosture": lambda p: da_posture(p.get("da_layer", "celestia")),
    "zkWorkflow": lambda p: zk_workflow(p.get("proof_system", "groth16")),
    "proofPlan": lambda p: proof_plan(p["chain_name"]),
    "validatorRotationPlan": lambda p: validator_rotation_plan(p["chain_name"]),
    "monitoringPlan": lambda p: monitoring_plan(p["chain_name"]),
}
