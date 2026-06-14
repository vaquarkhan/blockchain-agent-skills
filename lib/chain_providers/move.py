"""Move VM chain providers — Sui and Aptos (Phase 3)."""

from __future__ import annotations

import re

from .base import ChainMetadata, ChainProvider, TxModel, VMType

_MOVE_CHAINS: dict[str, ChainMetadata] = {
    "sui": ChainMetadata(
        name="sui",
        chain_id="mainnet",
        vm_type=VMType.MOVE,
        tx_model=TxModel.OBJECT,
        native_currency="SUI",
        block_time_seconds=0.5,
        confirmation_depth=10,
        mcp_server="move-rpc-server",
        token_standards=("Coin", "Kiosk"),
    ),
    "aptos": ChainMetadata(
        name="aptos",
        chain_id="mainnet",
        vm_type=VMType.MOVE,
        tx_model=TxModel.OBJECT,
        native_currency="APT",
        block_time_seconds=1.0,
        confirmation_depth=20,
        mcp_server="move-rpc-server",
        token_standards=("Fungible Asset v2", "Digital Asset"),
    ),
}

_SUI_ADDRESS = re.compile(r"^0x[a-fA-F0-9]{64}$")
_APTOS_ADDRESS = re.compile(r"^0x[a-fA-F0-9]{1,64}$")


class MoveChainProvider(ChainProvider):
    def resolve(self, chain_name: str) -> ChainMetadata:
        key = chain_name.lower().strip()
        if key not in _MOVE_CHAINS:
            raise ValueError(f"Unknown Move chain: {chain_name}")
        return _MOVE_CHAINS[key]

    def validate_address(self, address: str) -> bool:
        value = address.strip()
        return bool(_SUI_ADDRESS.match(value) or _APTOS_ADDRESS.match(value))

    def normalize_address(self, address: str) -> str:
        if not self.validate_address(address):
            raise ValueError(f"Invalid Move address: {address}")
        return address.strip().lower() if address.startswith("0x") else address.strip()
