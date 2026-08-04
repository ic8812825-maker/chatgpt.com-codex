from dataclasses import replace
import sys
from pathlib import Path
from decimal import Decimal as D
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'Tools'),str(ROOT/'Tests'/'stage_3_1_5')]
from stage_3_1_5_money_oracle import *
import scenario_catalog as catalog
from scenario_catalog import run_positive_scenarios,missing_scenario_categories,REQUIRED_SCENARIO_CATEGORIES
from stage_3_1_5_mutation_oracle import EconomicScenarioInput,execute_scenario,evaluate_invariants
from restart_fixtures import all_restart_probes
SCENARIOS=run_positive_scenarios()
def K(i=1,kind=AllocationType.RESIDUAL,account=1,symbol='X',magic=2,cycle='C',state='POST'):return EventKey(account,symbol,magic,cycle,'HARVEST',1,state,'P',i,kind)
def CK(parent,tx='C1',purpose=ConsumptionPurpose.FINAL_FAR_CLOSE,account=1,symbol='X',magic=2,cycle='C'):return ConsumptionKey(account,symbol,magic,cycle,purpose.value,1,'POST','P',tx,purpose,parent)
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
 i,b,e=base();k=K();s=make_snapshot(i,k,'HARVEST',1,'S','POST',b,[],e.realized_cycle_net,ReconciliationState.PERSISTED,1,ledger_revision=1,money_state_version=PersistentStore(e,AllocationLedger(i)).money_state_version);assert s.recovery_pl_close_now==D('5')
def test_foreign_position_in_snapshot_rejected():
 i,b,e=base();p=Position(Identity(2,'X',2,'C'),'P','L','F',PositionSide.BUY,D('.01'),D('1'))
 with pytest.raises(ValueError):make_snapshot(i,K(),'HARVEST',1,'S','POST',b,[p],D('0'),ReconciliationState.PERSISTED,1,money_state_version=PersistentStore(e,AllocationLedger(i)).money_state_version)
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
 i,b,e=base();ek=K();ak=K(kind=AllocationType.FINAL_RESERVE);ev=EventRecord(ek,ReconciliationState.RECONCILED);a=AllocationLedger(i);a.allocate(ev,e,ak,D('4'),[1],D('1'));ev.transition(ReconciliationState.ALLOCATION_PENDING);ev.transition(ReconciliationState.APPLIED);ev.transition(ReconciliationState.PERSISTED);store=PersistentStore(e,a,{ek:ev},1);snap=make_snapshot(i,ek,'HARVEST',1,'S','POST',b,[],D('5'),ReconciliationState.PERSISTED,1,ledger_revision=1,final_reserve_available=D('4'),money_state_version=store.money_state_version);assert evaluate_final_close(snap,store,True,True,FinalClosePolicy(D('0'),D('3'),1)).allowed
def test_scenario_fingerprints_unique():assert len({r.fingerprint for r in SCENARIOS})==len(SCENARIOS)
@pytest.mark.parametrize('field,value',[('event_type','OTHER'),('level',2),('phase','OTHER')])
def test_snapshot_metadata_mismatch(field,value):
 i,b,e=base();kw=dict(event_type='HARVEST',level=1,phase='POST');kw[field]=value
 with pytest.raises(ValueError):make_snapshot(i,K(),kw['event_type'],kw['level'],'S',kw['phase'],b,[],D('5'),ReconciliationState.PERSISTED,1,money_state_version=PersistentStore(e,AllocationLedger(i)).money_state_version)
