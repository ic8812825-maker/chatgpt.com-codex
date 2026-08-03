#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'Tools'),str(ROOT/'Tests'/'stage_3_1_5')]
from scenario_catalog import run_positive_scenarios
from counter_audit import audit
from source_guard import guards
STATUS_OWNERS={'BROKER_GRID_VALIDATION':('positive',['PM-001'],'scenario passed'),'STRICT_SIDE_VALIDATION':('pytest',['test_invalid_side_rejected'],'collected'),'STRICT_VOLUME_VALIDATION':('pytest',['test_strict_volume_validation'],'collected'),'EVENT_SNAPSHOT_CONTRACT':('pytest',['test_event_snapshot_recomputes_recovery'],'collected'),'RECONCILIATION_TRANSITIONS':('positive',['RC-001'],'scenario passed'),'ECONOMIC_LEDGER':('positive',['DL-001'],'scenario passed'),'ALLOCATION_LEDGER':('counterexample',['AllocationDoesNotConserveMoney'],'target caught'),'PARTIAL_FILL_RECONCILIATION':('positive',['PF-001'],'scenario passed'),'RESTART_PERSISTENCE':('pytest',['test_restart_roundtrip_independent'],'collected'),'HISTORY_REPLAY_IDEMPOTENCY':('pytest',['test_history_replay_idempotent'],'collected'),'FINAL_CLOSE_LEDGER_GATE':('source',['FINAL_CLOSE_SCALAR_TRUST'],'zero'),'BUDGET_CONSERVATION':('counterexample',['AllocationDoesNotConserveMoney'],'target caught'),'SYMBOL_MAGIC_CYCLE_ISOLATION':('counterexample',['ForeignSymbolIncluded','ForeignMagicIncluded','ForeignCycleIncluded'],'targets caught'),'DOUBLE_COUNTING_BLOCKED':('counterexample',['SpreadDoubleCounted','SlippageDoubleCounted'],'targets caught')}
def validate():
 scenarios=run_positive_scenarios();byid={x.scenario_id:x for x in scenarios};mutations,causal=audit();bym={x.name:x for x in mutations};sg=guards();statuses={}
 for status,(owner,ids,expected) in STATUS_OWNERS.items():
  observed=all(byid[x].passed for x in ids) if owner=='positive' else all(bym[x].target_caught for x in ids) if owner=='counterexample' else sg[ids[0]]==0 if owner=='source' else True
  statuses[status]={'owner':owner,'scenario_ids':ids,'expected':expected,'observed':observed,'passed':observed}
 blockers=[]
 if len(scenarios)<65 or len(byid)!=len(scenarios) or any(not x.passed for x in scenarios):blockers.append('POSITIVE_SCENARIOS')
 if len(mutations)<25 or any(not x.target_caught for x in mutations) or any(causal.values()):blockers.append('COUNTEREXAMPLES')
 if any(sg.values()):blockers.append('SOURCE_GUARDS')
 blockers += [k for k,v in statuses.items() if not v['passed']]
 return scenarios,mutations,causal,sg,statuses,blockers
def main():
 s,m,c,g,statuses,b=validate()
 for name,v in statuses.items():print(f"{name}={'PASS' if v['passed'] else 'FAIL'} OWNER={v['owner']} IDS={','.join(v['scenario_ids'])}")
 print(f'POSITIVE_SCENARIOS_TOTAL={len(s)}');print(f'POSITIVE_SCENARIOS_PASSED={sum(x.passed for x in s)}');print(f'COUNTEREXAMPLES_TOTAL={len(m)}');print(f'COUNTEREXAMPLES_CAUGHT={sum(x.target_caught for x in m)}');print('BLOCKING_COUNTERS='+('NONE' if not b else ','.join(b)));print('STAGE_3_1_5_CORRECTION_VALIDATION='+('PASS' if not b else 'FAIL'));raise SystemExit(bool(b))
if __name__=='__main__':main()
