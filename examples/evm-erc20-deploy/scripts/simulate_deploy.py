#!/usr/bin/env python3
"""Build simulate payload metadata for ERC-20 deploy (offline helper)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    plan = {
        "operation": "deploy_erc20",
        "chain": "ethereum",
        "simulate_tool": "eth_estimateGas",
        "guardrails": [
            "guardrails/transaction-safety.yaml",
            "guardrails/security.yaml",
        ],
        "templates": [
            "templates/mainnet-readiness.yaml",
            "templates/simulate-evidence.yaml",
        ],
        "contract_path": str(ROOT / "contracts" / "Token.sol"),
    }
    out = ROOT / "simulate-plan.json"
    out.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
