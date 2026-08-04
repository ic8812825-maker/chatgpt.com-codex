#!/usr/bin/env python3
import inspect,sys,ast
from dataclasses import replace
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Tools'))
from stage_3_1_5_mutation_oracle import *
EXPECTED_TARGETS={name:'REALIZED_MONEY_FROM_ELIGIBLE_DEALS' for name in MUTATIONS}
EXPECTED_TARGETS.update({'SellCloseUsesBid':'PROJECTED_MONEY_FORMULA','RequestedVolumeUsedInsteadOfActual':'PROJECTED_MONEY_FORMULA','ForeignSymbolIncluded':'IDENTITY_ISOLATION','ForeignMagicIncluded':'IDENTITY_ISOLATION','ForeignCycleIncluded':'IDENTITY_ISOLATION','ReserveAddedTwiceToRecoveryPL':'RECOVERY_MONEY_FORMULA','ReserveUsedForPartialFar':'CONSUMPTION_CONSERVATION','ForeignSymbolIncluded':'IDENTITY_ISOLATION','ForeignMagicIncluded':'IDENTITY_ISOLATION','ForeignCycleIncluded':'IDENTITY_ISOLATION','InitialIgnoredProfitIncluded':'REALIZED_MONEY_FROM_ELIGIBLE_DEALS','DepositIncluded':'REALIZED_MONEY_FROM_ELIGIBLE_DEALS','DuplicateDealApplied':'DEAL_EXACTLY_ONCE','DuplicateEventAppliedAfterRestart':'EVENT_EXACTLY_ONCE','PartialFillResidualLost':'ALLOCATION_CONSERVATION','AllocationDoesNotConserveMoney':'ALLOCATION_CONSERVATION','NegativeHarvestCreditsReserve':'REALIZED_MONEY_FROM_ELIGIBLE_DEALS','FinalClosePreviewTreatedAsActual':'FINAL_CLOSE_GATE_INTEGRITY','UnreconciledDealAllowsNextState':'EVENT_TRANSITION_VALIDITY'})
def audit():
 results=counterexamples(EXPECTED_TARGETS);unknown=False
 try:run_mutation('__UNKNOWN__');unknown=True
 except KeyError:pass
 clean=execute_scenario(); first=next(iter(MUTATIONS.values())); renamed=replace(first,display_name='Независимое имя'); a=execute_scenario(first.callable(EconomicScenarioInput()));b=execute_scenario(renamed.callable(EconomicScenarioInput()))
 rename_changed=a!=b or a.digest!=b.digest
 def domain_changed(r):
  target=EXPECTED_TARGETS[r.name]
  if target in ('REALIZED_MONEY_FROM_ELIGIBLE_DEALS','PROJECTED_MONEY_FORMULA','SOURCE_POOL_CONSERVATION','RECOVERY_MONEY_FORMULA'):return (r.clean_observables.projected_money,r.clean_observables.realized_cycle_net,r.clean_observables.recovery_pl_close_now,r.clean_observables.source_pool_net)!=(r.mutated_observables.projected_money,r.mutated_observables.realized_cycle_net,r.mutated_observables.recovery_pl_close_now,r.mutated_observables.source_pool_net)
  if target=='ALLOCATION_CONSERVATION':return r.clean_observables.digest.allocation!=r.mutated_observables.digest.allocation or r.clean_observables.allocations!=r.mutated_observables.allocations or r.clean_observables.residual!=r.mutated_observables.residual
  if target in ('EVENT_TRANSITION_VALIDITY','EVENT_EXACTLY_ONCE'):return (r.clean_observables.digest.event,r.clean_observables.event_applications,r.clean_observables.facts.reconciliation_input)!=(r.mutated_observables.digest.event,r.mutated_observables.event_applications,r.mutated_observables.facts.reconciliation_input)
  if target=='CONSUMPTION_CONSERVATION':return (r.clean_observables.consumptions,r.clean_observables.facts.allocation_consumed)!=(r.mutated_observables.consumptions,r.mutated_observables.facts.allocation_consumed)
  if target=='FINAL_CLOSE_GATE_INTEGRITY':return (r.clean_observables.final_close_allowed,r.clean_observables.reason_codes,r.clean_observables.facts.preview_execution)!=(r.mutated_observables.final_close_allowed,r.mutated_observables.reason_codes,r.mutated_observables.facts.preview_execution)
  return bool(r.changed_fields)
 material_domain_failures=sum(not domain_changed(r) for r in results)
 priority=('IDENTITY_ISOLATION','PROJECTED_MONEY_FORMULA','DEAL_EXACTLY_ONCE','EVENT_EXACTLY_ONCE','TRANSACTION_EXACTLY_ONCE','EVENT_TRANSITION_VALIDITY','REALIZED_MONEY_FROM_ELIGIBLE_DEALS','RECOVERY_MONEY_FORMULA','SOURCE_POOL_CONSERVATION','ALLOCATION_CONSERVATION','CONSUMPTION_CONSERVATION','PERSISTENCE_ROUNDTRIP','FINAL_CLOSE_GATE_INTEGRITY')
 first=lambda blockers:next((x for x in priority if x in blockers),None)
 wrong_first=sum(first(r.mutated_blockers)!=r.expected_target_blocker for r in results)
 mutation_not_applied=sum(not any(x.startswith('FAULT_') for x in r.mutated_observables.operation_trace) for r in results)
 unreached=sum(r.expected_target_blocker not in r.mutated_blockers for r in results)
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
 'HARDCODED_COUNTEREXAMPLE_RESULT':hardcoded,
 'MATERIAL_DOMAIN_FAILURES':material_domain_failures,
 'WRONG_EXCEPTION_CODE':sum(bool(r.mutated_observables.fault_evidence and r.mutated_observables.fault_evidence.exception) for r in results),
 'WRONG_FIRST_BLOCKER':wrong_first,'UNREACHED_TARGET_GUARD':unreached,'MUTATION_NOT_APPLIED':mutation_not_applied,
 'CORRECT_REJECTION_COUNTED_AS_KILL':sum(bool((e:=r.mutated_observables.fault_evidence) and e.operation_attempted and not e.operation_accepted and r.target_caught) for r in results),
 'GENERIC_FAULT_TRACE':sum(any(token=='FAULT_INPUT_OR_RULE' for token in r.mutated_observables.operation_trace) for r in results),
 'FAULT_ADAPTER_NOT_CALLED':sum(not (r.mutated_observables.fault_evidence and r.mutated_observables.fault_evidence.called) for r in results),
 'FAULT_OPERATION_REJECTED':sum(bool((e:=r.mutated_observables.fault_evidence) and not e.operation_accepted) for r in results),
 'FAULT_OPERATION_ACCEPTED_BUT_NO_EFFECT':sum(bool((e:=r.mutated_observables.fault_evidence) and e.operation_accepted and not e.persistence_effect and e.economic_effect==0) for r in results),
 'MANUAL_OBSERVABLE_ASSIGNMENT':sum(bool(r.changed_fields and not r.mutated_observables.fault_evidence) for r in results),
 'EXPECTED_REFERENCE_MUTATED':sum((r.clean_observables.facts.projected_reference,r.clean_observables.facts.realized_reference,r.clean_observables.facts.planned_allocation,r.clean_observables.facts.planned_residual)!=(r.mutated_observables.facts.projected_reference,r.mutated_observables.facts.realized_reference,r.mutated_observables.facts.planned_allocation,r.mutated_observables.facts.planned_residual) for r in results),
 'MUTATION_CONTROLS_EXPECTED_RESULT':sum(k.startswith('intended_') for k in EconomicScenarioInput.__dataclass_fields__),
 'MUTATION_NAME_CONTROLS_EXECUTION':sum(x in inspect.signature(execute_scenario).parameters for x in ('name','mutation','display_name')),
 'TARGET_GUARD_NOT_REACHED':unreached,'NO_MATERIAL_STATE_CHANGE':material_domain_failures,
 'NO_PERSISTENCE_EFFECT':sum(bool((e:=r.mutated_observables.fault_evidence) and not e.persistence_effect) for r in results)}
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
