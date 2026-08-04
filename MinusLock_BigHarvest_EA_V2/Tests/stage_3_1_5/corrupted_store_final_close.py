#!/usr/bin/env python3
"""Final Close вызывается на реально повреждённых in-memory stores со свежей версией."""
import copy,sys
from dataclasses import replace
from pathlib import Path
from decimal import Decimal as D
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Tools'))
from stage_3_1_5_money_oracle import *

def gate_fixture():
 i=Identity(1,'EURUSD',7,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));e=EconomicLedger(i,b);e.apply(Deal(i,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5')))
 k=EventKey(1,'EURUSD',7,'C','HARVEST',1,'POST','P',1,AllocationType.FINAL_RESERVE);ev=EventRecord(k);ev.transition(ReconciliationState.PENDING_RECONCILIATION);ev.transition(ReconciliationState.RECONCILED);a=AllocationLedger(i);a.allocate(ev,e,k,D('4'),[1]);ev.transition(ReconciliationState.ALLOCATION_PENDING);ev.transition(ReconciliationState.APPLIED);ev.transition(ReconciliationState.PERSISTED);store=PersistentStore(e,a,{k:ev},1)
 snap=make_snapshot(i,k,'HARVEST',1,'S','POST',b,(),D('5'),ReconciliationState.PERSISTED,1,ledger_revision=1,final_reserve_available=D('4'),money_state_version=store.money_state_version)
 return store,snap

def run():
 probes=[]
 def check(name,mutate,code):
  store,snapshot=gate_fixture();mutate(store);snapshot=replace(snapshot,money_state_version=store.money_state_version)
  gate=evaluate_final_close(snapshot,store,True,True,FinalClosePolicy(D('-1'),D('1'),1));expected='INTEGRITY_'+code.value
  probes.append({'name':name,'allowed':gate.allowed,'expected_code':expected,'actual_code':next((r for r in gate.reasons if r.startswith('INTEGRITY_')),None),'passed':not gate.allowed and 'LEDGER_INTEGRITY_FAILURE' in gate.reasons and expected in gate.reasons})
 check('IMPOSSIBLE_EVENT_HISTORY',lambda s:setattr(next(iter(s.events.values())),'history',next(iter(s.events.values())).history[:-1]),IntegrityCode.EVENT_STATE_REVISION_INVALID)
 def fill_mismatch(s):s.opening_costs['P']=OpenPositionCost(D('.5'),D('-5'),{999},D('-5'),D('1'),D('-10'),[FillRecord(1,D('.5'),D('.5'),D('1'),D('.5'),D('-5'))],1)
 check('FILL_TICKET_RECORD_MISMATCH',fill_mismatch,IntegrityCode.DUPLICATE_FILL_TICKET)
 def pool_over(s):p=next(iter(s.allocation.source_pools.values()));p.already_allocated=D('10')
 check('CORRELATED_SOURCE_OVERALLOCATION',pool_over,IntegrityCode.SOURCE_POOL_CONSERVATION_FAILURE)
 def foreign_pool(s):p=next(iter(s.allocation.source_pools.values()));p.key=replace(p.key,symbol='GBPUSD')
 check('FOREIGN_SOURCE_POOL',foreign_pool,IntegrityCode.SOURCE_POOL_FOREIGN_IDENTITY)
 return probes
if __name__=='__main__':
 p=run();[print(f"{x['name']}: FINAL_CLOSE_ALLOWED={x['allowed']} EXPECTED={x['expected_code']} ACTUAL={x['actual_code']}") for x in p];print('FINAL_CLOSE_CORRUPTED_STORE_REJECTION='+('PASS' if all(x['passed'] for x in p) else 'FAIL'));raise SystemExit(0 if all(x['passed'] for x in p) else 1)
