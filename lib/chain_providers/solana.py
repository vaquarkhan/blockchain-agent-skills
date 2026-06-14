"""Solana (SVM) chain provider — Phase 2."""

from __future__ import annotations

import re

from .base import ChainMetadata, ChainProvider, TxModel, VMType

_SOLANA = ChainMetadata(
    name="solana",
    chain_id="mainnet-beta",
    vm_type=VMType.SVM,
    tx_model=TxModel.ACCOUNT,
    native_currency="SOL",
    block_time_seconds=0.4,
    confirmation_depth=32,
    mcp_server="solana-rpc-server",
    token_standards=("SPL", "Token-2022", "Metaplex", "cNFT"),
)

# Base58 alphabet, 32–44 chars typical for pubkeys
_BASE58_PUBKEY = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")


class SolanaChainProvider(ChainProvider):
    def resolve(self, chain_name: str) -> ChainMetadata:
        key = chain_name.lower().strip()
        if key not in ("solana", "sol", "mainnet-beta", "devnet"):
            raise ValueError(f"Unknown Solana network: {chain_name}")
        if key == "devnet":
            return ChainMetadata(
                name="solana-devnet",
                chain_id="devnet",
                vm_type=VMType.SVM,
                tx_model=TxModel.ACCOUNT,
                native_currency="SOL",
                block_time_seconds=0.4,
                confirmation_depth=32,
                mcp_server="solana-rpc-server",
                token_standards=("SPL", "Token-2022"),
            )
        return _SOLANA

    def validate_address(self, address: str) -> bool:
        return bool(_BASE58_PUBKEY.match(address.strip()))

    def normalize_address(self, address: str) -> str:
        if not self.validate_address(address):
            raise ValueError(f"Invalid Solana pubkey: {address}")
        return address.strip()
