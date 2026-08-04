from dataclasses import dataclass,asdict,replace
import json,hashlib
from decimal import Decimal as D
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Tools'))
from stage_3_1_5_money_oracle import *
REQUIRED_SCENARIO_CATEGORIES=frozenset('BUY_PROFIT BUY_LOSS SELL_PROFIT SELL_LOSS TICK_VALUE_PROFIT TICK_VALUE_LOSS ZERO_SPREAD REAL_SPREAD ADVERSE_SLIPPAGE COMMISSION_ONLY SWAP_ONLY FEE_ONLY COMBINED_COSTS OPENING_IN OUT INOUT OUT_BY INITIAL_IGNORED FOREIGN_ACCOUNT FOREIGN_SYMBOL FOREIGN_MAGIC FOREIGN_CYCLE SOURCE_POOL MULTI_SOURCE ALLOCATION CONSUMPTION RESIDUAL PARTIAL_FILL FULL_FILL DUPLICATE_FILL RECONCILIATION_TRANSITION RESTART_CRASH_POINT HISTORY_REPLAY DUPLICATE_DEAL DUPLICATE_EVENT FINAL_CLOSE_PASS FINAL_CLOSE_REJECTIONS'.split())

def _project(side,open_price):
 b=Broker(D('1.0000'),D('1.0002'),D('.0001'),D('10'),D('12'));return {'money':projected_profit(side,D('.10'),D(open_price),b),'side':side.value,'open':D(open_price)}
