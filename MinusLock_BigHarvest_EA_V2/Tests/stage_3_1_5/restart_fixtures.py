import sys
from pathlib import Path
from decimal import Decimal as D
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Tools'))
from stage_3_1_5_money_oracle import *
def keys():
 event=EventKey(1,'X',2,'C','HARVEST',1,'POST','P',1,AllocationType.RESIDUAL)
 alloc=EventKey(1,'X',2,'C','HARVEST',1,'POST','P',1,AllocationType.FINAL_RESERVE)
 return event,alloc
def _state():
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));e=EconomicLedger(i,b);d=Deal(i,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5'));e.apply(d);ek,ak=keys();ev=EventRecord(ek);a=AllocationLedger(i);p=Position(i,'P','L','F',PositionSide.BUY,D('.01'),D('1'));return PersistentStore(e,a,{ek:ev},0,{'P':OpenPositionCost(D('.5'),D('-2'))},(p,)),d,ak
def advance(store,allocation_key):
 ev=next(iter(store.events.values()))
 if ev.state is ReconciliationState.DISCOVERED:ev.transition(ReconciliationState.PENDING_RECONCILIATION);return
 if ev.state is ReconciliationState.PENDING_RECONCILIATION:
  if not store.economic.closing_deals():raise ValueError('actual history absent')
  ev.transition(ReconciliationState.RECONCILED);return
 if ev.state is ReconciliationState.RECONCILED:
  ev.transition(ReconciliationState.ALLOCATION_PENDING);return
 if ev.state is ReconciliationState.ALLOCATION_PENDING:
  source=next(iter(store.economic.deals));
  if allocation_key not in store.allocation.records:
   shadow=EventRecord(ev.event_id,ReconciliationState.RECONCILED,ev.revision);store.allocation.allocate(shadow,store.economic,allocation_key,D('4'),[source],D('1'))
  ev.transition(ReconciliationState.APPLIED);return
 if ev.state is ReconciliationState.APPLIED:
  store.revision+=1;ev.transition(ReconciliationState.PERSISTED);return
 raise ValueError('terminal state')
def build_to(crash):
 store,d,ak=_state();ev=next(iter(store.events.values()))
 if crash in (ReconciliationState.CONFLICT,ReconciliationState.REJECTED):ev.transition(crash);return store,d,ak
 while ev.state is not crash:advance(store,ak)
 return store,d,ak
def restart_workflow(crash):
 old,deal,ak=build_to(crash);payload=old.serialize();new=PersistentStore.deserialize(payload);duplicate=new.replay_history([deal]);ev=next(iter(new.events.values()))
 if ev.state not in (ReconciliationState.CONFLICT,ReconciliationState.REJECTED):
  while ev.state is not ReconciliationState.PERSISTED:advance(new,ak)
 terminal_safe=ev.state in (ReconciliationState.CONFLICT,ReconciliationState.REJECTED)
 return {'canonical':payload==PersistentStore.deserialize(payload).serialize(),'duplicate':duplicate,'money':new.economic.realized_cycle_net,'reserve':new.allocation.available(AllocationType.FINAL_RESERVE),'terminal':ev.state,'irreversible':ev.irreversible_action_allowed,'revision':new.revision,'side_effects':len(new.allocation.records),'terminal_safe':terminal_safe}
def all_restart_probes():return {s:restart_workflow(s) for s in ReconciliationState}
