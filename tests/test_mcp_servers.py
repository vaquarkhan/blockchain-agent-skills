#!/usr/bin/env python3
"""Tests for MCP guardrails and tool registry parity."""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "mcp" / "_shared"
sys.path.insert(0, str(SHARED))

from guardrails import GuardrailError, require_simulation_evidence  # noqa: E402


class GuardrailTests(unittest.TestCase):
    def test_blocks_write_without_simulation(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(GuardrailError):
                require_simulation_evidence("eth_sendRawTransaction")

    def test_allows_write_with_simulation_flag(self) -> None:
        old = os.environ.get("SIMULATE_PASSED")
        os.environ["SIMULATE_PASSED"] = "true"
        try:
            require_simulation_evidence("eth_sendRawTransaction")
        finally:
            if old is None:
                os.environ.pop("SIMULATE_PASSED", None)
            else:
                os.environ["SIMULATE_PASSED"] = old


class McpRegistryTests(unittest.TestCase):
    def test_evm_tools_match_schema(self) -> None:
        server_dir = ROOT / "mcp" / "evm-rpc-server"
        schema = json.loads((server_dir / "tool-schemas.json").read_text(encoding="utf-8"))
        expected = {item["name"] for item in schema["tools"]}

        spec = importlib.util.spec_from_file_location("evm_server", server_dir / "server.py")
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(set(module.TOOLS.keys()), expected)


if __name__ == "__main__":
    unittest.main()
