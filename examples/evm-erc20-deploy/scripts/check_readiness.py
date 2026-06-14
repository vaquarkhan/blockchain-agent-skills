#!/usr/bin/env python3
"""Offline readiness check for ERC-20 deploy example (no RPC required)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]


def main() -> int:
    errors: list[str] = []
    token = ROOT / "contracts" / "Token.sol"
    if not token.exists():
        errors.append("missing contracts/Token.sol")
    if "pragma solidity" not in token.read_text(encoding="utf-8"):
        errors.append("Token.sol missing pragma")

    template = REPO / "templates" / "mainnet-readiness.yaml"
    if not template.exists():
        errors.append("missing templates/mainnet-readiness.yaml")

    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        return 1

    print("Readiness check passed: contract artifact and mainnet-readiness template present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