def test_snapshot_actual_ledger_revision_and_reserve():
 i,b,e=base();k=K();s=make_snapshot(i,k,'HARVEST',1,'S','POST',b,[],D('5'),ReconciliationState.PERSISTED,7,ledger_revision=9,final_reserve_available=D('2'),money_state_version=PersistentStore(e,AllocationLedger(i)).money_state_version);assert s.state_revision==7 and s.ledger_revision==9 and s.final_reserve_available==D('2')

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
 i,b,e=base(); k=K(kind=AllocationType.CARRY); a=AllocationLedger(i); a.allocate(EventRecord(k,ReconciliationState.RECONCILED),e,k,D('2'),[1]); s=PersistentStore(e,a,{k:EventRecord(k,ReconciliationState.RECONCILED)}).serialize(); assert next(iter(PersistentStore.deserialize(s).allocation.source_pools.values())).available==D('3')
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
  result=all_restart_probes()[state];assert result['terminal'] is ReconciliationState.PERSISTED and result['reserve']==D('3') and result['consumed']==D('1') and not result['duplicate_consume'] and result['side_effects']==1
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
 snap=make_snapshot(store.economic.identity,ek,'HARVEST',1,'S','POST',store.economic.broker,store.managed_positions,store.economic.realized_cycle_net,ReconciliationState.PERSISTED,1,ledger_revision=store.revision,final_reserve_available=store.allocation.available(AllocationType.FINAL_RESERVE),money_state_version=expected)
 assert 'MONEY_STATE_STALE' in evaluate_final_close(snap,store,True,True,FinalClosePolicy(D('-9'),D('1'),1)).reasons
def test_final_close_after_restart_uses_restored_positions_and_reserve():
 store,ek=_persisted_gate_store(); restored=PersistentStore.deserialize(store.serialize());assert restored.managed_positions and restored.allocation.available(AllocationType.FINAL_RESERVE)==D('4')
def test_final_close_after_restart_blocks_missing_source_pool():
 store,ek=_persisted_gate_store();store.allocation.source_pools.clear();snap=make_snapshot(store.economic.identity,ek,'HARVEST',1,'S','POST',store.economic.broker,store.managed_positions,D('5'),ReconciliationState.PERSISTED,1,ledger_revision=1,final_reserve_available=D('4'),money_state_version=store.money_state_version);assert 'SOURCE_POOL_MISSING' in evaluate_final_close(snap,store,True,True,FinalClosePolicy(D('-9'),D('1'),1)).reasons

def test_required_scenario_categories_complete():assert not missing_scenario_categories(SCENARIOS)
def test_loss_money_scenarios_present():assert sum(r.category in {'BUY_LOSS','SELL_LOSS'} and r.actual['money']<0 for r in SCENARIOS)>=2
def test_scenario_total_at_least_120():assert len(SCENARIOS)>=120

@pytest.mark.parametrize('field,value',[('entry','IN'),('deal_type','BALANCE'),('initial_ignored',True),('position_id','FOREIGN'),('actual_volume','.02'),('profit','6'),('swap','1'),('commission','-1'),('fee','-1')])
def test_persisted_source_deal_tamper_rejected(field,value):
 store,_=_persisted_gate_store();import json;doc=json.loads(store.serialize());doc['deals'][0][field]=value
 with pytest.raises(ValueError):PersistentStore.deserialize(json.dumps(doc))
def test_out_to_in_persistence_tamper_blocked():test_persisted_source_deal_tamper_rejected('entry','IN')

@pytest.mark.parametrize('field,value',[('consumption_event_type','OTHER'),('level',2),('phase','OTHER'),('position_identifier','OTHER')])
def test_consumption_route_metadata_rejected(field,value):
 i,b,e=base();ak=K(kind=AllocationType.FINAL_RESERVE);a=AllocationLedger(i);a.allocate(EventRecord(ak,ReconciliationState.RECONCILED),e,ak,D('2'),[1]);data=CK(ak).__dict__.copy();data[field]=value
 with pytest.raises(ValueError):a.consume(ak,ConsumptionKey(**data),D('1'))
def test_same_transaction_different_data_conflicts():
 i,b,e=base();ak=K(kind=AllocationType.FINAL_RESERVE);a=AllocationLedger(i);a.allocate(EventRecord(ak,ReconciliationState.RECONCILED),e,ak,D('2'),[1]);a.consume(ak,CK(ak),D('1'));data=CK(ak).__dict__.copy();data['level']=2
 with pytest.raises(ValueError):a.consume(ak,ConsumptionKey(**data),D('1'))

@pytest.mark.parametrize('target,field,value',[('allocations','consumed','1'),('allocations','revision',99),('source_pools','revision',99),('source_pools','residual','2')])
def test_persistence_conservation_tamper_rejected(target,field,value):
 store,_=_persisted_gate_store();import json;doc=json.loads(store.serialize());doc[target][0][field]=value
 with pytest.raises(ValueError):PersistentStore.deserialize(json.dumps(doc))
