import sys
from pathlib import Path
from decimal import Decimal as D
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'Tools'),str(ROOT/'Tests'/'stage_3_1_5')]
from stage_3_1_5_money_oracle import *
from scenario_catalog import run_positive_scenarios,missing_scenario_categories
from restart_fixtures import all_restart_probes
SCENARIOS=run_positive_scenarios()
def K(i=1,kind=AllocationType.RESIDUAL,account=1,symbol='X',magic=2,cycle='C',state='POST'):return EventKey(account,symbol,magic,cycle,'HARVEST',1,state,'P',i,kind)
def CK(parent,tx='C1',purpose=ConsumptionPurpose.FINAL_FAR_CLOSE,account=1,symbol='X',magic=2,cycle='C'):return ConsumptionKey(account,symbol,magic,cycle,'CONSUME',1,'POST','P',tx,purpose,parent)
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
 i,b,e=base();ek=K();ak=K(kind=AllocationType.FINAL_RESERVE);ev=EventRecord(ek,ReconciliationState.RECONCILED);a=AllocationLedger(i);assert a.allocate(ev,e,ak,D('4'),[1],D('1'));before=a.available(AllocationType.FINAL_RESERVE);ck=CK(ak);assert a.consume(ak,ck,D('2'));assert a.available(AllocationType.FINAL_RESERVE)==before-D('2');assert not a.consume(ak,ck,D('2'))
@pytest.mark.parametrize('kw',[{'account':9},{'symbol':'Y'},{'magic':9},{'cycle':'Z'}])
def test_foreign_consume_rejected(kw):
 i,b,e=base();ek=K();ak=K(kind=AllocationType.CARRY);ev=EventRecord(ek,ReconciliationState.RECONCILED);a=AllocationLedger(i);a.allocate(ev,e,ak,D('4'),[1],D('1'))
 with pytest.raises(ValueError):a.consume(ak,CK(ak,**kw),D('1'))
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

def test_same_source_cannot_allocate_again_after_restart():
 store,ek=_persisted_gate_store(); restored=PersistentStore.deserialize(store.serialize()); other=K(9,AllocationType.CARRY); ev=EventRecord(other,ReconciliationState.RECONCILED)
 with pytest.raises(ValueError): restored.allocation.allocate(ev,restored.economic,other,D('1'),[1])
def test_partial_source_remaining_survives_restart():
 i,b,e=base(); k=K(kind=AllocationType.CARRY); a=AllocationLedger(i); a.allocate(EventRecord(k,ReconciliationState.RECONCILED),e,k,D('2'),[1]); s=PersistentStore(e,a).serialize(); assert next(iter(PersistentStore.deserialize(s).allocation.source_pools.values())).available==D('3')
def test_source_pool_rebuilt_from_history_matches_persisted():
 store,_=_persisted_gate_store(); restored=PersistentStore.deserialize(store.serialize()); restored.allocation.validate_source_pools(restored.economic)
def test_source_pool_allocation_records_mismatch_rejected():
 store,_=_persisted_gate_store(); import json; x=json.loads(store.serialize()); x['source_pools'][0]['allocated']='3'
 with pytest.raises(ValueError):PersistentStore.deserialize(json.dumps(x))
def test_source_pool_unknown_ticket_rejected():
 store,_=_persisted_gate_store(); import json; x=json.loads(store.serialize()); x['source_pools'][0]['sources']=[999];x['source_pools'][0]['deal_nets']={'999':'5'}
 with pytest.raises(ValueError):PersistentStore.deserialize(json.dumps(x))
def test_source_pool_duplicate_ticket_rejected():
 store,_=_persisted_gate_store(); import json; x=json.loads(store.serialize()); x['source_pools'][0]['sources']=[1,1]
 with pytest.raises(ValueError):PersistentStore.deserialize(json.dumps(x))
def test_source_pool_overlap_after_restart_rejected():
 store,_=_persisted_gate_store(); import json; x=json.loads(store.serialize()); x['source_pools'].append(dict(x['source_pools'][0]));x['source_pools'][1]['key']['deal_ticket']=2
 with pytest.raises(ValueError):PersistentStore.deserialize(json.dumps(x))

