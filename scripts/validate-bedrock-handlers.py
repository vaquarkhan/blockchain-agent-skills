#!/usr/bin/env python3
"""Validate Bedrock manifest, generated artifacts, and handler routes."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "bedrock" / "manifest.json"
sys.path.insert(0, str(ROOT / "bedrock" / "lambda"))

from actions import ACTIONS  # noqa: E402


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    for skill in manifest["skills"]:
        name = skill["name"]
        skill_dir = ROOT / "skills" / name
        for artifact in ("skill-definition.yaml", "action-group.json", "openapi.yaml", "lambda/handler.py", "tests/test_handler.py"):
            path = skill_dir / artifact
            if not path.exists():
                errors.append(f"missing {path.relative_to(ROOT)}")
        for fn in skill["functions"]:
            if fn["name"] not in ACTIONS:
                errors.append(f"missing action implementation: {fn['name']}")

    if errors:
        print("Bedrock validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Bedrock validation passed ({len(manifest['skills'])} skills, {len(ACTIONS)} actions).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
