"""Tests for chain provider registry."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.chain_providers import resolve_chain, validate_address


def test_evm_resolve():
    meta = resolve_chain("ethereum")
    assert meta.chain_id == "1"
    assert meta.mcp_server == "evm-rpc-server"
    assert meta.native_currency == "ETH"


def test_evm_address():
    assert validate_address("ethereum", "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0")
    assert not validate_address("ethereum", "not-an-address")


def test_solana_resolve():
    meta = resolve_chain("solana")
    assert meta.vm_type.value == "svm"
    assert meta.confirmation_depth == 32
    assert meta.mcp_server == "solana-rpc-server"


def test_solana_address():
    assert validate_address("solana", "11111111111111111111111111111112")
    assert not validate_address("solana", "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0")


def test_near_resolve():
    meta = resolve_chain("near")
    assert meta.token_standards == ("NEP-141", "NEP-171", "NEP-177")


def test_near_address():
    assert validate_address("near", "alice.near")
    assert validate_address("near", "a" * 64)
    assert not validate_address("near", "invalid account!")


def test_cosmos_resolve():
    meta = resolve_chain("osmosis")
    assert meta.bech32_prefix == "osmo"
    assert meta.chain_id == "osmosis-1"


def test_cosmos_address():
    assert validate_address("cosmos", "cosmos1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnrql8a")
    assert not validate_address("cosmos", "osmo1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqn7qd5x")


if __name__ == "__main__":
    test_evm_resolve()
    test_evm_address()
    test_solana_resolve()
    test_solana_address()
    test_near_resolve()
    test_near_address()
    test_cosmos_resolve()
    test_cosmos_address()
    print("All 8 tests passed")
