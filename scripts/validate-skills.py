#!/usr/bin/env python3
"""Validate blockchain-agent-skills structure and SKILL.md frontmatter."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir.name}: missing SKILL.md"]

    text = skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    name = fm.get("name", "")
    desc = fm.get("description", "")

    if not name:
        errors.append(f"{skill_dir.name}: missing 'name' in frontmatter")
    elif not NAME_RE.match(name):
        errors.append(f"{skill_dir.name}: invalid name '{name}'")
    elif name != skill_dir.name:
        errors.append(f"{skill_dir.name}: name '{name}' != directory name")

    if not desc:
        errors.append(f"{skill_dir.name}: missing 'description' in frontmatter")
    elif len(desc) > 1024:
        errors.append(f"{skill_dir.name}: description exceeds 1024 chars")

    line_count = len(text.splitlines())
    if line_count > 500:
        errors.append(f"{skill_dir.name}: SKILL.md is {line_count} lines (max 500)")

    return errors


def main() -> int:
    if not SKILLS_DIR.exists():
        print(f"ERROR: {SKILLS_DIR} not found")
        return 1

    all_errors: list[str] = []
    skill_dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir())

    if not skill_dirs:
        print("ERROR: no skills found")
        return 1

    for skill_dir in skill_dirs:
        all_errors.extend(validate_skill(skill_dir))

    if all_errors:
        print(f"FAILED: {len(all_errors)} error(s)")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print(f"OK: {len(skill_dirs)} skills validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
