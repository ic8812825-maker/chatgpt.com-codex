import sys
from pathlib import Path
from decimal import Decimal as D
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Tools'))
from stage_3_1_5_money_oracle import *
def key(state,kind=AllocationType.FINAL_RESERVE,ticket=1):return EventKey(1,'X',2,'C','HARVEST',1,state.value,'P',ticket,kind)
def restart_probe(state:ReconciliationState):
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));e=EconomicLedger(i,b);d=Deal(i,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5'));e.apply(d);k=key(state);ev=EventRecord(k,state,3);a=AllocationLedger(i)
 if state in (ReconciliationState.RECONCILED,ReconciliationState.ALLOCATION_PENDING,ReconciliationState.APPLIED,ReconciliationState.PERSISTED):a.records[k]=AllocationRecord(k,(1,),D('4'),D('1'),D('1'),ReconciliationState.RECONCILED,1)
 s=PersistentStore(e,a,{k:ev},4,{'P':OpenPositionCost(D('.5'),D('-2'))});payload=s.serialize();r=PersistentStore.deserialize(payload);duplicate=r.replay_history([d]);return {'canonical':payload==r.serialize(),'duplicate':duplicate,'money':r.economic.realized_cycle_net,'reserve':r.allocation.available(AllocationType.FINAL_RESERVE),'state':r.events[k].state,'revision':r.revision,'cost':r.opening_costs['P'].unallocated_entry_cost}
def all_restart_probes():return {state:restart_probe(state) for state in ReconciliationState}
