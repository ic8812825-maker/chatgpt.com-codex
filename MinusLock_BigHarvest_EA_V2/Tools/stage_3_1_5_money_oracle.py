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
