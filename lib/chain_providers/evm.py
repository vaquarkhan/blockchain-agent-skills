"""EVM chain provider — Phase 1 chains."""

from __future__ import annotations

import re

from .base import ChainMetadata, ChainProvider, TxModel, VMType

_EVM_CHAINS: dict[str, ChainMetadata] = {
    "ethereum": ChainMetadata(
        name="ethereum",
        chain_id="1",
        vm_type=VMType.EVM,
        tx_model=TxModel.ACCOUNT,
        native_currency="ETH",
        block_time_seconds=12.0,
        confirmation_depth=12,
        mcp_server="evm-rpc-server",
        token_standards=("ERC-20", "ERC-721", "ERC-1155"),
    ),
    "arbitrum": ChainMetadata(
        name="arbitrum",
        chain_id="42161",
        vm_type=VMType.EVM,
        tx_model=TxModel.ACCOUNT,
        native_currency="ETH",
        block_time_seconds=0.25,
        confirmation_depth=20,
        mcp_server="evm-rpc-server",
        token_standards=("ERC-20", "ERC-721"),
    ),
    "base": ChainMetadata(
        name="base",
        chain_id="8453",
        vm_type=VMType.EVM,
        tx_model=TxModel.ACCOUNT,
        native_currency="ETH",
        block_time_seconds=2.0,
        confirmation_depth=20,
        mcp_server="evm-rpc-server",
        token_standards=("ERC-20", "ERC-721"),
    ),
    "polygon": ChainMetadata(
        name="polygon",
        chain_id="137",
        vm_type=VMType.EVM,
        tx_model=TxModel.ACCOUNT,
        native_currency="MATIC",
        block_time_seconds=2.0,
        confirmation_depth=128,
        mcp_server="evm-rpc-server",
        token_standards=("ERC-20", "ERC-721"),
    ),
}

_HEX_ADDRESS = re.compile(r"^0x[0-9a-fA-F]{40}$")


class EVMChainProvider(ChainProvider):
    def resolve(self, chain_name: str) -> ChainMetadata:
        key = chain_name.lower().strip()
        aliases = {"eth": "ethereum", "arb": "arbitrum", "matic": "polygon"}
        key = aliases.get(key, key)
        if key not in _EVM_CHAINS:
            raise ValueError(f"Unknown EVM chain: {chain_name}")
        return _EVM_CHAINS[key]

    def validate_address(self, address: str) -> bool:
        return bool(_HEX_ADDRESS.match(address.strip()))

    def normalize_address(self, address: str) -> str:
        if not self.validate_address(address):
            raise ValueError(f"Invalid EVM address: {address}")
        return address.strip().lower()
