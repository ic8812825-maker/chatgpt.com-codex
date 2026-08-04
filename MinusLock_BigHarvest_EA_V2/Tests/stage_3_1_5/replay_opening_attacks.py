#!/usr/bin/env python3
import sys,json
from pathlib import Path
from dataclasses import replace
from decimal import Decimal as D
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Tools'))
from stage_3_1_5_money_oracle import *
from corrupted_store_final_close import gate_fixture

def deal_results():
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));base=Deal(i,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5'));changes=[('PROFIT',{'profit':D('6')}),('SWAP',{'swap':D('1')}),('COMMISSION',{'commission':D('-1')}),('FEE',{'fee':D('-1')}),('VOLUME',{'actual_volume':D('.02')}),('ENTRY',{'entry':DealEntry.INOUT}),('TYPE',{'deal_type':DealType.SELL}),('POSITION',{'position_id':'Q'}),('ACCOUNT',{'identity':Identity(9,'X',2,'C')}),('SYMBOL',{'identity':Identity(1,'Y',2,'C')}),('MAGIC',{'identity':Identity(1,'X',9,'C')}),('CYCLE',{'identity':Identity(1,'X',2,'Z')})];out={}
 for name,change in changes:
  ledger=EconomicLedger(i,b);ledger.apply(base);before=(ledger.revision,ledger.realized_cycle_net,dict(ledger.deals));actual=None
  try:ledger.apply(replace(base,**change))
  except OracleIntegrityError as exc:actual=exc.code
  out['ALTERED_DEAL_'+name]=actual is IntegrityCode.DEAL_REPLAY_CONFLICT and before==(ledger.revision,ledger.realized_cycle_net,ledger.deals)
 return out

def event_results():
 key=EventKey(1,'X',2,'C','H',1,'P','P',1,AllocationType.RESIDUAL);event=EventRecord(key);event.transition(ReconciliationState.CONFLICT);store=PersistentStore(EconomicLedger(Identity(1,'X',2,'C'),Broker(D('1'),D('1'),D('.01'),D('1'),D('1'))),AllocationLedger(Identity(1,'X',2,'C')),{key:event});h=event.history[0]
 variants={'HISTORY':replace(event,history=(replace(h,terminal_reason='other'),)),'TERMINAL_REASON':replace(event,terminal_reason='other'),'TRANSITION_SOURCE':replace(event,history=(replace(h,source=ReconciliationState.RECONCILED),)),'TRANSITION_TARGET':replace(event,history=(replace(h,target=ReconciliationState.REJECTED),)),'TRANSITION_EVENT_KEY':replace(event,history=(replace(h,event_id=replace(key,level=2)),))};out={}
 for name,incoming in variants.items():
  actual=None
  try:store.apply_event(incoming)
  except OracleIntegrityError as exc:actual=exc.code
  out['SAME_STATE_REVISION_DIFFERENT_'+name]=actual is IntegrityCode.EVENT_REPLAY_CONFLICT
 return out

def opening_result():
 store,snapshot=gate_fixture();bad=OpenPositionCost(D('.5'),D('-1'),{1},D('-9'),D('1'),D('-10'),[FillRecord(1,D('.5'),D('.5'),D('1'),D('.5'),D('-9'))],1);store.opening_costs['P']=bad;code=None
 try:store.validate_integrity()
 except OracleIntegrityError as exc:code=exc.code
 snapshot=replace(snapshot,money_state_version=store.money_state_version);gate=evaluate_final_close(snapshot,store,True,True,FinalClosePolicy(D('-1'),D('1'),1))
 return code is IntegrityCode.OPENING_COST_ALLOCATION_MISMATCH and not gate.allowed and 'INTEGRITY_OPENING_COST_ALLOCATION_MISMATCH' in gate.reasons

def run():
 results={**deal_results(),**event_results(),'OPENING_COST_ALLOCATION_ATTACK':opening_result()};return results
if __name__=='__main__':
 r=run();[print(f'{k}={"PASS" if v else "FAIL"}') for k,v in r.items()];print('REPLAY_OPENING_ATTACKS='+('PASS' if r and all(r.values()) else 'FAIL'));raise SystemExit(0 if r and all(r.values()) else 1)
