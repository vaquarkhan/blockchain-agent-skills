#!/usr/bin/env python3
"""Emit IBC transfer planning artifact for blueprint example."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    plan = {
        "source_chain": "cosmoshub-4",
        "destination_chain": "osmosis-1",
        "template": "templates/ibc-transfer-plan.yaml",
        "checks": ["channel_open", "timeout_height_set", "simulate_passed"],
        "reference": "references/cosmos-ibc-patterns.md",
    }
    out = ROOT / "transfer-plan.json"
    out.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
