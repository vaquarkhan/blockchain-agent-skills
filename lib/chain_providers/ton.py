"""TON chain provider (Phase 4)."""

from __future__ import annotations

import re

from .base import ChainMetadata, ChainProvider, TxModel, VMType

_TON = ChainMetadata(
    name="ton",
    chain_id="mainnet",
    vm_type=VMType.TVM,
    tx_model=TxModel.ACCOUNT,
    native_currency="TON",
    block_time_seconds=5.0,
    confirmation_depth=10,
    mcp_server="ton-rpc-server",
    token_standards=("TEP-74", "TEP-62"),
)

_TON_ADDRESS = re.compile(r"^(EQ|UQ)[A-Za-z0-9_-]{46}$")


class TonChainProvider(ChainProvider):
    def resolve(self, chain_name: str) -> ChainMetadata:
        key = chain_name.lower().strip()
        if key not in ("ton", "mainnet"):
            raise ValueError(f"Unknown TON network: {chain_name}")
        return _TON

    def validate_address(self, address: str) -> bool:
        return bool(_TON_ADDRESS.match(address.strip()))

    def normalize_address(self, address: str) -> str:
        if not self.validate_address(address):
            raise ValueError(f"Invalid TON address: {address}")
        return address.strip()
