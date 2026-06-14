#!/usr/bin/env python3
"""Validate IBC transfer plan artifact."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "transfer-plan.json"


def main() -> int:
    if not PLAN.exists():
        print("Run: python scripts/plan_transfer.py")
        return 1
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    required = {"source_chain", "destination_chain", "template", "checks", "reference"}
    missing = required - set(plan.keys())
    if missing:
        print("Invalid plan, missing:", ", ".join(sorted(missing)))
        return 1
    print("IBC transfer plan validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
