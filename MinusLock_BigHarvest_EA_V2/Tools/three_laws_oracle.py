#!/usr/bin/env python3
"""Independent Decimal oracle for the Hybrid Split Big three-law contract."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal as D, ROUND_CEILING, ROUND_FLOOR
from math import ceil, log

@dataclass(frozen=True)
class Broker:
    point:D; tick_size:D; tick_value_profit:D; tick_value_loss:D; lot_step:D; min_lot:D
    tick_value_profit_down:D|None=None; tick_value_loss_down:D|None=None
    bid0:D=D('1.10000'); ask0:D=D('1.10010')
    def __post_init__(self):
        if min(self.point,self.tick_size,self.tick_value_profit,self.tick_value_loss,self.lot_step,self.min_lot)<=0: raise ValueError('positive broker quantities required')
        if self.tick_value_profit_down is not None and self.tick_value_profit_down<=0:raise ValueError('down profit tick value')
        if self.tick_value_loss_down is not None and self.tick_value_loss_down<=0:raise ValueError('down loss tick value')
        if self.bid0<=0 or self.ask0<self.bid0:raise ValueError('Ask must not be below Bid')
        if (self.ask0-self.bid0)/self.tick_size != ((self.ask0-self.bid0)/self.tick_size).to_integral_value():raise ValueError('spread must use tick grid')
    @property
    def spread_price(self)->D:return self.ask0-self.bid0
    def ticks_for_points(self,points:D)->int:
        ticks=points*self.point/self.tick_size
        if ticks!=ticks.to_integral_value(): raise ValueError('off tick grid')
        return int(ticks)
    def normalize(self,lot:D,rounding='floor')->D:
        if lot<=0:return D(0)
        mode=ROUND_FLOOR if rounding=='floor' else ROUND_CEILING
        value=(lot/self.lot_step).to_integral_value(rounding=mode)*self.lot_step
        return D(0) if value<self.min_lot else value

@dataclass(frozen=True)
class Costs:
    commission_open:D=D(0); commission_close:D=D(0); swap:D=D(0); fee:D=D(0); slippage:D=D(0)
    @property
    def total(self)->D:return sum((self.commission_open,self.commission_close,self.swap,self.fee,self.slippage),D(0))

@dataclass(frozen=True)
class Plan:
    far:D; core:D; trend:D; small:D; reserve_share:D; initial_far_loss:D
    reserve_initial:D=D(0); costs:Costs=Costs()
    def __post_init__(self):
        if min(self.far,self.core,self.trend,self.small,self.initial_far_loss,self.reserve_initial)<0: raise ValueError('negative magnitude')
        if not D(0)<self.reserve_share<=D(1):raise ValueError('reserve_share')
    @property
    def big(self):return self.core+self.trend
    @property
    def recovery_slope_lots(self):return self.big-self.small-self.far
    @property
    def reserve_slope_lots(self):return self.reserve_share*(self.big-self.small)-self.far

class Side(str,Enum): BUY='BUY';SELL='SELL'

def projected_profit(side:Side,lot:D,open_price:D,close_bid:D,close_ask:D,
                     tick_size:D,tick_value_profit:D,tick_value_loss:D)->D:
    close=close_bid if side is Side.BUY else close_ask
    price_delta=(close-open_price) if side is Side.BUY else (open_price-close)
    ticks=price_delta/tick_size
    if ticks!=ticks.to_integral_value():raise ValueError('profit prices off tick grid')
    value=tick_value_profit if ticks>=0 else tick_value_loss
    return lot*ticks*value

def trajectory(plan:Plan,broker:Broker,points:D,direction:str):
    if direction not in {'UP','DOWN'}:raise ValueError('direction')
    profit_value=broker.tick_value_profit if direction=='UP' or broker.tick_value_profit_down is None else broker.tick_value_profit_down
    loss_value=broker.tick_value_loss if direction=='UP' or broker.tick_value_loss_down is None else broker.tick_value_loss_down
    big_side=Side.BUY if direction=='UP' else Side.SELL;hedge_side=Side.SELL if direction=='UP' else Side.BUY
    big_open=broker.ask0 if big_side is Side.BUY else broker.bid0
    hedge_open=broker.bid0 if hedge_side is Side.SELL else broker.ask0
    rows=[]
    for k in range(broker.ticks_for_points(points)+1):
        move=D(k)*broker.tick_size*(D(1) if direction=='UP' else D(-1))
        bid=broker.bid0+move;ask=broker.ask0+move
        core=projected_profit(big_side,plan.core,big_open,bid,ask,broker.tick_size,profit_value,loss_value)
        trend=projected_profit(big_side,plan.trend,big_open,bid,ask,broker.tick_size,profit_value,loss_value)
        small=projected_profit(hedge_side,plan.small,hedge_open,bid,ask,broker.tick_size,profit_value,loss_value)
        far=-plan.initial_far_loss+projected_profit(hedge_side,plan.far,hedge_open,bid,ask,broker.tick_size,profit_value,loss_value)
        gross=plan.reserve_share*max(D(0),core+trend+small);net=gross-plan.costs.total
        recovery=core+trend+small+far-plan.costs.total
        rows.append({'bid':bid,'ask':ask,'core':core,'trend':trend,'small':small,'far':far,'gross_reserve':gross,'net_reserve':net,'recovery':recovery,'coverage':plan.reserve_initial+net+far})
    return rows

def strictly_increasing(values):return bool(values) and all(b>a for a,b in zip(values,values[1:]))
@dataclass(frozen=True)
class EventSnapshot:
    realized_pl:D;floating_pl:D;reserve_ledger:D;commission:D;swap:D;fee:D;slippage:D
    far_actual_lot:D;big_actual_lot:D;small_actual_lot:D;event_id:str

def recovery_pl(snapshot:EventSnapshot)->D:
    # Reserve is a separate ledger bucket and must not be counted twice in RecoveryPL.
    return snapshot.realized_pl+snapshot.floating_pl-sum(
        (snapshot.commission,snapshot.swap,snapshot.fee,snapshot.slippage),D(0))

def event_monotone(before:EventSnapshot,after:EventSnapshot,strict=False)->bool:
    if not before.event_id or not after.event_id or before.event_id==after.event_id:raise ValueError('distinct EventID required')
    delta=recovery_pl(after)-recovery_pl(before)
    return delta>0 if strict else delta>=0

@dataclass(frozen=True)
class BasketPosition:
    side:Side;lot:D;open_price:D

def risk_money(positions:tuple[BasketPosition,...],control_bid:D,broker:Broker,costs:Costs=Costs())->D:
    control_ask=control_bid+broker.spread_price
    money=sum((projected_profit(p.side,p.lot,p.open_price,control_bid,control_ask,
          broker.tick_size,broker.tick_value_profit,broker.tick_value_loss) for p in positions),D(0))
    return max(D(0),-money+costs.total)

def coverage_path(rows):
    values=[r['coverage'] for r in rows]
    start=next((i for i,row in enumerate(rows) if row['gross_reserve']>0),0)
    first=next((i for i,value in enumerate(values) if value>=0),None)
    required=values[start:]
    return {'levels_checked':len(required),'first_required_level':start,'first_catch_level':first,
            'coverage_monotone':all(b>=a for a,b in zip(required,required[1:])),
            'final_coverage':values[-1],'final_catch':values[-1]>=0}

def compression(old_far:D,new_far_raw:D,next_core_raw:D,next_trend_raw:D,small_next_raw:D,broker:Broker,gross_old:D):
    new_far=broker.normalize(new_far_raw);core=broker.normalize(next_core_raw);trend=broker.normalize(next_trend_raw);small=broker.normalize(small_next_raw,'ceiling')
    next_big=core+trend;gross_next=new_far+next_big+small;q=new_far/old_far if old_far>0 else D('Infinity')
    return {'new_far':new_far,'next_big':next_big,'gross_next':gross_next,'q':q,'new_far_pass':new_far==0 or D(0)<new_far<old_far,'next_big_pass':next_big<old_far,'gross_pass':gross_next<gross_old}

def q_domain(transitions,policy_q_cap:D):
    observed=[]
    for old_far,new_far,broker in transitions:
        old=broker.normalize(old_far);new=broker.normalize(new_far)
        if old<=0:raise ValueError('old Far outside grid')
        observed.append(new/old)
    maximum=max(observed,default=D(0))
    return {'transitions':len(observed),'observed_q_max':maximum,
            'policy_q_cap':policy_q_cap,'pass':bool(observed) and maximum<=policy_q_cap<D(1)}

def finite_bound(initial_far:D,q_max:D,broker:Broker)->int:
    if not D(0)<q_max<D(1) or initial_far<=0:raise ValueError('F>0 and 0<q<1 required')
    geometric=max(0,ceil(log(float(broker.min_lot/initial_far))/log(float(q_max))))
    grid=int((initial_far/broker.lot_step).to_integral_value(rounding=ROUND_CEILING))
    return min(grid,geometric+1)

def evaluate(plan:Plan,broker:Broker,points:D,direction:str):
    rows=trajectory(plan,broker,points,direction)
    path=coverage_path(rows)
    return {'lot_catch_up':plan.reserve_slope_lots>0,'recovery_slope':plan.recovery_slope_lots>0,
            'pointwise':strictly_increasing([r['recovery'] for r in rows]),
            'money_catch_up':path['final_catch'] and path['first_catch_level'] is not None and path['first_catch_level']<len(rows),
            'coverage_path':path,'rows':rows}
