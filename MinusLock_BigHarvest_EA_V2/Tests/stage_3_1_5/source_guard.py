#!/usr/bin/env python3
import ast
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def _function(tree,name):return next((n for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==name),None)
def guards():
 paths={n:ROOT/p for n,p in {'money':'Tools/stage_3_1_5_money_oracle.py','mutation':'Tools/stage_3_1_5_mutation_oracle.py','scenario':'Tests/stage_3_1_5/scenario_catalog.py','validator':'Tests/validate_stage_3_1_5_money_model.py','audit':'Tests/stage_3_1_5/counter_audit.py','extended':'Tests/stage_3_1_5/extended_probes.py'}.items()};src={k:p.read_text() for k,p in paths.items()};trees={k:ast.parse(v) for k,v in src.items()}
 evaluator=_function(trees['mutation'],'evaluate_invariants');empty_eval=any(isinstance(n,ast.Return) and isinstance(n.value,(ast.Set,ast.Tuple,ast.List)) and not n.value.elts for n in ast.walk(evaluator)) if evaluator else 1
 fingerprint=_function(trees['scenario'],'fingerprint');fingerprint_text=ast.unparse(fingerprint) if fingerprint else ''
 extended_or=sum(isinstance(n,ast.BoolOp) and isinstance(n.op,ast.Or) for n in ast.walk(trees['extended']))
 probe_names={n.name for n in ast.walk(trees['extended']) if isinstance(n,ast.FunctionDef)}
 required_probes={'metadata_mismatch','foreign_snapshot','source_reuse_after_restart','opening_in_allocation','unrelated_consumption','stale_economic','stale_allocation','stale_event','stale_positions','missing_version','early_crash','crash_during_allocation','crash_after_allocation','restart_allocation_once','restart_consumption_once','duplicate_event_replay','multi_source','out_to_in_tamper','partial_fill_restart','final_close_restart'}
 return {'CONSTANT_EMPTY_INVARIANTS':int(bool(empty_eval)),'TARGETS_IN_EXECUTOR':int('TARGETS' in src['mutation']),'BLOCKER_ASSIGNED_FROM_NAME':int('frozenset({TARGET' in src['mutation'] or 'mutated_blockers=frozenset' in src['mutation']),'GENERIC_SCENARIO_ARITHMETIC':int("actual=sum((D(i),D('1'))" in src['scenario'] ),'FINGERPRINT_USES_LABEL':int(any(x in fingerprint_text for x in ('self.name','self.category','scenario_id'))),'EXTENDED_RESULT_ALIAS':int(len(required_probes-probe_names)>0),'EXTENDED_UNRELATED_OR':extended_or,'MONEY_VERSION_OPTIONAL':int("version=kw.get('money_state_version')" not in src['money'] or 'MoneyStateVersion required' not in src['money']),'EVENT_VERSION_REVISION_SUM':int('sum(e.revision' in src['money']),'CAUSAL_IGNORES_MATERIAL':int('MATERIAL_DOMAIN_FAILURES' not in src['audit']),'VALIDATOR_NEW_OWNERS_MISSING':int('SOURCE_POOL_RESTORE_ELIGIBILITY' not in src['validator']),'UNCONDITIONAL_PASS':int("owner=='pytest'" in src['validator']),'HARDCODED_BLOCKING_NONE':int("print('BLOCKING_COUNTERS=NONE')" in src['validator']),'EXPECTED_ACTUAL_ALIAS':int('expected=actual' in src['scenario']),'REQUIRED_OWNER_MISSING':int('REQUIRED_EXECUTABLE_FIXTURES' not in src['scenario'])}
def main():
 g=guards();[print(f'{k}={v}') for k,v in g.items()];raise SystemExit(any(g.values()))
if __name__=='__main__':main()