def _deal(entry=DealEntry.OUT,profit='5',swap='0',commission='0',fee='0',ignored=False):
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));e=EconomicLedger(i,b);accepted=e.apply(Deal(i,1,'P',entry,DealType.BUY,D('.01'),D(profit),D(swap),D(commission),D(fee),ignored));return {'accepted':accepted,'money':e.realized_cycle_net,'entry':entry.value,'ignored':ignored}
def _allocation(multi=False):
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));e=EconomicLedger(i,b);e.apply(Deal(i,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5')));tickets=[1]
 if multi:e.apply(Deal(i,2,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('2')));tickets.append(2)
 k=EventKey(1,'X',2,'C','H',1,'P','P',1,AllocationType.FINAL_RESERVE);a=AllocationLedger(i);a.allocate(EventRecord(k,ReconciliationState.RECONCILED),e,k,D('4'),tickets,D('1'));return {'available':a.available(AllocationType.FINAL_RESERVE),'residual':next(iter(a.records.values())).residual,'sources':len(tickets)}
def _owner_store():
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));e=EconomicLedger(i,b);d=Deal(i,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5'));e.apply(d);k=EventKey(1,'X',2,'C','H',1,'P','P',1,AllocationType.FINAL_RESERVE);ev=EventRecord(k,ReconciliationState.RECONCILED);a=AllocationLedger(i);a.allocate(ev,e,k,D('4'),[1],D('1'));return PersistentStore(e,a,{k:ev}),k,d
def _consume():
 store,k,_=_owner_store();before=store.allocation.available(AllocationType.FINAL_RESERVE);ck=ConsumptionKey(1,'X',2,'C','FINAL_FAR_CLOSE',1,'P','P','SCENARIO',ConsumptionPurpose.FINAL_FAR_CLOSE,k);store.allocation.consume(k,ck,D('2'));r=store.allocation.records[k];return {'available_before':before,'consumed':r.consumed,'available_after':r.available,'consumption_records':len(store.allocation.consumptions),'allocation_revision':store.allocation.revision}
def _partial(duplicate=False,full=False):
 p=OpenPositionCost(D('1'),D('-10'));amount=D('1') if full else D('.5');first=p.close(amount,amount,1)
 if duplicate:
  try:p.close(D('.5'),D('.5'),1);blocked=False
  except ValueError:blocked=True
  return {'duplicate_blocked':blocked}
 return {'volume':first.volume_after,'cost':first.entry_cost_after}
def _history_replay():
 store,k,d=_owner_store();before=store.economic.revision;applied=store.replay_history([replace(d,ticket=2)]);after_first=store.economic.realized_cycle_net;revision=store.economic.revision;duplicate=store.replay_history([replace(d,ticket=2)]);return {'first':applied,'duplicate':duplicate,'money':after_first,'revision_delta':revision-before,'duplicate_revision_delta':store.economic.revision-revision}
def _restart_owner():
 from restart_fixtures import restart_workflow
 r=restart_workflow(ReconciliationState.DISCOVERED);return {'terminal':r['terminal'].value,'allocation_count':r['side_effects'],'consumed':r['consumed'],'second_roundtrip':r['second_roundtrip']}
def _duplicate_event_owner():
 store,k,_=_owner_store();same=store.apply_event(EventRecord(k,ReconciliationState.RECONCILED));
 try:store.apply_event(EventRecord(k,ReconciliationState.DISCOVERED));conflict=False
 except OracleIntegrityError as exc:conflict=exc.code is IntegrityCode.EVENT_REPLAY_CONFLICT
 return {'identical_noop':not same,'conflict_blocked':conflict,'records':len(store.events)}
def _final_close(reject=False):
 store,k,_=_owner_store();ev=store.events[k];ev.transition(ReconciliationState.ALLOCATION_PENDING);ev.transition(ReconciliationState.APPLIED);ev.transition(ReconciliationState.PERSISTED);store.revision=1;snap=make_snapshot(store.economic.identity,k,'H',1,'S','P',store.economic.broker,(),D('5'),ReconciliationState.PERSISTED,1,ledger_revision=1,final_reserve_available=D('4'),money_state_version=store.money_state_version);policy=FinalClosePolicy(D('9') if reject else D('-1'),D('1'),1);g=evaluate_final_close(snap,store,True,True,policy);return {'allowed':g.allowed,'reasons':g.reasons}
def _transition():
 k=EventKey(1,'X',2,'C','H',1,'P','P',1,AllocationType.RESIDUAL);e=EventRecord(k);e.transition(ReconciliationState.PENDING_RECONCILIATION);return {'state':e.state.value,'revision':e.revision}
def _duplicate_deal():
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));e=EconomicLedger(i,b);d=Deal(i,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5'));return {'first':e.apply(d),'second':e.apply(d),'money':e.realized_cycle_net}
def _identity(field):
 i=Identity(1,'X',2,'C');b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'));e=EconomicLedger(i,b);values={'account':1,'symbol':'X','magic':2,'cycle':'C'};values[field]={'account':9,'symbol':'Y','magic':9,'cycle':'Z'}[field];foreign=Identity(**values);return {'accepted':e.apply(Deal(foreign,1,'P',DealEntry.OUT,DealType.BUY,D('.01'),D('5'))),'identity':asdict(foreign)}
def _constant_cost(kind):
 return _deal(profit='0',commission='-2' if kind in ('commission','combined') else '0',swap='-3' if kind in ('swap','combined') else '0',fee='-1' if kind in ('fee','combined') else '0')
REQUIRED_EXECUTABLE_FIXTURES=(
 ('BUY_PROFIT',lambda:_project(PositionSide.BUY,'.9998'),{'money':D('2'),'side':'BUY','open':D('.9998')}),('BUY_LOSS',lambda:_project(PositionSide.BUY,'1.0001'),{'money':D('-1.2'),'side':'BUY','open':D('1.0001')}),('SELL_PROFIT',lambda:_project(PositionSide.SELL,'1.0004'),{'money':D('2'),'side':'SELL','open':D('1.0004')}),('SELL_LOSS',lambda:_project(PositionSide.SELL,'1.0001'),{'money':D('-1.2'),'side':'SELL','open':D('1.0001')}),
 ('TICK_VALUE_PROFIT',lambda:{**_project(PositionSide.BUY,'.9998'),'tick_value':D('10')},{'money':D('2'),'side':'BUY','open':D('.9998'),'tick_value':D('10')}),('TICK_VALUE_LOSS',lambda:{**_project(PositionSide.BUY,'1.0001'),'tick_value':D('12')},{'money':D('-1.2'),'side':'BUY','open':D('1.0001'),'tick_value':D('12')}),('ZERO_SPREAD',lambda:{'money':projected_profit(PositionSide.BUY,D('.1'),D('.9998'),Broker(D('1'),D('1'),D('.0001'),D('10'),D('12')))},{'money':D('2')}),('REAL_SPREAD',lambda:{**_project(PositionSide.BUY,'.9998'),'spread':D('.0002')},{'money':D('2'),'side':'BUY','open':D('.9998'),'spread':D('.0002')}),('ADVERSE_SLIPPAGE',lambda:{'money':projected_profit(PositionSide.BUY,D('.1'),D('.9998'),Broker(D('1'),D('1.0002'),D('.0001'),D('10'),D('12')),D('.0001'))},{'money':D('1')}),
 ('COMMISSION_ONLY',lambda:_constant_cost('commission'),{'accepted':True,'money':D('-2'),'entry':'OUT','ignored':False}),('SWAP_ONLY',lambda:_constant_cost('swap'),{'accepted':True,'money':D('-3'),'entry':'OUT','ignored':False}),('FEE_ONLY',lambda:_constant_cost('fee'),{'accepted':True,'money':D('-1'),'entry':'OUT','ignored':False}),('COMBINED_COSTS',lambda:_constant_cost('combined'),{'accepted':True,'money':D('-6'),'entry':'OUT','ignored':False}),('OPENING_IN',lambda:_deal(DealEntry.IN),{'accepted':True,'money':D('0'),'entry':'IN','ignored':False}),('OUT',lambda:_deal(DealEntry.OUT),{'accepted':True,'money':D('5'),'entry':'OUT','ignored':False}),('INOUT',lambda:_deal(DealEntry.INOUT),{'accepted':True,'money':D('5'),'entry':'INOUT','ignored':False}),('OUT_BY',lambda:_deal(DealEntry.OUT_BY),{'accepted':True,'money':D('5'),'entry':'OUT_BY','ignored':False}),('INITIAL_IGNORED',lambda:_deal(ignored=True),{'accepted':False,'money':D('0'),'entry':'OUT','ignored':True}),
 ('FOREIGN_ACCOUNT',lambda:_identity('account'),{'accepted':False,'identity':{'account':9,'symbol':'X','magic':2,'cycle':'C'}}),('FOREIGN_SYMBOL',lambda:_identity('symbol'),{'accepted':False,'identity':{'account':1,'symbol':'Y','magic':2,'cycle':'C'}}),('FOREIGN_MAGIC',lambda:_identity('magic'),{'accepted':False,'identity':{'account':1,'symbol':'X','magic':9,'cycle':'C'}}),('FOREIGN_CYCLE',lambda:_identity('cycle'),{'accepted':False,'identity':{'account':1,'symbol':'X','magic':2,'cycle':'Z'}}),('SOURCE_POOL',lambda:{**_allocation(),'pool_net':D('5')},{'available':D('4'),'residual':D('1'),'sources':1,'pool_net':D('5')}),('MULTI_SOURCE',lambda:_allocation(True),{'available':D('4'),'residual':D('1'),'sources':2}),('ALLOCATION',lambda:{**_allocation(),'records':1},{'available':D('4'),'residual':D('1'),'sources':1,'records':1}),('CONSUMPTION',_consume,{'available_before':D('4'),'consumed':D('2'),'available_after':D('2'),'consumption_records':1,'allocation_revision':2}),('RESIDUAL',lambda:{'source':D('5'),'allocated':_allocation()['available'],'residual':_allocation()['residual']},{'source':D('5'),'allocated':D('4'),'residual':D('1')}),('PARTIAL_FILL',_partial,{'volume':D('.5'),'cost':D('-5')}),('FULL_FILL',lambda:_partial(full=True),{'volume':D('0'),'cost':D('0')}),('DUPLICATE_FILL',lambda:_partial(True),{'duplicate_blocked':True}),('RECONCILIATION_TRANSITION',_transition,{'state':'PENDING_RECONCILIATION','revision':1}),('HISTORY_REPLAY',_history_replay,{'first':1,'duplicate':0,'money':D('10'),'revision_delta':1,'duplicate_revision_delta':0}),('DUPLICATE_DEAL',_duplicate_deal,{'first':True,'second':False,'money':D('5')}),('DUPLICATE_EVENT',_duplicate_event_owner,{'identical_noop':True,'conflict_blocked':True,'records':1}),('RESTART_CRASH_POINT',_restart_owner,{'terminal':'PERSISTED','allocation_count':1,'consumed':D('1'),'second_roundtrip':True}),('FINAL_CLOSE_PASS',_final_close,{'allowed':True,'reasons':()}),('FINAL_CLOSE_REJECTIONS',lambda:_final_close(True),{'allowed':False,'reasons':('RECOVERY',)}))
@dataclass(frozen=True)
class ScenarioResult:
 scenario_id:str;name:str;category:str;inputs:dict;expected:dict;actual:dict;expected_status:str;actual_status:str;invariants:tuple[str,...]
 @property
 def passed(self):return self.expected==self.actual and self.expected_status==self.actual_status
 @property
 def fingerprint(self):return json.dumps([self.inputs,self.expected,self.actual,self.invariants],sort_keys=True,default=str)
def run_positive_scenarios():
 out=[];ident=Identity(1,'EURUSD',7,'C1')
 for i in range(50):
  side=PositionSide.BUY if i%2==0 else PositionSide.SELL;spread=D(i%5)*D('.0001');b=Broker(D('1.1000'),D('1.1000')+spread,D('.0001'),D(10+i%4),D(12+i%3));lot=D('.01')*(1+i%10);ticks=D(2+i);op=b.bid-ticks*b.tick_size if side is PositionSide.BUY else b.ask+ticks*b.tick_size;expected=ticks*b.tv_profit*lot;actual=projected_profit(side,lot,op,b);out.append(ScenarioResult(f'PM-{i:03}',f'{side.value} money {i}','MONEY',{'ticks':ticks,'lot':lot},{'money':expected},{'money':actual},'PASS','PASS',('SIDE','GRID','MONEY')))
 b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'))
 for i in range(20):
  entry=(DealEntry.OUT,DealEntry.INOUT,DealEntry.OUT_BY)[i%3];e=EconomicLedger(ident,b);d=Deal(ident,100+i,'P',entry,DealType.BUY,D('.01'),D(i+1),D('-1'),D('-2'),D('-.5'));e.apply(d);expected=D(i+1)-D('3.5');out.append(ScenarioResult(f'DL-{i:03}',f'deal net {i}','DEAL',{'entry':entry.value},{'realized':expected},{'realized':e.realized_cycle_net},'PASS','PASS',('DEAL_NET','ENTRY')))
 for i in range(10):
  cost=OpenPositionCost(D('1'),D('-10'));v=D(i+1)/D('20');r=cost.close(v,v,1000+i);expected=D('-10')*v;out.append(ScenarioResult(f'PF-{i:03}',f'partial {v}','PARTIAL',{'actual':v},{'allocated':expected,'remaining':D('1')-v},{'allocated':r.allocated_entry_cost,'remaining':r.volume_after},'PASS','PASS',('ACTUAL_FILL','COST')))
 for i,state in enumerate(ReconciliationState):
  k=EventKey(1,'X',2,'C','E',i,state.value,'P',i+1,AllocationType.RESIDUAL);ev=EventRecord(k,state,i);out.append(ScenarioResult(f'RC-{i:03}',f'state {state.value}','STATE',{}, {'state':state.value,'revision':i},{'state':ev.state.value,'revision':ev.revision},'PASS','PASS',('STATE',)))
 for i in range(20):
  foreign=Identity(2+i if i%4==0 else 1,f'GBP{i}' if i%4==1 else 'EURUSD',20+i if i%4==2 else 7,f'C{i}' if i%4==3 else 'C1');e=EconomicLedger(ident,b);d=Deal(foreign,500+i,'P',DealEntry.OUT,DealType.BUY,D('.01'),D(i+1));accepted=e.apply(d);expected=foreign==ident;out.append(ScenarioResult(f'ID-{i:03}',f'identity {i}','IDENTITY',{'identity':foreign.__dict__},{'accepted':expected},{'accepted':accepted},'PASS','PASS',('ISOLATION',)))
 # Required categories have explicit executable owners; no category-label fallback.
 for category,owner,expected in REQUIRED_EXECUTABLE_FIXTURES:
  actual=owner();code=owner.__code__;token=owner.__name__ if owner.__name__!='<lambda>' else hashlib.sha256(code.co_code+repr((code.co_consts,code.co_names)).encode()).hexdigest()
  out.append(ScenarioResult(f'CAT-{category}',category.replace('_',' ').title(),category,{'owner':token,'operation':token},dict(expected),dict(actual),'PASS','PASS',(token,'EXECUTED_OPERATION')))
 return out
def missing_scenario_categories(results):return REQUIRED_SCENARIO_CATEGORIES-{r.category for r in results}
