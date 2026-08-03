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
  ck=ConsumptionKey(1,'X',2,'C','FINAL_FAR_CLOSE',1,'POST','P','RESTART-CONSUME',ConsumptionPurpose.FINAL_FAR_CLOSE,ak)
  if ck not in new.allocation.consumptions:new.allocation.consume(ak,ck,D('1'))
  new=PersistentStore.deserialize(new.serialize());duplicate_consume=new.allocation.consume(ak,ck,D('1'))
 else:duplicate_consume=False
 terminal_safe=ev.state in (ReconciliationState.CONFLICT,ReconciliationState.REJECTED)
 final_allowed=False
 if not terminal_safe:
  ek=next(iter(new.events));snap=make_snapshot(new.economic.identity,ek,'HARVEST',1,'R','POST',new.economic.broker,new.managed_positions,new.economic.realized_cycle_net,ReconciliationState.PERSISTED,new.revision,ledger_revision=new.revision,final_reserve_available=new.allocation.available(AllocationType.FINAL_RESERVE),money_state_version=new.money_state_version);final_allowed=evaluate_final_close(snap,new,True,True,FinalClosePolicy(D('-99'),D('1'),new.revision)).allowed
 return {'canonical':payload==PersistentStore.deserialize(payload).serialize(),'duplicate':duplicate,'money':new.economic.realized_cycle_net,'reserve':new.allocation.available(AllocationType.FINAL_RESERVE),'consumed':sum((c.amount for c in new.allocation.consumptions.values()),D('0')),'duplicate_consume':duplicate_consume,'terminal':ev.state,'irreversible':ev.irreversible_action_allowed,'revision':new.revision,'allocation_revision':new.allocation.revision,'event_revision':ev.revision,'side_effects':len(new.allocation.records),'terminal_safe':terminal_safe,'second_roundtrip':new.serialize()==PersistentStore.deserialize(new.serialize()).serialize(),'money_version':new.money_state_version,'final_close_allowed':final_allowed}
def all_restart_probes():return {s:restart_workflow(s) for s in ReconciliationState}
