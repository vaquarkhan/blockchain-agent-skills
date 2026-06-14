"""Hedera Hashgraph chain provider (Phase 4)."""

from __future__ import annotations

import re

from .base import ChainMetadata, ChainProvider, TxModel, VMType

_HEDERA = ChainMetadata(
    name="hedera",
    chain_id="mainnet",
    vm_type=VMType.EVM,
    tx_model=TxModel.ACCOUNT,
    native_currency="HBAR",
    block_time_seconds=3.0,
    confirmation_depth=10,
    mcp_server="hedera-rpc-server",
    token_standards=("HTS", "ERC-20"),
)

_ACCOUNT = re.compile(r"^0\.0\.\d+$")
_EVM_ALIAS = re.compile(r"^0x[a-fA-F0-9]{40}$")


class HederaChainProvider(ChainProvider):
    def resolve(self, chain_name: str) -> ChainMetadata:
        key = chain_name.lower().strip()
        if key not in ("hedera", "hbar", "mainnet"):
            raise ValueError(f"Unknown Hedera network: {chain_name}")
        return _HEDERA

    def validate_address(self, address: str) -> bool:
        value = address.strip()
        return bool(_ACCOUNT.match(value) or _EVM_ALIAS.match(value))

    def normalize_address(self, address: str) -> str:
        if not self.validate_address(address):
            raise ValueError(f"Invalid Hedera address: {address}")
        return address.strip()
