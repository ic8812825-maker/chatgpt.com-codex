from dataclasses import dataclass,replace
from decimal import Decimal as D
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Tools'))
from stage_3_1_5_money_oracle import *
from restart_fixtures import restart_workflow
@dataclass(frozen=True)
class ProbeResult: before:object;operation:str;after:object;reason:str;passed:bool
def _base():
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));e=EconomicLedger(i,b);e.apply(Deal(i,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5')));k=EventKey(1,'X',2,'C','H',1,'P','P',1,AllocationType.FINAL_RESERVE);ev=EventRecord(k,ReconciliationState.RECONCILED);a=AllocationLedger(i);a.allocate(ev,e,k,D('4'),[1],D('1'));return i,b,e,k,ev,a
def _store():
 i,b,e,k,ev,a=_base();ev.transition(ReconciliationState.ALLOCATION_PENDING);ev.transition(ReconciliationState.APPLIED);ev.transition(ReconciliationState.PERSISTED);s=PersistentStore(e,a,{k:ev},1);snap=make_snapshot(i,k,'H',1,'S','P',b,(),D('5'),ReconciliationState.PERSISTED,1,ledger_revision=1,final_reserve_available=D('4'),money_state_version=s.money_state_version);return s,snap
def metadata_mismatch():
 i,b,e,k,_,_=_base()
 try:make_snapshot(i,k,'OTHER',1,'S','P',b,(),D('5'),ReconciliationState.PERSISTED,1,money_state_version=PersistentStore(e,AllocationLedger(i)).money_state_version);ok=False;reason='accepted'
 except ValueError as x:ok=True;reason=str(x)
 return ProbeResult('valid metadata','change event_type','rejected',reason,ok)
def foreign_snapshot():
 i,b,e,k,_,_=_base();foreign=Identity(9,'X',2,'C')
 try:make_snapshot(foreign,k,'H',1,'S','P',b,(),D('5'),ReconciliationState.PERSISTED,1,money_state_version=PersistentStore(e,AllocationLedger(i)).money_state_version);ok=False;reason='accepted'
 except ValueError as x:ok=True;reason=str(x)
 return ProbeResult(i,'foreign identity',foreign,reason,ok)
def source_reuse_after_restart():
 s,_=_store();r=PersistentStore.deserialize(s.serialize());k=next(iter(r.allocation.records))
 try:r.allocation.allocate(EventRecord(k,ReconciliationState.RECONCILED),r.economic,replace(k,deal_ticket=2),D('1'),[1]);ok=False;reason='accepted'
 except ValueError as x:ok=True;reason=str(x)
 return ProbeResult(D('5'),'restart then reuse',r.allocation.available(AllocationType.FINAL_RESERVE),reason,ok)
def opening_in_allocation():
 i,b,_,k,_,_=_base();e=EconomicLedger(i,b);e.apply(Deal(i,1,'P',DealEntry.IN,DealType.BUY,D('.01'),D('5')))
 try:AllocationLedger(i).allocate(EventRecord(k,ReconciliationState.RECONCILED),e,k,D('1'),[1]);ok=False;reason='accepted'
 except ValueError as x:ok=True;reason=str(x)
 return ProbeResult(DealEntry.IN,'allocate',0,reason,ok)
def unrelated_consumption():
 i,b,e,k,ev,a=_base();bad=ConsumptionKey(1,'X',2,'C','FINAL_FAR_CLOSE',9,'P','OTHER','T',ConsumptionPurpose.FINAL_FAR_CLOSE,k)
 try:a.consume(k,bad,D('1'));ok=False;reason='accepted'
 except ValueError as x:ok=True;reason=str(x)
 return ProbeResult(a.available(AllocationType.FINAL_RESERVE),'unrelated event consume',a.available(AllocationType.FINAL_RESERVE),reason,ok)
def _stale(component):
 s,snap=_store();before=s.money_state_version
 if component=='economic':s.economic.revision+=1
 elif component=='allocation':s.allocation.revision+=1
 elif component=='event':next(iter(s.events.values())).revision+=1
 elif component=='positions':s.positions_revision+=1
 result=evaluate_final_close(snap,s,True,True,FinalClosePolicy(D('-1'),D('1'),1));return ProbeResult(before,f'stale {component}',s.money_state_version,','.join(result.reasons),'MONEY_STATE_STALE' in result.reasons)
def stale_economic():return _stale('economic')
def stale_allocation():return _stale('allocation')
def stale_event():return _stale('event')
def stale_positions():return _stale('positions')
def event_version_collision():
 s,_=_store();k=next(iter(s.events));other=replace(k,deal_ticket=2);s.events[other]=EventRecord(other,ReconciliationState.DISCOVERED,3);s.events[k].revision=1;a=s.money_state_version.event_store_digest;s.events[k].revision=2;s.events[other].revision=2;b=s.money_state_version.event_store_digest;return ProbeResult((1,3),'change revisions with same sum',(2,2),'collision safe',a!=b)
def missing_version():
 i,b,e,k,_,_=_base()
 try:make_snapshot(i,k,'H',1,'S','P',b,(),D('5'),ReconciliationState.PERSISTED,1);ok=False;reason='accepted'
 except ValueError as x:ok=True;reason=str(x)
 return ProbeResult('missing','construct snapshot','rejected',reason,ok)
def _crash(state):
 r=restart_workflow(state);return ProbeResult(state.value,'serialize/deserialize/resume',r,r['terminal'].value,r['side_effects']==1)
def early_crash():return _crash(ReconciliationState.DISCOVERED)
def crash_during_allocation():return _crash(ReconciliationState.ALLOCATION_PENDING)
def crash_after_allocation():return _crash(ReconciliationState.APPLIED)
def restart_allocation_once():return _crash(ReconciliationState.RECONCILED)
def restart_consumption_once():
 s,_=_store();k=next(iter(s.allocation.records));ck=ConsumptionKey(1,'X',2,'C','FINAL_FAR_CLOSE',1,'P','P','T',ConsumptionPurpose.FINAL_FAR_CLOSE,k);s.allocation.consume(k,ck,D('1'));r=PersistentStore.deserialize(s.serialize());again=r.allocation.consume(k,ck,D('1'));return ProbeResult(1,'restart and duplicate consumption',r.allocation.records[k].consumed,'duplicate noop',not again and r.allocation.records[k].consumed==1)
def duplicate_event_replay():
 s,_=_store();r=PersistentStore.deserialize(s.serialize());return ProbeResult(len(s.events),'replay same EventKey',len(r.events),'one record',len(r.events)==1)
def multi_source():
 i,b,e,k,ev,a=_base();e.apply(Deal(i,2,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('2')));k2=replace(k,deal_ticket=2,allocation_type=AllocationType.CARRY);a2=AllocationLedger(i);a2.allocate(EventRecord(k2,ReconciliationState.RECONCILED),e,k2,D('6'),[1,2]);return ProbeResult(D('7'),'allocate 6 from 5+2',a2.available(AllocationType.CARRY),'conserved',a2.available(AllocationType.CARRY)==6)
def out_to_in_tamper():
 s,_=_store();doc=json.loads(s.serialize());doc['deals'][0]['entry']='IN'
 try:PersistentStore.deserialize(json.dumps(doc));ok=False;reason='accepted'
 except ValueError as x:ok=True;reason=str(x)
 return ProbeResult('OUT','tamper persisted entry','IN',reason,ok)
def partial_fill_restart():
 s,_=_store();s.opening_costs['P']=OpenPositionCost(D('1'),D('-10'));s.opening_costs['P'].close(D('.5'),D('.4'),1);r=PersistentStore.deserialize(s.serialize());c=r.opening_costs['P'];return ProbeResult(D('-10'),'partial fill and restart',c.unallocated_entry_cost,'residual',c.unallocated_entry_cost==D('-6'))
def final_close_restart():
 s,snap=_store();r=PersistentStore.deserialize(s.serialize());snap=replace(snap,money_state_version=r.money_state_version);g=evaluate_final_close(snap,r,True,True,FinalClosePolicy(D('-1'),D('1'),1));return ProbeResult(False,'full restart Final Close',g.allowed,','.join(g.reasons),g.allowed)
PROBES=(metadata_mismatch,foreign_snapshot,source_reuse_after_restart,opening_in_allocation,unrelated_consumption,stale_economic,stale_allocation,stale_event,stale_positions,event_version_collision,missing_version,early_crash,crash_during_allocation,crash_after_allocation,restart_allocation_once,restart_consumption_once,duplicate_event_replay,multi_source,out_to_in_tamper,partial_fill_restart,final_close_restart)
def run_extended_probes():return {fn.__name__:fn() for fn in PROBES}
