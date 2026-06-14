#!/usr/bin/env python3
"""Run blockchain agent hooks by name."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HOOKS_DIR = Path(__file__).resolve().parent.parent / "hooks"


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/hook_runner.py <hook-name>")
        print("Available:", ", ".join(p.stem for p in HOOKS_DIR.glob("*.sh")))
        return 1

    name = sys.argv[1]
    for ext in (".sh", ".ps1"):
        hook = HOOKS_DIR / f"{name}{ext}"
        if hook.exists():
            if ext == ".sh":
                return subprocess.call(["bash", str(hook), *sys.argv[2:]])
            return subprocess.call(["pwsh", str(hook), *sys.argv[2:]])

    print(f"Hook not found: {name}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
