"""Write-operation guardrails for MCP broadcast tools."""

from __future__ import annotations

import os


class GuardrailError(RuntimeError):
    pass


def require_simulation_evidence(tool_name: str) -> None:
    """Block writes unless simulate-first evidence is present in environment."""
    if os.environ.get("BLOCKCHAIN_ALLOW_WRITE", "").lower() in {"1", "true", "yes"}:
        return
    if os.environ.get("SIMULATE_PASSED", "").lower() in {"1", "true", "yes"}:
        return
    if os.environ.get("SIMULATION_RUN_ID", "").strip():
        return
    raise GuardrailError(
        f"{tool_name} blocked: set SIMULATE_PASSED=true or SIMULATION_RUN_ID after successful simulation. "
        "Never pass private keys through MCP."
    )


def require_human_mainnet_confirm(tool_name: str, network: str | None = None) -> None:
    network_value = (network or os.environ.get("NETWORK", "")).lower()
    if "mainnet" not in network_value and os.environ.get("CHAIN_ENV", "").lower() not in {
        "mainnet",
        "production",
    }:
        return
    if os.environ.get("HUMAN_CONFIRMED", "").lower() in {"1", "true", "yes"}:
        return
    raise GuardrailError(
        f"{tool_name} blocked on mainnet: set HUMAN_CONFIRMED=true after human approval."
    )
