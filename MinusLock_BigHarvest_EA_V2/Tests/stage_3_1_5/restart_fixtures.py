import sys
from pathlib import Path
from decimal import Decimal as D
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Tools'))
from stage_3_1_5_money_oracle import *
def keys():
 event=EventKey(1,'X',2,'C','HARVEST',1,'POST','P',1,AllocationType.RESIDUAL)
 alloc=EventKey(1,'X',2,'C','HARVEST',1,'POST','P',1,AllocationType.FINAL_RESERVE)
 return event,alloc
def build_to(crash:ReconciliationState):
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));e=EconomicLedger(i,b);d=Deal(i,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5'));e.apply(d);ek,ak=keys();ev=EventRecord(ek);a=AllocationLedger(i);store=PersistentStore(e,a,{ek:ev},0,{'P':OpenPositionCost(D('.5'),D('-2'))})
 if crash in (ReconciliationState.CONFLICT,ReconciliationState.REJECTED):ev.transition(crash);return store,d,ak
 for target in (ReconciliationState.PENDING_RECONCILIATION,ReconciliationState.RECONCILED,ReconciliationState.ALLOCATION_PENDING,ReconciliationState.APPLIED,ReconciliationState.PERSISTED):
  if ev.state is ReconciliationState.RECONCILED and not a.records:a.allocate(ev,e,ak,D('4'),[1],D('1'))
  if ev.state is crash:break
  ev.transition(target)
  if ev.state is crash:break
 return store,d,ak
def restart_workflow(crash):
 old,deal,ak=build_to(crash);payload=old.serialize();new=PersistentStore.deserialize(payload);duplicate=new.replay_history([deal]);ev=next(iter(new.events.values()))
 if ev.state not in (ReconciliationState.CONFLICT,ReconciliationState.REJECTED,ReconciliationState.PERSISTED):
  while ev.state is not ReconciliationState.PERSISTED:ev.transition(next(iter(ALLOWED_TRANSITIONS[ev.state]-{ReconciliationState.CONFLICT,ReconciliationState.REJECTED})))
 return {'canonical':payload==PersistentStore.deserialize(payload).serialize(),'duplicate':duplicate,'money':new.economic.realized_cycle_net,'reserve':new.allocation.available(AllocationType.FINAL_RESERVE),'terminal':ev.state,'irreversible':ev.irreversible_action_allowed,'revision':new.revision}
def all_restart_probes():return {s:restart_workflow(s) for s in ReconciliationState}
