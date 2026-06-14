"""Substrate chain providers — Polkadot ecosystem (Phase 4)."""

from __future__ import annotations

import re

from .base import ChainMetadata, ChainProvider, TxModel, VMType

_SUBSTRATE_CHAINS: dict[str, ChainMetadata] = {
    "polkadot": ChainMetadata(
        name="polkadot",
        chain_id="polkadot",
        vm_type=VMType.SUBSTRATE,
        tx_model=TxModel.ACCOUNT,
        native_currency="DOT",
        block_time_seconds=6.0,
        confirmation_depth=10,
        mcp_server="substrate-rpc-server",
        token_standards=("PSP-22",),
    ),
    "kusama": ChainMetadata(
        name="kusama",
        chain_id="kusama",
        vm_type=VMType.SUBSTRATE,
        tx_model=TxModel.ACCOUNT,
        native_currency="KSM",
        block_time_seconds=6.0,
        confirmation_depth=10,
        mcp_server="substrate-rpc-server",
    ),
    "moonbeam": ChainMetadata(
        name="moonbeam",
        chain_id="moonbeam",
        vm_type=VMType.SUBSTRATE,
        tx_model=TxModel.ACCOUNT,
        native_currency="GLMR",
        block_time_seconds=12.0,
        confirmation_depth=10,
        mcp_server="substrate-rpc-server",
    ),
}

_SS58 = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{47,48}$")


class SubstrateChainProvider(ChainProvider):
    def resolve(self, chain_name: str) -> ChainMetadata:
        key = chain_name.lower().strip()
        if key not in _SUBSTRATE_CHAINS:
            raise ValueError(f"Unknown Substrate chain: {chain_name}")
        return _SUBSTRATE_CHAINS[key]

    def validate_address(self, address: str) -> bool:
        return bool(_SS58.match(address.strip()))

    def normalize_address(self, address: str) -> str:
        if not self.validate_address(address):
            raise ValueError(f"Invalid Substrate address: {address}")
        return address.strip()
