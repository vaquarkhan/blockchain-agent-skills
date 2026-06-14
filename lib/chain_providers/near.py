"""NEAR Protocol chain provider — Phase 2."""

from __future__ import annotations

import re

from .base import ChainMetadata, ChainProvider, TxModel, VMType

_NEAR = ChainMetadata(
    name="near",
    chain_id="mainnet",
    vm_type=VMType.NEAR,
    tx_model=TxModel.ACCOUNT,
    native_currency="NEAR",
    block_time_seconds=1.0,
    confirmation_depth=5,
    mcp_server="near-rpc-server",
    token_standards=("NEP-141", "NEP-171", "NEP-177"),
)

_AURORA = ChainMetadata(
    name="aurora",
    chain_id="1313161554",
    vm_type=VMType.EVM,
    tx_model=TxModel.ACCOUNT,
    native_currency="ETH",
    block_time_seconds=1.0,
    confirmation_depth=10,
    mcp_server="near-rpc-server",
    token_standards=("ERC-20", "ERC-721"),
)

_NAMED_ACCOUNT = re.compile(r"^([a-z0-9_-]+\.)*[a-z0-9_-]+\.near$")
_IMPLICIT_ACCOUNT = re.compile(r"^[0-9a-f]{64}$")


class NEARChainProvider(ChainProvider):
    def resolve(self, chain_name: str) -> ChainMetadata:
        key = chain_name.lower().strip()
        if key in ("aurora", "aurora-mainnet"):
            return _AURORA
        if key in ("near", "mainnet", "testnet"):
            return _NEAR
        raise ValueError(f"Unknown NEAR network: {chain_name}")

    def validate_address(self, address: str) -> bool:
        addr = address.strip().lower()
        return bool(_NAMED_ACCOUNT.match(addr) or _IMPLICIT_ACCOUNT.match(addr))

    def normalize_address(self, address: str) -> str:
        if not self.validate_address(address):
            raise ValueError(f"Invalid NEAR account: {address}")
        return address.strip().lower()
