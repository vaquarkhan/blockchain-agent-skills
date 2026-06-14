#!/usr/bin/env python3
"""Emit SPL mint planning artifact for blueprint example."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    plan = {
        "program": "spl-token",
        "steps": ["derive_mint_pda", "simulateTransaction", "set_authorities", "confirm_depth"],
        "templates": ["templates/tx-plan.yaml", "templates/simulate-evidence.yaml"],
        "references": ["references/solana-program-security.md"],
    }
    out = ROOT / "mint-plan.json"
    out.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
