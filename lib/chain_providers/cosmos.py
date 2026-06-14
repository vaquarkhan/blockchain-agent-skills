"""Cosmos / IBC chain provider — Phase 2."""

from __future__ import annotations

import re

from .base import ChainMetadata, ChainProvider, TxModel, VMType

_COSMOS_CHAINS: dict[str, ChainMetadata] = {
    "cosmos": ChainMetadata(
        name="cosmos",
        chain_id="cosmoshub-4",
        vm_type=VMType.COSMOS,
        tx_model=TxModel.ACCOUNT,
        native_currency="ATOM",
        block_time_seconds=6.0,
        confirmation_depth=7,
        mcp_server="cosmos-rpc-server",
        bech32_prefix="cosmos",
        token_standards=("CW-20", "CW-721", "ICS-20"),
    ),
    "osmosis": ChainMetadata(
        name="osmosis",
        chain_id="osmosis-1",
        vm_type=VMType.COSMOS,
        tx_model=TxModel.ACCOUNT,
        native_currency="OSMO",
        block_time_seconds=2.0,
        confirmation_depth=7,
        mcp_server="cosmos-rpc-server",
        bech32_prefix="osmo",
        token_standards=("CW-20", "ICS-20"),
    ),
    "celestia": ChainMetadata(
        name="celestia",
        chain_id="celestia",
        vm_type=VMType.COSMOS,
        tx_model=TxModel.ACCOUNT,
        native_currency="TIA",
        block_time_seconds=6.0,
        confirmation_depth=7,
        mcp_server="cosmos-rpc-server",
        bech32_prefix="celestia",
        token_standards=("ICS-20",),
    ),
    "injective": ChainMetadata(
        name="injective",
        chain_id="injective-1",
        vm_type=VMType.COSMOS,
        tx_model=TxModel.ACCOUNT,
        native_currency="INJ",
        block_time_seconds=1.0,
        confirmation_depth=7,
        mcp_server="cosmos-rpc-server",
        bech32_prefix="inj",
        token_standards=("CW-20", "ICS-20"),
    ),
}


class CosmosChainProvider(ChainProvider):
    def __init__(self, chain_name: str = "cosmos") -> None:
        self._chain_name = chain_name.lower().strip()

    def resolve(self, chain_name: str) -> ChainMetadata:
        key = chain_name.lower().strip()
        aliases = {"cosmoshub": "cosmos", "hub": "cosmos", "osmo": "osmosis"}
        key = aliases.get(key, key)
        if key not in _COSMOS_CHAINS:
            raise ValueError(f"Unknown Cosmos chain: {chain_name}")
        return _COSMOS_CHAINS[key]

    def validate_address(self, address: str) -> bool:
        meta = self.resolve(self._chain_name)
        prefix = meta.bech32_prefix or "cosmos"
        pattern = re.compile(rf"^{re.escape(prefix)}1[a-z0-9]{{38,58}}$")
        return bool(pattern.match(address.strip()))

    def normalize_address(self, address: str) -> str:
        if not self.validate_address(address):
            raise ValueError(f"Invalid Cosmos bech32 address: {address}")
        return address.strip()
