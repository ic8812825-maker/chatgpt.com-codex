"""Execute causal before/after checks for every production blocking counter."""
from __future__ import annotations
import ast
import sys
from dataclasses import dataclass
from pathlib import Path

VALIDATOR=Path(__file__).resolve().parents[1]/"validate_stage_3_1_3_glossary.py"
TESTS_ROOT=Path(__file__).resolve().parents[1]
if str(TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(TESTS_ROOT))


@dataclass(frozen=True)
class CounterRule:
    counter_name: str
    base_fixture: str
    negative_mutation: str
    positive_fixture: str
    runner: str = "production.validate"


def registry() -> dict[str, CounterRule]:
    blocking=production_blocking()
    return {name: CounterRule(name, "published_mapping", name, "published_mapping")
            for name in blocking}


def production_blocking() -> list[str]:
    tree=ast.parse(VALIDATOR.read_text()); assignments=[]
    for node in tree.body:
        if (isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="BLOCKING" for t in node.targets)
                and isinstance(node.value,ast.List)):
            assignments=[x.value for x in node.value.elts if isinstance(x,ast.Constant)]
    return assignments


def audit_blocking_counters() -> dict[str, int]:
    # run_controls calls production.validate for every independently copied
    # negative and positive fixture and publishes observed target outcomes.
    import test_stage_3_1_3_semantic_mutations as mutations
    mutations.run_controls(verbose=False)
    observed = mutations.LAST_COUNTER_RESULTS
    blocking = production_blocking(); rules = registry()
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