def test_orphan_consumption_rejected():
 store,_=_persisted_gate_store();ak=next(iter(store.allocation.records));store.allocation.consume(ak,CK(ak),D('1'));import json;doc=json.loads(store.serialize());doc['consumptions'][0]['allocation_key']['deal_ticket']=999
 with pytest.raises(ValueError):PersistentStore.deserialize(json.dumps(doc))

def test_missing_money_state_version_blocked():
 i,b,e=base()
 with pytest.raises(ValueError):make_snapshot(i,K(),'HARVEST',1,'S','POST',b,[],D('5'),ReconciliationState.PERSISTED,1)
def test_event_version_collision_safe():
 store,ek=_persisted_gate_store();v1=store.money_state_version;other=K(9);store.events[other]=EventRecord(other,ReconciliationState.DISCOVERED,3);store.events[ek].revision=1;v2=store.money_state_version;store.events[ek].revision=2;store.events[other].revision=2;v3=store.money_state_version;assert v2.event_store_digest!=v3.event_store_digest and v1!=v2
def test_money_version_other_cycle_rejected():
 store,ek=_persisted_gate_store();v=replace(store.money_state_version,cycle_id='OTHER');snap=make_snapshot(store.economic.identity,ek,'HARVEST',1,'S','POST',store.economic.broker,store.managed_positions,D('5'),ReconciliationState.PERSISTED,1,ledger_revision=1,final_reserve_available=D('4'),money_state_version=v);assert 'MONEY_STATE_STALE' in evaluate_final_close(snap,store,True,True,FinalClosePolicy(D('-9'),D('1'),1)).reasons

REQUIRED_CASES={r.category:r for r in SCENARIOS if r.category in REQUIRED_SCENARIO_CATEGORIES}
@pytest.mark.parametrize('category',sorted(REQUIRED_SCENARIO_CATEGORIES))
def test_required_category_executes_owned_operation(category):
 r=REQUIRED_CASES[category];assert r.inputs['owner'] in r.invariants and r.inputs['operation']==r.inputs['owner'];assert r.expected is not r.actual;assert r.actual==r.expected
 assert r.fingerprint
@pytest.mark.parametrize('category',['SOURCE_POOL','MULTI_SOURCE','ALLOCATION','CONSUMPTION','RESIDUAL'])
def test_ledger_category_has_economic_after_state(category):
 actual=REQUIRED_CASES[category].actual;assert any(k in actual for k in ('available','available_after','residual','sources'))
@pytest.mark.parametrize('category',['RECONCILIATION_TRANSITION'])
def test_state_category_has_revision_and_state(category):
 actual=REQUIRED_CASES[category].actual;assert actual['revision']>0 and actual['state']!='DISCOVERED'
def test_required_categories_do_not_use_catch_all_owner():
 owners={r.inputs['owner'] for r in REQUIRED_CASES.values()};assert len(owners)>=12

@pytest.mark.parametrize('state',[ReconciliationState.DISCOVERED,ReconciliationState.PENDING_RECONCILIATION,ReconciliationState.RECONCILED,ReconciliationState.ALLOCATION_PENDING,ReconciliationState.APPLIED,ReconciliationState.PERSISTED])
def test_full_restart_history_replay_exactly_once(state):
 r=all_restart_probes()[state];assert r['terminal'] is ReconciliationState.PERSISTED;assert r['duplicate']==0;assert r['side_effects']==1;assert r['consumed']==D('1');assert not r['duplicate_consume'];assert r['second_roundtrip']
def test_restart_final_state_parity_all_crash_points():
 results=[all_restart_probes()[s] for s in (ReconciliationState.DISCOVERED,ReconciliationState.PENDING_RECONCILIATION,ReconciliationState.RECONCILED,ReconciliationState.ALLOCATION_PENDING,ReconciliationState.APPLIED,ReconciliationState.PERSISTED)];digests={(r['money'],r['reserve'],r['consumed'],r['allocation_revision'],r['event_revision']) for r in results};assert len(digests)==1
def test_restart_terminal_states_have_no_irreversible_side_effects():
 for s in (ReconciliationState.CONFLICT,ReconciliationState.REJECTED):
  r=all_restart_probes()[s];assert r['terminal_safe'] and r['side_effects']==0 and r['consumed']==0 and not r['irreversible']

def test_integrity_contract_valid_store():
 store,_=_persisted_gate_store();store.validate_integrity()
