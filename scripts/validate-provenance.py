#!/usr/bin/env python3
"""Validate provenance.yaml and reference guide provenance footers."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
PROVENANCE_YAML = ROOT / "provenance" / "provenance.yaml"
REFERENCES = ROOT / "references"
SKILLS_JSON = ROOT / "provenance" / "skills-provenance.json"

REQUIRED_SECTIONS = ("## Authoritative sources", "## Provenance")
REQUIRED_ROWS = (
    "Source document",
    "Version / effective",
    "Last reviewed",
    "Reviewer",
    "Next review due",
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MIN_REFERENCE_LINES = 45


def validate_provenance_yaml() -> list[str]:
    errors: list[str] = []
    if not PROVENANCE_YAML.exists():
        return ["missing provenance/provenance.yaml"]
    if yaml is None:
        return ["PyYAML required: pip install pyyaml"]

    data = yaml.safe_load(PROVENANCE_YAML.read_text(encoding="utf-8"))
    for field in ("version", "review_policy", "standards"):
        if field not in data:
            errors.append(f"provenance.yaml missing top-level field: {field}")

    standards = data.get("standards", [])
    if not standards:
        errors.append("provenance.yaml standards list is empty")
        return errors

    ids: set[str] = set()
    for item in standards:
        sid = item.get("id")
        if not sid:
            errors.append("provenance standard missing id")
            continue
        if sid in ids:
            errors.append(f"duplicate provenance standard id: {sid}")
        ids.add(sid)
        for field in ("name", "version", "url", "last_reviewed", "next_review_due", "reviewer", "applies_to"):
            if field not in item:
                errors.append(f"provenance standard {sid} missing {field}")
        if item.get("last_reviewed") and not DATE_RE.match(str(item["last_reviewed"])):
            errors.append(f"provenance standard {sid} last_reviewed must be YYYY-MM-DD")
        if item.get("next_review_due") and not DATE_RE.match(str(item["next_review_due"])):
            errors.append(f"provenance standard {sid} next_review_due must be YYYY-MM-DD")
    return errors


def reference_paths() -> list[Path]:
    return sorted(p for p in REFERENCES.glob("*.md") if p.name != "README.md")


def validate_reference(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    line_count = len(text.splitlines())
    if line_count < MIN_REFERENCE_LINES:
        errors.append(f"{path.name}: expected >= {MIN_REFERENCE_LINES} lines, got {line_count}")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path.name}: missing section {section!r}")

    provenance_idx = text.find("## Provenance")
    if provenance_idx == -1:
        return errors

    provenance_block = text[provenance_idx:]
    for row in REQUIRED_ROWS:
        if f"**{row}**" not in provenance_block and row not in provenance_block:
            errors.append(f"{path.name}: provenance missing row {row!r}")

    sources_idx = text.find("## Authoritative sources")
    if sources_idx != -1:
        sources_block = text[sources_idx:provenance_idx]
        if "http" not in sources_block and not re.search(r"\[.*\]\(.*\)", sources_block):
            errors.append(f"{path.name}: Authoritative sources should include at least one link")

    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_provenance_yaml())
    refs = reference_paths()
    if not refs:
        errors.append("no reference guides found under references/")
    for path in refs:
        errors.extend(validate_reference(path))

    if not SKILLS_JSON.exists():
        errors.append("missing provenance/skills-provenance.json")

    if errors:
        print("Provenance validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Provenance validation passed ({len(yaml.safe_load(PROVENANCE_YAML.read_text())['standards'])} standards, {len(refs)} references).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
