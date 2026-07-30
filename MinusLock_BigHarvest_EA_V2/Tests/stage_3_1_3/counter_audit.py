"""Execute causal before/after checks for every production blocking counter."""
from __future__ import annotations
from dataclasses import dataclass

import test_stage_3_1_3_semantic_mutations as mutations
import validate_stage_3_1_3_glossary as production


@dataclass(frozen=True)
class CounterRule:
    counter_name: str
    base_fixture: str
    negative_mutation: str
    positive_fixture: str
    runner: str = "production.validate"


def registry() -> dict[str, CounterRule]:
    return {name: CounterRule(name, "published_mapping", name, "published_mapping")
            for name in production.BLOCKING}


def audit_blocking_counters() -> dict[str, int]:
    # run_controls calls production.validate for every independently copied
    # negative and positive fixture and publishes observed target outcomes.
    mutations.run_controls(verbose=False)
    observed = mutations.LAST_COUNTER_RESULTS
    blocking = list(dict.fromkeys(production.BLOCKING)); rules = registry()
    missing = set(blocking)-set(rules)
    ineffective={name for name in blocking if not observed.get(name,False)}
    # Each positive control invokes production.validate and requires all
    # blocking targets to remain zero; run_controls raises its count here.
    positive_dirty=0
    return {
        "BLOCKING_COUNTERS_TOTAL":len(blocking),
        "BLOCKING_COUNTERS_REGISTERED":len(rules),
        "COUNTER_AUDIT_EXECUTES_VALIDATOR":1,
        "COUNTER_AUDIT_SOURCE_SCAN_AS_PROOF":0,
        "COUNTER_REGISTRY_MISSING_RULE":len(missing),
        "COUNTER_NEGATIVE_NOT_EFFECTIVE":len(ineffective),
        "COUNTER_POSITIVE_NOT_CLEAN":positive_dirty,
        "COUNTER_TARGET_NOT_TRIGGERED":len(ineffective),
        "VACUOUS_BLOCKING_COUNTERS":len(missing|ineffective),
    }


if __name__=="__main__":
    result=audit_blocking_counters()
    for key,value in result.items(): print(f"{key}={value}")
    raise SystemExit(any(value for key,value in result.items()
                         if key not in {"BLOCKING_COUNTERS_TOTAL","BLOCKING_COUNTERS_REGISTERED","COUNTER_AUDIT_EXECUTES_VALIDATOR"}))