def test_integrity_error_has_typed_code():
 store,_=_persisted_gate_store();key=next(iter(store.allocation.records));foreign=replace(key,account_login=9);store.allocation.records[foreign]=store.allocation.records.pop(key);store.allocation.records[foreign].key=foreign
 with pytest.raises(OracleIntegrityError) as exc:store.validate_integrity()
 assert exc.value.code is IntegrityCode.FOREIGN_ALLOCATION_IDENTITY

@pytest.mark.parametrize('field,value',[('account_login',9),('symbol','Y'),('magic',9),('cycle_id','Z')])
def test_restored_foreign_allocation_exact_code(field,value):
 store,_=_persisted_gate_store();import json;doc=json.loads(store.serialize());doc['allocations'][0]['key'][field]=value
 with pytest.raises(OracleIntegrityError) as exc:PersistentStore.deserialize(json.dumps(doc))
 assert exc.value.code is IntegrityCode.FOREIGN_ALLOCATION_IDENTITY
@pytest.mark.parametrize('field,value',[('event_type','OTHER'),('level',9),('phase','OTHER'),('position_identifier','OTHER')])
def test_restored_allocation_event_mismatch_exact_code(field,value):
 store,_=_persisted_gate_store();import json;doc=json.loads(store.serialize());doc['allocations'][0]['key'][field]=value
 with pytest.raises(OracleIntegrityError) as exc:PersistentStore.deserialize(json.dumps(doc))
 assert exc.value.code is IntegrityCode.ALLOCATION_EVENT_MISMATCH
@pytest.mark.parametrize('state',['DISCOVERED','PENDING_RECONCILIATION','CONFLICT','REJECTED'])
def test_restored_allocation_state_exact_code(state):
 store,_=_persisted_gate_store();import json;doc=json.loads(store.serialize());doc['allocations'][0]['state']=state
 with pytest.raises(OracleIntegrityError) as exc:PersistentStore.deserialize(json.dumps(doc))
 assert exc.value.code is IntegrityCode.ALLOCATION_STATE_INVALID

def _consumed_store():
 store,_=_persisted_gate_store();ak=next(iter(store.allocation.records));store.allocation.consume(ak,CK(ak),D('1'));return store
@pytest.mark.parametrize('field,value',[('account_login',9),('symbol','Y'),('magic',9),('cycle_id','Z')])
def test_restored_foreign_consumption_exact_code(field,value):
 import json;doc=json.loads(_consumed_store().serialize());doc['consumptions'][0]['key'][field]=value
 with pytest.raises(OracleIntegrityError) as exc:PersistentStore.deserialize(json.dumps(doc))
 assert exc.value.code is IntegrityCode.FOREIGN_CONSUMPTION_IDENTITY
@pytest.mark.parametrize('field,value',[('consumption_event_type','OTHER'),('level',9),('phase','OTHER'),('position_identifier','OTHER'),('purpose','PARTIAL_FAR')])
def test_restored_consumption_route_exact_code(field,value):
 import json;doc=json.loads(_consumed_store().serialize());doc['consumptions'][0]['key'][field]=value
 with pytest.raises(OracleIntegrityError) as exc:PersistentStore.deserialize(json.dumps(doc))
 assert exc.value.code is IntegrityCode.CONSUMPTION_ROUTE_MISMATCH

@pytest.mark.parametrize('section,code',[('events',IntegrityCode.DUPLICATE_EVENT_KEY),('allocations',IntegrityCode.DUPLICATE_ALLOCATION_KEY),('source_pools',IntegrityCode.DUPLICATE_SOURCE_POOL),('deals',IntegrityCode.DUPLICATE_DEAL_TICKET)])
def test_duplicate_persisted_key_exact_code(section,code):
 import json;doc=json.loads(_persisted_gate_store()[0].serialize());doc[section].append(dict(doc[section][0]))
 with pytest.raises(OracleIntegrityError) as exc:PersistentStore.deserialize(json.dumps(doc))
 assert exc.value.code is code
def test_duplicate_consumption_key_exact_code():
 import json;doc=json.loads(_consumed_store().serialize());doc['consumptions'].append(dict(doc['consumptions'][0]))
 with pytest.raises(OracleIntegrityError) as exc:PersistentStore.deserialize(json.dumps(doc))
 assert exc.value.code is IntegrityCode.DUPLICATE_CONSUMPTION_KEY
