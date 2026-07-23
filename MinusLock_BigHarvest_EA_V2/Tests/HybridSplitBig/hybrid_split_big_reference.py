"""Executable, broker-agnostic mathematical reference for Hybrid Split Big.
It is deliberately not an MT5 replacement: all money comes from the injected calculator.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from math import ceil, floor, log
from typing import Callable, Iterable

MoneyCalculator = Callable[[str, float, float, float, float, float, float, float], float]

def linear_profit(direction: str, lot: float, open_price: float, close_price: float,
                  point_value: float, commission: float=0., swap: float=0., fee: float=0.) -> float:
    sign = 1.0 if direction == "BUY" else -1.0
    return sign * (close_price - open_price) * lot * point_value - commission - swap - fee

def down(v: float, step: float) -> float: return floor((v + 1e-12) / step) * step
def up(v: float, step: float) -> float: return ceil((v - 1e-12) / step) * step
def near(v: float, step: float) -> float: return floor(v / step + .5) * step

@dataclass(frozen=True)
class VolumeRules:
    minimum: float; maximum: float; step: float
    def valid(self, v: float) -> bool:
        return self.minimum <= v <= self.maximum and abs(v - down(v, self.step)) < 1e-9

@dataclass(frozen=True)
class Geometry:
    far: float; core: float; trend: float; small: float; reserve_share: float
    def catchup_ratio(self) -> float: return self.reserve_share * (self.core+self.trend-self.small) / self.far
    def recovery_slope(self) -> float: return self.core+self.trend-self.small-self.far

@dataclass
class Buckets:
    realized_cycle_pl: float = 0.; final_reserve_real: float = 0.; final_reserve_projected: float = 0.
    partial_available: float = 0.; partial_consumed: float = 0.; transition_available: float = 0.
    transition_consumed: float = 0.; carry: float = 0.; cumulative_transition_loss: float = 0.
    applied_events: set[str] = field(default_factory=set)
    def recovery_actual_final(self) -> float: return self.realized_cycle_pl
    def allocate_harvest(self, event: str, net: float, alpha: float, beta: float, gamma: float) -> bool:
        if event in self.applied_events: return False
        if min(alpha,beta,gamma) < 0 or abs(alpha+beta+gamma-1) > 1e-9: raise ValueError("invalid allocation shares")
        self.applied_events.add(event); self.realized_cycle_pl += net
        if net <= 0: return True
        partial, reserve = alpha*net, beta*net
        carry = net - partial - reserve # monetary residual is deliberately carried
        self.partial_available += partial; self.final_reserve_real += reserve; self.carry += carry
        self.final_reserve_projected = self.final_reserve_real
        return True
    def transition_allowed(self, net: float, per_loss: float, cumulative_loss: float, initial_far_risk: float, percent: float) -> bool:
        loss=max(-net,0.); new=self.cumulative_transition_loss+loss
        return net >= -per_loss and new <= cumulative_loss and new <= percent*initial_far_risk
    def record_transition(self, net: float) -> None:
        self.realized_cycle_pl += net; self.cumulative_transition_loss += max(-net,0.)

def projected_final(realized_before: float, projected_close_net: float) -> float: return realized_before + projected_close_net
def actual_final(realized_after_all_closes: float) -> float: return realized_after_all_closes
def coverage_deficit(remaining_far_cost: float, reserve: float, buffer: float) -> float: return max(remaining_far_cost,0.) + buffer - reserve

def finite_catchup(levels: Iterable[dict], min_gain: float, final_profit: float) -> int | None:
    previous=None
    for i, row in enumerate(levels, 1):
        d=row['deficit']
        if previous is not None and d > previous-min_gain+1e-9: return None
        if d <= 0 and row['recovery'] >= final_profit: return i
        previous=d
    return None

def next_geometry(far: float, new_far: float, core_ratio: float, trend_ratio: float, small_ratio: float, rules: VolumeRules) -> dict:
    c,t,s=(down(new_far*r, rules.step) for r in (core_ratio,trend_ratio,small_ratio))
    return {'core':c,'trend':t,'small':s,'gross':new_far+c+t+s,'big_gross':c+t,
            'slope':c+t-s-new_far, 'valid': all(rules.valid(v) for v in (c,t,s))}

def solve_new_far(old_far: float, old_gross: float, old_risk: float, core_ratio: float, trend_ratio: float, small_ratio: float,
                  rules: VolumeRules, transition: Callable[[float], float], risk: Callable[[float], float],
                  per_loss: float=0., cumulative_loss: float=0., prior_loss: float=0., initial_far_risk: float=1., percent: float=0.) -> dict:
    for n in (down(rules.minimum+i*rules.step, rules.step) for i in range(int((old_far-rules.minimum)/rules.step)+1)):
        if n < rules.minimum-1e-9 or n >= old_far-1e-9: continue
        g=next_geometry(old_far,n,core_ratio,trend_ratio,small_ratio,rules); net=transition(n); nrisk=risk(n)
        loss=prior_loss+max(-net,0.)
        if not g['valid'] or g['big_gross'] >= old_far-1e-9 or g['gross'] >= old_gross-1e-9 or nrisk >= old_risk-1e-9: continue
        if net < -per_loss or loss > cumulative_loss or loss > percent*initial_far_risk: continue
        return {'code':'PASS_NEW_FAR','new_far':n,'q':n/old_far,'transition_net':net,'next':g,'next_risk':nrisk}
    return {'code':'REJECT_NO_VALID_Q'}

def terminal_required(raw_new_far: float, normalized: float, old_far: float, rules: VolumeRules) -> bool:
    return raw_new_far < rules.minimum or normalized < rules.minimum or normalized >= old_far

def bounded_transitions(f0: float, terminal: float, qmax: float) -> int:
    if not (0 < qmax < 1 and terminal < f0): raise ValueError('invalid bound')
    return ceil(log(terminal/f0)/log(qmax))

def reconcile(requested: float, filled: float, tolerance: float=.000001) -> str:
    return 'RECONCILED' if abs(requested-filled)<=tolerance else 'ERROR_PARTIAL_EXECUTION'
