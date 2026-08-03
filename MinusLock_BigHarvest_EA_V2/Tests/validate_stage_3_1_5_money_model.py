#!/usr/bin/env python3
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'Tools'),str(ROOT/'Tests'/'stage_3_1_5')]
from scenario_catalog import run_positive_scenarios,missing_scenario_categories
from counter_audit import audit
from source_guard import guards
from restart_fixtures import all_restart_probes
from stage_3_1_5_mutation_oracle import extended_counterexample_probes
REQUIRED_EXPLOITS=frozenset(('SourcePoolPersistence','ManagedPositionsPersistence','SourceReuseBlocked','OpeningINCannotFundAllocation','UnrelatedConsumeRejected','EarlyCrashCompletesAllocation','RestartAllocationExactlyOnce','RestartConsumptionExactlyOnce'))
def validate():
 scenarios=run_positive_scenarios();mutations,causal,material=audit();extended=extended_counterexample_probes();restart=all_restart_probes();testfile=ROOT/'Tests'/'test_stage_3_1_5_money_model.py';pytest_run=subprocess.run([sys.executable,'-m','pytest','-q',str(testfile)],capture_output=True,text=True)
 owners={
 'SOURCE_POOL_PERSISTENCE':lambda:extended['SourcePoolPersistence'],
 'MANAGED_POSITION_PERSISTENCE':lambda:extended['ManagedPositionsPersistence'],
 'SOURCE_REUSE_AFTER_RESTART_BLOCKED':lambda:extended['SourceReuseBlocked'],
 'OPENING_IN_ALLOCATION_BLOCKED':lambda:extended['OpeningINCannotFundAllocation'],
 'CONSUMPTION_PARENT_BINDING':lambda:extended['UnrelatedConsumeRejected'],
 'EARLY_CRASH_SIDE_EFFECT_COMPLETION':lambda:extended['EarlyCrashCompletesAllocation'],
 'RESTART_ALLOCATION_EXACTLY_ONCE':lambda:extended['RestartAllocationExactlyOnce'],
 'RESTART_CONSUMPTION_EXACTLY_ONCE':lambda:extended['RestartConsumptionExactlyOnce'],
 'REQUIRED_SCENARIO_CATEGORIES':lambda:not missing_scenario_categories(scenarios),
 'REAL_ECONOMIC_MUTATIONS':lambda:all(m.target_caught and m.changed_fields for m in mutations),
 'EXTENDED_COUNTEREXAMPLES':lambda:REQUIRED_EXPLOITS<=extended.keys() and all(extended.values()),
 'CAUSAL_AUDIT':lambda:all(v==0 for v in causal.values()),
 'PYTEST':lambda:pytest_run.returncode==0}
 results={name:owner() for name,owner in owners.items()};sg=guards();results['SOURCE_GUARDS']=not any(sg.values())
 results['SCENARIOS']=len(scenarios)>=120 and len({s.fingerprint for s in scenarios})==len(scenarios) and all(s.expected is not s.actual and s.passed for s in scenarios)
 results['RESTART']=all(x['canonical'] and x['duplicate']==0 and (x['terminal_safe'] or x['side_effects']==1) for x in restart.values())
 blockers=sorted(k for k,v in results.items() if not v)
 return scenarios,mutations,causal,material,sg,restart,extended,pytest_run,results,blockers
def main():
 s,m,c,material,g,r,e,p,status,b=validate();print(f'PYTEST_EXECUTED={p.returncode==0}');print(f'POSITIVE_SCENARIOS_TOTAL={len(s)}');print(f'UNIQUE_FINGERPRINTS={len({x.fingerprint for x in s})}');print(f'MISSING_SCENARIO_CATEGORIES={len(missing_scenario_categories(s))}');print(f'LOSS_MONEY_SCENARIOS={sum(x.category in {"BUY_LOSS","SELL_LOSS"} for x in s)}');print(f'MUTATIONS_TOTAL={len(m)}');print(f'EXTENDED_COUNTEREXAMPLES={len(e)}');[print(f'{k}={"PASS" if v else "FAIL"}') for k,v in status.items()];print('BLOCKING_COUNTERS='+('NONE' if not b else ','.join(b)));print('STAGE_3_1_5_VALIDATION='+('PASS' if not b else 'FAIL'));raise SystemExit(bool(b))
if __name__=='__main__':main()
