#!/usr/bin/env python3
"""Immutable, auditable R4-R8 canonical contracts."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class HSBI_MalformedSourceValue:
    """A source value whose historical type cannot be silently normalized."""

    source_path: str
    source_type: str
    source_value: Any


@dataclass(frozen=True)
class HSBI_RuntimeContext:
    source_value: Any


@dataclass(frozen=True)
class HSBI_ManagedPosition:
    source_value: Any


@dataclass(frozen=True)
class HSBI_ExecutionIntent:
    source_value: Any


@dataclass(frozen=True)
class HSBI_QuoteSnapshot:
    source_value: Any


@dataclass(frozen=True)
class HSBI_ExecutionPricePolicy:
    source_value: Any


@dataclass(frozen=True)
class HSBI_DealEvidenceRecord:
    source_value: Any


@dataclass(frozen=True)
class HSBI_PersistedState:
    source_value: Any


@dataclass(frozen=True)
class HSBI_EconomicPolicy:
    source_value: Any


@dataclass(frozen=True)
class HSBI_ScenarioInput:
    """Canonical R4-R8 input accepted by the sole public execution target."""

    schema_version: int
    source_version: str
    source_function: str
    context: HSBI_RuntimeContext
    positions: tuple[HSBI_ManagedPosition, ...] | HSBI_MalformedSourceValue
    intents: tuple[HSBI_ExecutionIntent, ...] | HSBI_MalformedSourceValue
    snapshot: HSBI_QuoteSnapshot
    price_policy: HSBI_ExecutionPricePolicy
    deals: tuple[HSBI_DealEvidenceRecord, ...] | HSBI_MalformedSourceValue
    persisted_state: HSBI_PersistedState
    economic_policy: HSBI_EconomicPolicy
    source_payload: dict[str, Any]
    source_digest: str
    mapping_records: tuple[dict[str, Any], ...]
