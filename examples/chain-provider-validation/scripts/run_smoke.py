#!/usr/bin/env python3
"""Run chain-provider and skill validation smoke checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=REPO, check=True)


def main() -> int:
    run([sys.executable, "tests/test_chain_providers.py"])
    run([sys.executable, "scripts/validate-skills.py"])
    run([sys.executable, "scripts/validate-assets.py"])
    print("Chain provider smoke checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
