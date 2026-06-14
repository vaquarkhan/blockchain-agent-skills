"""Unified chain registry — routes to family-specific providers."""

from __future__ import annotations

from .base import ChainMetadata, VMType
from .cosmos import CosmosChainProvider, _COSMOS_CHAINS
from .evm import EVMChainProvider, _EVM_CHAINS
from .near import NEARChainProvider
from .solana import SolanaChainProvider

_EVM = EVMChainProvider()
_SOLANA = SolanaChainProvider()
_NEAR = NEARChainProvider()

_CHAIN_TO_VM: dict[str, VMType] = {}
for name in _EVM_CHAINS:
    _CHAIN_TO_VM[name] = VMType.EVM
_CHAIN_TO_VM.update(
    {
        "solana": VMType.SVM,
        "sol": VMType.SVM,
        "near": VMType.NEAR,
        "aurora": VMType.EVM,
        **{name: VMType.COSMOS for name in _COSMOS_CHAINS},
    }
)


def resolve_chain(chain_name: str) -> ChainMetadata:
    """Resolve any supported chain name to normalized metadata."""
    key = chain_name.lower().strip()
    vm = _CHAIN_TO_VM.get(key)
    if vm == VMType.EVM and key != "aurora":
        return _EVM.resolve(key)
    if vm == VMType.SVM:
        return _SOLANA.resolve(key)
    if key in ("near", "aurora", "mainnet", "testnet"):
        return _NEAR.resolve(key)
    if vm == VMType.COSMOS:
        return CosmosChainProvider(key).resolve(key)
    raise ValueError(f"Unsupported chain: {chain_name}")


def validate_address(chain_name: str, address: str) -> bool:
    """Validate address for the given chain."""
    meta = resolve_chain(chain_name)
    if meta.vm_type == VMType.EVM:
        return _EVM.validate_address(address)
    if meta.vm_type == VMType.SVM:
        return _SOLANA.validate_address(address)
    if meta.vm_type == VMType.NEAR:
        return _NEAR.validate_address(address)
    if meta.vm_type == VMType.COSMOS:
        return CosmosChainProvider(meta.name).validate_address(address)
    raise ValueError(f"No address validator for VM type: {meta.vm_type}")
