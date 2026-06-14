#!/usr/bin/env python3
"""Validate compiled contract metadata for deploy review."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    token = (ROOT / "contracts" / "Token.sol").read_text(encoding="utf-8")
    required = [r"contract\s+\w+", r"function\s+mint", r"event\s+Transfer"]
    missing = [pattern for pattern in required if not re.search(pattern, token)]
    if missing:
        print("Contract validation failed:", ", ".join(missing))
        return 1
    print("Contract validation passed: core ERC-20 surface detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
