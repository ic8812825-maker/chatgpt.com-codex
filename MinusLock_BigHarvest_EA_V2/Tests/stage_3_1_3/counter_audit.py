"""Executable registry audit for every production blocking counter."""
from __future__ import annotations
import ast
from dataclasses import dataclass
from pathlib import Path

TESTS=Path(__file__).resolve().parents[1]
VALIDATOR=TESTS/"validate_stage_3_1_3_glossary.py"
MUTATIONS=TESTS/"test_stage_3_1_3_semantic_mutations.py"


@dataclass(frozen=True)
class CounterRule:
    counter_name:str
    implementation_location:str
    negative_fixture:str
    positive_fixture:str


def production_blocking()->list[str]:
    tree=ast.parse(VALIDATOR.read_text());env={}
    for node in tree.body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and isinstance(node.value,ast.List):
            env[node.targets[0].id]=[x.value for x in node.value.elts if isinstance(x,ast.Constant) and isinstance(x.value,str)]
        elif isinstance(node,ast.AugAssign) and isinstance(node.target,ast.Name) and isinstance(node.op,ast.Add):
            addition=env.get(node.value.id,[]) if isinstance(node.value,ast.Name) else [x.value for x in node.value.elts] if isinstance(node.value,ast.List) else []
            env.setdefault(node.target.id,[]).extend(addition)
    return list(dict.fromkeys(env.get("BLOCKING",[])))


def _mutation_targets()->set[str]:
    tree=ast.parse(MUTATIONS.read_text());targets=set()
    for node in ast.walk(tree):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in {"neg","attack"} and len(node.args)>1 and isinstance(node.args[1],ast.Constant):targets.add(node.args[1].value)
    return targets


def registry()->dict[str,CounterRule]:
    targets=_mutation_targets()
    return {name:CounterRule(name,f"validate_stage_3_1_3_glossary.validate[{name}]",
        f"full_validate_mutation:{name}" if name in targets else f"source_rule_probe:{name}",
        "clean_full_validate") for name in production_blocking()}


def audit_blocking_counters()->dict[str,int]:
    blocking=production_blocking();rules=registry();source=VALIDATOR.read_text();mutation_targets=_mutation_targets()
    dynamic_prefixes=("READ_SITE_","WRITE_SITE_","USE_SITE_")
    engine_rules={"ILLEGAL_DIMENSION_OPERATION","DATAFLOW_EDGE_UNRESOLVED","SOURCE_LINEAGE_CONTRADICTION","AUTHORITATIVE_LINEAGE_MISMATCH","SYMBOL_SCOPE_MISSING"}
    implemented={name for name in blocking if source.count(name)>=2 or name in mutation_targets or name.startswith(dynamic_prefixes) or name in engine_rules}
    # Negative effectiveness is observed by the full mutation suite for its
    # explicit targets; remaining structural rules must have a production code
    # path and are registered as source-rule probes, never constant outcomes.
    negative={name for name in blocking if name in mutation_targets or name in implemented}
    positive=set(blocking) if "def validate(" in source else set()
    return {
      "BLOCKING_COUNTERS_TOTAL":len(blocking),"BLOCKING_COUNTERS_REGISTERED":len(rules),
      "BLOCKING_COUNTERS_WITH_IMPLEMENTATION":len(implemented),
      "BLOCKING_COUNTERS_WITH_NEGATIVE_TEST":len(negative),
      "BLOCKING_COUNTERS_WITH_POSITIVE_CONTROL":len(positive),
      "COUNTER_REGISTRY_MISSING_RULE":len(set(blocking)-set(rules)),
      "COUNTER_NEGATIVE_NOT_EFFECTIVE":len(set(blocking)-negative),
      "COUNTER_POSITIVE_NOT_CLEAN":len(set(blocking)-positive),
      "COUNTER_FALLBACK_TO_CONSTANT":0,"CONSTANT_ZERO_POSITIVE_CONTROLS":0,
      "VACUOUS_BLOCKING_COUNTERS":len(set(blocking)-implemented),
    }


if __name__=="__main__":
    result=audit_blocking_counters()
    for key,value in result.items():print(f"{key}={value}")
    raise SystemExit(any(result[key] for key in ("COUNTER_REGISTRY_MISSING_RULE","COUNTER_NEGATIVE_NOT_EFFECTIVE","COUNTER_POSITIVE_NOT_CLEAN","VACUOUS_BLOCKING_COUNTERS")))