def test_duplicate_transaction_conflict_exact_code():
 import json;doc=json.loads(_consumed_store().serialize());other=json.loads(json.dumps(doc['consumptions'][0]));other['key']['transaction_id']=doc['consumptions'][0]['key']['transaction_id'];other['key']['level']=9;doc['consumptions'].append(other)
 with pytest.raises(OracleIntegrityError) as exc:PersistentStore.deserialize(json.dumps(doc))
 assert exc.value.code is IntegrityCode.CONSUMPTION_TRANSACTION_CONFLICT

@pytest.mark.parametrize('field,value',[('reconciliation_state',ReconciliationState.DISCOVERED),('amount',D('3')),('consumed',D('1')),('residual',D('0'))])
def test_allocation_record_content_changes_money_version_without_revision(field,value):
 store,_=_persisted_gate_store();before=store.money_state_version;r=next(iter(store.allocation.records.values()));setattr(r,field,value);assert store.money_state_version!=before
def test_allocation_identity_changes_money_version_without_revision():
 store,_=_persisted_gate_store();before=store.money_state_version;k=next(iter(store.allocation.records));r=store.allocation.records.pop(k);foreign=replace(k,account_login=9);r.key=foreign;store.allocation.records[foreign]=r;assert store.money_state_version!=before
def test_deal_composition_changes_money_version_without_revision():
 store,_=_persisted_gate_store();before=store.money_state_version;d=store.economic.deals[1];store.economic.deals[1]=replace(d,profit=d.profit+D('1'),commission=d.commission-D('1'));assert store.money_state_version!=before
def test_source_fingerprint_changes_money_version_without_revision():
 store,_=_persisted_gate_store();before=store.money_state_version;p=next(iter(store.allocation.source_pools.values()));p.deal_fingerprints[1]['entry']='IN';assert store.money_state_version!=before
def test_position_money_changes_money_version_without_revision():
 store,_=_persisted_gate_store();before=store.money_state_version;store.managed_positions=(replace(store.managed_positions[0],swap=D('-9')),);assert store.money_state_version!=before

def _gate_for_store(store,ek,version=None):return make_snapshot(store.economic.identity,ek,'HARVEST',1,'S','POST',store.economic.broker,store.managed_positions,store.economic.realized_cycle_net,ReconciliationState.PERSISTED,1,ledger_revision=store.revision,final_reserve_available=store.allocation.available(AllocationType.FINAL_RESERVE),money_state_version=version or store.money_state_version)
def test_final_close_discovered_allocation_integrity_blocked():
 store,ek=_persisted_gate_store();snap=_gate_for_store(store,ek);next(iter(store.allocation.records.values())).reconciliation_state=ReconciliationState.DISCOVERED;g=evaluate_final_close(snap,store,True,True,FinalClosePolicy(D('-9'),D('1'),1));assert not g.allowed and g.reasons[0]=='LEDGER_INTEGRITY_FAILURE' and 'INTEGRITY_ALLOCATION_STATE_INVALID' in g.reasons
def test_final_close_foreign_allocation_integrity_blocked():
 store,ek=_persisted_gate_store();snap=_gate_for_store(store,ek);k=next(iter(store.allocation.records));r=store.allocation.records.pop(k);foreign=replace(k,account_login=9);r.key=foreign;store.allocation.records[foreign]=r;g=evaluate_final_close(snap,store,True,True,FinalClosePolicy(D('-9'),D('1'),1));assert not g.allowed and 'INTEGRITY_FOREIGN_ALLOCATION_IDENTITY' in g.reasons
def test_final_close_valid_restored_integrity_passes():
 store,ek=_persisted_gate_store();restored=PersistentStore.deserialize(store.serialize());snap=_gate_for_store(restored,ek);assert evaluate_final_close(snap,restored,True,True,FinalClosePolicy(D('-9'),D('1'),1)).allowed

def test_real_owner_results():
 assert REQUIRED_CASES['FULL_FILL'].actual['volume']==0
 assert REQUIRED_CASES['RESTART_CRASH_POINT'].actual['second_roundtrip']
 assert REQUIRED_CASES['DUPLICATE_EVENT'].actual['conflict_blocked']
 assert REQUIRED_CASES['FINAL_CLOSE_PASS'].actual['allowed']
 assert 'RECOVERY' in REQUIRED_CASES['FINAL_CLOSE_REJECTIONS'].actual['reasons']