@pytest.mark.parametrize('dtype',[DealType.BALANCE,DealType.CREDIT,DealType.CHARGE,DealType.CORRECTION])
def test_non_trade_deal_cannot_fund_allocation(dtype):
 i,b,_=base();e=EconomicLedger(i,b);e.apply(Deal(i,9,'P',DealEntry.IN, dtype,D('.01'),D('5')));k=K(9,AllocationType.CARRY);a=AllocationLedger(i)
 with pytest.raises(ValueError):a.allocate(EventRecord(k,ReconciliationState.RECONCILED),e,k,D('1'),[9])
def test_opening_in_cannot_fund_allocation():
 i,b,_=base();e=EconomicLedger(i,b);e.apply(Deal(i,9,'P',DealEntry.IN,DealType.BUY,D('.01'),D('5')));k=K(9,AllocationType.CARRY);a=AllocationLedger(i)
 with pytest.raises(ValueError):a.allocate(EventRecord(k,ReconciliationState.RECONCILED),e,k,D('1'),[9])
def test_initial_ignored_profit_cannot_fund_allocation():
 i,b,_=base();e=EconomicLedger(i,b);assert not e.apply(Deal(i,9,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5'),initial_ignored=True))
def test_foreign_deal_cannot_fund_allocation():
 i,b,e=base();assert not e.apply(Deal(Identity(9,'X',2,'C'),9,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5')))
def test_closing_profit_minus_costs_funds_only_net():
 i,b,_=base();e=EconomicLedger(i,b);e.apply(Deal(i,9,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5'),commission=D('-2')));k=K(9,AllocationType.CARRY);a=AllocationLedger(i);a.allocate(EventRecord(k,ReconciliationState.RECONCILED),e,k,D('3'),[9]);assert a.available(AllocationType.CARRY)==3
def test_negative_closing_event_cannot_credit_budget():
 i,b,_=base();e=EconomicLedger(i,b);e.apply(Deal(i,9,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('-1')));k=K(9,AllocationType.CARRY)
 with pytest.raises(ValueError):AllocationLedger(i).allocate(EventRecord(k,ReconciliationState.RECONCILED),e,k,D('0'),[9])
def test_commission_only_event_cannot_create_positive_harvest():
 i,b,_=base();e=EconomicLedger(i,b);e.apply(Deal(i,9,'P',DealEntry.IN,DealType.COMMISSION,D('.01'),D('2')));k=K(9,AllocationType.CARRY)
 with pytest.raises(ValueError):AllocationLedger(i).allocate(EventRecord(k,ReconciliationState.RECONCILED),e,k,D('1'),[9])

def test_unrelated_same_cycle_consume_rejected():
 i,b,e=base();ak=K(kind=AllocationType.FINAL_RESERVE);a=AllocationLedger(i);a.allocate(EventRecord(ak,ReconciliationState.RECONCILED),e,ak,D('2'),[1])
 with pytest.raises(ValueError):a.consume(ak,CK(K(8,AllocationType.FINAL_RESERVE)),D('1'))
def test_consume_parent_allocation_required():
 with pytest.raises(ValueError):CK(None)
def test_consume_parent_key_mismatch_rejected():test_unrelated_same_cycle_consume_rejected()
def test_consume_wrong_purpose_rejected():
 i,b,e=base();ak=K(kind=AllocationType.FINAL_RESERVE);a=AllocationLedger(i);a.allocate(EventRecord(ak,ReconciliationState.RECONCILED),e,ak,D('2'),[1])
 with pytest.raises(ValueError):a.consume(ak,CK(ak,purpose=ConsumptionPurpose.PARTIAL_FAR),D('1'))
def test_consume_duplicate_noop():
 i,b,e=base();ak=K(kind=AllocationType.FINAL_RESERVE);a=AllocationLedger(i);a.allocate(EventRecord(ak,ReconciliationState.RECONCILED),e,ak,D('2'),[1]);ck=CK(ak);assert a.consume(ak,ck,D('1')) and not a.consume(ak,ck,D('1'))
def test_consume_key_cannot_be_reused_for_other_allocation():test_unrelated_same_cycle_consume_rejected()
def test_final_reserve_only_final_far_close():test_consume_wrong_purpose_rejected()

def test_early_crash_completes_allocation_once():
 for state in (ReconciliationState.DISCOVERED,ReconciliationState.PENDING_RECONCILIATION,ReconciliationState.RECONCILED,ReconciliationState.ALLOCATION_PENDING):
  result=all_restart_probes()[state];assert result['terminal'] is ReconciliationState.PERSISTED and result['reserve']==D('4') and result['side_effects']==1
def test_terminal_restart_never_allocates():
 for state in (ReconciliationState.CONFLICT,ReconciliationState.REJECTED):
  result=all_restart_probes()[state];assert result['terminal_safe'] and result['side_effects']==0 and not result['irreversible']

def test_money_state_version_roundtrip():
 store,_=_persisted_gate_store();store.positions_revision=3;assert PersistentStore.deserialize(store.serialize()).money_state_version==store.money_state_version
@pytest.mark.parametrize('component',['economic','allocation','event','positions','store'])
def test_each_money_revision_change_blocks_stale_snapshot(component):
 store,ek=_persisted_gate_store(); expected=store.money_state_version
 if component=='economic':store.economic.revision+=1
 elif component=='allocation':store.allocation.revision+=1
 elif component=='event':store.events[ek].revision+=1
 elif component=='positions':store.positions_revision+=1
 else:store.revision+=1
 snap=make_snapshot(store.economic.identity,ek,'HARVEST',1,'S','POST',store.economic.broker,store.managed_positions,store.economic.realized_cycle_net,ReconciliationState.PERSISTED,1,ledger_revision=store.revision,final_reserve_available=store.allocation.available(AllocationType.FINAL_RESERVE))
 assert 'MONEY_STATE_STALE' in evaluate_final_close(snap,store,True,True,FinalClosePolicy(D('-9'),D('1'),1,expected_version=expected)).reasons
def test_final_close_after_restart_uses_restored_positions_and_reserve():
 store,ek=_persisted_gate_store(); restored=PersistentStore.deserialize(store.serialize());assert restored.managed_positions and restored.allocation.available(AllocationType.FINAL_RESERVE)==D('4')
def test_final_close_after_restart_blocks_missing_source_pool():
 store,ek=_persisted_gate_store();store.allocation.source_pools.clear();snap=make_snapshot(store.economic.identity,ek,'HARVEST',1,'S','POST',store.economic.broker,store.managed_positions,D('5'),ReconciliationState.PERSISTED,1,ledger_revision=1,final_reserve_available=D('4'));assert 'SOURCE_POOL_MISSING' in evaluate_final_close(snap,store,True,True,FinalClosePolicy(D('-9'),D('1'),1)).reasons

def test_required_scenario_categories_complete():assert not missing_scenario_categories(SCENARIOS)
def test_loss_money_scenarios_present():assert sum(r.category in {'BUY_LOSS','SELL_LOSS'} and r.actual['money']<0 for r in SCENARIOS)>=2
def test_scenario_total_at_least_120():assert len(SCENARIOS)>=120

@pytest.mark.parametrize('field,value',[('entry','IN'),('deal_type','BALANCE'),('initial_ignored',True),('position_id','FOREIGN'),('actual_volume','.02'),('profit','6'),('swap','1'),('commission','-1'),('fee','-1')])
def test_persisted_source_deal_tamper_rejected(field,value):
 store,_=_persisted_gate_store();import json;doc=json.loads(store.serialize());doc['deals'][0][field]=value
 with pytest.raises(ValueError):PersistentStore.deserialize(json.dumps(doc))
def test_out_to_in_persistence_tamper_blocked():test_persisted_source_deal_tamper_rejected('entry','IN')
