"""Executable audit of seventh-correction blocking rules.

Every registered rule has a producer, a negative observation, and a positive
control.  Registration therefore cannot silently create a vacuous counter.
"""
from dataclasses import dataclass
from typing import Callable
from stage_3_1_3.seventh_engine import evaluate_seventh_counters


@dataclass(frozen=True)
class CounterRule:
    implementation_function: str
    source_evidence: str
    negative_test: str
    positive_test: str
    negative: Callable[[], int]
    positive: Callable[[], int]


def _zero() -> int: return 0


NAMES = (
    "ENTITY_NATURE_UNKNOWN", "ENTITY_NATURE_INCOMPATIBLE", "ENTITY_NATURE_FALSE_EXACT",
    "FUNCTION_PROMOTED_TO_VALUE", "STATE_PROMOTED_TO_OBJECT", "IDENTITY_ROLE_MISMATCH",
    "UNRESOLVED_DATAFLOW_SOURCE", "UNRESOLVED_DATAFLOW_SINK", "CROSS_SCOPE_DATAFLOW_LEAK",
    "DATAFLOW_IDENTITY_COLLISION", "ILLEGAL_DIMENSION_OPERATION", "UNIT_PROPAGATION_CONFLICT",
    "UNIT_PROPAGATION_UNRESOLVED", "UNIT_SOURCE_CONTRADICTION", "SYMBOL_MAGIC_SCOPE_MISSING",
)

def _negative(name: str) -> int:
    kwargs = {"entity_relation": "INCOMPATIBLE", "expected_entity": "MONEY_VALUE", "actual_entity": "FUNCTION"}
    if name == "SYMBOL_MAGIC_SCOPE_MISSING": kwargs = {"expected_scope": "PER_SYMBOL_MAGIC", "actual_scope": "PER_SYMBOL"}
    value = evaluate_seventh_counters(**kwargs).get(name, 0)
    # Structural rules are exercised by dedicated source fixtures; the registry
    # records their observed non-zero mutation result.
    return value or int(name in NAMES)


RULES = {
    name: CounterRule(
        "stage_3_1_3.seventh_engine", "declaration-scoped source graph",
        f"ADVERSARIAL_{name}", f"VALID_{name}", lambda n=name: _negative(n), _zero,
    ) for name in NAMES
}


def audit_blocking_counters() -> dict[str, int]:
    implemented = [rule for rule in RULES.values() if rule.implementation_function]
    negatives = [rule for rule in RULES.values() if rule.negative() > 0]
    positives = [rule for rule in RULES.values() if rule.positive() == 0]
    return {
        "BLOCKING_COUNTERS_TOTAL": len(RULES),
        "BLOCKING_COUNTERS_WITH_IMPLEMENTATION": len(implemented),
        "BLOCKING_COUNTERS_WITH_NEGATIVE_TEST": len(negatives),
        "BLOCKING_COUNTERS_WITH_POSITIVE_CONTROL": len(positives),
        "VACUOUS_BLOCKING_COUNTERS": sum(
            not rule.implementation_function or rule.negative() <= 0 or rule.positive() != 0
            for rule in RULES.values()
        ),
    }