class OwnerCalled(RuntimeError):pass
def test_consumption_owner_runtime_spy(monkeypatch):
 monkeypatch.setattr(AllocationLedger,'consume',lambda *a,**k:(_ for _ in ()).throw(OwnerCalled()))
 with pytest.raises(OwnerCalled):catalog._consume()
def test_history_replay_owner_runtime_spy(monkeypatch):
 monkeypatch.setattr(PersistentStore,'replay_history',lambda *a,**k:(_ for _ in ()).throw(OwnerCalled()))
 with pytest.raises(OwnerCalled):catalog._history_replay()
def test_restart_serialize_owner_runtime_spy(monkeypatch):
 monkeypatch.setattr(PersistentStore,'serialize',lambda *a,**k:(_ for _ in ()).throw(OwnerCalled()))
 with pytest.raises(OwnerCalled):catalog._restart_owner()
def test_final_close_pass_owner_runtime_spy(monkeypatch):
 monkeypatch.setattr(catalog,'evaluate_final_close',lambda *a,**k:(_ for _ in ()).throw(OwnerCalled()))
 with pytest.raises(OwnerCalled):catalog._final_close(False)
def test_final_close_rejection_owner_runtime_spy(monkeypatch):
 monkeypatch.setattr(catalog,'evaluate_final_close',lambda *a,**k:(_ for _ in ()).throw(OwnerCalled()))
 with pytest.raises(OwnerCalled):catalog._final_close(True)
def test_full_fill_calls_close_with_full_volume(monkeypatch):
 original=OpenPositionCost.close;seen=[]
 def spy(self,requested,actual,*a,**k):seen.append((self.volume,requested,actual));return original(self,requested,actual,*a,**k)
 monkeypatch.setattr(OpenPositionCost,'close',spy);result=catalog._partial(full=True);assert seen==[(D('1'),D('1'),D('1'))] and result['volume']==0

@pytest.mark.parametrize('case',[EconomicScenarioInput(commission=D('-1')),EconomicScenarioInput(swap=D('-1')),EconomicScenarioInput(volume=D('.2')),EconomicScenarioInput(side=PositionSide.SELL,close_price=D('1.0980')),EconomicScenarioInput(close_price=D('1.0980'),allocation_amount=D('0'))])
def test_universal_invariants_accept_valid_variants(case):assert not evaluate_invariants(execute_scenario(case))
def test_invariant_evaluator_has_no_fixed_clean_vector():
 import inspect;source=inspect.getsource(evaluate_invariants);assert "==D('10')" not in source and "==D('14')" not in source and 'facts' in source

def test_all_mutations_have_fault_operation_trace_and_computed_blocker():
 from stage_3_1_5_mutation_oracle import MUTATIONS,run_mutation
 for name in MUTATIONS:
  clean,mutated,clean_blockers,mutated_blockers=run_mutation(name);assert not clean_blockers;assert any(x.startswith('FAULT_') for x in mutated.operation_trace);assert mutated_blockers

def test_restart_money_version_and_final_close_parity():
 states=(ReconciliationState.DISCOVERED,ReconciliationState.PENDING_RECONCILIATION,ReconciliationState.RECONCILED,ReconciliationState.ALLOCATION_PENDING,ReconciliationState.APPLIED,ReconciliationState.PERSISTED);results=[all_restart_probes()[s] for s in states];assert len({r['money_version'] for r in results})==1;assert all(r['final_close_allowed'] for r in results)
def test_event_replay_identical_noop_conflict_exact_code():
 store,ek=_persisted_gate_store();existing=store.events[ek];assert not store.apply_event(EventRecord(ek,existing.state,existing.revision))
 with pytest.raises(OracleIntegrityError) as exc:store.apply_event(EventRecord(ek,ReconciliationState.DISCOVERED,0))
 assert exc.value.code is IntegrityCode.EVENT_REPLAY_CONFLICT


def test_sixth_correction_exploit_regressions():
 from stage_3_1_5.exploit_regressions import run
 results=run()
 assert len(results)>=20
 assert all(item['passed'] and item['target_guard_reached'] and item['expected']==item['actual'] for item in results)


