import sys
from pathlib import Path
from decimal import Decimal as D
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'Tools'),str(ROOT/'Tests'/'stage_3_1_5')]
from stage_3_1_5_money_oracle import *
from scenario_catalog import run_positive_scenarios
from restart_fixtures import all_restart_probes
SCENARIOS=run_positive_scenarios()
def K(i=1,kind=AllocationType.RESIDUAL,account=1,symbol='X',magic=2,cycle='C',state='POST'):return EventKey(account,symbol,magic,cycle,'HARVEST',1,state,'P',i,kind)
def base():
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));e=EconomicLedger(i,b);e.apply(Deal(i,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5')));return i,b,e
@pytest.mark.parametrize('r',SCENARIOS,ids=lambda x:x.scenario_id)
def test_scenario_independent_fields(r):
 assert r.expected is not r.actual;assert r.expected==r.actual;assert r.expected_status==r.actual_status;assert r.invariants
@pytest.mark.parametrize('field,value',[('bid',D('1.001')),('ask',D('1.001')),('tick_size',D('0')),('tv_profit',D('0')),('tv_loss',D('-1'))])
def test_broker_invalid(field,value):
 q=dict(bid=D('1'),ask=D('1'),tick_size=D('.01'),tv_profit=D('1'),tv_loss=D('1'));q[field]=value
 with pytest.raises(ValueError):Broker(**q)
def test_event_snapshot_recomputes_recovery():
 i,b,e=base();k=K();s=make_snapshot(i,k,'HARVEST',1,'S','POST',b,[],e.realized_cycle_net,ReconciliationState.PERSISTED,1,ledger_revision=1);assert s.recovery_pl_close_now==D('5')
def test_foreign_position_in_snapshot_rejected():
 i,b,e=base();p=Position(Identity(2,'X',2,'C'),'P','L','F',PositionSide.BUY,D('.01'),D('1'))
 with pytest.raises(ValueError):make_snapshot(i,K(),'HARVEST',1,'S','POST',b,[p],D('0'),ReconciliationState.PERSISTED,1)
def test_allocation_and_consume_identity():
 i,b,e=base();ek=K();ak=K(kind=AllocationType.FINAL_RESERVE);ev=EventRecord(ek,ReconciliationState.RECONCILED);a=AllocationLedger(i);assert a.allocate(ev,e,ak,D('4'),[1],D('1'));before=a.available(AllocationType.FINAL_RESERVE);ck=K(2,AllocationType.CARRY);assert a.consume(ak,ck,D('2'),AllocationType.CARRY);assert a.available(AllocationType.FINAL_RESERVE)==before-D('2');assert not a.consume(ak,ck,D('2'),AllocationType.CARRY)
@pytest.mark.parametrize('kw',[{'account':9},{'symbol':'Y'},{'magic':9},{'cycle':'Z'}])
def test_foreign_consume_rejected(kw):
 i,b,e=base();ek=K();ak=K(kind=AllocationType.CARRY);ev=EventRecord(ek,ReconciliationState.RECONCILED);a=AllocationLedger(i);a.allocate(ev,e,ak,D('4'),[1],D('1'))
 with pytest.raises(ValueError):a.consume(ak,K(2,AllocationType.CARRY,**kw),D('1'),AllocationType.CARRY)
def test_multi_source_aggregate():
 i,b,e=base();e.apply(Deal(i,2,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('2')));ek=K();ak=K(kind=AllocationType.CARRY);a=AllocationLedger(i);assert a.allocate(EventRecord(ek,ReconciliationState.RECONCILED),e,ak,D('6'),[1,2])
def test_restart_all_states():
 for state,r in all_restart_probes().items():assert r['canonical'] and r['duplicate']==0 and r['money']==D('5')
def test_opening_in_not_realized():
 i,b,e=base();e2=EconomicLedger(i,b);e2.apply(Deal(i,3,'P',DealEntry.IN,DealType.BUY,D('.01'),D('5')));assert e2.realized_cycle_net==0
def test_partial_fill_conservation():
 _,b,_=base();p=OpenPositionCost(D('1'),D('-10'));r1=p.close(D('.4'),D('.3'),1,b);r2=p.close(D('.7'),D('.7'),2,b);assert p.volume==0 and p.unallocated_entry_cost==0 and r1.allocated_entry_cost+r2.allocated_entry_cost==D('-10')
def test_final_close_gate():
 i,b,e=base();ek=K();ak=K(kind=AllocationType.FINAL_RESERVE);ev=EventRecord(ek,ReconciliationState.RECONCILED);a=AllocationLedger(i);a.allocate(ev,e,ak,D('4'),[1],D('1'));ev.transition(ReconciliationState.ALLOCATION_PENDING);ev.transition(ReconciliationState.APPLIED);ev.transition(ReconciliationState.PERSISTED);store=PersistentStore(e,a,{ek:ev},1);snap=make_snapshot(i,ek,'HARVEST',1,'S','POST',b,[],D('5'),ReconciliationState.PERSISTED,1,ledger_revision=1,final_reserve_available=D('4'));assert evaluate_final_close(snap,store,True,True,FinalClosePolicy(D('0'),D('3'),1)).allowed
def test_scenario_fingerprints_unique():assert len({r.fingerprint for r in SCENARIOS})==len(SCENARIOS)
@pytest.mark.parametrize('field,value',[('event_type','OTHER'),('level',2),('phase','OTHER')])
def test_snapshot_metadata_mismatch(field,value):
 i,b,e=base();kw=dict(event_type='HARVEST',level=1,phase='POST');kw[field]=value
 with pytest.raises(ValueError):make_snapshot(i,K(),kw['event_type'],kw['level'],'S',kw['phase'],b,[],D('5'),ReconciliationState.PERSISTED,1)
def test_snapshot_actual_ledger_revision_and_reserve():
 i,b,e=base();k=K();s=make_snapshot(i,k,'HARVEST',1,'S','POST',b,[],D('5'),ReconciliationState.PERSISTED,7,ledger_revision=9,final_reserve_available=D('2'));assert s.state_revision==7 and s.ledger_revision==9 and s.final_reserve_available==D('2')

# Third-correction persistence regressions
def _persisted_gate_store():
 i,b,e=base(); ek=K(); ak=K(kind=AllocationType.FINAL_RESERVE); ev=EventRecord(ek,ReconciliationState.RECONCILED); a=AllocationLedger(i); a.allocate(ev,e,ak,D("4"),[1],D("1")); ev.transition(ReconciliationState.ALLOCATION_PENDING); ev.transition(ReconciliationState.APPLIED); ev.transition(ReconciliationState.PERSISTED); p=Position(i,"P","L","F",PositionSide.BUY,D(".01"),D("1"),D("-.1"),D("-.2"),D("-.3")); return PersistentStore(e,a,{ek:ev},1,{},(p,)),ek
def test_source_pool_survives_restart():
    store, key = _persisted_gate_store()
    restored = PersistentStore.deserialize(store.serialize())
    assert restored.allocation.source_pools == store.allocation.source_pools

def test_source_pool_available_survives_restart():
    store, _ = _persisted_gate_store(); restored=PersistentStore.deserialize(store.serialize())
    assert [p.available for p in restored.allocation.source_pools.values()] == [p.available for p in store.allocation.source_pools.values()]

def test_source_pool_revision_survives_restart():
    store, _ = _persisted_gate_store(); restored=PersistentStore.deserialize(store.serialize())
    assert [p.revision for p in restored.allocation.source_pools.values()] == [p.revision for p in store.allocation.source_pools.values()]

def test_managed_positions_survive_restart():
    store, _ = _persisted_gate_store(); restored=PersistentStore.deserialize(store.serialize())
    assert restored.managed_positions == store.managed_positions

def test_position_identity_survives_restart():
    store, _ = _persisted_gate_store(); restored=PersistentStore.deserialize(store.serialize())
    assert all(p.identity == store.economic.identity for p in restored.managed_positions)

def test_position_money_fields_survive_restart():
    store, _ = _persisted_gate_store(); restored=PersistentStore.deserialize(store.serialize())
    assert [(p.swap,p.exit_commission,p.exit_fee) for p in restored.managed_positions] == [(p.swap,p.exit_commission,p.exit_fee) for p in store.managed_positions]

def test_corrupted_source_pool_rejected():
    store, _ = _persisted_gate_store(); import json
    doc=json.loads(store.serialize()); doc['source_pools'][0]['available']='999'
    with pytest.raises(ValueError): PersistentStore.deserialize(json.dumps(doc))

def test_corrupted_managed_position_rejected():
    store, _ = _persisted_gate_store(); import json
    doc=json.loads(store.serialize()); doc['managed_positions'][0]['symbol']='FOREIGN' if 'symbol' in doc['managed_positions'][0] else None
    doc['managed_positions'][0]['identity']['symbol']='FOREIGN'
    with pytest.raises(ValueError): PersistentStore.deserialize(json.dumps(doc))
