#!/usr/bin/env python3
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'Tools'),str(ROOT/'Tests'/'stage_3_1_5')]
from scenario_catalog import run_positive_scenarios
from counter_audit import audit
from source_guard import guards
from restart_fixtures import all_restart_probes
from stage_3_1_5_mutation_oracle import extended_counterexample_probes
def validate():
 scenarios=run_positive_scenarios();mutations,causal=audit();sg=guards();restart=all_restart_probes();extended=extended_counterexample_probes();testfile=ROOT/'Tests'/'test_stage_3_1_5_money_model.py';pytest_run=subprocess.run([sys.executable,'-m','pytest','-q',str(testfile)],capture_output=True,text=True)
 blockers=[]
 if pytest_run.returncode:blockers.append('PYTEST_FAILED')
 if len(scenarios)<100 or len({x.scenario_id for x in scenarios})!=len(scenarios) or len({x.fingerprint for x in scenarios})!=len(scenarios):blockers.append('SCENARIOS')
 if any(x.expected is x.actual or not x.passed for x in scenarios):blockers.append('EXPECTED_ACTUAL')
 if any(v for k,v in causal.items()):blockers.append('CAUSAL')
 if any(sg.values()):blockers.append('SOURCE_GUARDS')
 if not all(x.target_caught and x.changed_fields for x in mutations):blockers.append('MUTATIONS')
 if not all(extended.values()):blockers.append('EXTENDED_COUNTEREXAMPLES')
 if not all(x['canonical'] and x['duplicate']==0 for x in restart.values()):blockers.append('RESTART')
 return scenarios,mutations,causal,sg,restart,extended,pytest_run,blockers
def main():
 s,m,c,g,r,e,p,b=validate();print(f'PYTEST_EXECUTED={p.returncode==0}');print(f'POSITIVE_SCENARIOS_TOTAL={len(s)}');print(f'UNIQUE_FINGERPRINTS={len({x.fingerprint for x in s})}');print(f'COUNTEREXAMPLES_TOTAL={len(m)+len(e)}');print('BLOCKING_COUNTERS='+('NONE' if not b else ','.join(b)));print('STAGE_3_1_5_CORRECTION_VALIDATION='+('PASS' if not b else 'FAIL'));raise SystemExit(bool(b))
if __name__=='__main__':main()
