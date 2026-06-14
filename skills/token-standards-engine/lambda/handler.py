#!/usr/bin/env python3
"""Bedrock Lambda entrypoint for token-standards-engine."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HANDLER = ROOT / "bedrock" / "lambda" / "handler.py"
sys.path.insert(0, str(HANDLER.parent))

spec = importlib.util.spec_from_file_location("bedrock_handler", HANDLER)
if spec is None or spec.loader is None:
    raise RuntimeError("Cannot load bedrock handler")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

lambda_handler = module.lambda_handler
