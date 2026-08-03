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
 identity:Identity; event_id:str; event_type:str; level:int; scenario:str; phase:str; broker:Broker
 managed_positions:tuple[Position,...]; actual_lots:tuple[D,...]; actual_open_prices:tuple[D,...]
 final_reserve_available:D; partial_far_budget_available:D; carry_available:D; transition_budget_available:D
 residual:D; commission:D; swap:D; fee:D; slippage_diagnostic:D; reconciliation_state:ReconciliationState
 applied_deal_tickets:frozenset[int]; pending_deal_tickets:frozenset[int]; state_revision:int
 realized_cycle_net:D; floating_close_now:D; recovery_pl_close_now:D
 def __post_init__(self):
  if self.actual_lots!=tuple(p.volume for p in self.managed_positions): raise ValueError('actual lot mismatch')
  if self.actual_open_prices!=tuple(p.open_price for p in self.managed_positions): raise ValueError('open price mismatch')
  if self.recovery_pl_close_now!=self.realized_cycle_net+self.floating_close_now: raise ValueError('recovery mismatch')
def floating_total(identity:Identity,positions:Iterable[Position],broker:Broker,slippage:D=D('0'))->D:
 return sum((projected_profit(p.side,p.volume,p.open_price,broker,slippage)+p.swap+p.exit_commission+p.exit_fee for p in positions if p.identity==identity),D('0'))
def make_snapshot(identity:Identity,event_id:str,event_type:str,level:int,scenario:str,phase:str,broker:Broker,positions:Iterable[Position],realized:D,state:ReconciliationState,revision:int,**kw)->EventSnapshot:
 ps=tuple(p for p in positions if p.identity==identity); floating=floating_total(identity,ps,broker,kw.get('slippage_diagnostic',D('0')))
 return EventSnapshot(identity,event_id,event_type,level,scenario,phase,broker,ps,tuple(p.volume for p in ps),tuple(p.open_price for p in ps),kw.get('final_reserve_available',D('0')),kw.get('partial_far_budget_available',D('0')),kw.get('carry_available',D('0')),kw.get('transition_budget_available',D('0')),kw.get('residual',D('0')),kw.get('commission',D('0')),kw.get('swap',D('0')),kw.get('fee',D('0')),kw.get('slippage_diagnostic',D('0')),state,frozenset(kw.get('applied_deal_tickets',())),frozenset(kw.get('pending_deal_tickets',())),revision,realized,floating,realized+floating)