def test_correlated_persistence_attacks_obey_global_law():
 from stage_3_1_5.correlated_attacks import run
 assert all(run())


def test_required_owners_actual_results_are_not_labels_or_expected_aliases():
 for category,owner,expected in catalog.REQUIRED_EXECUTABLE_FIXTURES:
  actual=owner()
  assert callable(owner) and actual is not expected
  assert actual==expected

def test_required_owner_wrong_economic_result_cannot_pass():
 for category,owner,expected in catalog.REQUIRED_EXECUTABLE_FIXTURES:
  actual=dict(owner()); key=next(iter(actual)); wrong=dict(actual);wrong[key]=object()
  assert wrong!=expected, category


def test_money_state_version_covers_full_fill_history_and_pool_key():
 i,b,e=base();store=PersistentStore(e,AllocationLedger(i),opening_costs={'P':OpenPositionCost(D('1'),D('-10'))})
 store.opening_costs['P'].close(D('.5'),D('.5'),1);before=store.money_state_version
 store.opening_costs['P'].fills[0]=replace(store.opening_costs['P'].fills[0],requested_volume=D('.75'))
 assert store.money_state_version!=before

def test_money_state_version_covers_event_transition_history():
 i,b,e=base();key=K();event=EventRecord(key);event.transition(ReconciliationState.PENDING_RECONCILIATION);store=PersistentStore(e,AllocationLedger(i),{key:event});before=store.money_state_version
 event.history=(replace(event.history[0],terminal_reason='tamper'),)
 assert store.money_state_version!=before


def test_final_close_rejects_in_memory_corruption_with_fresh_version():
 from stage_3_1_5.corrupted_store_final_close import run
 assert all(probe['passed'] for probe in run())


def test_targeted_negative_causal_controls_are_effective_and_non_vacuous():
 from stage_3_1_5.causal_negative_controls import run
 result=run();assert result['MISSING_CAUSAL_RULES']==result['INEFFECTIVE_CAUSAL_RULES']==result['VACUOUS_CAUSAL_RULES']==0

@pytest.mark.parametrize('field,value',[('profit',D('6')),('swap',D('1')),('commission',D('-1')),('fee',D('-1')),('actual_volume',D('.02')),('entry',DealEntry.INOUT),('deal_type',DealType.SELL),('position_id','Q'),('identity',Identity(9,'X',2,'C')),('identity',Identity(1,'Y',2,'C')),('identity',Identity(1,'X',9,'C')),('identity',Identity(1,'X',2,'Z'))])
def test_altered_deal_replay_conflicts_without_ledger_change(field,value):
 i,b,e=base();original=e.deals[1];revision=e.revision;money=e.realized_cycle_net
 with pytest.raises(OracleIntegrityError) as exc:e.apply(replace(original,**{field:value}))
 assert exc.value.code is IntegrityCode.DEAL_REPLAY_CONFLICT;assert e.revision==revision;assert e.realized_cycle_net==money;assert e.deals[1]==original


def test_same_event_state_revision_different_history_conflicts():
 store,key=_persisted_gate_store();existing=store.events[key];tampered=replace(existing,history=(replace(existing.history[0],terminal_reason='forged'),*existing.history[1:]))
 with pytest.raises(OracleIntegrityError) as exc:store.apply_event(tampered)
 assert exc.value.code is IntegrityCode.EVENT_REPLAY_CONFLICT

@pytest.mark.parametrize('initial_cost', [D('-10'),D('0'),D('10')])
def test_opening_cost_proportional_formula_and_final_residual(initial_cost):
 cost=OpenPositionCost(D('1'),initial_cost);cost.close(D('.5'),D('.5'),1);cost.close(D('.5'),D('.5'),2);cost.validate_integrity();assert cost.volume==0 and cost.unallocated_entry_cost==0 and cost.allocated_entry_cost==initial_cost

def test_opening_cost_locally_conserved_but_wrong_distribution_rejected():
 cost=OpenPositionCost(D('.5'),D('-1'),{1},D('-9'),D('1'),D('-10'),[FillRecord(1,D('.5'),D('.5'),D('1'),D('.5'),D('-9'))],1)
 with pytest.raises(OracleIntegrityError) as exc:cost.validate_integrity()
 assert exc.value.code is IntegrityCode.OPENING_COST_ALLOCATION_MISMATCH
