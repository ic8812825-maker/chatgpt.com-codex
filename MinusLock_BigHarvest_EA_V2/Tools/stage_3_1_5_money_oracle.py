"""Executable Decimal proof model for Stage 3.1.5; independent from MQL5."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from decimal import Decimal
from enum import Enum
import json
import hashlib
from typing import Iterable
D=Decimal
class PositionSide(str,Enum): BUY="BUY"; SELL="SELL"
class DealEntry(str,Enum): IN="IN"; OUT="OUT"; INOUT="INOUT"; OUT_BY="OUT_BY"
class DealType(str,Enum):
 BUY="BUY"; SELL="SELL"; BALANCE="BALANCE"; CREDIT="CREDIT"; CHARGE="CHARGE"; CORRECTION="CORRECTION"; COMMISSION="COMMISSION"; OTHER="OTHER"
class ReconciliationState(str,Enum):
 DISCOVERED="DISCOVERED"; PENDING_RECONCILIATION="PENDING_RECONCILIATION"; RECONCILED="RECONCILED"; ALLOCATION_PENDING="ALLOCATION_PENDING"; APPLIED="APPLIED"; PERSISTED="PERSISTED"; CONFLICT="CONFLICT"; REJECTED="REJECTED"
class AllocationType(str,Enum): PARTIAL_FAR="PARTIAL_FAR"; FINAL_RESERVE="FINAL_RESERVE"; CARRY="CARRY"; TRANSITION="TRANSITION"; RESIDUAL="RESIDUAL"
class IntegrityCode(str,Enum):
 FOREIGN_ALLOCATION_IDENTITY="FOREIGN_ALLOCATION_IDENTITY"; ALLOCATION_EVENT_MISMATCH="ALLOCATION_EVENT_MISMATCH"; ALLOCATION_STATE_INVALID="ALLOCATION_STATE_INVALID"; ALLOCATION_SOURCE_POOL_MISSING="ALLOCATION_SOURCE_POOL_MISSING"; FOREIGN_CONSUMPTION_IDENTITY="FOREIGN_CONSUMPTION_IDENTITY"; CONSUMPTION_ROUTE_MISMATCH="CONSUMPTION_ROUTE_MISMATCH"; CONSUMPTION_TRANSACTION_CONFLICT="CONSUMPTION_TRANSACTION_CONFLICT"; DUPLICATE_EVENT_KEY="DUPLICATE_EVENT_KEY"; DUPLICATE_ALLOCATION_KEY="DUPLICATE_ALLOCATION_KEY"; DUPLICATE_CONSUMPTION_KEY="DUPLICATE_CONSUMPTION_KEY"; DUPLICATE_DEAL_TICKET="DUPLICATE_DEAL_TICKET"; DUPLICATE_SOURCE_POOL="DUPLICATE_SOURCE_POOL"; DUPLICATE_POSITION="DUPLICATE_POSITION"; SOURCE_TICKET_REUSED="SOURCE_TICKET_REUSED"; SOURCE_POOL_HISTORY_MISMATCH="SOURCE_POOL_HISTORY_MISMATCH"; MONEY_STATE_STALE="MONEY_STATE_STALE"; LEDGER_INTEGRITY_FAILURE="LEDGER_INTEGRITY_FAILURE"
 SOURCE_POOL_FOREIGN_IDENTITY="SOURCE_POOL_FOREIGN_IDENTITY"; SOURCE_POOL_EVENT_MISMATCH="SOURCE_POOL_EVENT_MISMATCH"; SOURCE_POOL_CONSERVATION_FAILURE="SOURCE_POOL_CONSERVATION_FAILURE"; SOURCE_POOL_KEY_MISMATCH="SOURCE_POOL_KEY_MISMATCH"
 FOREIGN_EVENT_IDENTITY="FOREIGN_EVENT_IDENTITY"; EVENT_RECORD_KEY_MISMATCH="EVENT_RECORD_KEY_MISMATCH"; EVENT_STATE_REVISION_INVALID="EVENT_STATE_REVISION_INVALID"; ALLOCATION_EVENT_ROUTE_MISMATCH="ALLOCATION_EVENT_ROUTE_MISMATCH"
 OPENING_COST_STATE_INVALID="OPENING_COST_STATE_INVALID"; OPENING_COST_CONSERVATION_FAILURE="OPENING_COST_CONSERVATION_FAILURE"; DUPLICATE_FILL_TICKET="DUPLICATE_FILL_TICKET"; NON_FINITE_MONEY_VALUE="NON_FINITE_MONEY_VALUE"; PERSISTENCE_SCHEMA_INVALID="PERSISTENCE_SCHEMA_INVALID"
class OracleIntegrityError(ValueError):
 def __init__(self,code:IntegrityCode,detail:str=''):self.code=code;super().__init__(f'{code.value}:{detail}')
def require_integrity(ok:bool,code:IntegrityCode,detail:str=''):
 if not ok:raise OracleIntegrityError(code,detail)
class ConsumptionPurpose(str,Enum): FINAL_FAR_CLOSE="FINAL_FAR_CLOSE"; PARTIAL_FAR="PARTIAL_FAR"; CARRY="CARRY"; TRANSITION="TRANSITION"
@dataclass(frozen=True,order=True)
class EventKey:
 account_login:int; symbol:str; magic:int; cycle_id:str; event_type:str; level:int; phase:str; position_identifier:str; deal_ticket:int; allocation_type:AllocationType
 def __post_init__(self):
  if not self.symbol or not self.cycle_id or not self.event_type or not self.phase or not self.position_identifier or self.deal_ticket<=0:raise ValueError('incomplete EventKey')
 def to_dict(self):return {**asdict(self),'allocation_type':self.allocation_type.value}
 @classmethod
 def from_dict(cls,x):return cls(**{**x,'allocation_type':AllocationType(x['allocation_type'])})
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
def event_identity_projection(k:EventKey):return (k.account_login,k.symbol,k.magic,k.cycle_id,k.event_type,k.level,k.phase,k.position_identifier,k.deal_ticket)
@dataclass(frozen=True)
class EventIdentity:
 account_login:int; symbol:str; magic:int; cycle_id:str; event_type:str; level:int; phase:str; position_identifier:str; deal_ticket:int
 @classmethod
 def from_key(cls,key:EventKey):return cls(*event_identity_projection(key))
@dataclass(frozen=True,order=True)
class ConsumptionKey:
 account_login:int; symbol:str; magic:int; cycle_id:str; consumption_event_type:str; level:int; phase:str; position_identifier:str; transaction_id:str; purpose:ConsumptionPurpose; parent_allocation_key:EventKey
 def __post_init__(self):
  if not self.symbol or not self.cycle_id or not self.consumption_event_type or not self.phase or not self.position_identifier or not self.transaction_id or not isinstance(self.parent_allocation_key,EventKey):raise ValueError('incomplete ConsumptionKey')
 def to_dict(self):
  d=asdict(self);d['purpose']=self.purpose.value;d['parent_allocation_key']=self.parent_allocation_key.to_dict();return d
 @classmethod
 def from_dict(cls,x):return cls(**{**x,'purpose':ConsumptionPurpose(x['purpose']),'parent_allocation_key':EventKey.from_dict(x['parent_allocation_key'])})
@dataclass(frozen=True)
class ConsumptionRoute:
 allocation_type:AllocationType; purpose:ConsumptionPurpose; event_type:str
 def matches(self,key:ConsumptionKey)->bool:return key.purpose is self.purpose and key.consumption_event_type==self.event_type
@dataclass(frozen=True)
class EventSnapshot:
 identity:Identity; event_key:EventKey; event_type:str; level:int; scenario:str; phase:str; broker:Broker
 managed_positions:tuple[Position,...]; actual_lots:tuple[D,...]; actual_open_prices:tuple[D,...]
 final_reserve_available:D; partial_far_budget_available:D; carry_available:D; transition_budget_available:D
 residual:D; commission:D; swap:D; fee:D; slippage_diagnostic:D; reconciliation_state:ReconciliationState
 applied_deal_tickets:frozenset[int]; pending_deal_tickets:frozenset[int]; state_revision:int; ledger_revision:int
 realized_cycle_net:D; floating_close_now:D; recovery_pl_close_now:D; money_state_version:'MoneyStateVersion'
 def __post_init__(self):
  if (self.event_key.account_login,self.event_key.symbol,self.event_key.magic,self.event_key.cycle_id)!=(self.identity.account,self.identity.symbol,self.identity.magic,self.identity.cycle):raise ValueError('snapshot identity mismatch')
  if (self.event_type,self.level,self.phase)!=(self.event_key.event_type,self.event_key.level,self.event_key.phase):raise ValueError('snapshot metadata mismatch')
  if any(p.identity!=self.identity or not p.identifier or not p.leg_id or not p.role or not isinstance(p.side,PositionSide) for p in self.managed_positions):raise ValueError('foreign/invalid position')
  if len({p.leg_id for p in self.managed_positions})!=len(self.managed_positions):raise ValueError('duplicate leg')
  if len({p.identifier for p in self.managed_positions})!=len(self.managed_positions):raise ValueError('duplicate position')
  for p in self.managed_positions:self.broker.validate_lot(p.volume);self.broker.validate_price(p.open_price)
  if self.actual_lots!=tuple(p.volume for p in self.managed_positions): raise ValueError('actual lot mismatch')
  if self.actual_open_prices!=tuple(p.open_price for p in self.managed_positions): raise ValueError('open price mismatch')
  recalculated=floating_total(self.identity,self.managed_positions,self.broker,self.slippage_diagnostic)
  if self.floating_close_now!=recalculated:raise ValueError('floating mismatch')
  if self.recovery_pl_close_now!=self.realized_cycle_net+recalculated: raise ValueError('recovery mismatch')
def floating_total(identity:Identity,positions:Iterable[Position],broker:Broker,slippage:D=D('0'))->D:
 return sum((projected_profit(p.side,p.volume,p.open_price,broker,slippage)+p.swap+p.exit_commission+p.exit_fee for p in positions if p.identity==identity),D('0'))
def make_snapshot(identity:Identity,event_key:EventKey,event_type:str,level:int,scenario:str,phase:str,broker:Broker,positions:Iterable[Position],realized:D,state:ReconciliationState,revision:int,**kw)->EventSnapshot:
 ps=tuple(positions)
 if any(p.identity!=identity for p in ps):raise ValueError('foreign position')
 floating=floating_total(identity,ps,broker,kw.get('slippage_diagnostic',D('0')))
 version=kw.get('money_state_version')
 if not isinstance(version,MoneyStateVersion):raise ValueError('MoneyStateVersion required')
 return EventSnapshot(identity,event_key,event_type,level,scenario,phase,broker,ps,tuple(p.volume for p in ps),tuple(p.open_price for p in ps),kw.get('final_reserve_available',D('0')),kw.get('partial_far_budget_available',D('0')),kw.get('carry_available',D('0')),kw.get('transition_budget_available',D('0')),kw.get('residual',D('0')),kw.get('commission',D('0')),kw.get('swap',D('0')),kw.get('fee',D('0')),kw.get('slippage_diagnostic',D('0')),state,frozenset(kw.get('applied_deal_tickets',())),frozenset(kw.get('pending_deal_tickets',())),revision,kw.get('ledger_revision',revision),realized,floating,realized+floating,version)
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
def deal_fingerprint(d:Deal)->dict:
 return {'identity':asdict(d.identity),'ticket':d.ticket,'position_id':d.position_id,'entry':d.entry.value,'deal_type':d.deal_type.value,'actual_volume':str(d.actual_volume),'profit':str(d.profit),'swap':str(d.swap),'commission':str(d.commission),'fee':str(d.fee),'initial_ignored':d.initial_ignored}
MANAGED_DEAL_TYPES={DealType.BUY,DealType.SELL,DealType.COMMISSION}
@dataclass
class EconomicLedger:
 identity:Identity; broker:Broker; deals:dict[int,Deal]=field(default_factory=dict); revision:int=0
 def apply(self,deal:Deal)->bool:
  deal.validate(self.broker)
  if deal.identity!=self.identity or deal.deal_type not in MANAGED_DEAL_TYPES or deal.initial_ignored:return False
  if deal.ticket in self.deals:return False
  self.deals[deal.ticket]=deal;self.revision+=1;return True
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
 key:ConsumptionKey; allocation_key:EventKey; amount:D; purpose:ConsumptionPurpose; revision:int
@dataclass
class ReconciledSourcePool:
 key:EventKey; source_deal_tickets:tuple[int,...]; deal_nets:dict[int,D]; deal_fingerprints:dict[int,dict]=field(default_factory=dict); already_allocated:D=D('0'); residual:D=D('0'); revision:int=0
 @property
 def aggregate_actual_source_net(self):return sum(self.deal_nets.values(),D('0'))
 @property
 def available(self):return self.aggregate_actual_source_net-self.already_allocated-self.residual
 def validate_conservation(self):
  require_integrity(self.aggregate_actual_source_net>D('0') and self.already_allocated>=D('0') and self.residual>=D('0') and self.already_allocated+self.residual<=self.aggregate_actual_source_net,IntegrityCode.SOURCE_POOL_CONSERVATION_FAILURE)
@dataclass
class AllocationLedger:
 identity:Identity; records:dict[EventKey,AllocationRecord]=field(default_factory=dict); consumptions:dict[ConsumptionKey,ConsumptionRecord]=field(default_factory=dict); revision:int=0; source_pools:dict[tuple[int,...],ReconciledSourcePool]=field(default_factory=dict)
 def allocated_from_source(self,ticket:int)->D:return sum((r.amount+r.residual for r in self.records.values() if ticket in r.source_deal_tickets),D('0'))
 def allocate(self,event:EventRecord,economic:EconomicLedger,key:EventKey,amount:D,sources:Iterable[int],residual:D=D('0'),projected:bool=False)->bool:
  source=tuple(sources)
  if not isinstance(event.event_id,EventKey) or not isinstance(key,EventKey):raise ValueError('typed key required')
  if event.state is not ReconciliationState.RECONCILED or projected or amount<0 or not source or key in self.records:raise ValueError('allocation not reconciled/duplicate')
  if event_identity_projection(event.event_id)!=event_identity_projection(key):raise ValueError('event/allocation key mismatch')
  if (key.account_login,key.symbol,key.magic,key.cycle_id)!=(self.identity.account,self.identity.symbol,self.identity.magic,self.identity.cycle):raise ValueError('foreign allocation')
  if any(t not in economic.deals for t in source):raise ValueError('unknown source')
  source_deals=tuple(economic.deals[t] for t in source)
  closing=(DealEntry.OUT,DealEntry.INOUT,DealEntry.OUT_BY)
  if not any(d.entry in closing and d.deal_type in (DealType.BUY,DealType.SELL) for d in source_deals):raise ValueError('closing harvest required')
  if any(d.entry not in closing and d.deal_type is not DealType.COMMISSION for d in source_deals):raise ValueError('ineligible opening source')
  pool_key=tuple(sorted(source))
  if any(set(pool_key)&set(existing) and existing!=pool_key for existing in self.source_pools):raise ValueError('ticket reused by another pool')
  pool=self.source_pools.get(pool_key)
  if pool is None:
   pool=ReconciledSourcePool(event.event_id,pool_key,{t:economic.deals[t].net for t in pool_key},{t:deal_fingerprint(economic.deals[t]) for t in pool_key});self.source_pools[pool_key]=pool
  elif pool.available<=0:raise OracleIntegrityError(IntegrityCode.SOURCE_TICKET_REUSED)
  if pool.aggregate_actual_source_net<=0 or amount+residual>pool.available:raise ValueError('aggregate conservation')
  self.revision+=1;pool.already_allocated+=amount;pool.residual+=residual;pool.revision=self.revision;self.records[key]=AllocationRecord(key,source,amount,D('0'),residual,event.state,self.revision);return True
 def available(self,kind:AllocationType)->D:return sum((r.available for r in self.records.values() if r.key.allocation_type is kind),D('0'))
 def validate_source_pools(self,economic:EconomicLedger,events:dict[EventKey,EventRecord]|None=None)->None:
  seen=set()
  for tickets,pool in self.source_pools.items():
   pool.validate_conservation()
   identity=(self.identity.account,self.identity.symbol,self.identity.magic,self.identity.cycle)
   require_integrity((pool.key.account_login,pool.key.symbol,pool.key.magic,pool.key.cycle_id)==identity,IntegrityCode.SOURCE_POOL_FOREIGN_IDENTITY)
   require_integrity(tuple(sorted(pool.source_deal_tickets))==tickets and set(tickets)==set(pool.deal_nets)==set(pool.deal_fingerprints),IntegrityCode.SOURCE_POOL_KEY_MISMATCH)
   if events is not None:
    parent=events.get(pool.key)
    require_integrity(parent is not None and parent.event_id==pool.key,IntegrityCode.SOURCE_POOL_EVENT_MISMATCH)
   if seen.intersection(tickets):raise ValueError('overlapping source pools')
   seen.update(tickets)
   if any(t not in economic.deals or economic.deals[t].net!=pool.deal_nets.get(t) or deal_fingerprint(economic.deals[t])!=pool.deal_fingerprints.get(t) for t in tickets):raise ValueError('source pool history mismatch')
   if not any(economic.deals[t].entry in (DealEntry.OUT,DealEntry.INOUT,DealEntry.OUT_BY) and economic.deals[t].deal_type in (DealType.BUY,DealType.SELL) for t in tickets):raise ValueError('source pool closing harvest missing')
   records=[r for r in self.records.values() if tuple(sorted(r.source_deal_tickets))==tickets]
   require_integrity(pool.already_allocated==sum((r.amount for r in records),D('0')) and pool.residual==sum((r.residual for r in records),D('0')),IntegrityCode.SOURCE_POOL_CONSERVATION_FAILURE)
  for key,record in self.records.items():
   if tuple(sorted(record.source_deal_tickets)) not in self.source_pools:raise ValueError('allocation source pool missing')
   consumed=sum((c.amount for c in self.consumptions.values() if c.allocation_key==key),D('0'))
   if consumed!=record.consumed or record.amount!=record.consumed+record.available or record.available<0:raise ValueError('allocation consumption mismatch')
  if any(c.allocation_key not in self.records or c.key.parent_allocation_key!=c.allocation_key for c in self.consumptions.values()):raise ValueError('orphan consumption')
  revisions=[r.revision for r in self.records.values()]+[p.revision for p in self.source_pools.values()]+[c.revision for c in self.consumptions.values()]
  if revisions and self.revision!=max(revisions):raise ValueError('allocation revision mismatch')
 def consume(self,allocation_key:EventKey,consume_key:ConsumptionKey,amount:D)->bool:
  if not isinstance(consume_key,ConsumptionKey) or amount<=0 or allocation_key not in self.records:raise ValueError('invalid consume')
  if (consume_key.account_login,consume_key.symbol,consume_key.magic,consume_key.cycle_id)!=(self.identity.account,self.identity.symbol,self.identity.magic,self.identity.cycle):raise ValueError('foreign consume')
  if consume_key.parent_allocation_key!=allocation_key:raise ValueError('parent allocation mismatch')
  if (consume_key.level,consume_key.phase,consume_key.position_identifier)!=(allocation_key.level,allocation_key.phase,allocation_key.position_identifier):raise ValueError('consumption event route mismatch')
  for existing in self.consumptions:
   if existing.transaction_id==consume_key.transaction_id:
    if existing==consume_key:return False
    raise ValueError('consumption transaction conflict')
  if consume_key in self.consumptions:return False
  r=self.records[allocation_key]
  routes={AllocationType.FINAL_RESERVE:ConsumptionRoute(AllocationType.FINAL_RESERVE,ConsumptionPurpose.FINAL_FAR_CLOSE,'FINAL_FAR_CLOSE'),AllocationType.PARTIAL_FAR:ConsumptionRoute(AllocationType.PARTIAL_FAR,ConsumptionPurpose.PARTIAL_FAR,'PARTIAL_FAR'),AllocationType.CARRY:ConsumptionRoute(AllocationType.CARRY,ConsumptionPurpose.CARRY,'CARRY'),AllocationType.TRANSITION:ConsumptionRoute(AllocationType.TRANSITION,ConsumptionPurpose.TRANSITION,'TRANSITION')}
  if r.reconciliation_state is not ReconciliationState.RECONCILED or not routes.get(r.key.allocation_type) or not routes[r.key.allocation_type].matches(consume_key):raise ValueError('purpose/event route forbidden')
  if amount>r.available:raise ValueError('over-consume')
  self.revision+=1;r.consumed+=amount;r.revision=self.revision;self.consumptions[consume_key]=ConsumptionRecord(consume_key,allocation_key,amount,consume_key.purpose,self.revision);return True
@dataclass(frozen=True)
class PartialFillResult:
 volume_before:D; requested_volume:D; actual_closed_volume:D; volume_after:D
 entry_cost_before:D; allocated_entry_cost:D; entry_cost_after:D
@dataclass(frozen=True)
class FillRecord:
 ticket:int; requested_volume:D; actual_volume:D; volume_before:D; volume_after:D; allocated_cost:D
@dataclass
class OpenPositionCost:
 volume:D; unallocated_entry_cost:D; applied_fill_tickets:set[int]=field(default_factory=set); allocated_entry_cost:D=D('0'); initial_volume:D|None=None; initial_opening_cost:D|None=None; fills:list[FillRecord]=field(default_factory=list); revision:int=0
 def __post_init__(self):
  if self.initial_volume is None:self.initial_volume=self.volume+sum((f.actual_volume for f in self.fills),D('0'))
  if self.initial_opening_cost is None:self.initial_opening_cost=self.unallocated_entry_cost+self.allocated_entry_cost
 def validate_integrity(self):
  require_integrity(self.initial_volume is not None and self.initial_volume>D('0') and D('0')<=self.volume<=self.initial_volume,IntegrityCode.OPENING_COST_STATE_INVALID)
  require_integrity(self.initial_opening_cost==self.allocated_entry_cost+self.unallocated_entry_cost,IntegrityCode.OPENING_COST_CONSERVATION_FAILURE)
  require_integrity(len(self.applied_fill_tickets)==len(self.fills)==len({f.ticket for f in self.fills}),IntegrityCode.DUPLICATE_FILL_TICKET)
  cursor=self.initial_volume
  allocated=D('0')
  for fill in self.fills:
   require_integrity(fill.requested_volume>D('0') and D('0')<fill.actual_volume<=fill.requested_volume and fill.volume_before==cursor and fill.volume_after==cursor-fill.actual_volume,IntegrityCode.OPENING_COST_STATE_INVALID)
   cursor=fill.volume_after;allocated+=fill.allocated_cost
  require_integrity(cursor==self.volume and allocated==self.allocated_entry_cost,IntegrityCode.OPENING_COST_CONSERVATION_FAILURE)
 def close(self,requested:D,actual:D,ticket:int=1,broker:Broker|None=None)->PartialFillResult:
  before=self.volume; cost=self.unallocated_entry_cost
  if ticket in self.applied_fill_tickets:raise ValueError('duplicate fill')
  if requested<=0 or requested>before or actual<=0 or actual>requested or actual>before:raise ValueError('zero/overfill/request mismatch')
  if broker:broker.validate_lot(requested);broker.validate_lot(actual)
  self.applied_fill_tickets.add(ticket)
  allocated=cost if actual==before else cost*actual/before
  self.volume-=actual; self.unallocated_entry_cost-=allocated;self.allocated_entry_cost+=allocated
  self.revision+=1;self.fills.append(FillRecord(ticket,requested,actual,before,self.volume,allocated))
  return PartialFillResult(before,requested,actual,self.volume,cost,allocated,self.unallocated_entry_cost)
@dataclass
class PersistentStore:
 economic:EconomicLedger; allocation:AllocationLedger; events:dict[EventKey,EventRecord]=field(default_factory=dict); revision:int=0; opening_costs:dict[str,OpenPositionCost]=field(default_factory=dict); managed_positions:tuple[Position,...]=(); positions_revision:int=0
 @property
 def money_state_version(self):
  digest=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,default=str,separators=(',',':')).encode()).hexdigest()
  events=digest([(k.to_dict(),v.state.value,v.revision) for k,v in sorted(self.events.items())]);pools=digest([(k,p.deal_nets,p.deal_fingerprints,p.already_allocated,p.residual,p.revision) for k,p in sorted(self.allocation.source_pools.items())]);cons=digest([(k.to_dict(),v.allocation_key.to_dict(),v.amount,v.purpose.value,v.revision) for k,v in sorted(self.allocation.consumptions.items())]);costs=digest([(k,v.volume,v.unallocated_entry_cost,sorted(v.applied_fill_tickets),v.allocated_entry_cost) for k,v in sorted(self.opening_costs.items())]);allocations=digest([(k.to_dict(),r.source_deal_tickets,r.amount,r.consumed,r.available,r.residual,r.reconciliation_state.value,r.revision) for k,r in sorted(self.allocation.records.items())]);deals=digest([deal_fingerprint(d) for _,d in sorted(self.economic.deals.items())]);positions=digest([asdict(p) for p in self.managed_positions]);broker=digest(asdict(self.economic.broker));metadata=digest({'identity':asdict(self.economic.identity),'revision':self.revision,'positions_revision':self.positions_revision,'economic_revision':self.economic.revision,'allocation_revision':self.allocation.revision})
  i=self.economic.identity;return MoneyStateVersion(i.account,i.symbol,i.magic,i.cycle,broker,deals,allocations,pools,cons,events,positions,costs,metadata)
 def validate_integrity(self)->None:
  identity=self.economic.identity
  money_values=[]
  for deal in self.economic.deals.values():money_values.extend((deal.actual_volume,deal.profit,deal.swap,deal.commission,deal.fee))
  require_integrity(all(isinstance(value,D) and value.is_finite() for value in money_values),IntegrityCode.NON_FINITE_MONEY_VALUE)
  for dictionary_key,event in self.events.items():
   require_integrity(dictionary_key==event.event_id,IntegrityCode.EVENT_RECORD_KEY_MISMATCH)
   require_integrity((dictionary_key.account_login,dictionary_key.symbol,dictionary_key.magic,dictionary_key.cycle_id)==(identity.account,identity.symbol,identity.magic,identity.cycle),IntegrityCode.FOREIGN_EVENT_IDENTITY)
   require_integrity(event.revision>=0 and not (event.state is ReconciliationState.PERSISTED and event.revision<1),IntegrityCode.EVENT_STATE_REVISION_INVALID)
  for cost in self.opening_costs.values():cost.validate_integrity()
  for key,r in self.allocation.records.items():
   require_integrity((key.account_login,key.symbol,key.magic,key.cycle_id)==(identity.account,identity.symbol,identity.magic,identity.cycle),IntegrityCode.FOREIGN_ALLOCATION_IDENTITY)
   event=next((e for ek,e in self.events.items() if EventIdentity.from_key(ek)==EventIdentity.from_key(key)),None);require_integrity(event is not None,IntegrityCode.ALLOCATION_EVENT_MISMATCH)
   require_integrity(event.event_id.allocation_type in (AllocationType.RESIDUAL,key.allocation_type),IntegrityCode.ALLOCATION_EVENT_ROUTE_MISMATCH)
   require_integrity(r.reconciliation_state is ReconciliationState.RECONCILED and r.amount>=0 and r.consumed>=0 and r.consumed<=r.amount and r.residual>=0,IntegrityCode.ALLOCATION_STATE_INVALID)
   require_integrity(tuple(sorted(r.source_deal_tickets)) in self.allocation.source_pools,IntegrityCode.ALLOCATION_SOURCE_POOL_MISSING)
  transactions={}
  for key,c in self.allocation.consumptions.items():
   require_integrity((key.account_login,key.symbol,key.magic,key.cycle_id)==(identity.account,identity.symbol,identity.magic,identity.cycle),IntegrityCode.FOREIGN_CONSUMPTION_IDENTITY)
   require_integrity(c.allocation_key in self.allocation.records and key.parent_allocation_key==c.allocation_key,IntegrityCode.CONSUMPTION_ROUTE_MISMATCH)
   route=(key.level,key.phase,key.position_identifier)==(c.allocation_key.level,c.allocation_key.phase,c.allocation_key.position_identifier)
   routes={AllocationType.FINAL_RESERVE:(ConsumptionPurpose.FINAL_FAR_CLOSE,'FINAL_FAR_CLOSE'),AllocationType.PARTIAL_FAR:(ConsumptionPurpose.PARTIAL_FAR,'PARTIAL_FAR'),AllocationType.CARRY:(ConsumptionPurpose.CARRY,'CARRY'),AllocationType.TRANSITION:(ConsumptionPurpose.TRANSITION,'TRANSITION')};allocation=self.allocation.records[c.allocation_key];expected=routes.get(allocation.key.allocation_type)
   require_integrity(route and expected==(key.purpose,key.consumption_event_type) and c.purpose is key.purpose and c.amount>0,IntegrityCode.CONSUMPTION_ROUTE_MISMATCH)
   prior=transactions.get(key.transaction_id);require_integrity(prior is None or prior==c,IntegrityCode.CONSUMPTION_TRANSACTION_CONFLICT);transactions[key.transaction_id]=c
  self.allocation.validate_source_pools(self.economic,self.events)
 def serialize(self)->str:
  deals=[{'ticket':x.ticket,'position_id':x.position_id,'entry':x.entry.value,'deal_type':x.deal_type.value,'actual_volume':str(x.actual_volume),'profit':str(x.profit),'swap':str(x.swap),'commission':str(x.commission),'fee':str(x.fee),'initial_ignored':x.initial_ignored} for x in self.economic.deals.values()]
  allocations=[{'key':r.key.to_dict(),'sources':r.source_deal_tickets,'amount':str(r.amount),'consumed':str(r.consumed),'residual':str(r.residual),'state':r.reconciliation_state.value,'revision':r.revision} for r in self.allocation.records.values()]
  consumptions=[{'key':r.key.to_dict(),'allocation_key':r.allocation_key.to_dict(),'amount':str(r.amount),'purpose':r.purpose.value,'revision':r.revision} for r in self.allocation.consumptions.values()]
  pools=[{'key':p.key.to_dict(),'sources':p.source_deal_tickets,'deal_nets':{str(k):str(v) for k,v in p.deal_nets.items()},'deal_fingerprints':{str(k):v for k,v in p.deal_fingerprints.items()},'allocated':str(p.already_allocated),'residual':str(p.residual),'available':str(p.available),'revision':p.revision} for p in self.allocation.source_pools.values()]
  positions=[{'identity':asdict(p.identity),'identifier':p.identifier,'leg_id':p.leg_id,'role':p.role,'side':p.side.value,'volume':str(p.volume),'open_price':str(p.open_price),'swap':str(p.swap),'exit_commission':str(p.exit_commission),'exit_fee':str(p.exit_fee)} for p in self.managed_positions]
  data={'schema_version':6,'identity':asdict(self.economic.identity),'broker':{k:str(v) for k,v in asdict(self.economic.broker).items()},'deals':deals,'allocations':allocations,'consumptions':consumptions,'source_pools':pools,'managed_positions':positions,'positions_revision':self.positions_revision,'allocation_revision':self.allocation.revision,'events':[{'key':k.to_dict(),'state':v.state.value,'revision':v.revision} for k,v in self.events.items()],'opening_costs':{k:{'volume':str(v.volume),'cost':str(v.unallocated_entry_cost),'tickets':sorted(v.applied_fill_tickets),'allocated':str(v.allocated_entry_cost),'initial_volume':str(v.initial_volume),'initial_cost':str(v.initial_opening_cost),'revision':v.revision,'fills':[{'ticket':f.ticket,'requested':str(f.requested_volume),'actual':str(f.actual_volume),'before':str(f.volume_before),'after':str(f.volume_after),'cost':str(f.allocated_cost)} for f in v.fills]} for k,v in self.opening_costs.items()},'revision':self.revision}
  return json.dumps(data,sort_keys=True,separators=(',',':'))
 @classmethod
 def deserialize(cls,payload:str)->'PersistentStore':
  x=json.loads(payload)
  required={'schema_version','identity','broker','deals','allocations','consumptions','source_pools','managed_positions','positions_revision','allocation_revision','events','opening_costs','revision'}
  require_integrity(isinstance(x,dict) and required<=set(x) and x['schema_version']==6,IntegrityCode.PERSISTENCE_SCHEMA_INVALID)
  def reject_non_finite(value):
   if isinstance(value,dict):
    for nested in value.values():reject_non_finite(nested)
   elif isinstance(value,list):
    for nested in value:reject_non_finite(nested)
   elif isinstance(value,str) and value.lower() in {'nan','infinity','-infinity','inf','-inf'}:raise OracleIntegrityError(IntegrityCode.NON_FINITE_MONEY_VALUE,value)
  reject_non_finite(x)
  def unique(rows,key,code):
   seen=set()
   for row in rows:
    value=key(row);require_integrity(value not in seen,code);seen.add(value)
  canonical=lambda value:json.dumps(value,sort_keys=True,separators=(',',':'))
  unique(x['deals'],lambda q:q['ticket'],IntegrityCode.DUPLICATE_DEAL_TICKET);unique(x['events'],lambda q:canonical(q['key']),IntegrityCode.DUPLICATE_EVENT_KEY);unique(x['allocations'],lambda q:canonical(q['key']),IntegrityCode.DUPLICATE_ALLOCATION_KEY);unique(x['consumptions'],lambda q:canonical(q['key']),IntegrityCode.DUPLICATE_CONSUMPTION_KEY);unique(x['consumptions'],lambda q:q['key']['transaction_id'],IntegrityCode.CONSUMPTION_TRANSACTION_CONFLICT);unique(x.get('source_pools',[]),lambda q:tuple(q['sources']),IntegrityCode.DUPLICATE_SOURCE_POOL);unique(x.get('managed_positions',[]),lambda q:q['identifier'],IntegrityCode.DUPLICATE_POSITION);unique(x.get('managed_positions',[]),lambda q:q['leg_id'],IntegrityCode.DUPLICATE_POSITION)
  ident=Identity(**x['identity']);broker=Broker(**{k:D(v) for k,v in x['broker'].items()});econ=EconomicLedger(ident,broker)
  for q in x['deals']:
   deal=Deal(ident,q['ticket'],q['position_id'],DealEntry(q['entry']),DealType(q['deal_type']),D(q['actual_volume']),D(q['profit']),D(q['swap']),D(q['commission']),D(q['fee']),q['initial_ignored'])
   if not econ.apply(deal):raise ValueError('persisted deal rejected')
  allocation=AllocationLedger(ident,revision=x['allocation_revision'])
  for q in x['allocations']:
   k=EventKey.from_dict(q['key']);allocation.records[k]=AllocationRecord(k,tuple(q['sources']),D(q['amount']),D(q['consumed']),D(q['residual']),ReconciliationState(q['state']),q['revision'])
  for q in x['consumptions']:
   k=ConsumptionKey.from_dict(q['key']);allocation.consumptions[k]=ConsumptionRecord(k,EventKey.from_dict(q['allocation_key']),D(q['amount']),ConsumptionPurpose(q['purpose']),q['revision'])
  for q in x.get('source_pools',[]):
   k=EventKey.from_dict(q['key']); tickets=tuple(q['sources']); nets={int(t):D(v) for t,v in q['deal_nets'].items()}
   if tickets in allocation.source_pools:raise ValueError('duplicate source pool')
   require_integrity(tuple(sorted(tickets))==tickets and set(tickets)==set(nets)==set(int(t) for t in q['deal_fingerprints']),IntegrityCode.SOURCE_POOL_KEY_MISMATCH)
   require_integrity(all(t in econ.deals and econ.deals[t].net==nets[t] for t in tickets),IntegrityCode.SOURCE_POOL_HISTORY_MISMATCH)
   fingerprints={int(t):v for t,v in q['deal_fingerprints'].items()};pool=ReconciledSourcePool(k,tickets,nets,fingerprints,D(q['allocated']),D(q['residual']),q['revision'])
   if pool.available!=D(q['available']):raise ValueError('corrupted source pool balance')
   allocation.source_pools[tickets]=pool
  events={EventKey.from_dict(q['key']):EventRecord(EventKey.from_dict(q['key']),ReconciliationState(q['state']),q['revision']) for q in x['events']};costs={k:OpenPositionCost(D(v['volume']),D(v['cost']),set(v['tickets']),D(v['allocated']),D(v.get('initial_volume',v['volume'])),D(v.get('initial_cost',v['cost'])),[FillRecord(f['ticket'],D(f['requested']),D(f['actual']),D(f['before']),D(f['after']),D(f['cost'])) for f in v.get('fills',[])],v.get('revision',0)) for k,v in x['opening_costs'].items()}
  positions=[]
  for q in x.get('managed_positions',[]):
   pi=Identity(**q['identity']); p=Position(pi,q['identifier'],q['leg_id'],q['role'],PositionSide(q['side']),D(q['volume']),D(q['open_price']),D(q['swap']),D(q['exit_commission']),D(q['exit_fee']))
   if pi!=ident or not p.identifier or not p.leg_id or not p.role:raise ValueError('corrupted managed position')
   broker.validate_lot(p.volume);broker.validate_price(p.open_price);positions.append(p)
  if len({p.identifier for p in positions})!=len(positions) or len({p.leg_id for p in positions})!=len(positions):raise ValueError('duplicate managed position')
  store=cls(econ,allocation,events,x['revision'],costs,tuple(positions),x.get('positions_revision',0));store.validate_integrity();return store
 def replay_history(self,history:Iterable[Deal])->int:return self.economic.replay(history)
 def apply_event(self,record:EventRecord)->bool:
  existing=self.events.get(record.event_id)
  if existing:
   if (existing.state,existing.revision)==(record.state,record.revision):return False
   raise OracleIntegrityError(IntegrityCode.DUPLICATE_EVENT_KEY,'conflicting replay')
  self.events[record.event_id]=record;self.revision+=1;return True
@dataclass(frozen=True)
class MoneyStateVersion: account:int; symbol:str; magic:int; cycle_id:str; broker_digest:str; economic_ledger_digest:str; allocation_ledger_digest:str; source_pool_digest:str; consumption_digest:str; event_store_digest:str; managed_positions_digest:str; opening_cost_digest:str; persistent_metadata_digest:str
@dataclass(frozen=True)
class FinalClosePolicy: threshold:D; required_deficit:D; current_revision:int; preview:bool=False
@dataclass(frozen=True)
class GateResult: allowed:bool; recovery:D; reserve:D; deficit:D; reasons:tuple[str,...]
def evaluate_final_close(snapshot:EventSnapshot,store:PersistentStore,risk_ok:bool,margin_ok:bool,policy:FinalClosePolicy)->GateResult:
 reasons=[];identity=store.economic.identity
 try:store.validate_integrity()
 except OracleIntegrityError as exc:
  reasons.extend(('LEDGER_INTEGRITY_FAILURE','INTEGRITY_'+exc.code.value))
 except (ValueError,KeyError,TypeError):
  reasons.extend(('LEDGER_INTEGRITY_FAILURE','INTEGRITY_'+IntegrityCode.PERSISTENCE_SCHEMA_INVALID.value))
 if snapshot.identity!=identity:reasons.append('FOREIGN_IDENTITY')
 if snapshot.broker!=store.economic.broker:reasons.append('BROKER_MISMATCH')
 if snapshot.managed_positions!=store.managed_positions:reasons.append('POSITIONS_MISMATCH')
 if snapshot.reconciliation_state is not ReconciliationState.PERSISTED:reasons.append('SNAPSHOT_NOT_PERSISTED')
 event=store.events.get(snapshot.event_key)
 if not event or event.state is not ReconciliationState.PERSISTED:reasons.append('UNRECONCILED')
 if any(e.state is not ReconciliationState.PERSISTED for e in store.events.values()):reasons.append('PENDING_EVENT')
 if snapshot.pending_deal_tickets:reasons.append('PENDING_DEALS')
 if snapshot.realized_cycle_net!=store.economic.realized_cycle_net:reasons.append('REALIZED_MISMATCH')
 reserve=store.allocation.available(AllocationType.FINAL_RESERVE)
 if snapshot.final_reserve_available!=reserve:reasons.append('RESERVE_MISMATCH')
 if snapshot.state_revision!=policy.current_revision or snapshot.ledger_revision!=store.revision:reasons.append('STALE')
 if snapshot.money_state_version!=store.money_state_version:reasons.append('MONEY_STATE_STALE')
 if store.allocation.records and not store.allocation.source_pools:reasons.append('SOURCE_POOL_MISSING')
 recovery=store.economic.realized_cycle_net+floating_total(identity,store.managed_positions,store.economic.broker,snapshot.slippage_diagnostic)
 if recovery<=policy.threshold:reasons.append('RECOVERY')
 if reserve<policy.required_deficit:reasons.append('RESERVE')
 if not risk_ok:reasons.append('RISK')
 if not margin_ok:reasons.append('MARGIN')
 if policy.preview:reasons.append('PREVIEW_NOT_ACTUAL')
 return GateResult(not reasons,recovery,reserve,policy.required_deficit,tuple(dict.fromkeys(reasons)))
