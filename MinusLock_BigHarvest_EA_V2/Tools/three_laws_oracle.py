#!/usr/bin/env python3
"""Independent Decimal oracle for the Hybrid Split Big three-law contract."""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal as D, ROUND_CEILING, ROUND_FLOOR
from math import ceil, log

@dataclass(frozen=True)
class Broker:
    point:D; tick_size:D; tick_value_profit:D; tick_value_loss:D; lot_step:D; min_lot:D
    def __post_init__(self):
        if min(self.point,self.tick_size,self.tick_value_profit,self.tick_value_loss,self.lot_step,self.min_lot)<=0: raise ValueError('positive broker quantities required')
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

def leg(lot:D,ticks:int,tick_value:D,favorable:bool)->D:
    return lot*D(ticks)*tick_value*(D(1) if favorable else D(-1))

def trajectory(plan:Plan,broker:Broker,points:D,direction:str):
    if direction not in {'UP','DOWN'}:raise ValueError('direction')
    rows=[]
    for k in range(broker.ticks_for_points(points)+1):
        core=leg(plan.core,k,broker.tick_value_profit,True);trend=leg(plan.trend,k,broker.tick_value_profit,True)
        small=leg(plan.small,k,broker.tick_value_loss,False)
        far=-plan.initial_far_loss+leg(plan.far,k,broker.tick_value_loss,False)
        gross=plan.reserve_share*max(D(0),core+trend+small);net=gross-plan.costs.total
        recovery=core+trend+small+far-plan.costs.total
        rows.append({'core':core,'trend':trend,'small':small,'far':far,'gross_reserve':gross,'net_reserve':net,'recovery':recovery,'coverage':plan.reserve_initial+net+far})
    return rows

def strictly_increasing(values):return bool(values) and all(b>a for a,b in zip(values,values[1:]))
def event_monotone(before:D,realized_transfer:D,floating_after:D,new_costs:D)->bool:return realized_transfer+floating_after-new_costs>=before

def compression(old_far:D,new_far_raw:D,next_core_raw:D,next_trend_raw:D,small_next_raw:D,broker:Broker,gross_old:D):
    new_far=broker.normalize(new_far_raw);core=broker.normalize(next_core_raw);trend=broker.normalize(next_trend_raw);small=broker.normalize(small_next_raw,'ceiling')
    next_big=core+trend;gross_next=new_far+next_big+small;q=new_far/old_far if old_far>0 else D('Infinity')
    return {'new_far':new_far,'next_big':next_big,'gross_next':gross_next,'q':q,'new_far_pass':new_far==0 or D(0)<new_far<old_far,'next_big_pass':next_big<old_far,'gross_pass':gross_next<gross_old}

def finite_bound(initial_far:D,q_max:D,broker:Broker)->int:
    if not D(0)<q_max<D(1) or initial_far<=0:raise ValueError('F>0 and 0<q<1 required')
    geometric=max(0,ceil(log(float(broker.min_lot/initial_far))/log(float(q_max))))
    grid=int((initial_far/broker.lot_step).to_integral_value(rounding=ROUND_CEILING))
    return min(grid,geometric+1)

def evaluate(plan:Plan,broker:Broker,points:D,direction:str):
    rows=trajectory(plan,broker,points,direction)
    return {'lot_catch_up':plan.reserve_slope_lots>0,'recovery_slope':plan.recovery_slope_lots>0,'pointwise':strictly_increasing([r['recovery'] for r in rows]),'money_catch_up':rows[-1]['coverage']>=0,'rows':rows}
