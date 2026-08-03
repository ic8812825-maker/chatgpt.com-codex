#!/usr/bin/env python3
import inspect,sys,ast
from dataclasses import replace
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Tools'))
from stage_3_1_5_mutation_oracle import *
EXPECTED_TARGETS={name:'REALIZED_MONEY' for name in MUTATIONS}
EXPECTED_TARGETS.update({'ReserveAddedTwiceToRecoveryPL':'ALLOCATION_LEDGER','ReserveUsedForPartialFar':'FINAL_CLOSE','ForeignSymbolIncluded':'REALIZED_MONEY','ForeignMagicIncluded':'REALIZED_MONEY','ForeignCycleIncluded':'REALIZED_MONEY','InitialIgnoredProfitIncluded':'FINAL_CLOSE','DepositIncluded':'FINAL_CLOSE','DuplicateDealApplied':'REALIZED_MONEY','DuplicateEventAppliedAfterRestart':'EVENT_STATE','PartialFillResidualLost':'ALLOCATION_LEDGER','AllocationDoesNotConserveMoney':'ALLOCATION_LEDGER','NegativeHarvestCreditsReserve':'REALIZED_MONEY','FinalClosePreviewTreatedAsActual':'FINAL_CLOSE','UnreconciledDealAllowsNextState':'EVENT_STATE'})
def audit():
 results=counterexamples(EXPECTED_TARGETS);unknown=False
 try:run_mutation('__UNKNOWN__');unknown=True
 except KeyError:pass
 clean=execute_scenario(); first=next(iter(MUTATIONS.values())); renamed=replace(first,display_name='Независимое имя'); a=execute_scenario(first.callable(EconomicScenarioInput()));b=execute_scenario(renamed.callable(EconomicScenarioInput()))
 rename_changed=a!=b or a.digest!=b.digest
 extended_source=inspect.getsource(extended_counterexample_probes);tree=ast.parse(extended_source);hardcoded=sum(isinstance(v,ast.Constant) and v.value is True for n in ast.walk(tree) if isinstance(n,ast.Dict) for v in n.values)
 counters={
 'MISSING_MUTATIONS':len(set(EXPECTED_TARGETS)-set(MUTATIONS)),
 'INEFFECTIVE_MUTATIONS':sum(not r.changed_fields for r in results),
 'VACUOUS_MUTATIONS':sum(bool(r.clean_blockers) for r in results),
 'SELF_REFERENTIAL_MUTATIONS':sum(x in inspect.signature(execute_scenario).parameters for x in ('name','mutation','blocker')),
 'WRONG_TARGET':sum(not r.target_caught for r in results),
 'CLEAN_RUN_BLOCKED':len(evaluate_invariants(clean)),
 'NAME_DEPENDENT_RESULT':int(any(x in inspect.signature(execute_scenario).parameters for x in ('name','mutation'))),
 'RENAME_CHANGED_RESULT':int(rename_changed),
 'UNKNOWN_MUTATION_ACCEPTED':int(unknown),
 'HARDCODED_COUNTEREXAMPLE_RESULT':hardcoded}
 material={
 'NO_PROJECTED_MONEY_CHANGE':sum(r.clean_observables.projected_money==r.mutated_observables.projected_money for r in results),
 'NO_REALIZED_MONEY_CHANGE':sum(r.clean_observables.realized_cycle_net==r.mutated_observables.realized_cycle_net for r in results),
 'NO_LEDGER_CHANGE':sum(not r.ledger_changed for r in results),
 'NO_ALLOCATION_CHANGE':sum(r.clean_observables.digest.allocation==r.mutated_observables.digest.allocation for r in results),
 'NO_EVENT_STATE_CHANGE':sum(r.clean_observables.digest.event==r.mutated_observables.digest.event for r in results),
 'NO_PERSISTENCE_CHANGE':sum(r.clean_observables.digest.persistence==r.mutated_observables.digest.persistence for r in results),
 'NO_FINAL_GATE_CHANGE':sum(r.clean_observables.final_close_allowed==r.mutated_observables.final_close_allowed for r in results),
 'NO_MATERIAL_OUTCOME_CHANGE':sum(not r.changed_fields for r in results)}
 return results,counters,material
def main():
 rs,c,m=audit();print(f'COUNTEREXAMPLES_TOTAL={len(rs)}');print(f'COUNTEREXAMPLES_CAUGHT={sum(r.target_caught for r in rs)}');[print(f'{k}={v}') for k,v in {**c,**m}.items()];ok=all(v==0 for v in c.values());print('BLOCKER_CAUSAL_AUDIT='+('PASS' if ok else 'FAIL'));raise SystemExit(not ok)
if __name__=='__main__':main()
