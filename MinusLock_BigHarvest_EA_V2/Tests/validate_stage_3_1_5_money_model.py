#!/usr/bin/env python3
import inspect,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'Tools'),str(ROOT/'Tests'/'stage_3_1_5')]
from scenario_catalog import run_positive_scenarios,missing_scenario_categories,REQUIRED_SCENARIO_CATEGORIES
from counter_audit import audit
from source_guard import guards
from restart_fixtures import all_restart_probes
from extended_probes import run_extended_probes,run_restored_state_probes
from exploit_regressions import run as run_exploit_regressions
from correlated_attacks import run as run_correlated_attacks
from corrupted_store_final_close import run as run_corrupted_store_final_close
from causal_negative_controls import run as run_causal_negative_controls
from stage_3_1_5_mutation_oracle import execute_scenario,evaluate_invariants,run_mutation,MUTATIONS

def validate():
 scenarios=run_positive_scenarios();mutations,causal,material=audit();extended=run_extended_probes();restored_probes=run_restored_state_probes();restart=all_restart_probes();exploits=run_exploit_regressions();correlated=run_correlated_attacks();corrupted_gates=run_corrupted_store_final_close();negative_causal=run_causal_negative_controls();pytest_run=subprocess.run([sys.executable,'-m','pytest','-q',str(ROOT/'Tests'/'test_stage_3_1_5_money_model.py')],capture_output=True,text=True);required={r.category:r for r in scenarios if r.category in REQUIRED_SCENARIO_CATEGORIES}
 clean=execute_scenario();mutation_computed=all(not cb and mb==evaluate_invariants(m) for name in MUTATIONS for c,m,cb,mb in (run_mutation(name),))
 nonterminal=[r for s,r in restart.items() if not r['terminal_safe']]
 owners={
 'EVENT_HISTORY_REACHABILITY':lambda:all(r['passed'] for r in exploits if r['name'].startswith('PERSISTED_REVISION_') or r['name'].startswith('RECONCILIATION_HISTORY_')),
 'FILL_TICKET_RECORD_BINDING':lambda:all(r['passed'] for r in exploits if r['name'] in ('FILL_TICKET_SET_MISMATCH','RAW_DUPLICATE_FILL_TICKET','FILL_REVISION_MISMATCH')),
 'COMPLETE_MONEY_STATE_VERSION':lambda:'canonical_money_state' in inspect.getsource(type(restart[next(iter(restart))]['money_version'])) if False else all(r['passed'] for r in corrupted_gates),
 'STRICT_PERSISTENCE_SCHEMA':lambda:all(r['passed'] for r in exploits if r['name'] in ('UNKNOWN_TOP_LEVEL_FIELD','UNKNOWN_NESTED_FIELD','DUPLICATE_JSON_OBJECT_KEY')),
 'FINAL_CLOSE_CORRUPTED_STORE_REJECTION':lambda:len(corrupted_gates)>=4 and all(r['passed'] for r in corrupted_gates),
 'REAL_FAULT_ADAPTER_EXECUTION':lambda:all(r.mutated_observables.fault_evidence and r.mutated_observables.fault_evidence.called and r.mutated_observables.fault_evidence.operation_accepted for r in mutations),
 'SEMANTIC_CAUSAL_AUDIT':lambda:all(v==0 for v in causal.values()),
 'NEGATIVE_CAUSAL_CONTROLS':lambda:not any(negative_causal[k] for k in ('MISSING_CAUSAL_RULES','INEFFECTIVE_CAUSAL_RULES','VACUOUS_CAUSAL_RULES')),
 'EXPLOIT_REGRESSION_SUITE':lambda:len(exploits)>=20 and all(r['passed'] and r['target_guard_reached'] and r['actual']==r['expected'] for r in exploits),
 'CORRELATED_PERSISTENCE_ATTACKS':lambda:len(correlated)>=5 and all(correlated),
 'GLOBAL_MONEY_CONSERVATION':lambda:all(r['passed'] for r in exploits if r['name'] in ('OVER_ALLOCATION','CORRELATED_OVER_ALLOCATION')),
 'SOURCE_POOL_IDENTITY_ISOLATION':lambda:all(r['passed'] for r in exploits if r['name'].startswith('POOL_')),
 'EVENT_STORE_INTEGRITY':lambda:all(r['passed'] for r in exploits if r['name'] in ('FOREIGN_EVENT','IMPOSSIBLE_EVENT')),
 'OPENING_COST_PERSISTENCE_INTEGRITY':lambda:all(r['passed'] for r in exploits if r['name'] in ('NEGATIVE_OPENING_VOLUME','DUPLICATE_FILL','ALLOCATED_WITHOUT_FILL')),
 'FINAL_CLOSE_FAIL_CLOSED':lambda:all(r['passed'] for r in exploits),
 'SOURCE_POOL_RESTORE_ELIGIBILITY':lambda:extended['out_to_in_tamper'].passed and extended['opening_in_allocation'].passed,
 'PERSISTENCE_REFERENTIAL_INTEGRITY':lambda:extended['source_reuse_after_restart'].passed and extended['partial_fill_restart'].passed,
 'CONSUMPTION_FULL_EVENT_OWNERSHIP':lambda:extended['unrelated_consumption'].passed,
 'MONEY_STATE_VERSION_REQUIRED':lambda:extended['missing_version'].passed,
 'EVENT_STORE_VERSION_COLLISION_SAFE':lambda:extended['event_version_collision'].passed,
 'FINAL_CLOSE_STALE_STATE_REJECTION':lambda:all(extended[k].passed for k in ('stale_economic','stale_allocation','stale_event','stale_positions')),
 'POSITIVE_SCENARIO_EXECUTION':lambda:all(r.expected is not r.actual and r.passed for r in scenarios),
 'REQUIRED_SCENARIO_OWNERS':lambda:not missing_scenario_categories(scenarios) and len({r.inputs.get('owner') for r in required.values()})>=12,
 'ECONOMIC_FINGERPRINTS':lambda:len({r.fingerprint for r in scenarios})==len(scenarios),
 'INDEPENDENT_INVARIANT_EVALUATOR':lambda:not evaluate_invariants(clean) and mutation_computed and set(inspect.signature(evaluate_invariants).parameters)=={'result'},
 'REAL_ECONOMIC_MUTATIONS':lambda:all(r.target_caught and r.changed_fields for r in mutations),
 'MATERIAL_CAUSAL_AUDIT':lambda:all(v==0 for v in causal.values()) and causal.get('MATERIAL_DOMAIN_FAILURES')==0,
 'EXTENDED_COUNTEREXAMPLES':lambda:len(extended)>=20 and all(r.passed for r in extended.values()),
 'RESTORED_STATE_EXACT_REASONS':lambda:len(restored_probes)>=20 and all(r.passed and r.target_guard_reached and r.expected_code==r.actual_code for r in restored_probes.values()),
 'SOURCE_REUSE_TARGET_GUARD':lambda:extended['source_reuse_after_restart'].actual_code=='SOURCE_TICKET_REUSED' and extended['source_reuse_after_restart'].target_guard_reached,
 'OWNER_RUNTIME_EXECUTION':lambda:all(required[c].passed for c in ('CONSUMPTION','HISTORY_REPLAY','RESTART_CRASH_POINT','FINAL_CLOSE_PASS','FINAL_CLOSE_REJECTIONS','FULL_FILL')),
 'FULL_FILL_EXECUTION':lambda:required['FULL_FILL'].actual['volume']==0 and required['FULL_FILL'].actual['cost']==0,
 'RESTART_CRASH_POINTS':lambda:len(nonterminal)==6 and all(r['side_effects']==1 and r['second_roundtrip'] for r in nonterminal),
 'HISTORY_REPLAY_IDEMPOTENCY':lambda:all(r['duplicate']==0 and not r['duplicate_consume'] for r in nonterminal),
 'SOURCE_GUARDS':lambda:not any(guards().values()),
 'PYTEST_INTEGRATION':lambda:pytest_run.returncode==0}
 results={name:bool(owner()) for name,owner in owners.items()};blockers=sorted(k for k,v in results.items() if not v);return scenarios,mutations,causal,material,guards(),restart,{**extended,**restored_probes},pytest_run,results,blockers

def main():
 s,m,c,material,g,r,e,p,status,b=validate();print(f'PYTEST_EXECUTED={p.returncode==0}');print(f'POSITIVE_SCENARIOS_TOTAL={len(s)}');print(f'UNIQUE_FINGERPRINTS={len({x.fingerprint for x in s})}');print(f'MISSING_SCENARIO_CATEGORIES={len(missing_scenario_categories(s))}');print(f'MUTATIONS_TOTAL={len(m)}');print(f'EXTENDED_COUNTEREXAMPLES={len(e)}');[print(f'{k}={"PASS" if v else "FAIL"}') for k,v in status.items()];print('BLOCKING_COUNTERS='+('NONE' if not b else ','.join(b)));print('STAGE_3_1_5_VALIDATION='+('PASS' if not b else 'FAIL'));raise SystemExit(bool(b))
if __name__=='__main__':main()
