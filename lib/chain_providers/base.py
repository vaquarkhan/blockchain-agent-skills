"""ChainProvider interface — chain-agnostic metadata and address validation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class VMType(str, Enum):
    EVM = "evm"
    SVM = "svm"
    NEAR = "near"
    COSMOS = "cosmos"
    MOVE = "move"
    UTXO = "utxo"
    TVM = "tvm"
    SUBSTRATE = "substrate"


class TxModel(str, Enum):
    ACCOUNT = "account"
    UTXO = "utxo"
    OBJECT = "object"


@dataclass(frozen=True)
class ChainMetadata:
    name: str
    chain_id: str
    vm_type: VMType
    tx_model: TxModel
    native_currency: str
    block_time_seconds: float
    confirmation_depth: int
    mcp_server: str
    bech32_prefix: Optional[str] = None
    token_standards: tuple[str, ...] = ()


class ChainProvider(ABC):
    """Normalize chain-specific differences behind a single interface."""

    @abstractmethod
    def resolve(self, chain_name: str) -> ChainMetadata:
        """Resolve chain name or alias to normalized metadata."""

    @abstractmethod
    def validate_address(self, address: str) -> bool:
        """Validate address format for this chain family."""

    @abstractmethod
    def normalize_address(self, address: str) -> str:
        """Return canonical address representation."""
