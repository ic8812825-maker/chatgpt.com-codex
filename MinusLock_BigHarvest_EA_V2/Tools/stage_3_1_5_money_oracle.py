"""Executable Decimal proof model for Stage 3.1.5; independent from MQL5."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from decimal import Decimal
from enum import Enum
import json
from typing import Iterable
D=Decimal
class PositionSide(str,Enum): BUY="BUY"; SELL="SELL"
class DealEntry(str,Enum): IN="IN"; OUT="OUT"; INOUT="INOUT"; OUT_BY="OUT_BY"
class DealType(str,Enum):
 BUY="BUY"; SELL="SELL"; BALANCE="BALANCE"; CREDIT="CREDIT"; CHARGE="CHARGE"; CORRECTION="CORRECTION"; COMMISSION="COMMISSION"; OTHER="OTHER"
class ReconciliationState(str,Enum):
 DISCOVERED="DISCOVERED"; PENDING_RECONCILIATION="PENDING_RECONCILIATION"; RECONCILED="RECONCILED"; ALLOCATION_PENDING="ALLOCATION_PENDING"; APPLIED="APPLIED"; PERSISTED="PERSISTED"; CONFLICT="CONFLICT"; REJECTED="REJECTED"
class AllocationType(str,Enum): PARTIAL_FAR="PARTIAL_FAR"; FINAL_RESERVE="FINAL_RESERVE"; CARRY="CARRY"; TRANSITION="TRANSITION"; RESIDUAL="RESIDUAL"
def grid(value:D,step:D)->bool: return step>0 and value%step==0
@dataclass(frozen=True)
class Identity: account:int; symbol:str; magic:int; cycle:str
@dataclass(frozen=True)
class Broker:
 bid:D; ask:D; tick_size:D; tv_profit:D; tv_loss:D; lot_step:D=D('.01'); min_lot:D=D('.01')
 def __post_init__(self):
  if self.tick_size<=0 or self.tv_profit<=0 or self.tv_loss<=0 or self.ask<self.bid: raise ValueError('invalid broker')
  if not all(grid(x,self.tick_size) for x in (self.bid,self.ask,self.ask-self.bid)): raise ValueError('off-grid quote')
 def validate_price(self,p:D):
  if not grid(p,self.tick_size): raise ValueError('off-grid price')
 def validate_lot(self,lot:D):
  if lot<=0 or lot<self.min_lot or not grid(lot,self.lot_step): raise ValueError('invalid lot')
@dataclass(frozen=True)
class Position:
 identity:Identity; identifier:str; leg_id:str; role:str; side:PositionSide; volume:D; open_price:D
 swap:D=D('0'); exit_commission:D=D('0'); exit_fee:D=D('0')
def projected_profit(side:PositionSide,lot:D,open_price:D,broker:Broker,slippage:D=D('0')) -> D:
 if not isinstance(side,PositionSide): raise ValueError('invalid side')
 broker.validate_lot(lot); broker.validate_price(open_price)
 if slippage<0 or not grid(slippage,broker.tick_size): raise ValueError('invalid slippage')
 close=broker.bid-slippage if side is PositionSide.BUY else broker.ask+slippage
 broker.validate_price(close); movement=close-open_price if side is PositionSide.BUY else open_price-close
 ticks=movement/broker.tick_size
 return ticks*(broker.tv_profit if ticks>=0 else broker.tv_loss)*lot
@dataclass(frozen=True)
class EventSnapshot:
 identity:Identity; event_key:EventKey; event_type:str; level:int; scenario:str; phase:str; broker:Broker
 managed_positions:tuple[Position,...]; actual_lots:tuple[D,...]; actual_open_prices:tuple[D,...]
 final_reserve_available:D; partial_far_budget_available:D; carry_available:D; transition_budget_available:D
 residual:D; commission:D; swap:D; fee:D; slippage_diagnostic:D; reconciliation_state:ReconciliationState
 applied_deal_tickets:frozenset[int]; pending_deal_tickets:frozenset[int]; state_revision:int; ledger_revision:int
 realized_cycle_net:D; floating_close_now:D; recovery_pl_close_now:D
 def __post_init__(self):
  if (self.event_key.account_login,self.event_key.symbol,self.event_key.magic,self.event_key.cycle_id)!=(self.identity.account,self.identity.symbol,self.identity.magic,self.identity.cycle):raise ValueError('snapshot identity mismatch')
  if len({p.identifier for p in self.managed_positions})!=len(self.managed_positions):raise ValueError('duplicate position')
  for p in self.managed_positions:self.broker.validate_lot(p.volume);self.broker.validate_price(p.open_price)
  if self.actual_lots!=tuple(p.volume for p in self.managed_positions): raise ValueError('actual lot mismatch')
  if self.actual_open_prices!=tuple(p.open_price for p in self.managed_positions): raise ValueError('open price mismatch')
  if self.recovery_pl_close_now!=self.realized_cycle_net+self.floating_close_now: raise ValueError('recovery mismatch')
def floating_total(identity:Identity,positions:Iterable[Position],broker:Broker,slippage:D=D('0'))->D:
 return sum((projected_profit(p.side,p.volume,p.open_price,broker,slippage)+p.swap+p.exit_commission+p.exit_fee for p in positions if p.identity==identity),D('0'))
def make_snapshot(identity:Identity,event_key:EventKey,event_type:str,level:int,scenario:str,phase:str,broker:Broker,positions:Iterable[Position],realized:D,state:ReconciliationState,revision:int,**kw)->EventSnapshot:
 ps=tuple(p for p in positions if p.identity==identity); floating=floating_total(identity,ps,broker,kw.get('slippage_diagnostic',D('0')))
 return EventSnapshot(identity,event_key,event_type,level,scenario,phase,broker,ps,tuple(p.volume for p in ps),tuple(p.open_price for p in ps),kw.get('final_reserve_available',D('0')),kw.get('partial_far_budget_available',D('0')),kw.get('carry_available',D('0')),kw.get('transition_budget_available',D('0')),kw.get('residual',D('0')),kw.get('commission',D('0')),kw.get('swap',D('0')),kw.get('fee',D('0')),kw.get('slippage_diagnostic',D('0')),state,frozenset(kw.get('applied_deal_tickets',())),frozenset(kw.get('pending_deal_tickets',())),revision,kw.get('ledger_revision',revision),realized,floating,realized+floating)
ALLOWED_TRANSITIONS={
 ReconciliationState.DISCOVERED:frozenset((ReconciliationState.PENDING_RECONCILIATION,ReconciliationState.CONFLICT,ReconciliationState.REJECTED)),
 ReconciliationState.PENDING_RECONCILIATION:frozenset((ReconciliationState.RECONCILED,ReconciliationState.CONFLICT,ReconciliationState.REJECTED)),
 ReconciliationState.RECONCILED:frozenset((ReconciliationState.ALLOCATION_PENDING,ReconciliationState.CONFLICT,ReconciliationState.REJECTED)),
 ReconciliationState.ALLOCATION_PENDING:frozenset((ReconciliationState.APPLIED,ReconciliationState.CONFLICT,ReconciliationState.REJECTED)),
 ReconciliationState.APPLIED:frozenset((ReconciliationState.PERSISTED,ReconciliationState.CONFLICT)),
 ReconciliationState.PERSISTED:frozenset(),ReconciliationState.CONFLICT:frozenset(),ReconciliationState.REJECTED:frozenset()}
@dataclass
class EventRecord:
 event_id:EventKey; state:ReconciliationState=ReconciliationState.DISCOVERED; revision:int=0
 def transition(self,target:ReconciliationState)->bool:
  if target==self.state:return False
  if self.state in (ReconciliationState.CONFLICT,ReconciliationState.REJECTED,ReconciliationState.PERSISTED) or target not in ALLOWED_TRANSITIONS[self.state]: raise ValueError('invalid reconciliation transition')
  self.state=target; self.revision+=1; return True
 @property
 def irreversible_action_allowed(self): return self.state is ReconciliationState.PERSISTED
@dataclass(frozen=True)
class Deal:
 identity:Identity; ticket:int; position_id:str; entry:DealEntry; deal_type:DealType; actual_volume:D
 profit:D; swap:D=D('0'); commission:D=D('0'); fee:D=D('0'); initial_ignored:bool=False
 def validate(self,broker:Broker):
  if not self.position_id or self.ticket<=0 or not isinstance(self.entry,DealEntry) or not isinstance(self.deal_type,DealType): raise ValueError('invalid deal')
  broker.validate_lot(self.actual_volume)
 @property
 def net(self): return self.profit+self.swap+self.commission+self.fee
MANAGED_DEAL_TYPES={DealType.BUY,DealType.SELL,DealType.COMMISSION}
@dataclass
class EconomicLedger:
 identity:Identity; broker:Broker; deals:dict[int,Deal]=field(default_factory=dict)
 def apply(self,deal:Deal)->bool:
  deal.validate(self.broker)
  if deal.identity!=self.identity or deal.deal_type not in MANAGED_DEAL_TYPES or deal.initial_ignored:return False
  if deal.ticket in self.deals:return False
  self.deals[deal.ticket]=deal; return True
 def replay(self,history:Iterable[Deal])->int:return sum(self.apply(x) for x in history)
 @property
 def realized_cycle_net(self):return sum((x.net for x in self.deals.values() if x.entry in (DealEntry.OUT,DealEntry.INOUT,DealEntry.OUT_BY) or x.deal_type is DealType.COMMISSION),D('0'))
 def closing_deals(self):return tuple(x for x in self.deals.values() if x.entry in (DealEntry.OUT,DealEntry.INOUT,DealEntry.OUT_BY))
@dataclass
class AllocationRecord:
 key:EventKey; source_deal_tickets:tuple[int,...]; amount:D; consumed:D; residual:D; reconciliation_state:ReconciliationState; revision:int=0
 @property
 def available(self):return self.amount-self.consumed
@dataclass(frozen=True)
class ConsumptionRecord:
 key:EventKey; allocation_key:EventKey; amount:D; purpose:AllocationType; revision:int
@dataclass
class AllocationLedger:
 identity:Identity; records:dict[EventKey,AllocationRecord]=field(default_factory=dict); consumptions:dict[EventKey,ConsumptionRecord]=field(default_factory=dict); revision:int=0
 def allocated_from_source(self,ticket:int)->D:return sum((r.amount+r.residual for r in self.records.values() if ticket in r.source_deal_tickets),D('0'))
 def allocate(self,event:EventRecord,economic:EconomicLedger,key:EventKey,amount:D,sources:Iterable[int],residual:D=D('0'),projected:bool=False)->bool:
  source=tuple(sources)
  if event.state is not ReconciliationState.RECONCILED or projected or amount<0 or not source or key in self.records:raise ValueError('allocation not reconciled/duplicate')
  if (key.account_login,key.symbol,key.magic,key.cycle_id)!=(self.identity.account,self.identity.symbol,self.identity.magic,self.identity.cycle):raise ValueError('foreign allocation')
  if any(t not in economic.deals for t in source):raise ValueError('unknown source')
  for t in source:
   net=economic.deals[t].net
   if net<=0 or self.allocated_from_source(t)+amount+residual>net:raise ValueError('global conservation')
  self.revision+=1;self.records[key]=AllocationRecord(key,source,amount,D('0'),residual,event.state,self.revision);return True
 def available(self,kind:AllocationType)->D:return sum((r.available for r in self.records.values() if r.key.allocation_type is kind),D('0'))
 def consume(self,allocation_key:EventKey,consume_key:EventKey,amount:D,purpose:AllocationType)->bool:
  if amount<=0 or allocation_key not in self.records:raise ValueError('invalid consume')
  if consume_key in self.consumptions:return False
  r=self.records[allocation_key]
  if r.key.allocation_type is AllocationType.FINAL_RESERVE and purpose is AllocationType.PARTIAL_FAR:raise ValueError('reserve forbidden')
  if amount>r.available:raise ValueError('over-consume')
  self.revision+=1;r.consumed+=amount;r.revision=self.revision;self.consumptions[consume_key]=ConsumptionRecord(consume_key,allocation_key,amount,purpose,self.revision);return True
@dataclass(frozen=True)
class PartialFillResult:
 volume_before:D; requested_volume:D; actual_closed_volume:D; volume_after:D
 entry_cost_before:D; allocated_entry_cost:D; entry_cost_after:D
@dataclass
class OpenPositionCost:
 volume:D; unallocated_entry_cost:D; applied_fill_tickets:set[int]=field(default_factory=set)
 def close(self,requested:D,actual:D,ticket:int=1,broker:Broker|None=None)->PartialFillResult:
  before=self.volume; cost=self.unallocated_entry_cost
  if ticket in self.applied_fill_tickets:raise ValueError('duplicate fill')
  if requested<=0 or actual<=0 or actual>requested or actual>before:raise ValueError('zero/overfill/request mismatch')
  if broker:broker.validate_lot(actual)
  self.applied_fill_tickets.add(ticket)
  allocated=cost if actual==before else cost*actual/before
  self.volume-=actual; self.unallocated_entry_cost-=allocated
  return PartialFillResult(before,requested,actual,self.volume,cost,allocated,self.unallocated_entry_cost)
@dataclass
class PersistentStore:
 economic:EconomicLedger; allocation:AllocationLedger; events:dict[EventKey,EventRecord]=field(default_factory=dict); revision:int=0; opening_costs:dict[str,OpenPositionCost]=field(default_factory=dict)
 def serialize(self)->str:
  deals=[{'ticket':x.ticket,'position_id':x.position_id,'entry':x.entry.value,'deal_type':x.deal_type.value,'actual_volume':str(x.actual_volume),'profit':str(x.profit),'swap':str(x.swap),'commission':str(x.commission),'fee':str(x.fee),'initial_ignored':x.initial_ignored} for x in self.economic.deals.values()]
  allocations=[{'key':r.key.to_dict(),'sources':r.source_deal_tickets,'amount':str(r.amount),'consumed':str(r.consumed),'residual':str(r.residual),'state':r.reconciliation_state.value,'revision':r.revision} for r in self.allocation.records.values()]
  consumptions=[{'key':r.key.to_dict(),'allocation_key':r.allocation_key.to_dict(),'amount':str(r.amount),'purpose':r.purpose.value,'revision':r.revision} for r in self.allocation.consumptions.values()]
  data={'identity':asdict(self.economic.identity),'broker':{k:str(v) for k,v in asdict(self.economic.broker).items()},'deals':deals,'allocations':allocations,'consumptions':consumptions,'allocation_revision':self.allocation.revision,'events':[{'key':k.to_dict(),'state':v.state.value,'revision':v.revision} for k,v in self.events.items()],'opening_costs':{k:{'volume':str(v.volume),'cost':str(v.unallocated_entry_cost),'tickets':sorted(v.applied_fill_tickets)} for k,v in self.opening_costs.items()},'revision':self.revision}
  return json.dumps(data,sort_keys=True,separators=(',',':'))
 @classmethod
 def deserialize(cls,payload:str)->'PersistentStore':
  x=json.loads(payload);ident=Identity(**x['identity']);broker=Broker(**{k:D(v) for k,v in x['broker'].items()});econ=EconomicLedger(ident,broker)
  for q in x['deals']:econ.apply(Deal(ident,q['ticket'],q['position_id'],DealEntry(q['entry']),DealType(q['deal_type']),D(q['actual_volume']),D(q['profit']),D(q['swap']),D(q['commission']),D(q['fee']),q['initial_ignored']))
  allocation=AllocationLedger(ident,revision=x['allocation_revision'])
  for q in x['allocations']:
   k=EventKey.from_dict(q['key']);allocation.records[k]=AllocationRecord(k,tuple(q['sources']),D(q['amount']),D(q['consumed']),D(q['residual']),ReconciliationState(q['state']),q['revision'])
  for q in x['consumptions']:
   k=EventKey.from_dict(q['key']);allocation.consumptions[k]=ConsumptionRecord(k,EventKey.from_dict(q['allocation_key']),D(q['amount']),AllocationType(q['purpose']),q['revision'])
  events={EventKey.from_dict(q['key']):EventRecord(EventKey.from_dict(q['key']),ReconciliationState(q['state']),q['revision']) for q in x['events']};costs={k:OpenPositionCost(D(v['volume']),D(v['cost']),set(v['tickets'])) for k,v in x['opening_costs'].items()}
  return cls(econ,allocation,events,x['revision'],costs)
 def replay_history(self,history:Iterable[Deal])->int:return self.economic.replay(history)
@dataclass(frozen=True)
class GateResult: allowed:bool; recovery:D; reserve:D; deficit:D; reasons:tuple[str,...]
def evaluate_final_close(snapshot:EventSnapshot,store:PersistentStore,positions:Iterable[Position],broker:Broker,risk_ok:bool,margin_ok:bool,threshold:D,required_deficit:D,current_revision:int,preview:bool=False)->GateResult:
 reasons=[]
 if snapshot.identity!=store.economic.identity:reasons.append('FOREIGN_IDENTITY')
 if snapshot.broker!=broker:reasons.append('BROKER_MISMATCH')
 recovery=store.economic.realized_cycle_net+floating_total(store.economic.identity,positions,broker,snapshot.slippage_diagnostic)
 reserve=store.allocation.available(AllocationType.FINAL_RESERVE)
 event=store.events.get(snapshot.event_key)
 if not event or event.state is not ReconciliationState.PERSISTED:reasons.append('UNRECONCILED')
 if snapshot.pending_deal_tickets:reasons.append('PENDING_DEALS')
 if any(e.state is not ReconciliationState.PERSISTED for e in store.events.values()):reasons.append('PENDING_ALLOCATION')
 if recovery<=threshold:reasons.append('RECOVERY')
 if reserve<required_deficit:reasons.append('RESERVE')
 if not risk_ok:reasons.append('RISK')
 if not margin_ok:reasons.append('MARGIN')
 if snapshot.state_revision!=current_revision or snapshot.ledger_revision!=store.revision:reasons.append('STALE')
 if preview:reasons.append('PREVIEW_NOT_ACTUAL')
 return GateResult(not reasons,recovery,reserve,required_deficit,tuple(reasons))
@dataclass(frozen=True,order=True)
class EventKey:
 account_login:int; symbol:str; magic:int; cycle_id:str; event_type:str; level:int; phase:str
 position_identifier:str; deal_ticket:int; allocation_type:AllocationType
 def __post_init__(self):
  if not self.symbol or not self.cycle_id or not self.event_type or not self.phase or not self.position_identifier or self.deal_ticket<=0:raise ValueError('incomplete EventKey')
 def to_dict(self):return {**asdict(self),'allocation_type':self.allocation_type.value}
 @classmethod
 def from_dict(cls,x):return cls(**{**x,'allocation_type':AllocationType(x['allocation_type'])})
