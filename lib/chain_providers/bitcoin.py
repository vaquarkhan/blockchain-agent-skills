"""Bitcoin UTXO chain provider (Phase 4)."""

from __future__ import annotations

import re

from .base import ChainMetadata, ChainProvider, TxModel, VMType

_BITCOIN = ChainMetadata(
    name="bitcoin",
    chain_id="mainnet",
    vm_type=VMType.UTXO,
    tx_model=TxModel.UTXO,
    native_currency="BTC",
    block_time_seconds=600.0,
    confirmation_depth=6,
    mcp_server="bitcoin-rpc-server",
    token_standards=("Ordinals", "BRC-20"),
)

_LIGHTNING = ChainMetadata(
    name="lightning",
    chain_id="mainnet",
    vm_type=VMType.UTXO,
    tx_model=TxModel.UTXO,
    native_currency="BTC",
    block_time_seconds=1.0,
    confirmation_depth=3,
    mcp_server="bitcoin-rpc-server",
    token_standards=("BOLT11",),
)

_SEGWIT = re.compile(r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,62}$")


class BitcoinChainProvider(ChainProvider):
    def resolve(self, chain_name: str) -> ChainMetadata:
        key = chain_name.lower().strip()
        if key in ("lightning", "ln"):
            return _LIGHTNING
        if key in ("bitcoin", "btc", "mainnet"):
            return _BITCOIN
        raise ValueError(f"Unknown Bitcoin network: {chain_name}")

    def validate_address(self, address: str) -> bool:
        return bool(_SEGWIT.match(address.strip()))

    def normalize_address(self, address: str) -> str:
        if not self.validate_address(address):
            raise ValueError(f"Invalid Bitcoin address: {address}")
        return address.strip()
