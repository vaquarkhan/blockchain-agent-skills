#!/usr/bin/env python3
"""Blockchain-only hook runner for session start and pre-broadcast guards."""

from __future__ import annotations

import argparse
import fnmatch
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run blockchain agent repository hooks.")
    parser.add_argument(
        "hook",
        choices=["session-start", "tx-simulate-pre", "mainnet-guard"],
    )
    parser.add_argument("workspace", nargs="?", default=".")
    return parser.parse_args()


def has_glob(workspace: Path, *patterns: str) -> bool:
    for path in workspace.rglob("*"):
        if any(part.startswith(".") and part not in {".github"} for part in path.parts):
            if ".git" in path.parts:
                continue
        relative = path.relative_to(workspace).as_posix()
        if any(fnmatch.fnmatch(relative, pattern) for pattern in patterns):
            return True
    return False


def is_toolkit_repo(workspace: Path) -> bool:
    return (workspace / "skills" / "using-blockchain-agent-skills" / "SKILL.md").exists()


def run_session_start(workspace: Path) -> int:
    print("\nBlockchain Hooks: session start")
    print(f"Workspace: {workspace}\n")
    if is_toolkit_repo(workspace):
        print("Start here:")
        print("- skills/using-blockchain-agent-skills/SKILL.md")
        print("- skills/transaction-lifecycle/SKILL.md")
        print("\nSuggested presets:")
        print("- presets/evm-core/PRESET.md")
        print("\nSuggested examples:")
        print("- examples/evm-erc20-deploy/")
        print("- examples/chain-provider-validation/")
        print("\nNext: /plan → /simulate → /confirm → /broadcast → /confirm-depth")
        return 0

    signals: list[str] = []
    if has_glob(workspace, "foundry.toml", "hardhat.config.*", "**/*.sol"):
        signals.append("evm")
    if has_glob(workspace, "Anchor.toml", "programs/**/*.rs"):
        signals.append("solana")
    if has_glob(workspace, "**/Cargo.toml"):
        signals.append("rust-contracts")

    print("Detected signals:", ", ".join(signals) if signals else "generic blockchain consumer")
    print("Load skills/using-blockchain-agent-skills/SKILL.md and matching preset.")
    return 0


def run_tx_simulate_pre(_workspace: Path) -> int:
    print("TX SIMULATE PRE-CHECK")
    print("- Require eth_call / simulateTransaction success before broadcast")
    print("- Attach templates/simulate-evidence.yaml to the change record")
    print("- Set SIMULATE_PASSED=true only after verified simulation")
    return 0


def run_mainnet_guard(_workspace: Path) -> int:
    print("MAINNET GUARD")
    print("- Human confirmation required for mainnet and high-value flows")
    print("- Set HUMAN_CONFIRMED=true after approval")
    print("- Complete templates/mainnet-readiness.yaml")
    return 0


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    runners = {
        "session-start": run_session_start,
        "tx-simulate-pre": run_tx_simulate_pre,
        "mainnet-guard": run_mainnet_guard,
    }
    return runners[args.hook](workspace)


if __name__ == "__main__":
    sys.exit(main())
