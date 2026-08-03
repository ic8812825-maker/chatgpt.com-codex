#!/usr/bin/env python3
import sys
from pathlib import Path
from decimal import Decimal as D
import pytest
ROOT=Path(__file__).resolve().parents[1]; sys.path[:0]=[str(ROOT/'Tools'),str(ROOT/'Tests'/'stage_3_1_5')]
from stage_3_1_5_money_oracle import *
from scenario_catalog import run_positive_scenarios
SCENARIOS=run_positive_scenarios()
@pytest.mark.parametrize('result',SCENARIOS,ids=lambda x:x.scenario_id)
def test_positive_scenario(result): assert result.passed
@pytest.mark.parametrize('field,value',[('bid',D('1.10001')),('ask',D('1.10021')),('tick_size',D('0')),('tv_profit',D('0')),('tv_loss',D('-1'))])
def test_broker_validation_rejects(field,value):
 kw=dict(bid=D('1.1000'),ask=D('1.1002'),tick_size=D('.0001'),tv_profit=D('10'),tv_loss=D('10'));kw[field]=value
 with pytest.raises(ValueError):Broker(**kw)
@pytest.mark.parametrize('lot',[D('0'),D('-.1'),D('.015')])
def test_strict_volume_validation(lot):
 with pytest.raises(ValueError):Broker(D('1'),D('1'),D('.0001'),D('10'),D('10')).validate_lot(lot)
def test_invalid_side_rejected():
 with pytest.raises(ValueError):projected_profit('SELL',D('.1'),D('1'),Broker(D('1'),D('1'),D('.0001'),D('10'),D('10')))
def test_event_snapshot_recomputes_recovery():
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));s=make_snapshot(i,'E','H',1,'S','P',b,[],D('3'),ReconciliationState.DISCOVERED,0);assert s.recovery_pl_close_now==D('3')
def test_reconciliation_invalid_jump():
 with pytest.raises(ValueError):EventRecord('E').transition(ReconciliationState.PERSISTED)
def test_history_replay_idempotent():
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));e=EconomicLedger(i,b);d=Deal(i,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('2'));assert e.replay([d,d])==1
def test_restart_roundtrip_independent():
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));e=EconomicLedger(i,b);e.apply(Deal(i,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('2')));s=PersistentStore(e,AllocationLedger(i),{'E':EventRecord('E',ReconciliationState.PENDING_RECONCILIATION,1)},2);r=PersistentStore.deserialize(s.serialize());assert r is not s and r.economic.realized_cycle_net==D('2') and r.events['E'].state is ReconciliationState.PENDING_RECONCILIATION
def test_partial_overfill_and_zero_rejected():
 for v in (D('0'),D('2')):
  with pytest.raises(ValueError):OpenPositionCost(D('1'),D('-2')).close(v,v)
def main():
 failed=[x for x in SCENARIOS if not x.passed];print(f'POSITIVE_SCENARIOS_TOTAL={len(SCENARIOS)}');print(f'POSITIVE_SCENARIOS_PASSED={len(SCENARIOS)-len(failed)}');raise SystemExit(bool(failed))
if __name__=='__main__':main()
def test_allocation_conservation_and_duplicate():
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));e=EconomicLedger(i,b);e.apply(Deal(i,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5')));ev=EventRecord('E',ReconciliationState.RECONCILED);a=AllocationLedger(i);assert a.allocate(ev,e,AllocationType.FINAL_RESERVE,D('4'),[1],D('1'));assert not a.allocate(ev,e,AllocationType.FINAL_RESERVE,D('4'),[1],D('1'))
def test_final_close_ledger_gate():
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));e=EconomicLedger(i,b);e.apply(Deal(i,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5')));a=AllocationLedger(i);a.records[('E',AllocationType.FINAL_RESERVE)]=AllocationRecord(i,'E',(1,),AllocationType.FINAL_RESERVE,D('4'),D('4'),D('0'),D('0'),ReconciliationState.RECONCILED);ev=EventRecord('E',ReconciliationState.PERSISTED);s=PersistentStore(e,a,{'E':ev},1);snap=make_snapshot(i,'E','FINAL',1,'S','POST',b,[],e.realized_cycle_net,ReconciliationState.PERSISTED,1);assert evaluate_final_close(snap,s,[],b,True,True,D('0'),D('3'),1).allowed;assert not evaluate_final_close(snap,s,[],b,False,True,D('0'),D('3'),1).allowed
